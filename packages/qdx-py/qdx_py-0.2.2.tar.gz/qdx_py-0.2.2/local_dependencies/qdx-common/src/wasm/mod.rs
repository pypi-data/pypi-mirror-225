use wasm_bindgen::prelude::*;

use crate::{pdb, AtomCheckStrictness, Conformer};

#[wasm_bindgen]
pub fn from_pdb(pdb_contents: &str) -> JsValue {
    match pdb::from_pdb(pdb_contents, None, None) {
        Ok(conformer) => serde_wasm_bindgen::to_value(&conformer).unwrap(),
        Err(e) => serde_wasm_bindgen::to_value(&e).unwrap(),
    }
}

#[wasm_bindgen]
pub fn to_pdb(conformer: JsValue) -> JsValue {
    let conformer: Conformer = serde_wasm_bindgen::from_value(conformer).unwrap();
    serde_wasm_bindgen::to_value(&pdb::to_pdb(conformer)).unwrap()
}

#[wasm_bindgen]
pub fn fragment(
    conformer: JsValue,
    backbone_steps: usize,
    terminal_fragment_sidechain_size: Option<usize>,
) -> JsValue {
    let mut conformer: Conformer = serde_wasm_bindgen::from_value(conformer).unwrap();
    let fragments = conformer.fragment(backbone_steps, terminal_fragment_sidechain_size);
    conformer.topology.fragments = Some(fragments);
    conformer.topology.fragment_charges = conformer.topology.explicit_fragment_charges();
    serde_wasm_bindgen::to_value(&conformer).unwrap()
}

#[wasm_bindgen]
pub fn perceive_formal_charges(conformer: JsValue, ensure_no_missing_atoms: bool) -> JsValue {
    let mut conformer: Conformer = serde_wasm_bindgen::from_value(conformer).unwrap();
    let strictness = if ensure_no_missing_atoms {
        AtomCheckStrictness::All
    } else {
        AtomCheckStrictness::None
    };
    match conformer.perceive_formal_charges(strictness) {
        Ok(()) => serde_wasm_bindgen::to_value(&conformer).unwrap(),
        Err(e) => serde_wasm_bindgen::to_value(&e.to_string()).unwrap(),
    }
}

#[wasm_bindgen]
pub fn perceive_bonds(conformer: JsValue, ensure_no_missing_atoms: bool) -> JsValue {
    let mut conformer: Conformer = serde_wasm_bindgen::from_value(conformer).unwrap();
    let strictness = if ensure_no_missing_atoms {
        AtomCheckStrictness::All
    } else {
        AtomCheckStrictness::None
    };
    match conformer.perceive_bonds(strictness) {
        Ok(()) => serde_wasm_bindgen::to_value(&conformer).unwrap(),
        Err(e) => serde_wasm_bindgen::to_value(&e.to_string()).unwrap(),
    }
}

#[wasm_bindgen]
pub fn perceive_bonds_legacy(conformer: JsValue, tolerance: f32) -> JsValue {
    let mut conformer: Conformer = serde_wasm_bindgen::from_value(conformer).unwrap();
    conformer.topology.connectivity = Some(conformer.topology.implicit_connectivity(tolerance));
    serde_wasm_bindgen::to_value(&conformer).unwrap()
}
