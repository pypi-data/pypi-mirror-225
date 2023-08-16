extern crate ndarray;
extern crate num_cpus;

use std::fs::File;
use std::io::Read;
use std::path::Path;

use ndarray::Array2;
use numpy::{PyArray2};
use pyo3::prelude::*;
use rayon::prelude::*;
use serde::{Deserialize, Serialize};
use zip::read::ZipArchive;

#[derive(Serialize, Deserialize)]
struct Batch {
    label: String,
    feature_vector: String,
}


#[derive(Serialize, Deserialize)]
struct Metadata {
    count: usize,
    files: Option<Vec<Batch>>,
    sdk_version: String,
}


struct Entry {
    label: String,
    feature_vector: Vec<f32>,
}


fn read_file_from_archive(filepath: &str, arcname: &str) -> Result<String, Box<dyn std::error::Error>> {
    if Path::new(filepath).exists() == false {
        panic!("File does not exist: {:#?}", filepath);
    }
    let file = File::open(filepath)?;
    let mut zip = ZipArchive::new(file)?;
    let mut arcfile = zip.by_name(arcname)?;
    let mut contents = String::new();
    arcfile.read_to_string(&mut contents)?;

    Ok(contents)
}

fn read_batch(batch: &Batch, filepath: &str) -> Result<Vec<Entry>, Box<dyn std::error::Error>> {
    // open the file from the very start
    // as it is running in parallel we should be good to go
    let labels_str = read_file_from_archive(filepath, &batch.label)?;
    let feature_vectors_str = read_file_from_archive(filepath, &batch.feature_vector)?;

    let entries: Vec<Entry> = labels_str
        .lines()
        .zip(feature_vectors_str.lines())
        .map(|(label, feature_vector)| Entry {
            label: label.to_string(),
            feature_vector: feature_vector.to_string()
                .trim_matches(|c| c == '[' || c == ']')
                .split(",")
                .map(|x| x.trim().parse::<f32>().unwrap())
                .collect(),
        })
        .collect();

    Ok(entries)
}


fn unpack_internal(filepath: &str) -> Result<(Vec<String>, Vec<Vec<f32>>), Box<dyn std::error::Error>> {
    // Open the zip archive
    let metadata_str = read_file_from_archive(filepath, "meta.json")?;
    let metadata: Metadata = serde_json::from_str(&metadata_str)?;

    let feature_vectors_count = metadata.count;

    if feature_vectors_count == 0 {
        return Ok((
            Vec::new(),
            Vec::new(),
        ));
    }

    let default_batch = Batch {
        label: "labels.txt".to_string(),
        feature_vector: "features.txt".to_string(),
    };

    let mut batches: Vec<&Batch> = Vec::new();

    let files = metadata.files.unwrap_or_default();
    for batch in files.iter() {
        batches.push(batch);
    }

    if batches.len() == 0 {
        // support older versions of rcdb versions, like generated from fvm
        batches.push(&default_batch);
    }

    // do following transformation:
    // batch -> list<Entry> -> list<(label, feature_vector)> -> (list<label>, list<feature_vector>) -> (Array1<label>, Array2<feature_vector>)
    let result = batches
        .par_iter()
        .map(|batch| { // Batch = {labels: labels_1.txt, features: features_1.txt}
            read_batch(batch, filepath)   // returns Vec<Entry>
                .unwrap()
                .par_iter()
                .map(|entry| {
                    (
                        entry.label.clone(),
                        entry.feature_vector.clone()
                    )
                })
                .collect::<Vec<(String, Vec::<f32>)>>()
        })
        .flatten() // [(l, fv), (l, fv)]
        .collect::<Vec<(String, Vec::<f32>)>>();

    let (labels, features): (Vec<String>, Vec<Vec<f32>>) = result.into_par_iter().unzip();
    Ok((labels, features))

}


/// rust usage only
pub fn unpack(filepath: &str) -> Result<(Vec<String>, Array2<f32>), Box<dyn std::error::Error>> {
    let (labels, features) = unpack_internal(filepath).unwrap();
    let features_arr = Array2::<f32>::from_shape_vec((features.len(), 512), features.into_par_iter().flatten().collect()).unwrap();
    Ok((labels, features_arr))
}


#[pymodule]
fn rcdb_unpacker(_py: Python, m: &PyModule) -> PyResult<()> {
    /// Unpacks the RCDB file and returns labels and features np.ndarray
    /// supply with filepath to the rcdb file
    #[pyfn(m)]
    fn unpack<'py>(py: Python<'py>, filepath: &str) -> (Vec<String>, &'py PyArray2<f32>) {

        // TODO: overwrite pyo3 panic into something manageable
        let (labels, features) = unpack_internal(filepath).unwrap();
        let features_arr = PyArray2::from_vec2(py, &features).unwrap();

        (labels, features_arr)
    }
    Ok(())
}


#[cfg(test)]
mod tests {
    use std::path::PathBuf;

    use super::*;

    #[test]
    fn can_read_zero_size_rcdb() {
        let mut d = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        d.push("resources");
        d.push("zeta_export.rcdb");
        println!("path: {:#?}", d.display());

        let _ = match unpack_internal(d.to_str().unwrap()) {
            Ok((labels, _features)) => assert_eq!(labels.len(), 0),
            Err(err) => panic!("Error: {}", err),
        };
    }

    #[test]
    fn can_read_symphony_rcdb(){
        let mut d = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        d.push("resources");
        d.push("symphony_137_fvs.rcdb");
        println!("path: {:#?}", d.display());

        let _ = match unpack_internal(d.to_str().unwrap()) {
            Ok((labels, _features)) => assert_eq!(labels.len(), 137),
            Err(err) => panic!("Error: {}", err),
        };
    }

    #[test]
    fn can_read_feature_vectors_with_spaces(){
        let mut d = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        d.push("resources");
        d.push("reference_db.rcdb");  // file with spaces
        println!("path: {:#?}", d.display());

        let _ = match unpack_internal(d.to_str().unwrap()) {
            Ok((labels, _features)) => assert_eq!(labels.len(), 43),
            Err(err) => panic!("Error: {}", err),
        };
    }

    #[test]
    fn internal_unpack_format() {
        let mut d = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        d.push("resources");
        d.push("symphony_137_fvs.rcdb");
        println!("path: {:#?}", d.display());

        let (labels, features) = match unpack(d.to_str().unwrap()) {
            Ok((labels, features)) => (labels, features),
            Err(err) => panic!("Error: {}", err),
        };
        assert_eq!(labels.len(), 137);
        assert_eq!(features.shape(), &[137, 512]);
    }
}
