use std::{
    fs::File,
    io::Read,
};

use anyhow::Result;
use ndarray::Array2;
use numpy::PyArray2;
use pyo3::create_exception;
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


type Entry = (String, Vec<f32>);


fn read_file_from_archive(filepath: &str, arcname: &str) -> Result<String> {
    let file = match File::open(filepath) {
        Ok(file) => file,
        Err(err) => {
            return Err(anyhow::anyhow!(
                "Cannot open file {}: {}",
                filepath,
                err.to_string()
            ))
        }
    };

    let mut zip = match ZipArchive::new(file) {
        Ok(zip) => zip,
        Err(err) => {
            return Err(anyhow::anyhow!(
                "Cannot open zip archive {}: {}",
                filepath,
                err.to_string()
            ))
        }
    };

    let mut arcfile = match zip.by_name(arcname) {
        Ok(arcfile) => arcfile,
        Err(err) => {
            return Err(anyhow::anyhow!(
                "Cannot open file {} from archive {}: {}",
                arcname,
                filepath,
                err.to_string()
            ))
        }
    };
    let mut contents = String::new();
    arcfile.read_to_string(&mut contents)?;

    Ok(contents)
}


fn parse_feature_vector_string(fv: &str) -> Vec<f32> {
    fv.strip_prefix("[").unwrap_or(fv)
        .strip_suffix("]").unwrap_or(fv)
        .split(",")
        .map(|x| x.trim().parse::<f32>().unwrap())
        .collect()
}


fn parse_feature_vectors(feature_vectors: Vec<&str>) -> Vec<Vec<f32>> {
    feature_vectors
        .into_par_iter()
        .map(|fv| parse_feature_vector_string(fv))
        .collect()
}


fn read_batch(batch: &Batch, filepath: &str) -> Vec<Entry> {
    // open the file from the very start
    // as it is running in parallel we should be good to go
    let labels_str = read_file_from_archive(filepath, &batch.label).unwrap();
    let feature_vectors_str = read_file_from_archive(filepath, &batch.feature_vector).unwrap();

    let entries: Vec<Entry> = labels_str
        .lines()
        .zip(feature_vectors_str.lines())
        .map(|(label, feature_vector)| {
            (
                label.to_string(),
                parse_feature_vector_string(feature_vector),
            )
        })
        .collect();
    entries
}


fn unpack_internal(filepath: &str) -> Result<(Vec<String>, Vec<Vec<f32>>)> {
    // Open the zip archive
    let metadata_str = read_file_from_archive(filepath, "meta.json")?;
    let metadata: Metadata = serde_json::from_str(&metadata_str)?;

    let feature_vectors_count = metadata.count;

    if feature_vectors_count == 0 {
        return Ok((Vec::new(), Vec::new()));
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
    // batch -> list<Entry> -> list<(label, feature_vector)> -> (list<label>, list<feature_vector>)
    let result = batches
        .par_iter()
        .map(|batch| { // Batch = {labels: labels_1.txt, features: features_1.txt}
            read_batch(batch, filepath)   // returns Vec<Entry>
        })
        .flatten() // [(l, fv), (l, fv)]
        .collect::<Vec<(String, Vec::<f32>)>>();

    let (labels, features): (Vec<String>, Vec<Vec<f32>>) = result.into_iter().unzip();

    Ok((labels, features))
}


/// rust usage only
pub fn unpack(filepath: &str) -> Result<(Vec<String>, Array2<f32>)> {
    let (labels, features) = unpack_internal(filepath).unwrap();
    let features_arr = Array2::<f32>::from_shape_vec((features.len(), 512), features.into_iter().flatten().collect()).unwrap();

    Ok((labels, features_arr))
}


create_exception!(rcdb_unpacker, RcdbUnpackerError, pyo3::exceptions::PyException);

#[pymodule]
fn rcdb_unpacker(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add("RcdbUnpackerError", _py.get_type::<RcdbUnpackerError>())?;

    /// Unpacks the RCDB file and returns labels and features np.ndarray
    /// supply with filepath to the rcdb file
    #[pyfn(m)]
    fn unpack<'py>(py: Python<'py>, filepath: &str) -> PyResult<(Vec<String>, &'py PyArray2<f32>)> {
        match unpack_internal(filepath) {
            Ok((labels, features)) => Ok((labels, PyArray2::from_vec2(py, &features).unwrap())),
            Err(err) => Err(RcdbUnpackerError::new_err(err.to_string())),
        }
    }

    /// parse list of string representation of feature vectors
    /// [fv, fv, fv, ...]
    /// where fv can be in either formats:
    /// [1.0, 2.0, 3.0, ...], or
    /// 1.0, 2.0, 3.0, ...
    /// returns np.ndarray
    #[pyfn(m)]
    fn parse_fvs<'py>(py: Python<'py>, feature_vectors: Vec<&str>) -> PyResult<&'py PyArray2<f32>> {
        let features = parse_feature_vectors(feature_vectors);
        Ok(PyArray2::from_vec2(py, &features).unwrap())
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
    fn can_read_symphony_rcdb() {
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
    fn can_read_feature_vectors_with_spaces() {
        let mut path_buf = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        path_buf.push("resources");
        path_buf.push("reference_db.rcdb");  // file with spaces
        println!("path: {:#?}", path_buf.display());

        let _ = match unpack_internal(path_buf.to_str().unwrap()) {
            Ok((labels, _features)) => assert_eq!(labels.len(), 43),
            Err(err) => panic!("Error: {}", err),
        };
    }

    #[test]
    fn internal_unpack_format() {
        let mut path_buf = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        path_buf.push("resources");
        path_buf.push("symphony_137_fvs.rcdb");
        println!("path: {:#?}", path_buf.display());

        let (labels, features) = match unpack(path_buf.to_str().unwrap()) {
            Ok((labels, features)) => (labels, features),
            Err(err) => panic!("Error: {}", err),
        };
        assert_eq!(labels.len(), 137);
        assert_eq!(features.shape(), &[137, 512]);
    }

    #[test]
    fn raise_exception_when_no_file_found() {
        let mut path_buf = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        path_buf.push("resources");
        path_buf.push("non_existing_file.rcdb");
        println!("path: {:#?}", path_buf.display());

        let _ = match unpack_internal(path_buf.to_str().unwrap()) {
            Ok((_labels, _features)) => {},
            Err(err) => assert!(err.to_string().contains("Cannot open file")),
        };
    }

    #[test]
    fn parse_feature_vector_string_test() {
        let fv = "[1.0, 2.0, 3.0]";
        let parsed = parse_feature_vector_string(fv);
        assert_eq!(parsed, vec![1.0, 2.0, 3.0]);

        let fv = "1.0, 2.0, 3.0";
        let parsed = parse_feature_vector_string(fv);
        assert_eq!(parsed, vec![1.0, 2.0, 3.0]);

        let fv = "1.0,2.0,3.0";
        let parsed = parse_feature_vector_string(fv);
        assert_eq!(parsed, vec![1.0, 2.0, 3.0]);
    }

    #[test]
    fn parse_feature_vectors_test() {
        let fvs = vec!["[1.0, -2.0, 3.0]", "1.0, -2.0, 3.0", "1.0,-2.0,3.0"];
        let parsed = parse_feature_vectors(fvs);
        assert_eq!(parsed, vec![vec![1.0, -2.0, 3.0], vec![1.0, -2.0, 3.0], vec![1.0, -2.0, 3.0]]);
    }
}
