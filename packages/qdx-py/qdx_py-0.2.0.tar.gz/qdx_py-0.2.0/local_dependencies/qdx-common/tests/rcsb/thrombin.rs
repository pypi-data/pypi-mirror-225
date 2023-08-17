use itertools::zip_eq;

use crate::it::util::load_test_pdb;
use qdx_common::AtomCheckStrictness;

#[test]
fn load_and_fix_pdb2zff() -> anyhow::Result<()> {
    let models = &mut load_test_pdb("data/rcsb/thrombin/2zff.pdb")?;
    assert_eq!(models.len(), 1);

    let model = &mut models[0];
    // Unset charges for a complete test
    if let Some(atom_charges) = &mut model.topology.atom_charges {
        for atom_charge in atom_charges {
            *atom_charge = std::i8::MIN;
        }
    }
    // Use false here because there are missing atoms in this PDB file
    model.perceive_bonds(AtomCheckStrictness::All)?;
    model.perceive_formal_charges(AtomCheckStrictness::All)?;

    // Load reference charges
    let ref_model = &mut load_test_pdb("data/rcsb/thrombin/2zff.pdb")?[0];

    // Compare charges we added to charges in file
    if let (Some(aas), Some(ref_aas), Some(atom_charges), Some(ref_atom_charges)) = (
        &model.amino_acids,
        &ref_model.amino_acids,
        &model.topology.atom_charges,
        &ref_model.topology.atom_charges,
    ) {
        for (aa, ref_aa) in zip_eq(aas, ref_aas) {
            for (atom_idx, ref_atom_idx) in zip_eq(aa, ref_aa) {
                let atom_charge = atom_charges[*atom_idx as usize];
                let ref_atom_charge = ref_atom_charges[*ref_atom_idx as usize];
                if atom_charge != ref_atom_charge {
                    assert_eq!(atom_charge, ref_atom_charge);
                }
            }
        }
    }

    Ok(())
}
