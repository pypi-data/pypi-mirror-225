use std::{
    collections::{HashMap, HashSet},
    convert::From,
};

#[cfg(feature = "graphql")]
use async_graphql::Enum;
use itertools::Itertools;
use lazy_static::lazy_static;
use qdx_derive::Typedef;
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};
use strum_macros::EnumString;

use crate::bond::{
    Bond, BondOrder, BOND_ORDER_DOUBLE, BOND_ORDER_ONEANDAHALF, BOND_ORDER_RING, BOND_ORDER_SINGLE,
};

#[derive(thiserror::Error, Debug)]
pub enum Error {
    #[error("invalid amino acid name, found '{found}'")]
    ParseNameError { found: String },
    #[error("terminal residue has bad hydrogens, found '{found:?}'")]
    BadTerminusError { found: Vec<String> },
}

pub struct BondTemplate(pub &'static str, pub &'static str, pub BondOrder);

pub enum Terminus {
    C,
    N,
}

#[derive(Clone, Debug)]
pub struct ProtonationState {
    pub missing_hydrogens: HashSet<&'static str>,
    pub heavy_atom_charges: Vec<i8>,
}

impl ProtonationState {
    pub fn default(n_atoms: u32) -> ProtonationState {
        ProtonationState {
            missing_hydrogens: From::from([]),
            heavy_atom_charges: vec![0; n_atoms as usize],
        }
    }
}

pub struct AminoAcidTemplate {
    pub name: &'static str,
    pub protonation_state_variants: HashMap<&'static str, ProtonationState>,
    pub heavy_atom_labels: Vec<&'static str>,
    pub hydrogen_labels: HashSet<&'static str>,
    pub bonds: Vec<BondTemplate>,
}

impl AminoAcidTemplate {
    pub const CAP_RESIDUES: [&str; 3] = ["ACE", "NME", "NMA"];
    /// Stores labels only present in termini. The label "H" is needed here because of PRO and HYP.
    pub const TERMINI_ATOMS: [&str; 6] = ["OXT", "HXT", "H1", "H2", "H3", "H"];

    /// An amino acid template is a cap if it's in our explicit list of cap-like residues.
    /// Ideally these should be HETATM since they aren't amino acids, but they aren't always.
    pub fn is_cap(&self) -> bool {
        AminoAcidTemplate::CAP_RESIDUES.contains(&self.name)
    }

    /// Checks if the amino acid specified by the set of atom labels passed in is a terminus by
    /// checking if it has any atoms present only in termini. It's invalid for a non-terminal amino
    /// acid to have any of these atoms.
    /// `aa_atom_labels` must contain all atoms, including hydrogens, in a single amino acid.
    /// NOTE: There's no need to include "H" in the case of PRO and HYP in the check here because to
    ///       be a terminal residue it must contain at least one numbered H label anyway.
    /// TODO: This fails for an N-terminus that isn't expected to be protonated. We're only using it
    ///       during charge assignment right now, where protonation is assumed.
    pub fn is_terminus(&self, aa_atom_labels: &HashSet<&str>, terminus_type: Terminus) -> bool {
        if self.is_cap() {
            return false;
        }
        match terminus_type {
            Terminus::C => aa_atom_labels.contains("OXT"),
            Terminus::N => ["H1", "H2", "H3"]
                .iter()
                .any(|ter_h_label| aa_atom_labels.contains(ter_h_label)),
        }
    }

    /// Matches the atom labels passed in with a protonation state.
    /// `aa_atom_labels` must contain all hydrogen atoms in the single amino acid residue to check,
    /// but there is no problem if it contains more (e.g. the heavy atoms too).
    /// As expected, it will return None if there is no protonation state found.
    pub fn find_protonation_state(
        &self,
        aa_atom_labels: &HashSet<&str>,
    ) -> Option<ProtonationState> {
        let missing_hydrogens = self
            .hydrogen_labels
            .iter()
            .filter_map(|&k| (!aa_atom_labels.contains(&k)).then_some(k))
            .collect::<HashSet<&str>>();
        // Return the matching variant, if there is one
        self.protonation_state_variants
            .values()
            .find(|state| state.missing_hydrogens == missing_hydrogens)
            .cloned()
    }

    /// Produce the bonds for the passed-in amino acid data, for atoms only present in termini.
    /// Returns an empty iterator if the amino acid data doesn't correspond to a terminal residue.
    /// `aa_atom_map` maps the atom label to the atom index for a single amino acid residue,
    /// allowing us to generate the correct bond objects.
    /// NOTE: Caps are handled explicitly, and not as terminal residues.
    pub fn gen_termini_bonds<'a>(
        &'a self,
        aa_atom_map: &'a HashMap<&'a str, u32>,
    ) -> impl Iterator<Item = Bond> + 'a {
        // Handle hydrogens that should be connected to the nitrogen
        // The label "H" by itself is handled as a non-termini bond, except for PRO and HYP
        let ter_h_labels = if ["PRO", "HYP"].contains(&self.name) {
            vec!["H", "H1", "H2", "H3"]
        } else {
            vec!["H1", "H2", "H3"]
        };
        let new_connections = aa_atom_map
            .keys()
            .filter(move |&k| ter_h_labels.contains(k))
            .filter_map(
                |ter_h_label| match (aa_atom_map.get("N"), aa_atom_map.get(ter_h_label)) {
                    (Some(a_idx1), Some(a_idx2)) => Some(Bond(
                        *a_idx1.min(a_idx2),
                        *a_idx1.max(a_idx2),
                        BOND_ORDER_SINGLE,
                    )),
                    _ => None,
                },
            );
        // Handle oxygens at residues at the beginning of chains (and their possible hydrogen)
        let b1 = (aa_atom_map.keys().contains(&"OXT"))
            .then_some(match (aa_atom_map.get("OXT"), aa_atom_map.get("C")) {
                (Some(a_idx1), Some(a_idx2)) => Some(Bond(
                    *a_idx1.min(a_idx2),
                    *a_idx1.max(a_idx2),
                    BOND_ORDER_SINGLE,
                )),
                _ => None,
            })
            .flatten();
        let b2 = (aa_atom_map.keys().contains(&"HXT"))
            .then_some(match (aa_atom_map.get("OXT"), aa_atom_map.get("HXT")) {
                (Some(a_idx1), Some(a_idx2)) => Some(Bond(
                    *a_idx1.min(a_idx2),
                    *a_idx1.max(a_idx2),
                    BOND_ORDER_SINGLE,
                )),
                _ => None,
            })
            .flatten();
        new_connections
            .chain(std::iter::once(b1).flatten())
            .chain(std::iter::once(b2).flatten())
            .filter(|_| !self.is_cap()) // Caps have unique, explicit termini; return empty list
    }

    /// Produce the charges for the passed-in amino acid data, for the relevant terminal heavy atom.
    /// This means the charge for the "OXT" on a c-terminus, and for the "N" on the n-terminus.
    /// `aa_atom_labels` must contain all hydrogen atoms in the single amino acid residue to check,
    /// but there is no problem if it contains more (e.g. the heavy atoms too).
    /// Returns a BadTerminusError if the charge doesn't match an acceptable one.
    pub fn gen_termini_charge(
        &self,
        aa_atom_labels: &HashSet<&str>,
        terminus_type: Terminus,
    ) -> Result<i8, Error> {
        match terminus_type {
            Terminus::C => {
                let n_hs_term = aa_atom_labels.iter().filter(|&&k| k == "HXT").count() as i8;
                if (0..=1).contains(&n_hs_term) {
                    return Ok(n_hs_term - 1); // c terminus has 1 hydrogen at neutral charge
                }
            }
            Terminus::N => {
                let mut n_hs_term = aa_atom_labels
                    .iter()
                    .filter(|k| ["H", "H1", "H2", "H3"].contains(k))
                    .count() as i8;
                // Proline and hydroxyproline have an extra bond on this nitrogen
                if ["PRO", "HYP"].contains(&self.name) {
                    n_hs_term += 1;
                }
                if (2..=3).contains(&n_hs_term) {
                    return Ok(n_hs_term - 2); // n terminus has 2 hydrogen at neutral charge
                }
            }
        };
        Err(Error::BadTerminusError {
            found: aa_atom_labels.iter().map(|l| l.to_string()).collect(),
        })
    }
}

lazy_static! {
    #[rustfmt::skip]
    static ref GLY: AminoAcidTemplate = AminoAcidTemplate {
        name: "GLY",
        heavy_atom_labels: From::from([
            "N", "CA", "C", "O"]),
        protonation_state_variants: From::from(
            [("GLY", ProtonationState::default(4))]),
        hydrogen_labels: From::from([
            "H", "HA2", "HA3"]),
        bonds: vec![
            BondTemplate("N", "CA", BOND_ORDER_SINGLE),
            BondTemplate("C", "O", BOND_ORDER_DOUBLE),
            BondTemplate("CA", "C", BOND_ORDER_SINGLE),
            BondTemplate("N", "H", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA2", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA3", BOND_ORDER_SINGLE),
        ],
    };
    #[rustfmt::skip]
    static ref ALA: AminoAcidTemplate = AminoAcidTemplate {
        name: "ALA",
        heavy_atom_labels: From::from([
            "N", "CA", "C", "O", "CB"]),
        protonation_state_variants: From::from(
            [("ALA", ProtonationState::default(5))]),
        hydrogen_labels: From::from([
            "H", "HA", "HB1", "HB2", "HB3"]),
        bonds: vec![
            BondTemplate("N", "CA", BOND_ORDER_SINGLE),
            BondTemplate("C", "O", BOND_ORDER_DOUBLE),
            BondTemplate("CA", "C", BOND_ORDER_SINGLE),
            BondTemplate("CB", "CA", BOND_ORDER_SINGLE),
            BondTemplate("N", "H", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB1", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB2", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB3", BOND_ORDER_SINGLE),
        ],
    };
    #[rustfmt::skip]
    static ref VAL: AminoAcidTemplate = AminoAcidTemplate {
        name: "VAL",
        heavy_atom_labels: From::from([
            "N", "CA", "C", "O", "CB", "CG1", "CG2"]),
        protonation_state_variants: From::from(
            [("VAL", ProtonationState::default(7))]),
        hydrogen_labels: From::from([
            "H", "HA", "HB", "HG11", "HG12", "HG13", "HG21", "HG22", "HG23"]),
        bonds: vec![
            BondTemplate("N", "CA", BOND_ORDER_SINGLE),
            BondTemplate("C", "O", BOND_ORDER_DOUBLE),
            BondTemplate("CA", "C", BOND_ORDER_SINGLE),
            BondTemplate("CB", "CA", BOND_ORDER_SINGLE),
            BondTemplate("CG1", "CB", BOND_ORDER_SINGLE),
            BondTemplate("CG2", "CB", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB", BOND_ORDER_SINGLE),
            BondTemplate("CG1", "HG11", BOND_ORDER_SINGLE),
            BondTemplate("CG1", "HG12", BOND_ORDER_SINGLE),
            BondTemplate("CG1", "HG13", BOND_ORDER_SINGLE),
            BondTemplate("CG2", "HG21", BOND_ORDER_SINGLE),
            BondTemplate("CG2", "HG22", BOND_ORDER_SINGLE),
            BondTemplate("CG2", "HG23", BOND_ORDER_SINGLE),
            BondTemplate("N", "H", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB", BOND_ORDER_SINGLE),
            BondTemplate("CG1", "HG11", BOND_ORDER_SINGLE),
            BondTemplate("CG1", "HG12", BOND_ORDER_SINGLE),
            BondTemplate("CG1", "HG13", BOND_ORDER_SINGLE),
            BondTemplate("CG2", "HG21", BOND_ORDER_SINGLE),
            BondTemplate("CG2", "HG22", BOND_ORDER_SINGLE),
            BondTemplate("CG2", "HG23", BOND_ORDER_SINGLE),
        ],
    };
    #[rustfmt::skip]
    static ref LEU: AminoAcidTemplate = AminoAcidTemplate {
        name: "LEU",
        heavy_atom_labels: From::from([
            "N", "CA", "C", "O", "CB", "CG", "CD1", "CD2"]),
        protonation_state_variants: From::from(
            [("LEU", ProtonationState::default(8))]),
        hydrogen_labels: From::from([
            "H", "HA", "HB2", "HB3", "HG", "HD11", "HD12", "HD13", "HD21", "HD22", "HD23"]),
        bonds: vec![
            BondTemplate("N", "CA", BOND_ORDER_SINGLE),
            BondTemplate("C", "O", BOND_ORDER_DOUBLE),
            BondTemplate("CA", "C", BOND_ORDER_SINGLE),
            BondTemplate("CB", "CA", BOND_ORDER_SINGLE),
            BondTemplate("CG", "CB", BOND_ORDER_SINGLE),
            BondTemplate("CD1", "CG", BOND_ORDER_SINGLE),
            BondTemplate("CD2", "CG", BOND_ORDER_SINGLE),
            BondTemplate("N", "H", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB2", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB3", BOND_ORDER_SINGLE),
            BondTemplate("CG", "HG", BOND_ORDER_SINGLE),
            BondTemplate("CD1", "HD11", BOND_ORDER_SINGLE),
            BondTemplate("CD1", "HD12", BOND_ORDER_SINGLE),
            BondTemplate("CD1", "HD13", BOND_ORDER_SINGLE),
            BondTemplate("CD2", "HD21", BOND_ORDER_SINGLE),
            BondTemplate("CD2", "HD22", BOND_ORDER_SINGLE),
            BondTemplate("CD2", "HD23", BOND_ORDER_SINGLE),
        ],
    };
    #[rustfmt::skip]
    static ref ILE: AminoAcidTemplate = AminoAcidTemplate {
        name: "ILE",
        heavy_atom_labels: From::from([
            "N", "CA", "C", "O", "CB", "CG1", "CG2", "CD1"]),
        protonation_state_variants: From::from(
            [("ILE", ProtonationState::default(8))]),
        hydrogen_labels: From::from([
            "H", "HA", "HB", "HG12", "HG13", "HG21", "HG22", "HG23", "HD11", "HD12", "HD13"]),
        bonds: vec![
            BondTemplate("N", "CA", BOND_ORDER_SINGLE),
            BondTemplate("C", "O", BOND_ORDER_DOUBLE),
            BondTemplate("CA", "C", BOND_ORDER_SINGLE),
            BondTemplate("CB", "CA", BOND_ORDER_SINGLE),
            BondTemplate("CG1", "CB", BOND_ORDER_SINGLE),
            BondTemplate("CG2", "CB", BOND_ORDER_SINGLE),
            BondTemplate("CD1", "CG1", BOND_ORDER_SINGLE),
            BondTemplate("N", "H", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB", BOND_ORDER_SINGLE),
            BondTemplate("CG1", "HG12", BOND_ORDER_SINGLE),
            BondTemplate("CG1", "HG13", BOND_ORDER_SINGLE),
            BondTemplate("CG2", "HG21", BOND_ORDER_SINGLE),
            BondTemplate("CG2", "HG22", BOND_ORDER_SINGLE),
            BondTemplate("CG2", "HG23", BOND_ORDER_SINGLE),
            BondTemplate("CD1", "HD11", BOND_ORDER_SINGLE),
            BondTemplate("CD1", "HD12", BOND_ORDER_SINGLE),
            BondTemplate("CD1", "HD13", BOND_ORDER_SINGLE),
        ],
    };
    #[rustfmt::skip]
    static ref PRO: AminoAcidTemplate = AminoAcidTemplate {
        name: "PRO",
        heavy_atom_labels: From::from([
            "N", "CA", "C", "O", "CB", "CG", "CD"]),
        protonation_state_variants: From::from(
            [("PRO", ProtonationState::default(7))]),
        hydrogen_labels: From::from([
            "HA", "HB2", "HB3", "HG2", "HG3", "HD2", "HD3"]),
        bonds: vec![
            BondTemplate("N", "CA", BOND_ORDER_SINGLE),
            BondTemplate("C", "O", BOND_ORDER_DOUBLE),
            BondTemplate("CA", "C", BOND_ORDER_SINGLE),
            BondTemplate("CB", "CA", BOND_ORDER_SINGLE),
            BondTemplate("CG", "CB", BOND_ORDER_SINGLE),
            BondTemplate("CD", "CG", BOND_ORDER_SINGLE),
            BondTemplate("CD", "N", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB2", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB3", BOND_ORDER_SINGLE),
            BondTemplate("CG", "HG2", BOND_ORDER_SINGLE),
            BondTemplate("CG", "HG3", BOND_ORDER_SINGLE),
            BondTemplate("CD", "HD2", BOND_ORDER_SINGLE),
            BondTemplate("CD", "HD3", BOND_ORDER_SINGLE),
        ],
    };
    #[rustfmt::skip]
    static ref SER: AminoAcidTemplate = AminoAcidTemplate {
        name: "SER",
        heavy_atom_labels: From::from([
            "N", "CA", "C", "O", "CB", "OG"]),
        protonation_state_variants: From::from(
            [("SER", ProtonationState::default(6))]),
        hydrogen_labels: From::from([
            "H", "HA", "HB2", "HB3", "HG"]),
        bonds: vec![
            BondTemplate("N", "CA", BOND_ORDER_SINGLE),
            BondTemplate("C", "O", BOND_ORDER_DOUBLE),
            BondTemplate("CA", "C", BOND_ORDER_SINGLE),
            BondTemplate("CB", "CA", BOND_ORDER_SINGLE),
            BondTemplate("OG", "CB", BOND_ORDER_SINGLE),
            BondTemplate("N", "H", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB2", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB3", BOND_ORDER_SINGLE),
            BondTemplate("OG", "HG", BOND_ORDER_SINGLE),
        ],
    };
    #[rustfmt::skip]
    static ref THR: AminoAcidTemplate = AminoAcidTemplate {
        name: "THR",
        heavy_atom_labels: From::from([
            "N", "CA", "C", "O", "CB", "OG1", "CG2"]),
        protonation_state_variants: From::from(
            [("THR", ProtonationState::default(7))]),
        hydrogen_labels: From::from([
            "H", "HA", "HB", "HG1", "HG21", "HG22", "HG23"]),
        bonds: vec![
            BondTemplate("N", "CA", BOND_ORDER_SINGLE),
            BondTemplate("C", "O", BOND_ORDER_DOUBLE),
            BondTemplate("CA", "C", BOND_ORDER_SINGLE),
            BondTemplate("CB", "CA", BOND_ORDER_SINGLE),
            BondTemplate("OG1", "CB", BOND_ORDER_SINGLE),
            BondTemplate("CG2", "CB", BOND_ORDER_SINGLE),
            BondTemplate("N", "H", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB", BOND_ORDER_SINGLE),
            BondTemplate("OG1", "HG1", BOND_ORDER_SINGLE),
            BondTemplate("CG2", "HG21", BOND_ORDER_SINGLE),
            BondTemplate("CG2", "HG22", BOND_ORDER_SINGLE),
            BondTemplate("CG2", "HG23", BOND_ORDER_SINGLE),
        ],
    };
    #[rustfmt::skip]
    static ref ASN: AminoAcidTemplate = AminoAcidTemplate {
        name: "ASN",
        heavy_atom_labels: From::from([
            "N", "CA", "C", "O", "CB", "CG", "OD1", "ND2"]),
        protonation_state_variants: From::from(
            [("ASN", ProtonationState::default(8))]),
        hydrogen_labels: From::from([
            "H", "HA", "HB2", "HB3", "HD21", "HD22"]),
        bonds: vec![
            BondTemplate("N", "CA", BOND_ORDER_SINGLE),
            BondTemplate("C", "O", BOND_ORDER_DOUBLE),
            BondTemplate("CA", "C", BOND_ORDER_SINGLE),
            BondTemplate("CB", "CA", BOND_ORDER_SINGLE),
            BondTemplate("CG", "CB", BOND_ORDER_SINGLE),
            BondTemplate("OD1", "CG", BOND_ORDER_DOUBLE),
            BondTemplate("ND2", "CG", BOND_ORDER_SINGLE),
            BondTemplate("N", "H", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB2", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB3", BOND_ORDER_SINGLE),
            BondTemplate("ND2", "HD21", BOND_ORDER_SINGLE),
            BondTemplate("ND2", "HD22", BOND_ORDER_SINGLE),
        ],
    };
    #[rustfmt::skip]
    static ref GLN: AminoAcidTemplate = AminoAcidTemplate {
        name: "GLN",
        heavy_atom_labels: From::from([
            "N", "CA", "C", "O", "CB", "CG", "CD", "OE1", "NE2"]),
        protonation_state_variants: From::from(
            [("GLN", ProtonationState::default(9))]),
        hydrogen_labels: From::from([
            "H", "HA", "HB2", "HB3", "HG2", "HG3", "HE21", "HE22"]),
        bonds: vec![
            BondTemplate("N", "CA", BOND_ORDER_SINGLE),
            BondTemplate("C", "O", BOND_ORDER_DOUBLE),
            BondTemplate("CA", "C", BOND_ORDER_SINGLE),
            BondTemplate("CB", "CA", BOND_ORDER_SINGLE),
            BondTemplate("CG", "CB", BOND_ORDER_SINGLE),
            BondTemplate("CD", "CG", BOND_ORDER_SINGLE),
            BondTemplate("OE1", "CD", BOND_ORDER_DOUBLE),
            BondTemplate("NE2", "CD", BOND_ORDER_SINGLE),
            BondTemplate("N", "H", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB2", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB3", BOND_ORDER_SINGLE),
            BondTemplate("CG", "HG2", BOND_ORDER_SINGLE),
            BondTemplate("CG", "HG3", BOND_ORDER_SINGLE),
            BondTemplate("NE2", "HE21", BOND_ORDER_SINGLE),
            BondTemplate("NE2", "HE22", BOND_ORDER_SINGLE),
        ],
    };
    #[rustfmt::skip]
    static ref CYS: AminoAcidTemplate = AminoAcidTemplate {
        name: "CYS",
        heavy_atom_labels: From::from([
            "N", "CA", "C", "O", "CB", "SG"]),
        protonation_state_variants: From::from([(
            "CYS",
            ProtonationState {
                missing_hydrogens: From::from([]),
                heavy_atom_charges: vec![0, 0, 0, 0, 0, 0] }
        ), (
            "CYD",
            ProtonationState {
                missing_hydrogens: From::from(["HG"]),
                heavy_atom_charges: vec![0, 0, 0, 0, 0, -1] }
        ), (
            "CYX",
            ProtonationState {
                missing_hydrogens: From::from(["HG"]),
                heavy_atom_charges: vec![0, 0, 0, 0, 0, -1] }
        )]),
        hydrogen_labels: From::from([
            "H", "HA", "HB2", "HB3", "HG"]),
        bonds: vec![
            BondTemplate("N", "CA", BOND_ORDER_SINGLE),
            BondTemplate("C", "O", BOND_ORDER_DOUBLE),
            BondTemplate("CA", "C", BOND_ORDER_SINGLE),
            BondTemplate("CB", "CA", BOND_ORDER_SINGLE),
            BondTemplate("SG", "CB", BOND_ORDER_SINGLE),
            BondTemplate("N", "H", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB2", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB3", BOND_ORDER_SINGLE),
            BondTemplate("SG", "HG", BOND_ORDER_SINGLE), // Optional (without -> CYD/CYX)
        ],
    };
    #[rustfmt::skip]
    static ref MET: AminoAcidTemplate = AminoAcidTemplate {
        name: "MET",
        heavy_atom_labels: From::from([
            "N", "CA", "C", "O", "CB", "CG", "SD", "CE"]),
        protonation_state_variants: From::from(
            [("MET", ProtonationState::default(8))]),
        hydrogen_labels: From::from([
            "H", "HA", "HB2", "HB3", "HG2", "HG3", "HE1", "HE2", "HE3"]),
        bonds: vec![
            BondTemplate("N", "CA", BOND_ORDER_SINGLE),
            BondTemplate("C", "O", BOND_ORDER_DOUBLE),
            BondTemplate("CA", "C", BOND_ORDER_SINGLE),
            BondTemplate("CB", "CA", BOND_ORDER_SINGLE),
            BondTemplate("CG", "CB", BOND_ORDER_SINGLE),
            BondTemplate("SD", "CG", BOND_ORDER_SINGLE),
            BondTemplate("CE", "SD", BOND_ORDER_SINGLE),
            BondTemplate("N", "H", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB2", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB3", BOND_ORDER_SINGLE),
            BondTemplate("CG", "HG2", BOND_ORDER_SINGLE),
            BondTemplate("CG", "HG3", BOND_ORDER_SINGLE),
            BondTemplate("CE", "HE1", BOND_ORDER_SINGLE),
            BondTemplate("CE", "HE2", BOND_ORDER_SINGLE),
            BondTemplate("CE", "HE3", BOND_ORDER_SINGLE),
        ],
    };
    #[rustfmt::skip]
    static ref PHE: AminoAcidTemplate = AminoAcidTemplate {
        name: "PHE",
        heavy_atom_labels: From::from([
            "N", "CA", "C", "O", "CB", "CG", "CD1", "CD2", "CE1", "CE2", "CZ"]),
        protonation_state_variants: From::from(
            [("PHE", ProtonationState::default(11))]),
        hydrogen_labels: From::from([
            "H", "HA", "HB2", "HB3", "HD1", "HD2", "HE1", "HE2", "HZ"]),
        bonds: vec![
            BondTemplate("N", "CA", BOND_ORDER_SINGLE),
            BondTemplate("C", "O", BOND_ORDER_DOUBLE),
            BondTemplate("CA", "C", BOND_ORDER_SINGLE),
            BondTemplate("CB", "CA", BOND_ORDER_SINGLE),
            BondTemplate("CG", "CB", BOND_ORDER_SINGLE),
            BondTemplate("CD1", "CG", BOND_ORDER_RING),
            BondTemplate("CD2", "CG", BOND_ORDER_RING),
            BondTemplate("CE1", "CD1", BOND_ORDER_RING),
            BondTemplate("CE2", "CD2", BOND_ORDER_RING),
            BondTemplate("CZ", "CE1", BOND_ORDER_RING),
            BondTemplate("CZ", "CE2", BOND_ORDER_RING),
            BondTemplate("N", "H", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB2", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB3", BOND_ORDER_SINGLE),
            BondTemplate("CD1", "HD1", BOND_ORDER_SINGLE),
            BondTemplate("CD2", "HD2", BOND_ORDER_SINGLE),
            BondTemplate("CE1", "HE1", BOND_ORDER_SINGLE),
            BondTemplate("CE2", "HE2", BOND_ORDER_SINGLE),
            BondTemplate("CZ", "HZ", BOND_ORDER_SINGLE),
        ],
    };
    #[rustfmt::skip]
    static ref TYR: AminoAcidTemplate = AminoAcidTemplate {
        name: "TYR",
        heavy_atom_labels: From::from([
            "N", "CA", "C", "O", "CB", "CG", "CD1", "CD2", "CE1", "CE2", "CZ", "OH"]),
        protonation_state_variants: From::from([(
            "TYR",
            ProtonationState {
                missing_hydrogens: From::from([]),
                heavy_atom_charges: vec![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] }
        ), (
            "TYD",
            ProtonationState {
                missing_hydrogens: From::from(["HH"]),
                heavy_atom_charges: vec![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1] }
        )]),
        hydrogen_labels: From::from([
            "H", "HA", "HB2", "HB3", "HD1", "HD2", "HE1", "HE2", "HH"]),
        bonds: vec![
            BondTemplate("N", "CA", BOND_ORDER_SINGLE),
            BondTemplate("C", "O", BOND_ORDER_DOUBLE),
            BondTemplate("CA", "C", BOND_ORDER_SINGLE),
            BondTemplate("CB", "CA", BOND_ORDER_SINGLE),
            BondTemplate("CG", "CB", BOND_ORDER_SINGLE),
            BondTemplate("CD1", "CG", BOND_ORDER_RING),
            BondTemplate("CD2", "CG", BOND_ORDER_RING),
            BondTemplate("CE1", "CD1", BOND_ORDER_RING),
            BondTemplate("CE2", "CD2", BOND_ORDER_RING),
            BondTemplate("CZ", "CE1", BOND_ORDER_RING),
            BondTemplate("CZ", "CE2", BOND_ORDER_RING),
            BondTemplate("OH", "CZ", BOND_ORDER_SINGLE),
            BondTemplate("N", "H", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB2", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB3", BOND_ORDER_SINGLE),
            BondTemplate("CD1", "HD1", BOND_ORDER_SINGLE),
            BondTemplate("CD2", "HD2", BOND_ORDER_SINGLE),
            BondTemplate("CE1", "HE1", BOND_ORDER_SINGLE),
            BondTemplate("CE2", "HE2", BOND_ORDER_SINGLE),
            BondTemplate("OH", "HH", BOND_ORDER_SINGLE), // Optional (without -> TYD)
        ],
    };
    #[rustfmt::skip]
    static ref TRP: AminoAcidTemplate = AminoAcidTemplate {
        name: "TRP",
        heavy_atom_labels: From::from([
            "N", "CA", "C", "O", "CB", "CG", "CD1", "CD2", "NE1", "CE2", "CE3", "CZ2", "CZ3", "CH2"]),
        protonation_state_variants: From::from(
            [("TRP", ProtonationState::default(14))]),
        hydrogen_labels: From::from([
            "H", "HA", "HB2", "HB3", "HD1", "HE1", "HE3", "HZ2", "HZ3", "HH2"]),
        bonds: vec![
            BondTemplate("N", "CA", BOND_ORDER_SINGLE),
            BondTemplate("C", "O", BOND_ORDER_DOUBLE),
            BondTemplate("CA", "C", BOND_ORDER_SINGLE),
            BondTemplate("CB", "CA", BOND_ORDER_SINGLE),
            BondTemplate("CG", "CB", BOND_ORDER_SINGLE),
            BondTemplate("CD1", "CG", BOND_ORDER_RING),
            BondTemplate("CD2", "CG", BOND_ORDER_RING),
            BondTemplate("NE1", "CD1", BOND_ORDER_RING),
            BondTemplate("CE2", "CD2", BOND_ORDER_RING),
            BondTemplate("CE2", "NE1", BOND_ORDER_RING),
            BondTemplate("CE3", "CD2", BOND_ORDER_RING),
            BondTemplate("CZ2", "CE2", BOND_ORDER_RING),
            BondTemplate("CZ3", "CE3", BOND_ORDER_RING),
            BondTemplate("CH2", "CZ2", BOND_ORDER_RING),
            BondTemplate("CH2", "CZ3", BOND_ORDER_RING),
            BondTemplate("N", "H", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB2", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB3", BOND_ORDER_SINGLE),
            BondTemplate("CD1", "HD1", BOND_ORDER_SINGLE),
            BondTemplate("NE1", "HE1", BOND_ORDER_SINGLE),
            BondTemplate("CD2", "HD2", BOND_ORDER_SINGLE),
            BondTemplate("CE3", "HE3", BOND_ORDER_SINGLE),
            BondTemplate("CZ2", "HZ2", BOND_ORDER_SINGLE),
            BondTemplate("CZ3", "HZ3", BOND_ORDER_SINGLE),
            BondTemplate("CH2", "HH2", BOND_ORDER_SINGLE),
        ],
    };
    //#[rustfmt::skip]
    static ref ASP: AminoAcidTemplate = AminoAcidTemplate {
        name: "ASP",
        heavy_atom_labels: From::from([
            "N", "CA", "C", "O", "CB", "CG", "OD1", "OD2"]),
        protonation_state_variants: From::from([(
            "ASP",
            ProtonationState {
                missing_hydrogens: From::from(["HD2"]),
                heavy_atom_charges: vec![0, 0, 0, 0, 0, 0, 0, -1] }
        ), (
            "ASH",
            ProtonationState {
                missing_hydrogens: From::from([]),
                heavy_atom_charges: vec![0, 0, 0, 0, 0, 0, 0, 0] }
        )]),
        hydrogen_labels: From::from([
            "H", "HA", "HB2", "HB3", "HD2"]),
        bonds: vec![
            BondTemplate("N", "CA", BOND_ORDER_SINGLE),
            BondTemplate("C", "O", BOND_ORDER_DOUBLE),
            BondTemplate("CA", "C", BOND_ORDER_SINGLE),
            BondTemplate("CB", "CA", BOND_ORDER_SINGLE),
            BondTemplate("CG", "CB", BOND_ORDER_SINGLE),
            BondTemplate("OD1", "CG", BOND_ORDER_ONEANDAHALF),
            BondTemplate("OD2", "CG", BOND_ORDER_ONEANDAHALF),
            BondTemplate("N", "H", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB2", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB3", BOND_ORDER_SINGLE),
            BondTemplate("OD2", "HD2", BOND_ORDER_SINGLE), // Optional (ASH)
        ],
    };
    #[rustfmt::skip]
    static ref GLU: AminoAcidTemplate = AminoAcidTemplate {
        name: "GLU",
        heavy_atom_labels: From::from([
            "N", "CA", "C", "O", "CB", "CG", "CD", "OE1", "OE2"]),
        protonation_state_variants: From::from([(
            "GLU",
            ProtonationState {
                missing_hydrogens: From::from(["HE2"]),
                heavy_atom_charges: vec![0, 0, 0, 0, 0, 0, 0, 0, -1] }
        ), (
            "GLH",
            ProtonationState {
                missing_hydrogens: From::from([]),
                heavy_atom_charges: vec![0, 0, 0, 0, 0, 0, 0, 0, 0] }
        )]),
        hydrogen_labels: From::from([
            "H", "HA", "HB2", "HB3", "HG2", "HG3", "HE2"]),
        bonds: vec![
            BondTemplate("N", "CA", BOND_ORDER_SINGLE),
            BondTemplate("C", "O", BOND_ORDER_DOUBLE),
            BondTemplate("CA", "C", BOND_ORDER_SINGLE),
            BondTemplate("CB", "CA", BOND_ORDER_SINGLE),
            BondTemplate("CG", "CB", BOND_ORDER_SINGLE),
            BondTemplate("CD", "CG", BOND_ORDER_SINGLE),
            BondTemplate("OE1", "CD", BOND_ORDER_ONEANDAHALF),
            BondTemplate("OE2", "CD", BOND_ORDER_ONEANDAHALF),
            BondTemplate("N", "H", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB2", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB3", BOND_ORDER_SINGLE),
            BondTemplate("CG", "HG2", BOND_ORDER_SINGLE),
            BondTemplate("CG", "HG3", BOND_ORDER_SINGLE),
            BondTemplate("OE2", "HE2", BOND_ORDER_SINGLE), // Optional (GLH)
        ],
    };
    #[rustfmt::skip]
    static ref HIS: AminoAcidTemplate = AminoAcidTemplate {
        name: "HIS",
        heavy_atom_labels: From::from([
            "N", "CA", "C", "O", "CB", "CG", "ND1", "CD2", "CE1", "NE2"]),
        protonation_state_variants: From::from([(
            "HIS",
            ProtonationState {
                missing_hydrogens: From::from(["HD1"]),
                heavy_atom_charges: vec![0, 0, 0, 0, 0, 0, 0, 0, 0, 0] }
        ), (
            "HIN",
            ProtonationState {
                missing_hydrogens: From::from(["HD1", "HE2"]),
                heavy_atom_charges: vec![0, 0, 0, 0, 0, 0, 0, 0, 0, -1] }
        ), (
            "HID",
            ProtonationState {
                missing_hydrogens: From::from(["HE2"]),
                heavy_atom_charges: vec![0, 0, 0, 0, 0, 0, 0, 0, 0, 0] }
        ), (
            "HIE",
            ProtonationState {
                missing_hydrogens: From::from(["HD1"]),
                heavy_atom_charges: vec![0, 0, 0, 0, 0, 0, 0, 0, 0, 0] }
        ), (
            "HIP",
            ProtonationState {
                missing_hydrogens: From::from([]),
                heavy_atom_charges: vec![0, 0, 0, 0, 0, 0, 0, 0, 0, 1] }
        )]),
        hydrogen_labels: From::from([
            "H", "HA", "HB2", "HB3", "HD1", "HD2", "HE1", "HE2"]),
        bonds: vec![
            BondTemplate("N", "CA", BOND_ORDER_SINGLE),
            BondTemplate("C", "O", BOND_ORDER_DOUBLE),
            BondTemplate("CA", "C", BOND_ORDER_SINGLE),
            BondTemplate("CB", "CA", BOND_ORDER_SINGLE),
            BondTemplate("CG", "CB", BOND_ORDER_SINGLE),
            BondTemplate("ND1", "CG", BOND_ORDER_RING),
            BondTemplate("CD2", "CG", BOND_ORDER_RING),
            BondTemplate("CE1", "ND1", BOND_ORDER_RING),
            BondTemplate("NE2", "CD2", BOND_ORDER_RING),
            BondTemplate("NE2", "CE1", BOND_ORDER_RING),
            BondTemplate("N", "H", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB2", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB3", BOND_ORDER_SINGLE),
            // HIN: HD2, HE1
            // HID: HD2, HE1, HD1
            // HIE: HD2, HE1, HE2 (also called HIS)
            // HIP: HD2, HE1, HD1, HE2
            BondTemplate("ND1", "HD1", BOND_ORDER_SINGLE),
            BondTemplate("CD2", "HD2", BOND_ORDER_SINGLE),
            BondTemplate("CE1", "HE1", BOND_ORDER_SINGLE),
            BondTemplate("NE2", "HE2", BOND_ORDER_SINGLE),
        ],
    };
    #[rustfmt::skip]
    static ref LYS: AminoAcidTemplate = AminoAcidTemplate {
        name: "LYS",
        heavy_atom_labels: From::from([
            "N", "CA", "C", "O", "CB", "CG", "CD", "CE", "NZ"]),
        protonation_state_variants: From::from([(
            "LYS",
            ProtonationState {
                missing_hydrogens: From::from([]),
                heavy_atom_charges: vec![0, 0, 0, 0, 0, 0, 0, 0, 1] }
        ), (
            "LYD",
            ProtonationState {
                missing_hydrogens: From::from(["HZ3"]),
                heavy_atom_charges: vec![0, 0, 0, 0, 0, 0, 0, 0, 0] }
        ), (
            "LYN",
            ProtonationState {
                missing_hydrogens: From::from(["HZ3"]),
                heavy_atom_charges: vec![0, 0, 0, 0, 0, 0, 0, 0, 0] }
        )]),
        hydrogen_labels: From::from([
            "H", "HA", "HB2", "HB3", "HG2", "HG3", "HD2", "HD3", "HE2", "HE3", "HZ1", "HZ2", "HZ3"]),
        bonds: vec![
            BondTemplate("N", "CA", BOND_ORDER_SINGLE),
            BondTemplate("C", "O", BOND_ORDER_DOUBLE),
            BondTemplate("CA", "C", BOND_ORDER_SINGLE),
            BondTemplate("CB", "CA", BOND_ORDER_SINGLE),
            BondTemplate("CG", "CB", BOND_ORDER_SINGLE),
            BondTemplate("CD", "CG", BOND_ORDER_SINGLE),
            BondTemplate("CE", "CD", BOND_ORDER_SINGLE),
            BondTemplate("NZ", "CE", BOND_ORDER_SINGLE),
            BondTemplate("N", "H", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB2", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB3", BOND_ORDER_SINGLE),
            BondTemplate("CG", "HG2", BOND_ORDER_SINGLE),
            BondTemplate("CG", "HG3", BOND_ORDER_SINGLE),
            BondTemplate("CD", "HD2", BOND_ORDER_SINGLE),
            BondTemplate("CD", "HD3", BOND_ORDER_SINGLE),
            BondTemplate("CE", "HE2", BOND_ORDER_SINGLE),
            BondTemplate("CE", "HE3", BOND_ORDER_SINGLE),
            BondTemplate("NZ", "HZ1", BOND_ORDER_SINGLE),
            BondTemplate("NZ", "HZ2", BOND_ORDER_SINGLE),
            BondTemplate("NZ", "HZ3", BOND_ORDER_SINGLE), // Optional (without -> LYD/LYN)
        ],
    };
    #[rustfmt::skip]
    static ref ARG: AminoAcidTemplate = AminoAcidTemplate {
        name: "ARG",
        heavy_atom_labels: From::from([
            "N", "CA", "C", "O", "CB", "CG", "CD", "NE", "CZ", "NH1", "NH2"]),
        protonation_state_variants: From::from([(
            "ARG",
            ProtonationState {
                missing_hydrogens: From::from([]),
                heavy_atom_charges: vec![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1] }
        )]),
        hydrogen_labels: From::from([
            "H", "HA", "HB2", "HB3", "HG2", "HG3", "HD2", "HD3", "HE", "HH11", "HH12", "HH21", "HH22"]),
        bonds: vec![
            BondTemplate("N", "CA", BOND_ORDER_SINGLE),
            BondTemplate("C", "O", BOND_ORDER_DOUBLE),
            BondTemplate("CA", "C", BOND_ORDER_SINGLE),
            BondTemplate("CB", "CA", BOND_ORDER_SINGLE),
            BondTemplate("CG", "CB", BOND_ORDER_SINGLE),
            BondTemplate("CD", "CG", BOND_ORDER_SINGLE),
            BondTemplate("NE", "CD", BOND_ORDER_SINGLE),
            BondTemplate("CZ", "NE", BOND_ORDER_SINGLE),
            BondTemplate("NH1", "CZ", BOND_ORDER_ONEANDAHALF),
            BondTemplate("NH2", "CZ", BOND_ORDER_ONEANDAHALF),
            BondTemplate("N", "H", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB2", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB3", BOND_ORDER_SINGLE),
            BondTemplate("CG", "HG2", BOND_ORDER_SINGLE),
            BondTemplate("CG", "HG3", BOND_ORDER_SINGLE),
            BondTemplate("CD", "HD2", BOND_ORDER_SINGLE),
            BondTemplate("CD", "HD3", BOND_ORDER_SINGLE),
            BondTemplate("NE", "HE", BOND_ORDER_SINGLE),
            BondTemplate("NH1", "HH11", BOND_ORDER_SINGLE),
            BondTemplate("NH1", "HH12", BOND_ORDER_SINGLE),
            BondTemplate("NH2", "HH21", BOND_ORDER_SINGLE),
            BondTemplate("NH2", "HH22", BOND_ORDER_SINGLE),
        ],
    };
    #[rustfmt::skip]
    static ref HYP: AminoAcidTemplate = AminoAcidTemplate {
        name: "HYP",
        heavy_atom_labels: From::from([
            "N", "CA", "C", "O", "CB", "CG", "CD", "OD"]),
        protonation_state_variants: From::from(
            [("HYP", ProtonationState::default(8))]),
        hydrogen_labels: From::from([
            "HA", "HB2", "HB3", "HG", "HD2", "HD3", "HD"]),
        bonds: vec![
            BondTemplate("N", "CA", BOND_ORDER_SINGLE),
            BondTemplate("C", "O", BOND_ORDER_DOUBLE),
            BondTemplate("CA", "C", BOND_ORDER_SINGLE),
            BondTemplate("CB", "CA", BOND_ORDER_SINGLE),
            BondTemplate("CG", "CB", BOND_ORDER_SINGLE),
            BondTemplate("CD", "CG", BOND_ORDER_SINGLE),
            BondTemplate("CD", "N", BOND_ORDER_SINGLE),
            BondTemplate("OD", "CG", BOND_ORDER_SINGLE),
            BondTemplate("CA", "HA", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB2", BOND_ORDER_SINGLE),
            BondTemplate("CB", "HB3", BOND_ORDER_SINGLE),
            BondTemplate("CG", "HG", BOND_ORDER_SINGLE),
            BondTemplate("CD", "HD2", BOND_ORDER_SINGLE),
            BondTemplate("CD", "HD3", BOND_ORDER_SINGLE),
            BondTemplate("OD", "HD", BOND_ORDER_SINGLE),
        ],
    };
    #[rustfmt::skip]
    static ref ACE: AminoAcidTemplate = AminoAcidTemplate {
        name: "ACE",
        heavy_atom_labels: From::from([
            "CH3", "C", "O"]),
        protonation_state_variants: From::from(
            [("ACE", ProtonationState::default(3))]),
        hydrogen_labels: From::from([
            "H1", "H2", "H3"]),
        bonds: vec![
            BondTemplate("C", "CH3", BOND_ORDER_SINGLE),
            BondTemplate("C", "O", BOND_ORDER_DOUBLE),
            BondTemplate("CH3", "H1", BOND_ORDER_SINGLE),
            BondTemplate("CH3", "H2", BOND_ORDER_SINGLE),
            BondTemplate("CH3", "H3", BOND_ORDER_SINGLE),
        ],
    };
    #[rustfmt::skip]
    static ref NME: AminoAcidTemplate = AminoAcidTemplate {
        name: "NME",
        heavy_atom_labels: From::from([
            "N", "C"]),
        protonation_state_variants: From::from(
            [("NME", ProtonationState::default(2))]),
        hydrogen_labels: From::from([
            "H", "H1", "H2", "H3"]),
        bonds: vec![
            BondTemplate("N", "C", BOND_ORDER_SINGLE),
            BondTemplate("N", "H", BOND_ORDER_SINGLE),
            BondTemplate("C", "H1", BOND_ORDER_SINGLE),
            BondTemplate("C", "H2", BOND_ORDER_SINGLE),
            BondTemplate("C", "H3", BOND_ORDER_SINGLE),
        ],
    };
    #[rustfmt::skip]
    static ref NMA: AminoAcidTemplate = AminoAcidTemplate {
        name: "NMA",
        heavy_atom_labels: From::from([
            "N", "CA"]),
        protonation_state_variants: From::from(
            [("NMA", ProtonationState::default(2))]),
        hydrogen_labels: From::from([
            "H", "1HA", "2HA", "3HA"]),
        bonds: vec![
            BondTemplate("N", "CA", BOND_ORDER_SINGLE),
            BondTemplate("N", "H", BOND_ORDER_SINGLE),
            BondTemplate("CA", "1HA", BOND_ORDER_SINGLE),
            BondTemplate("CA", "2HA", BOND_ORDER_SINGLE),
            BondTemplate("CA", "3HA", BOND_ORDER_SINGLE),
        ],
    };
}

pub fn aa_template_by_tok(aa_tok: AminoAcid) -> Option<&'static AminoAcidTemplate> {
    match aa_tok {
        AminoAcid::GLY => Some(&GLY),
        AminoAcid::ALA => Some(&ALA),
        AminoAcid::VAL => Some(&VAL),
        AminoAcid::LEU => Some(&LEU),
        AminoAcid::ILE => Some(&ILE),
        AminoAcid::PRO => Some(&PRO),
        AminoAcid::SER => Some(&SER),
        AminoAcid::THR => Some(&THR),
        AminoAcid::ASN => Some(&ASN),
        AminoAcid::GLN => Some(&GLN),
        AminoAcid::CYS => Some(&CYS),
        AminoAcid::MET => Some(&MET),
        AminoAcid::PHE => Some(&PHE),
        AminoAcid::TYR => Some(&TYR),
        AminoAcid::TRP => Some(&TRP),
        AminoAcid::ASP => Some(&ASP),
        AminoAcid::GLU => Some(&GLU),
        AminoAcid::HIS => Some(&HIS),
        AminoAcid::LYS => Some(&LYS),
        AminoAcid::ARG => Some(&ARG),
        AminoAcid::HYP => Some(&HYP),
        AminoAcid::ACE => Some(&ACE),
        AminoAcid::NME => Some(&NME),
        AminoAcid::NMA => Some(&NMA),
        AminoAcid::UNK => None,
    }
}

#[derive(Copy, Clone, Debug, Default, EnumString, PartialEq, Eq, PartialOrd, Ord, Typedef)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[cfg_attr(feature = "graphql", derive(Enum))]
pub enum AminoAcid {
    /// Glycine
    GLY,
    /// Alanine
    ALA,
    /// Valine
    VAL,
    /// Leucine
    LEU,
    /// Isoleucine
    ILE,
    /// Proline
    PRO,
    /// Serine
    SER,
    /// Threonine
    THR,
    /// Asparagine
    ASN,
    /// Glutamine
    GLN,
    /// Cysteine
    CYS,
    /// Methionine
    MET,
    /// Phenylalanine
    PHE,
    /// Tyrosine
    TYR,
    /// Tryptophan
    TRP,
    /// Aspartate
    ASP,
    /// Glutamate
    GLU,
    /// Histidine
    HIS,
    /// Lysine
    LYS,
    /// Arginine
    ARG,
    /// Hydroxyproline
    HYP,
    /// Acetyl capping group
    ACE,
    /// C-terminal N-methyl amide capping group
    NME,
    /// C-terminal N-methyl amide and acetyl capping group
    NMA,
    /// Unknown
    #[default]
    UNK,
}

impl AminoAcid {
    /// Convert from the 3-char PDB standard names to the respective amino acid.
    /// If the standard name is not recognised, then the amino acid reverts to
    /// UNK. See
    /// http://www.rcsb.org/pdb/file_formats/pdb/pdbguide2.2/part_79.html for
    /// more information about the PDB standard names.
    pub fn from_pdb_std_name(name: &str) -> Result<Self, Error> {
        match name {
            "GLY" => Ok(Self::GLY),
            "ALA" => Ok(Self::ALA),
            "VAL" => Ok(Self::VAL),
            "LEU" => Ok(Self::LEU),
            "ILE" => Ok(Self::ILE),
            "PRO" => Ok(Self::PRO),
            "SER" => Ok(Self::SER),
            "THR" => Ok(Self::THR),
            "ASN" => Ok(Self::ASN),
            "GLN" => Ok(Self::GLN),
            "CYS" => Ok(Self::CYS),
            "MET" => Ok(Self::MET),
            "PHE" => Ok(Self::PHE),
            "TYR" => Ok(Self::TYR),
            "TRP" => Ok(Self::TRP),
            "ASP" => Ok(Self::ASP),
            "GLU" => Ok(Self::GLU),
            "HIS" => Ok(Self::HIS),
            "LYS" => Ok(Self::LYS),
            "ARG" => Ok(Self::ARG),
            "HYP" => Ok(Self::HYP),
            "ACE" => Ok(Self::ACE),
            "NME" => Ok(Self::NME),
            "NMA" => Ok(Self::NMA),
            "UNK" => Ok(Self::UNK),
            _ => Err(Error::ParseNameError {
                found: name.to_string(),
            }),
        }
    }

    /// Convert to the 3-char PDB standard names for the respective amino acid.
    /// See http://www.rcsb.org/pdb/file_formats/pdb/pdbguide2.2/part_79.html
    /// for more information about the PDB standard names.
    pub fn to_pdb_std_name(&self) -> &'static str {
        match self {
            Self::GLY => "GLY",
            Self::ALA => "ALA",
            Self::VAL => "VAL",
            Self::LEU => "LEU",
            Self::ILE => "ILE",
            Self::PRO => "PRO",
            Self::SER => "SER",
            Self::THR => "THR",
            Self::ASN => "ASN",
            Self::GLN => "GLN",
            Self::CYS => "CYS",
            Self::MET => "MET",
            Self::PHE => "PHE",
            Self::TYR => "TYR",
            Self::TRP => "TRP",
            Self::ASP => "ASP",
            Self::GLU => "GLU",
            Self::HIS => "HIS",
            Self::LYS => "LYS",
            Self::ARG => "ARG",
            Self::HYP => "HYP",
            Self::ACE => "ACE",
            Self::NME => "NME",
            Self::NMA => "NMA",
            Self::UNK => "UNK",
        }
    }
}