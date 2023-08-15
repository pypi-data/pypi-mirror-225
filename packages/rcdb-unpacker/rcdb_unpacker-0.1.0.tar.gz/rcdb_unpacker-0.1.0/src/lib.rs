extern crate ndarray;
#[macro_use]
extern crate num_cpus;

use std::fs::File;
use std::io::Read;
use std::path::Path;

use numpy::{IntoPyArray, PyArray1, PyArray2};
use ndarray::{Array1, Array2};
use ndarray::prelude::*;
use pyo3::prelude::*;
use pyo3::types::{PyList, PyString};
use pyo3::wrap_pyfunction;
use rayon::prelude::*;
use serde::{Deserialize, Serialize};
use zip::read::ZipArchive;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}


#[derive(Serialize, Deserialize)]
struct Batch {
    label: String,
    feature_vector: String,
}


#[derive(Serialize, Deserialize)]
struct Metadata {
    count: usize,
    files: Vec<Batch>,
    sdk_version: String,
    model_codename: String,
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
                .split(",")
                .map(|x| x.parse::<f32>().unwrap())
                .collect(),
        })
        .collect();

    Ok(entries)
}


fn unpack_internal(filepath: &str) -> Result<(Vec<String>, Array2<f32>), Box<dyn std::error::Error>> {
    // Open the zip archive
    let metadata_str = read_file_from_archive(filepath, "meta.json")?;
    let metadata: Metadata = serde_json::from_str(&metadata_str)?;

    let feature_vectors_count = metadata.count;
    println!("Feature vectors count: {:#?}", feature_vectors_count);
    if feature_vectors_count == 0 {
        return Ok((
            Vec::new(),
            Array2::<f32>::zeros((0, 512)),
        ));
    }

    let mut batches: Vec<&Batch> = Vec::new();
    for batch in metadata.files.iter() {
        batches.push(batch);
    }

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
    // allocation twice
    let fv_ndarray = Array2::<f32>::from_shape_vec((feature_vectors_count, 512), features.into_par_iter().flatten().collect()).unwrap();

    Ok((labels, fv_ndarray))

    // for batch in batches.iter() {
    //     let entries = read_batch(batch, filepath).unwrap();
    //     for entry in entries.iter() {
    //         println!("Entry: {:#?} {:#?}", entry.label, entry.feature_vector.len());
    //     }
    // }
    // batch -> list<Entry> -> list<(label, feature_vector)> -> (list<label>, list<feature_vector>) -> (Array1<label>, Array2<feature_vector>)
}


#[pymodule]
fn rcdb_unpacker(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;

    /// Unpacks the RCDB file and returns labels and features np.ndarray
    #[pyfn(m)]
    fn unpack<'py>(py: Python<'py>, filepath: &str) -> (Vec<String>, &'py PyArray2<f32>) {
        let (labels_arr, features_arr) = unpack_internal(filepath).unwrap();

        let features_arr = features_arr.into_pyarray(py);

        (labels_arr, features_arr)
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
            Ok((labels, features)) => assert_eq!(labels.len(), 0),
            Err(err) => panic!("Error: {}", err),
        };
    }
}
