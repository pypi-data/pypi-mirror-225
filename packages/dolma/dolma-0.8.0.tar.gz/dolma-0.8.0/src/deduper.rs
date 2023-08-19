use std::collections::VecDeque;
use std::fs::OpenOptions;
use std::io;
use std::io::{BufRead, BufReader, BufWriter, Write};
use std::path::PathBuf;
use std::sync::atomic::{AtomicU32, Ordering};
use std::sync::Arc;

use flate2::read::MultiGzDecoder;
use flate2::write::GzEncoder;
use flate2::Compression;
use serde_json::{json, Value};
use threadpool::ThreadPool;

use crate::bloom_filter::BloomFilter;
use crate::s3_util;
use crate::shard::shard_config::WorkDirConfig;
use crate::shard::{find_objects_matching_patterns, FileCache};

use deduper_config::*;

pub fn run(config: DeduperConfig) -> Result<u32, u32> {
    let bloom_filter = BloomFilter::initialize(&config.bloom_filter).unwrap();
    let bloom_filter = Arc::new(bloom_filter);

    let paths = find_objects_matching_patterns(&config.documents)
        .unwrap()
        .clone();

    if !(config.dedupe.paragraphs.is_some() ^ config.dedupe.documents.is_some()) {
        log::error!("Must dedupe either paragraphs or documents");
        return Err(paths.len() as u32);
    }

    let threadpool = ThreadPool::new(config.processes);
    let failed_shard_count = AtomicU32::new(0);
    let failed_shard_count_ref = Arc::new(failed_shard_count);
    for p in paths {
        let path = p.clone();
        let work_dirs = config.work_dir.clone();
        let dedupe = config.dedupe.clone();
        let bloom_filter = bloom_filter.clone();
        let failed_shard_count_ref = failed_shard_count_ref.clone();
        threadpool.execute(move || {
            let result = write_attributes(path, work_dirs, dedupe, bloom_filter);
            match result {
                Ok(_) => {}
                Err(e) => {
                    log::error!("Failed to process {:?}: {}", p, e);
                    failed_shard_count_ref.fetch_add(1, Ordering::Relaxed);
                }
            }
        });
    }
    threadpool.join();

    let bloom_filter_file = PathBuf::from(&config.bloom_filter.file);
    log::info!("Writing bloom filter to {:?}...", config.bloom_filter.file);
    bloom_filter.write_to_file(&bloom_filter_file).unwrap();
    log::info!("Bloom filter written.");

    let failure_count = failed_shard_count_ref.fetch_add(0, Ordering::Relaxed);
    match failure_count {
        0 => {
            log::info!("Done!");
            return Ok(failure_count);
        }
        _ => {
            log::error!("{} shards failed to process.", failure_count);
            return Err(failure_count);
        }
    }
}

// Write attributes for the documents in the given file:
// For doc-level deduping, check the Bloom filter for existence of the configured key and set the configured attribute to true.
// For paragraph-level deduping, check the Bloom filter for existence of a paragraph in the text and add a span to the configured attribute.
fn write_attributes(
    docs_location: String,
    work_dirs: WorkDirConfig,
    dedupe_config: DedupeConfig,
    bloom_filter: Arc<BloomFilter>,
) -> Result<(), io::Error> {
    let cache = FileCache {
        s3_client: Box::new(s3_util::new_client(None)?),
        work: work_dirs.clone(),
    };

    let attrs_location = {
        let mut attr_prefix = "/attributes/".to_owned();
        attr_prefix.push_str(&dedupe_config.name);
        attr_prefix.push_str("/");
        docs_location
            .to_owned()
            .replace("/documents/", &attr_prefix)
    };
    let local_output = cache.prepare_output(&attrs_location)?;
    if local_output.exists() {
        log::info!("Skipping {:?} because it already exists", attrs_location);
        return Ok(());
    }
    log::info!(
        "Writing attributes for {} to {}",
        docs_location,
        local_output.display()
    );

    std::fs::create_dir_all(local_output.parent().unwrap())?;

    log::info!(
        "Writing attributes for {} to {}",
        docs_location,
        local_output.display()
    );
    {
        let local_input = cache.prepare_input(&docs_location)?;
        let input_file = OpenOptions::new()
            .read(true)
            .write(false)
            .create(false)
            .open(local_input.clone())?;
        let reader = BufReader::with_capacity(1024 * 1024, MultiGzDecoder::new(input_file));

        let tmp_output = OpenOptions::new()
            .read(false)
            .write(true)
            .create(true)
            .truncate(true)
            .open(&local_output)?;

        let mut writer = BufWriter::with_capacity(
            1024 * 1024,
            GzEncoder::new(tmp_output, Compression::default()),
        );

        let mut line_number = 0;
        for line in reader.lines() {
            match line {
                Ok(_) => {}
                Err(e) => {
                    log::error!(
                        "Error reading line {} of {}: {}",
                        line_number,
                        &docs_location,
                        e
                    );
                    break;
                }
            }
            line_number += 1;
            let line = line?;
            let data: Value = serde_json::from_str(&line)?;
            let mut attributes = json!({});

            match dedupe_config.documents {
                Some(ref cfg) => {
                    let document_key = {
                        let mut finder = jsonpath_rust::JsonPathFinder::from_str("{}", &cfg.key)
                            .map_err(|e| io::Error::new(io::ErrorKind::Other, e))
                            .unwrap();
                        finder.set_json(Box::new(data.clone()));
                        finder
                            .find()
                            .as_array()
                            .unwrap()
                            .get(0)
                            .unwrap()
                            .as_str()
                            .unwrap()
                            .to_string()
                    };

                    if dedupe_config.skip_empty.unwrap_or(false) && document_key.trim().is_empty() {
                        // skip empty documents if dedupe_config.skip_empty is true
                        // and the document key is empty after trimming (i.e., removing whitespace)
                        continue;
                    } else {
                        let mut dedupe_key = VecDeque::with_capacity(1);
                        dedupe_key.push_back(document_key.as_str());
                        if bloom_filter.contains(&dedupe_key) {
                            attributes[&cfg.attribute_name] = Value::Bool(true);
                        } else if !bloom_filter.read_only {
                            bloom_filter.insert(&dedupe_key);
                        }
                    }
                }
                None => {}
            }
            match dedupe_config.paragraphs {
                None => {}
                Some(ref cfg) => {
                    // Split the text into paragraphs and check each one.
                    let text = data["text"].as_str().unwrap();
                    let text_length = text.len();
                    let mut offset = 0;
                    let paragraphs = text.split("\n");
                    let mut duplicate_paragraph_spans = Vec::new();
                    for p in paragraphs {
                        let par_start = offset;
                        offset += p.chars().count();
                        if offset < text_length - 1 {
                            offset += 1; // For the newline
                        }
                        let par_end = offset;

                        if dedupe_config.skip_empty.unwrap_or(false) && p.trim().is_empty() {
                            // skip empty paragraphs if dedupe_config.skip_empty is true
                            // and the paragraph is empty after trimming (i.e., removing whitespace)
                            continue;
                        } else {
                            let mut dedupe_key = VecDeque::with_capacity(1);
                            dedupe_key.push_back(p);
                            if bloom_filter.contains(&dedupe_key) {
                                let span = vec![
                                    Value::Number(par_start.into()),
                                    Value::Number(par_end.into()),
                                    Value::Number(1.into()),
                                ];
                                // add span to duplicate_paragraph_spans
                                duplicate_paragraph_spans.push(Value::Array(span));
                            } else if !bloom_filter.read_only {
                                bloom_filter.insert(&dedupe_key);
                            }
                        }
                    }
                    attributes[&cfg.attribute_name] = Value::Array(duplicate_paragraph_spans);
                }
            }
            let mut output_object = json!({});
            output_object["id"] = data["id"].clone();
            output_object["attributes"] = attributes;
            serde_json::to_writer(&mut writer, &output_object)?;
            writer.write_all(b"\n")?;
        }
        std::fs::remove_file(local_input)?;
    }
    cache.finalize_output(&attrs_location)?;
    Ok(())
}

pub mod deduper_config {
    use serde::{Deserialize, Serialize};
    use std::fs::File;
    use std::io;

    use crate::bloom_filter::BloomFilterConfig;
    use crate::shard::shard_config::*;

    #[derive(Serialize, Deserialize, Clone)]
    pub struct DuplicateKeyConfig {
        // Remove duplicate paragraphs
        pub paragraphs: bool,
        // Use this key to dedupe whole documents
        pub document_key: Option<String>,
    }

    #[derive(Serialize, Deserialize, Clone)]
    pub struct DocumentDedupeConfig {
        pub attribute_name: String,
        pub key: String,
    }

    #[derive(Serialize, Deserialize, Clone)]
    pub struct ParagraphDedupeConfig {
        pub attribute_name: String,
    }

    #[derive(Serialize, Deserialize, Clone)]
    pub struct DedupeConfig {
        pub name: String,
        pub documents: Option<DocumentDedupeConfig>,
        pub paragraphs: Option<ParagraphDedupeConfig>,

        pub skip_empty: Option<bool>,
    }

    #[derive(Serialize, Deserialize, Clone)]
    pub struct DeduperConfig {
        pub documents: Vec<String>,
        pub work_dir: WorkDirConfig,
        pub dedupe: DedupeConfig,
        pub bloom_filter: BloomFilterConfig,
        pub processes: usize,
    }

    impl DeduperConfig {
        pub fn read_from_file(path: &str) -> Result<DeduperConfig, io::Error> {
            let file = File::open(path)?;
            let reader = io::BufReader::new(file);
            let config: DeduperConfig = serde_json::from_reader(reader)?;
            Ok(config)
        }
        pub fn parse_from_string(s: &str) -> Result<DeduperConfig, io::Error> {
            let config: DeduperConfig = serde_json::from_str(s)?;
            Ok(config)
        }
    }
}
