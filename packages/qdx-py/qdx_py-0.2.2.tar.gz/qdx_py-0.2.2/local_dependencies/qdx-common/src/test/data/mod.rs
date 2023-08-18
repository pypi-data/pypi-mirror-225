use std::path::{Path, PathBuf};

pub mod pdb_1fcx;
pub mod pdb_4hhb;
pub mod qc_json_w15;

pub fn load_test_file(filepath_stem: impl AsRef<Path> + Clone) -> anyhow::Result<String> {
    let manifest_path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    let mut data_path = manifest_path.join("tests").join("data");

    if !data_path.exists() {
        data_path = manifest_path.join("qdx-common").join("tests").join("data");
    }

    data_path.push(filepath_stem);
    Ok(std::fs::read_to_string(data_path)?)
}

pub fn sdf_1a30_ligand() -> anyhow::Result<String> {
    load_test_file("sdfs/ligand_1a30.sdf")
}

pub fn sdf_alt_charge() -> anyhow::Result<String> {
    load_test_file("sdfs/alt_charge.sdf")
}

pub fn sdf_isopropyl() -> anyhow::Result<String> {
    load_test_file("sdfs/isopropyl.sdf")
}

pub fn sdf_rank_1() -> anyhow::Result<String> {
    load_test_file("sdfs/rank_1.sdf")
}
