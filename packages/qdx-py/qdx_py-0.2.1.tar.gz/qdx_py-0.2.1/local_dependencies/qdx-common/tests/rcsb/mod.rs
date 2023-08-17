use qdx_common::{
    pdb::{from_pdb, to_pdb},
    AtomCheckStrictness,
};

use crate::it::util::load_test_pdb;

pub mod hif2a;
pub mod thrombin;
pub mod vhl;

pub fn compare_and_check_bonds(
    path: &str,
    n_models: usize,
    strictness: AtomCheckStrictness,
) -> anyhow::Result<()> {
    let models = load_test_pdb(path)?;
    assert_eq!(models.len(), n_models);

    for mut model in models {
        // check that pdb formatting and parsing works as intended
        let model1 = from_pdb(to_pdb(model.clone()), None, None)?;
        assert_eq!(model1.len(), 1);
        let model2 = from_pdb(to_pdb(model1[0].clone()), None, None)?;
        assert_eq!(model2.len(), 1);
        assert_eq!(model1[0], model2[0]);

        model.perceive_bonds(strictness.clone())?;
    }

    Ok(())
}
