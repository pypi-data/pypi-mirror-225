use std::fs;
use std::path::{Path, PathBuf};

use qdx_common::pdb::from_pdb;
use qdx_common::Conformer;

pub fn load_test_pdb(filepath_stem: impl AsRef<Path> + Clone) -> anyhow::Result<Vec<Conformer>> {
    let manifest_path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    let mut pdb_path = manifest_path.join("tests");
    // we are doing a workspace test and want to find the project directory
    if !pdb_path.exists() {
        pdb_path = manifest_path.join("qdx-common").join("tests");
        // list contents of dir
        let contents = fs::read_dir(&pdb_path)?;
        for entry in contents {
            eprintln!("{:?}", entry?);
        }
    }
    pdb_path.push(filepath_stem);
    Ok(from_pdb(fs::read_to_string(pdb_path)?, None, None)?)
}
