use std::collections::BTreeSet;
use std::path::Path;

use assertables::*;
use itertools::zip_eq;

use crate::it::util::load_test_pdb;
use qdx_common::AtomCheckStrictness;
use qdx_common::{AminoAcid, AminoAcidTemplate, Conformer, Label, Topology};

fn build_example_aa_conformer() -> Conformer {
    Conformer {
        topology: Topology {
            symbols: vec!["H".into(), "H".into(), "O".into(), "C".into()],
            geometry: vec![1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 4.0, 4.0, 4.0],
            atom_charges: None,
            partial_charges: None,
            atom_labels: None,
            alts: None,
            connectivity: None,
            fragments: None,
            fragment_charges: None,
        },
        amino_acids: Some(vec![vec![0, 1, 2], vec![3]]),
        amino_acid_seq: Some(vec![AminoAcid::UNK, AminoAcid::UNK]),
        amino_acid_seq_ids: Some(vec![0, 1]),
        amino_acid_insertion_codes: Some(vec!["".to_string(), "".to_string()]),
        amino_acid_labels: Some(vec![
            Label(0, "H2O".into()),
            Label(1, "SINGLE_ATOM_C".into()),
        ]),
        residues: Some(vec![vec![0, 1, 2], vec![3]]),
        residue_seq: Some(vec!["HOH".into(), "SINGLE_ATOM_C".into()]),
        residue_seq_ids: Some(vec![0, 1]),
        residue_insertion_codes: Some(vec!["".to_string(), "".to_string()]),
        residue_labels: Some(vec![
            Label(0, "H2O".into()),
            Label(1, "SINGLE_ATOM_C".into()),
        ]),
        subunits: None,
    }
}

fn build_example_residue_conformer() -> Conformer {
    Conformer {
        topology: Topology {
            symbols: vec!["H".into(), "H".into(), "O".into(), "C".into()],
            geometry: vec![1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 4.0, 4.0, 4.0],
            atom_charges: None,
            partial_charges: None,
            atom_labels: None,
            alts: None,
            connectivity: None,
            fragments: None,
            fragment_charges: None,
        },
        amino_acids: None,
        amino_acid_seq: None,
        amino_acid_seq_ids: None,
        amino_acid_insertion_codes: None,
        amino_acid_labels: None,
        residues: Some(vec![vec![0, 1, 2], vec![3]]),
        residue_seq: Some(vec!["HOH".into(), "SINGLE_ATOM_C".into()]),
        residue_seq_ids: Some(vec![0, 1]),
        residue_insertion_codes: Some(vec!["".to_string(), "".to_string()]),
        residue_labels: Some(vec![
            Label(0, "H2O".into()),
            Label(1, "SINGLE_ATOM_C".into()),
        ]),
        subunits: None,
    }
}

#[test]
fn test_conformer_creation() {
    let mut conformer = build_example_aa_conformer();
    assert_eq!(conformer.topology.symbols.len(), 4);
    assert_eq!(conformer.topology.symbols, ["H", "H", "O", "C"]);
    assert_eq!(conformer.topology.geometry.len(), 12);
    assert_eq!(
        conformer.topology.geometry,
        [1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 4.0, 4.0, 4.0]
    );
    // Test amino acid -specific stuff
    let aa = conformer.amino_acids.unwrap();
    assert_eq!(aa.len(), 2);
    assert_eq!(aa, [vec![0, 1, 2], vec![3]]);
    assert_eq!(conformer.amino_acid_seq.as_ref().unwrap().len(), 2);
    assert_eq!(conformer.amino_acid_seq_ids.as_ref().unwrap().len(), 2);
    assert_eq!(conformer.amino_acid_labels.as_ref().unwrap().len(), 2);
    // Test residue -specific stuff
    conformer = build_example_residue_conformer();
    let r = conformer.residues.as_ref().unwrap();
    assert_eq!(r.len(), 2);
    assert_eq!(r, &[vec![0, 1, 2], vec![3]]);
    assert_eq!(conformer.residue_seq.as_ref().unwrap().len(), 2);
    assert_eq!(conformer.residue_labels.as_ref().unwrap().len(), 2);
    assert!(conformer.is_valid());
}

#[test]
fn test_conformer_drop_amino_acids() {
    let mut conformer = build_example_aa_conformer();
    // Remove a set of amino acids and all the atoms it references from a conformer
    conformer.drop_amino_acids(&[1]);
    assert_eq!(conformer.topology.symbols.len(), 3);
    assert_eq!(conformer.topology.symbols, ["H", "H", "O"]);
    assert_eq!(conformer.topology.geometry.len(), 9);
    assert_eq!(
        conformer.topology.geometry,
        [1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0]
    );
    let aa = conformer.amino_acids.as_ref().unwrap();
    assert_eq!(aa.len(), 1);
    assert_eq!(aa, &[vec![0, 1, 2]]);
    assert_eq!(conformer.amino_acid_seq.as_ref().unwrap().len(), 1);
    assert_eq!(conformer.amino_acid_seq_ids.as_ref().unwrap().len(), 1);
    assert_eq!(conformer.amino_acid_labels.as_ref().unwrap().len(), 1);
    assert!(conformer.is_valid());
}

#[test]
fn test_conformer_keep_amino_acids() {
    let mut conformer = build_example_aa_conformer();
    conformer.keep_amino_acids(&[0]);
    let aas = conformer.amino_acids.as_ref().unwrap();
    assert_eq!(aas.len(), 1);
    assert_eq!(aas, &[vec![0, 1, 2]]);
    assert!(conformer.is_valid());
}

#[test]
fn test_conformer_drop_residues() {
    let mut conformer = build_example_residue_conformer();
    // Remove a set of residues and all the atoms it references from a conformer
    conformer.drop_residues(&[0]);
    assert_eq!(conformer.topology.symbols.len(), 1);
    assert_eq!(conformer.topology.symbols, ["C"]);
    assert_eq!(conformer.topology.geometry.len(), 3);
    assert_eq!(conformer.topology.geometry, [4.0, 4.0, 4.0]);
    let rs = conformer.residues.as_ref().unwrap();
    assert_eq!(rs.len(), 1);
    assert_eq!(rs, &[vec![0]]);
    assert_eq!(conformer.residue_seq.as_ref().unwrap().len(), 1);
    assert_eq!(conformer.residue_labels.as_ref().unwrap().len(), 1);
    assert!(conformer.is_valid());
}

#[test]
fn test_conformer_keep_residues() {
    let mut conformer = build_example_residue_conformer();
    conformer.keep_residues(&[1]);
    let rs = conformer.residues.as_ref().unwrap();
    assert_eq!(rs.len(), 1);
    assert_eq!(rs, &[vec![0]]);
    assert!(conformer.is_valid());
}

#[test]
fn test_conformer_amino_acids_near_point() {
    let conformer = build_example_aa_conformer();
    let nearby_aas_1 = conformer.get_amino_acids_near_point(&[2.5, 2.5, 2.5], 1.0);
    assert_eq!(nearby_aas_1.len(), 1);
    assert_eq!(nearby_aas_1, vec![0]);
    let nearby_aas_2 = conformer.get_amino_acids_near_point(&[3.5, 3.5, 3.5], 1.0);
    assert_eq!(nearby_aas_2.len(), 2);
    assert_eq!(nearby_aas_2, vec![0, 1]);
    assert!(conformer.is_valid());
}

fn test_conformer_add_aa_bonds(
    filename: impl AsRef<Path> + std::fmt::Debug,
    strictness: AtomCheckStrictness,
) -> anyhow::Result<()> {
    let aa_conformer = &mut load_test_pdb(&filename)?[0];
    aa_conformer
        .topology
        .connectivity
        .as_mut()
        .expect("")
        .clear();
    aa_conformer.perceive_bonds(strictness)?;
    // Get reference
    let aa_ref_conformer = &load_test_pdb(&filename)?[0];
    let bonds = BTreeSet::from_iter(
        aa_conformer
            .topology
            .connectivity
            .as_ref()
            .expect("No bonds in test amino acid!"),
    );
    let ref_bonds = BTreeSet::from_iter(
        aa_ref_conformer
            .topology
            .connectivity
            .as_ref()
            .expect("No bonds in reference amino acid!"),
    );
    for (bond, ref_bond) in zip_eq(bonds, ref_bonds) {
        assert_eq!(bond.0, ref_bond.0);
        assert_eq!(bond.1, ref_bond.1);
        let d = aa_conformer.topology.distance_between_atoms(bond.0, bond.1);
        assert_ge!(d, 0.965);
        assert_le!(d, 1.815);
        assert_eq!(
            aa_conformer.topology.symbols[bond.0 as usize],
            aa_ref_conformer.topology.symbols[ref_bond.0 as usize]
        );
        assert_eq!(
            aa_conformer.topology.symbols[bond.1 as usize],
            aa_ref_conformer.topology.symbols[ref_bond.1 as usize]
        );
        if bond.2 < 254 && ref_bond.2 < 254 {
            if bond.2 != ref_bond.2 {
                dbg!(&filename);
            }
            assert_eq!(bond.2, ref_bond.2);
        }
    }
    assert!(aa_conformer.is_valid());
    Ok(())
}

#[test]
fn test_conformer_add_aa_bonds_all() -> anyhow::Result<()> {
    for aa_name in [
        "ALA", "ARG", "ASN", "ASP", "CYS", "GLN", "GLU", "GLY", "HIS", "HYP", "ILE", "LEU", "LYS",
        "MET", "PHE", "PRO", "SER", "THR", "TRP", "TYR", "VAL",
    ] {
        test_conformer_add_aa_bonds(
            format!("data/amino_acids/{aa_name}_ideal.pdb"),
            AtomCheckStrictness::All,
        )?;
    }
    for cap_name in ["ACE", "NME", "NMA"] {
        test_conformer_add_aa_bonds(
            format!("data/amino_acids/{cap_name}_ideal.pdb"),
            AtomCheckStrictness::Heavy,
        )?;
    }
    Ok(())
}

fn test_conformer_add_aa_charges(
    filename: impl AsRef<Path> + std::fmt::Debug,
    strictness: AtomCheckStrictness,
) -> anyhow::Result<()> {
    let aa_conformer = &mut load_test_pdb(&filename)?[0];
    // Unset charges for a complete test
    if let Some(atom_charges) = &mut aa_conformer.topology.atom_charges {
        for atom_charge in atom_charges.iter_mut() {
            *atom_charge = std::i8::MIN;
        }
    }
    aa_conformer.perceive_formal_charges(strictness)?;
    // Get reference
    let aa_ref_conformer = &load_test_pdb(&filename)?[0];
    let atom_charges = Vec::from_iter(
        aa_conformer
            .topology
            .atom_charges
            .as_ref()
            .expect("No bonds in test amino acid!"),
    );
    let ref_atom_charges = Vec::from_iter(
        aa_ref_conformer
            .topology
            .atom_charges
            .as_ref()
            .expect("No bonds in reference amino acid!"),
    );
    for (atom_charge, ref_atom_charge) in zip_eq(atom_charges, ref_atom_charges) {
        assert_eq!(atom_charge, ref_atom_charge);
    }
    assert!(aa_conformer.is_valid());
    Ok(())
}

#[test]
fn test_conformer_add_aa_charges_all() -> anyhow::Result<()> {
    for aa_name in [
        "ALA", "ARG", "ASN", "ASP", "CYS", "GLN", "GLU", "GLY", "HIS", "HYP", "ILE", "LEU", "LYS",
        "MET", "PHE", "PRO", "SER", "THR", "TRP", "TYR", "VAL",
    ] {
        test_conformer_add_aa_charges(
            format!("data/amino_acids/{aa_name}_ideal.pdb"),
            AtomCheckStrictness::All,
        )?;
    }
    for cap_name in AminoAcidTemplate::CAP_RESIDUES {
        test_conformer_add_aa_charges(
            format!("data/amino_acids/{cap_name}_ideal.pdb"),
            AtomCheckStrictness::Heavy,
        )?;
    }
    Ok(())
}

#[test]
fn test_conformer_add_aa_bonds_6mj7() -> anyhow::Result<()> {
    let pdb_conformer = &mut load_test_pdb("data/6mj7_noalts.pdb")?[0];
    pdb_conformer.perceive_bonds(AtomCheckStrictness::Heavy)?;
    let bonds = BTreeSet::from_iter(
        pdb_conformer
            .topology
            .connectivity
            .as_ref()
            .expect("expected bonds after bond perception"),
    );
    for bond in bonds {
        let d = pdb_conformer
            .topology
            .distance_between_atoms(bond.0, bond.1);
        assert_ge!(d, 0.9);
        assert_le!(d, 2.1);
    }
    assert!(pdb_conformer.is_valid());
    Ok(())
}

#[test]
fn test_conformer_add_aa_bonds_5hnb() -> anyhow::Result<()> {
    // This is the source PDB for OpenFF cdk8, then
    //   - protonated with dd-fixer pdb2pqr,
    //   - manually modified to have correct charge.
    let pdb_conformer = &mut load_test_pdb("data/openff/5hnb_prepped.pdb")?[0];
    // Unset charges for a complete test
    if let Some(atom_charges) = &mut pdb_conformer.topology.atom_charges {
        for atom_charge in atom_charges.iter_mut() {
            *atom_charge = std::i8::MIN;
        }
    }
    pdb_conformer.perceive_bonds(AtomCheckStrictness::All)?;
    let bonds = BTreeSet::from_iter(
        pdb_conformer
            .topology
            .connectivity
            .as_ref()
            .expect("expected bonds after bond perception"),
    );
    for bond in bonds {
        let d = pdb_conformer
            .topology
            .distance_between_atoms(bond.0, bond.1);
        assert_ge!(d, 0.9);
        assert_le!(d, 2.1);
    }
    pdb_conformer.perceive_formal_charges(AtomCheckStrictness::All)?;
    let ref_pdb_conformer = &load_test_pdb("data/openff/5hnb_prepped.pdb")?[0];
    let mut prev_aa_atom_id = std::u32::MIN;
    let mut prev_aa_seq_id = std::i32::MIN;
    for (aa, &curr_aa_seq_id) in zip_eq(
        pdb_conformer.amino_acids.as_ref().unwrap(),
        pdb_conformer.amino_acid_seq_ids.as_ref().unwrap(),
    ) {
        // Make sure each chain has monotonically increasing (or equal) sequence IDs
        pdb_conformer
            .subunits
            .as_ref()
            .unwrap()
            .iter()
            .filter(|subunit| subunit.contains(&aa[0]) && subunit.contains(&prev_aa_atom_id))
            .for_each(|_| {
                assert_ge!(curr_aa_seq_id, prev_aa_seq_id);
            });
        prev_aa_atom_id = aa[0];
        prev_aa_seq_id = curr_aa_seq_id;
        for &atom_index in aa.iter() {
            let i = atom_index as usize;
            let (atom_label, atom_charge, ref_atom_label, ref_atom_charge) = (
                &pdb_conformer.topology.atom_labels.as_ref().unwrap()[i],
                &pdb_conformer.topology.atom_charges.as_ref().unwrap()[i],
                &ref_pdb_conformer.topology.atom_labels.as_ref().unwrap()[i],
                &ref_pdb_conformer.topology.atom_charges.as_ref().unwrap()[i],
            );
            assert_eq!(atom_label, ref_atom_label);
            assert_eq!(atom_charge, ref_atom_charge);
        }
    }
    assert!(pdb_conformer.is_valid());
    Ok(())
}
