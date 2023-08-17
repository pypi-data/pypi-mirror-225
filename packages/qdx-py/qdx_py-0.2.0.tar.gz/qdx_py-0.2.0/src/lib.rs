use std::collections::HashSet;

use pyo3::{exceptions::PyRuntimeError, prelude::*};
use qdx_common::{AtomCheckStrictness, Conformer};

/// Returns the json for a qdx conformer, converted from a pdb
#[pyfunction]
fn pdb_to_conformer(
    pdb_contents: String,
    keep_residues: Option<HashSet<String>>,
    skip_residues: Option<HashSet<String>>,
) -> PyResult<String> {
    serde_json::to_string(
        &qdx_common::convert::pdb::from_pdb(pdb_contents, keep_residues, skip_residues)
            .map_err(|e| PyRuntimeError::new_err(e.to_string()))?,
    )
    .map_err(|e| PyRuntimeError::new_err(e.to_string()))
}

/// Returns the the pdb for a qdx conformer string
#[pyfunction]
fn conformer_to_pdb(conformer_contents: String) -> PyResult<String> {
    Ok(qdx_common::convert::pdb::to_pdb(
        serde_json::from_str(&conformer_contents)
            .map_err(|e| PyRuntimeError::new_err(e.to_string()))?,
    ))
}

/// Concatenates two conformers
#[pyfunction]
fn concat(conformer_1_contents: String, conformer_2_contents: String) -> PyResult<String> {
    let mut conformer_1: Conformer = serde_json::from_str(&conformer_1_contents)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    let conformer_2: Conformer = serde_json::from_str(&conformer_2_contents)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;
    conformer_1.extend(conformer_2);

    serde_json::to_string(&conformer_1).map_err(|e| PyRuntimeError::new_err(e.to_string()))
}

/// Charges standard amino acids in a conformer
#[pyfunction]
fn formal_charge(conformer_contents: String, strictness: String) -> PyResult<String> {
    let mut conformer: Conformer = serde_json::from_str(&conformer_contents)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    let strictness: AtomCheckStrictness =
        serde_json::from_str(&strictness).map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    conformer
        .perceive_formal_charges(strictness)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    serde_json::to_string(&conformer).map_err(|e| PyRuntimeError::new_err(e.to_string()))
}

/// Fragments a conformer, updating the fragment formal charges based on existing atom charges
#[pyfunction]
fn fragment(
    conformer_contents: String,
    backbone_steps: usize,
    terminal_fragment_sidechain_size: Option<usize>,
) -> PyResult<String> {
    let mut conformer: Conformer = serde_json::from_str(&conformer_contents)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    conformer.topology.fragments =
        Some(conformer.fragment(backbone_steps, terminal_fragment_sidechain_size));

    conformer.topology.fragment_charges = conformer.topology.explicit_fragment_charges();

    serde_json::to_string(&conformer).map_err(|e| PyRuntimeError::new_err(e.to_string()))
}

/// QDX-Common utilities for python
#[pymodule]
fn qdx_py(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(pdb_to_conformer, m)?)?;
    m.add_function(wrap_pyfunction!(conformer_to_pdb, m)?)?;
    m.add_function(wrap_pyfunction!(concat, m)?)?;
    m.add_function(wrap_pyfunction!(formal_charge, m)?)?;
    m.add_function(wrap_pyfunction!(fragment, m)?)?;
    Ok(())
}
