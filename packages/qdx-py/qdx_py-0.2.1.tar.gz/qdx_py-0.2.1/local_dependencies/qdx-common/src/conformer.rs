use std::collections::{HashMap, HashSet};
use std::fmt::{self, Display};

#[cfg(feature = "graphql")]
use async_graphql::{InputObject, SimpleObject};
use itertools::Itertools;
use petgraph::algo::{astar, kosaraju_scc};
use petgraph::visit::Bfs;
use qdx_derive::Typedef;
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};

use crate::bond::{Bond, BOND_ORDER_SINGLE};
use crate::{
    amino_acid::{aa_template_by_tok, AminoAcid, AminoAcidTemplate, BondTemplate, Terminus},
    topology::{Alt, Topology},
};

const DEFAULT_LARGEST_SIDECHAIN: usize = 5;

#[derive(Clone, Debug, Eq, PartialEq, PartialOrd, Ord, Typedef)]
#[cfg_attr(feature = "serde", derive(::serde::Deserialize, ::serde::Serialize))]
pub struct Label(pub u32, pub String);

#[cfg(feature = "graphql")]
async_graphql::scalar!(Label);

impl Display for Label {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}-{}", self.0, self.1)
    }
}

fn with_index<T, F>(mut f: F) -> impl FnMut(&T) -> bool
where
    F: FnMut(usize, &T) -> bool,
{
    let mut i = 0;
    move |item| (f(i, item), i += 1).0
}

#[derive(thiserror::Error, Clone, Debug)]
pub enum Error {
    #[error("bad protonation state for {aa:?}: {hydrogen_atoms:?}")]
    BadProtonationState {
        aa: AminoAcid,
        hydrogen_atoms: Vec<String>,
    },
    #[error("missing conformer data for this amino acid")]
    MissingAminoAcidConformerData,
    #[error("missing heavy atoms {missing_atoms:?} in {aa:?}")]
    MissingAminoAcidHeavyAtoms {
        aa: AminoAcid,
        missing_atoms: Vec<String>,
    },
    #[error("missing template for {aa:?}")]
    MissingAminoAcidTemplate { aa: AminoAcid },
    #[error("duplicate atoms in {aa:?}: {duplicate_atoms:?} appear more than once")]
    DuplicateAtomsInAminoAcid {
        aa: AminoAcid,
        duplicate_atoms: Vec<String>,
    },
    #[error("wrong atoms in {aa:?}: {wrong_atoms:?} should not be present")]
    WrongAtomsInAminoAcid {
        aa: AminoAcid,
        wrong_atoms: Vec<String>,
    },
}

/// Allows us to change how strict we are when we check for missing atoms, add bonds, etc.
///
/// When we check for missing atoms, we can pass `Heavy` to only check that all heavy atoms are
/// present, `Hydrogens` to only check hydrogens, or `All` to check both. We can also pass `None` to
/// skip these checks, which might be convenient if running a bunch of functions that involve
/// strictness en masse and want to simply set one variable to disable any checking.
///
/// The bond and formal charge perception routines rely on predetermined atom sets to do their work.
/// When these states are incorrect in various ways, things can go wrong.
/// - In perceive_formal_charges: currently needs all atoms to be present; otherwise, the proper
///   protonation states will not be found. Passing `None` to this routine will just give slightly
///   less clear errors in the case of missing atoms.
/// - In perceive_bonds: can handle `Heavy` or `All` strictness levels (the former will only add
///   heavy atom bonds).
#[derive(Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
pub enum AtomCheckStrictness {
    None,
    Heavy,
    Hydrogens,
    All,
}

#[derive(Clone, Debug, Default, PartialEq, Typedef)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[cfg_attr(
    feature = "graphql",
    derive(InputObject, SimpleObject),
    graphql(rename_fields = "snake_case", input_name = "ConformerInput")
)]
pub struct Conformer {
    pub topology: Topology,

    /// Each element defines an amino acid which is itself a vector of indices
    /// into the topology that identify which atoms are part of the amino acid.
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub amino_acids: Option<Vec<Vec<u32>>>,
    /// The amino acid sequence.
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub amino_acid_seq: Option<Vec<AminoAcid>>,
    /// The sequence index of each amino acid relative to its parent gene. This
    /// is useful because structures often do not represent an entire protein,
    /// and it is desirable to map each amino acid to its position in the entire
    /// sequence (this is how most amino acids are referenced in literature).
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub amino_acid_seq_ids: Option<Vec<i32>>,
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub amino_acid_insertion_codes: Option<Vec<String>>,
    /// General purpose labels for the amino acids. For example, it can be used
    /// to capture the references used by PDB files for identifying insertion
    /// codes.
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub amino_acid_labels: Option<Vec<Label>>,

    /// Residues that are not amino acids.
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub residues: Option<Vec<Vec<u32>>>,
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub residue_seq: Option<Vec<String>>,
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub residue_seq_ids: Option<Vec<i32>>,
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub residue_insertion_codes: Option<Vec<String>>,
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub residue_labels: Option<Vec<Label>>,

    /// Subunits are used to identify substructures within the topology. For
    /// example, distinct monomers, side-chains, peptides, proteins, small
    /// molecules, and so on. Each element defines a chain which is itself a
    /// vector of indices into the topology that identify which atoms are part
    /// of the chain.
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub subunits: Option<Vec<Vec<u32>>>,
}

impl Conformer {
    pub fn is_valid(&self) -> bool {
        if let Some(amino_acid_seq) = &self.amino_acid_seq {
            if self.amino_acids.is_none() {
                return false;
            }
            if amino_acid_seq.len() != self.amino_acids.as_ref().unwrap().len() {
                return false;
            }
        }
        if let Some(amino_acid_labels) = &self.amino_acid_labels {
            if self.amino_acid_seq.is_none() {
                return false;
            }
            if amino_acid_labels.len() != self.amino_acid_seq.as_ref().unwrap().len() {
                return false;
            }
        }
        if let Some(amino_acid_seq_ids) = &self.amino_acid_seq_ids {
            if self.amino_acid_seq.is_none() {
                return false;
            }
            if amino_acid_seq_ids.len() != self.amino_acid_seq.as_ref().unwrap().len() {
                return false;
            }
        }
        if let Some(residue_seq) = &self.residue_seq {
            if self.residues.is_none() {
                return false;
            }
            if residue_seq.len() != self.residues.as_ref().unwrap().len() {
                return false;
            }
        }
        if let Some(residue_labels) = &self.residue_labels {
            if self.residue_seq.is_none() {
                return false;
            }
            if residue_labels.len() != self.residue_seq.as_ref().unwrap().len() {
                return false;
            }
        }
        self.topology.is_valid()
    }

    /// Remove a set of amino acids and all the atoms it references from a conformer
    ///
    /// # Example
    /// ```
    /// use qdx_common::*;
    /// let mut conformer = Conformer {
    ///     topology: Topology {
    ///         symbols: vec!["H".into(), "H".into(), "O".into(), "C".into()],
    ///         geometry: vec![1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 4.0, 4.0, 4.0],
    ///         atom_charges: None, partial_charges: None, atom_labels: None, alts: None,
    ///         connectivity: None,
    ///         fragments: None, fragment_charges: None,
    ///     },
    ///     amino_acids: Some(vec![vec![0, 1, 2], vec![3]]),
    ///     amino_acid_seq: Some(vec![AminoAcid::UNK, AminoAcid::UNK]),
    ///     amino_acid_seq_ids: Some(vec![0, 1]),
    ///     amino_acid_insertion_codes: Some(vec!["".to_string(), "".to_string()]),
    ///     amino_acid_labels: Some(vec![Label(0, "H2O".into()), Label(1, "SINGLE_ATOM_C".into())]),
    ///     residues: None, residue_seq: None, residue_seq_ids: None, residue_insertion_codes: None, residue_labels: None,
    ///     subunits: None,
    /// };
    /// conformer.drop_amino_acids(&vec![1]);
    /// // Only one amino acid left with 3 remaining atoms, which have been reindexed
    /// assert_eq!(conformer.amino_acids, Some(vec![vec![0, 1, 2]]));
    /// assert_eq!(conformer.topology.symbols, vec!["H", "H", "O"]);
    /// ```
    pub fn drop_amino_acids(&mut self, aas_to_drop: &[usize]) {
        debug_assert!(self.is_valid());

        if let Some(aas) = &mut self.amino_acids {
            // Get the atoms in the amino acid to drop
            let atoms_to_drop = aas_to_drop
                .iter()
                .flat_map(|aa_to_drop| &aas[*aa_to_drop])
                .copied()
                .collect::<Vec<_>>();
            self.topology.drop_atoms(&atoms_to_drop);

            // Filter the amino acid data
            aas.retain(with_index(|i, _| !aas_to_drop.contains(&i)));

            // Reindex atoms in existing amino acids
            for aa in aas.iter_mut() {
                for atom_i in aa.iter_mut() {
                    *atom_i -= atoms_to_drop
                        .iter()
                        .filter(|atom_j| **atom_j < *atom_i)
                        .count() as u32;
                }
            }

            // Filter the supplemental amino acid data
            if let (Some(aa_seq), Some(aa_seq_ids), Some(aa_labels)) = (
                &mut self.amino_acid_seq,
                &mut self.amino_acid_seq_ids,
                &mut self.amino_acid_labels,
            ) {
                aa_seq.retain(with_index(|i, _| !aas_to_drop.contains(&i)));
                aa_seq_ids.retain(with_index(|i, _| !aas_to_drop.contains(&i)));
                aa_labels.retain(with_index(|i, _| !aas_to_drop.contains(&i)));
            }
        }
        debug_assert!(self.is_valid());
    }

    /// Isolate a set of amino acids and all the atoms it references in a conformer
    pub fn keep_amino_acids(&mut self, aas_to_keep: &[usize]) {
        if let Some(aas) = &mut self.amino_acids {
            let aas_to_drop = (0..aas.len())
                .filter(|i| !aas_to_keep.contains(i))
                .collect::<Vec<_>>();
            self.drop_amino_acids(&aas_to_drop);
        }
    }

    /// Filter amino acids by seq_id, which have to be unique
    pub fn drop_amino_acid_by_seq_id(&mut self, amino_acid_seq_ids_to_drop: Vec<i32>) {
        if let Some(aa_seq_ids) = &self.amino_acid_seq_ids {
            let aas_to_drop = amino_acid_seq_ids_to_drop
                .iter()
                .filter_map(|seq_id_j| aa_seq_ids.iter().position(|seq_id_i| seq_id_i == seq_id_j))
                .collect::<Vec<usize>>();
            self.drop_amino_acids(&aas_to_drop);
        }
    }

    /// Filter amino acids by label, which don't have to be unique, and all matching are dropped
    pub fn drop_amino_acid_by_label(&mut self, amino_acid_labels_to_drop: Vec<Label>) {
        if let Some(aa_labels) = &self.amino_acid_labels {
            let aas_to_drop = aa_labels
                .iter()
                .enumerate()
                .filter_map(|(i, label_i)| amino_acid_labels_to_drop.contains(label_i).then_some(i))
                .collect::<Vec<usize>>();
            self.drop_amino_acids(&aas_to_drop);
        }
    }

    /// Remove a set of residues and all the atoms it references from a conformer
    ///
    /// # Example
    /// ```
    /// use qdx_common::*;
    /// let mut conformer = Conformer {
    ///     topology: Topology {
    ///         symbols: vec!["H".into(), "H".into(), "O".into(), "C".into()],
    ///         geometry: vec![1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 4.0, 4.0, 4.0],
    ///         atom_charges: None, partial_charges: None, atom_labels: None, alts: None,
    ///         connectivity: None,
    ///         fragments: None, fragment_charges: None,
    ///     },
    ///     amino_acids: None, amino_acid_seq: None, amino_acid_seq_ids: None, amino_acid_insertion_codes: None, amino_acid_labels: None,
    ///     residues: Some(vec![vec![0, 1, 2], vec![3]]),
    ///     residue_seq: Some(vec!["HOH".into(), "SINGLE_ATOM_C".into()]),
    ///     residue_seq_ids: Some(vec![0, 1]),
    ///     residue_insertion_codes: Some(vec!["".to_string(), "".to_string()]),
    ///     residue_labels: Some(vec![Label(0, "H2O".into()), Label(1, "SINGLE_ATOM_C".into())]),
    ///     subunits: None,
    /// };
    /// conformer.drop_residues(&vec![0]);
    /// // Only one residue left with the final remaining atom, which has been reindexed
    /// assert_eq!(conformer.residues, Some(vec![vec![0]]));
    /// assert_eq!(conformer.topology.symbols, vec!["C"]);
    /// ```
    pub fn drop_residues(&mut self, rs_to_drop: &[usize]) {
        debug_assert!(self.is_valid());

        if let Some(rs) = &mut self.residues {
            // Get the atoms in the residues to drop
            let atoms_to_drop = rs_to_drop
                .iter()
                .flat_map(|r_to_drop| &rs[*r_to_drop])
                .copied()
                .collect::<Vec<_>>();
            self.topology.drop_atoms(&atoms_to_drop);

            // Filter the residue data
            rs.retain(with_index(|i, _| !rs_to_drop.contains(&i)));

            // Reindex atoms in existing residues
            for r in rs.iter_mut() {
                for atom_i in r.iter_mut() {
                    *atom_i -= atoms_to_drop
                        .iter()
                        .filter(|atom_j| **atom_j < *atom_i)
                        .count() as u32;
                }
            }

            // Filter the supplemental residue data
            if let (Some(r_seq), Some(r_labels)) = (&mut self.residue_seq, &mut self.residue_labels)
            {
                r_seq.retain(with_index(|i, _| !rs_to_drop.contains(&i)));
                r_labels.retain(with_index(|i, _| !rs_to_drop.contains(&i)));
            }
        }
        debug_assert!(self.is_valid());
    }

    /// Isolate a set of residues and all the atoms it references in a conformer
    pub fn keep_residues(&mut self, residues_to_keep: &[usize]) {
        if let Some(residues) = &mut self.residues {
            let residues_to_drop = (0..residues.len())
                .filter(|i| !residues_to_keep.contains(i))
                .collect::<Vec<_>>();
            self.drop_residues(&residues_to_drop);
        }
    }

    /// Filter residues by label, which don't have to be unique, and all matching are dropped
    ///
    /// # Example
    /// ```
    /// use qdx_common::conformer::Conformer;
    /// use qdx_common::conformer::Label;
    /// use qdx_common::topology::Topology;
    /// let mut conformer = Conformer {
    ///     topology: Topology {
    ///         symbols: vec!["H".into(), "H".into(), "O".into(), "C".into()],
    ///         geometry: vec![1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 4.0, 4.0, 4.0],
    ///         atom_charges: None, partial_charges: None, atom_labels: None, alts: None,
    ///         connectivity: None,
    ///         fragments: None, fragment_charges: None,
    ///     },
    ///     amino_acids: None, amino_acid_seq: None, amino_acid_seq_ids: None, amino_acid_insertion_codes: None, amino_acid_labels: None,
    ///     residues: Some(vec![
    ///         vec![0, 1, 2],
    ///         vec![3]
    ///     ]),
    ///     residue_seq: Some(vec![
    ///         "HOH".into(),
    ///         "SINGLE_ATOM_C".into()
    ///     ]),
    ///     residue_seq_ids: Some(vec![
    ///         0,
    ///         1
    ///     ]),
    ///     residue_insertion_codes: Some(vec![
    ///         "".to_string(),
    ///         "".to_string()
    ///     ]),
    ///     residue_labels: Some(vec![
    ///         Label(0, "H2O".into()),
    ///         Label(1, "SINGLE_ATOM_C".into())
    ///     ]),
    ///     subunits: None,
    /// };
    /// conformer.drop_residue_by_label(vec![Label(0, "H2O".into())]);
    /// assert_eq!(
    ///     conformer.residues,
    ///     Some(vec![vec![0]]));
    /// assert_eq!(
    ///     conformer.residue_seq,
    ///     Some(vec!["SINGLE_ATOM_C".into()])
    /// );
    /// assert_eq!(
    ///     conformer.residue_labels,
    ///     Some(vec![Label(1, "SINGLE_ATOM_C".into())])
    /// );
    pub fn drop_residue_by_label(&mut self, residue_labels_to_drop: Vec<Label>) {
        if let Some(r_labels) = &self.residue_labels {
            let rs_to_drop = r_labels
                .iter()
                .enumerate()
                .filter_map(|(i, label_i)| residue_labels_to_drop.contains(label_i).then_some(i))
                .collect::<Vec<usize>>();
            self.drop_residues(&rs_to_drop);
        }
    }

    /// Create a vector of amino acid indices based on whether any atom in that amino acid is within
    /// the threshold of the reference point.
    pub fn get_amino_acids_near_point(
        &self,
        reference_point: &[f32; 3],
        threshold: f32,
    ) -> Vec<usize> {
        self.topology
            .get_atom_sets_near_point(reference_point, threshold, &self.amino_acids)
    }

    /// Create a vector of residue indices based on whether any atom in that residue is within the
    /// threshold of the reference point.
    pub fn get_residues_near_point(
        &self,
        reference_point: &[f32; 3],
        threshold: f32,
    ) -> Vec<usize> {
        self.topology
            .get_atom_sets_near_point(reference_point, threshold, &self.residues)
    }

    /// Extend this assembly with another.
    pub fn extend(&mut self, other: Self) {
        debug_assert!(self.is_valid() && other.is_valid());

        // Track the offest of atom indices so that we can update incoming indices from
        // the other assembly.
        let offset = self.topology.symbols.len() as u32;

        // Extend the alternate topology
        let offset_alts = other.topology.alts.as_ref().map(|alts| {
            alts.iter()
                .map(|Alt(i, is)| Alt(i + offset, is.iter().map(|i| i + offset).collect()))
                .collect::<Vec<_>>()
        });
        if let Some(alts) = &mut self.topology.alts {
            if let Some(offset_alts) = offset_alts {
                alts.extend(offset_alts);
            }
        } else {
            self.topology.alts = offset_alts;
        }

        // Extend the topology
        self.topology.extend(other.topology);

        // Extend amino acids
        if let Some(amino_acid_seq) = &mut self.amino_acid_seq {
            if let Some(other_amino_acid_seq) = other.amino_acid_seq {
                amino_acid_seq.extend(other_amino_acid_seq);
            }
        } else {
            self.amino_acid_seq = other.amino_acid_seq;
        }

        // Extend amino acid labels
        if let Some(amino_acid_labels) = &mut self.amino_acid_labels {
            if let Some(other_amino_acid_labels) = other.amino_acid_labels {
                amino_acid_labels.extend(other_amino_acid_labels);
            }
        } else {
            self.amino_acid_labels = other.amino_acid_labels;
        }

        // Extend amino acid atoms
        let offset_amino_acid = other.amino_acids.map(|amino_acid| {
            amino_acid
                .iter()
                .map(|amino_acid| amino_acid.iter().map(|i| i + offset).collect())
                .collect::<Vec<_>>()
        });
        if let Some(amino_acid) = &mut self.amino_acids {
            if let Some(offset_amino_acid) = offset_amino_acid {
                amino_acid.extend(offset_amino_acid);
            }
        } else {
            self.amino_acids = offset_amino_acid;
        }

        // Extend residues
        if let Some(residue_seq) = &mut self.residue_seq {
            if let Some(other_residue_seq) = other.residue_seq {
                residue_seq.extend(other_residue_seq);
            }
        } else {
            self.residue_seq = other.residue_seq;
        }

        // Extend amino acid labels
        if let Some(residue_labels) = &mut self.residue_labels {
            if let Some(other_residue_labels) = other.residue_labels {
                residue_labels.extend(other_residue_labels);
            }
        } else {
            self.residue_labels = other.residue_labels;
        }

        // Extend residue atoms
        let offset_residue = other.residues.map(|residue| {
            residue
                .iter()
                .map(|residue| residue.iter().map(|i| i + offset).collect())
                .collect::<Vec<_>>()
        });
        if let Some(residue) = &mut self.residues {
            if let Some(offset_residue) = offset_residue {
                residue.extend(offset_residue);
            }
        } else {
            self.residues = offset_residue;
        }

        // Extend subunits
        let offset_subunits = other.subunits.map(|subunits| {
            subunits
                .iter()
                .map(|subunit| subunit.iter().map(|i| i + offset).collect())
                .collect::<Vec<_>>()
        });
        if let Some(subunits) = &mut self.subunits {
            if let Some(offset_subunits) = offset_subunits {
                subunits.extend(offset_subunits);
            }
        } else {
            self.subunits = offset_subunits;
        }

        debug_assert!(self.is_valid());
    }

    /// Break a protein into fragments along the backbone C-C bonds.
    /// After breaking, will move `backbone_steps` along the backbone before breaking again.
    /// Will not break the backbone within `terminal_fragment_sidechain_size` steps
    /// to prevent fragmenting side-chains.
    /// Returns the fragments
    pub fn fragment(
        &self,
        backbone_steps: usize,
        terminal_fragment_sidechain_size: Option<usize>,
    ) -> Vec<Vec<u32>> {
        let sulphurs = self
            .topology
            .symbols
            .iter()
            .enumerate()
            .filter_map(|(idx, e)| if e == "S" { Some(idx as u32) } else { None })
            .collect::<HashSet<_>>();

        let mut drop_connections = vec![];
        if let Some(connectivity) = &self.topology.connectivity {
            for (bond_idx, Bond(i, j, ..)) in connectivity.iter().enumerate() {
                // if connection is S-S, break bond and remove from connectivity to prevent loops
                if [i, j].iter().all(|x| sulphurs.contains(x)) {
                    drop_connections.push(bond_idx);
                }
            }
        }

        // Remove S-S connections
        let mut no_ss_topology = self.topology.clone();
        no_ss_topology.connectivity = no_ss_topology.connectivity.map(|x| {
            x.iter()
                .enumerate()
                .filter_map(|(idx, x)| {
                    if drop_connections.contains(&idx) {
                        None
                    } else {
                        Some(*x)
                    }
                })
                .sorted()
                .collect()
        });

        let mut fragments = vec![];
        let mut graph = no_ss_topology.to_graph();
        let sections = kosaraju_scc(&graph);
        if sections.len() > 1 {
            eprintln!("backbone broken {}", sections.len());
        }
        for sec in sections {
            let first = *sec.iter().min().unwrap();
            let last = *sec.iter().max().unwrap();
            let backbone = astar(&graph, first, |finish| finish == last, |_| 1, |_| 0);
            if let Some(backbone) = backbone {
                // NOTE: means fragments must have /minimum/ size, not max
                let mut i = backbone_steps;
                let mut breaks = vec![];
                breaks.push(first);

                let final_atom = if backbone.1.len()
                    < terminal_fragment_sidechain_size.unwrap_or(DEFAULT_LARGEST_SIDECHAIN)
                {
                    backbone.1.len()
                } else {
                    backbone.1.len() - DEFAULT_LARGEST_SIDECHAIN
                };

                while i < final_atom {
                    // can break
                    if graph[backbone.1[i]].2 == "C" && graph[backbone.1[i + 1]].2 == "C" {
                        breaks.push(backbone.1[i + 1]);
                        graph.remove_edge(
                            graph.find_edge(backbone.1[i], backbone.1[i + 1]).unwrap(),
                        );
                        i += backbone_steps;
                    } else {
                        i += 1;
                    }
                }

                for bs in breaks.iter().enumerate() {
                    let mut bfs = Bfs::new(&graph, *(bs.1));
                    let mut atoms = vec![];
                    while let Some(visited) = bfs.next(&graph) {
                        atoms.push(graph[visited].0 as u32);
                    }
                    fragments.push(atoms);
                }
            }
        }

        fragments
    }

    /// Get charges for fragments and atoms by checking similar substructures
    pub fn substructure_charges(&self, uneven_ok: bool) -> (Option<Vec<isize>>, Vec<isize>) {
        // Fix connectivity if it was stripped at an earlier stage
        let graph = if let Some(con) = &self.topology.connectivity {
            if con.len() < self.topology.symbols.len() / 4 {
                let mut prot = self.clone();
                eprintln!(
                    "WARNING USING IMPLICIT CONNECTIVITY connection {} symbols {}",
                    con.len(),
                    self.topology.symbols.len()
                );
                prot.topology.connectivity = Some(prot.topology.implicit_connectivity(0.05));
                prot.topology.connectivity = Some(
                    prot.topology
                        .connectivity
                        .unwrap_or(Default::default())
                        .into_iter()
                        .map(|bond| Bond(bond.0.min(bond.1), bond.0.max(bond.1), bond.2))
                        .sorted()
                        .dedup_by(|b1, b2| {
                            (b1.0 == b2.0 && b1.1 == b2.1) || (b1.0 == b2.1 && b1.1 == b2.0)
                        })
                        .collect(),
                );
                prot.topology.to_graph()
            } else {
                self.topology.to_graph()
            }
        } else {
            let mut prot = self.clone();
            //prot.topology.connectivity = Some(prot.topology.implicit_connectivity(0.15, checked));
            prot.topology.connectivity = Some(
                prot.topology
                    .connectivity
                    .unwrap_or(Default::default())
                    .into_iter()
                    .map(|bond| Bond(bond.0.min(bond.1), bond.0.max(bond.1), bond.2))
                    .sorted()
                    .dedup_by(|b1, b2| {
                        (b1.0 == b2.0 && b1.1 == b2.1) || (b1.0 == b2.1 && b1.1 == b2.0)
                    })
                    .collect(),
            );
            prot.topology.to_graph()
        };

        let mut arginines_charged = HashSet::<usize>::new();

        let mut atom_charges = graph
            .node_indices()
            .map(|node_idx| {
                let (atom_id, _, element) = &graph[node_idx];
                let edges = graph.edges(node_idx);
                let degree = edges.clone().count();
                let charge = match (element.as_str(), degree) {
                    //
                    ("N", 4) => 1, // we have NRH3+ group
                    ("N", 3) => {
                        // we have =NR2+ group
                        let neighbors = graph.neighbors(node_idx);
                        let c_neighbors = neighbors.clone().filter(|n| {
                            let (_, _, n_element) = &graph[*n];
                            n_element == "C" && graph.edges(*n).count() == 3
                        });
                        let mut charge = 0;
                        for cn in c_neighbors {
                            let neighbors = graph.neighbors(cn);
                            let o_neighbors = neighbors.clone().filter(|n| {
                                let (_, _, n_element) = &graph[*n];
                                let edge = graph[graph.find_edge(cn, *n).unwrap()];
                                n_element == "O" && edge.1 >= 2
                            });

                            charge = if o_neighbors.count() > 0 {
                                0
                            } else if edges.clone().filter(|e| e.weight().1 == 1).count() == 2 {
                                let aa_idx = self.amino_acids.as_ref().map(|aaa| {
                                    aaa.iter()
                                        .enumerate()
                                        .find(|(_, atoms)| atoms.contains(&(*atom_id as u32)))
                                        .expect("atom is not in any amino acid")
                                        .0
                                });
                                if let Some(aa_idx) = aa_idx {
                                    match self.amino_acid_seq.as_ref().map(|aas| aas[aa_idx]) {
                                        Some(AminoAcid::ARG) => {
                                            if !arginines_charged.contains(&aa_idx) {
                                                tracing::debug!("charging {} in arganine", atom_id);
                                                arginines_charged.insert(aa_idx);
                                                1
                                            } else {
                                                tracing::debug!(
                                                    "already charged arganine, skipping {}",
                                                    atom_id
                                                );
                                                0
                                            }
                                        }
                                        Some(AminoAcid::HIS) => 0,
                                        _ => 1,
                                    }
                                } else {
                                    1
                                }
                            } else {
                                0
                            };
                        }
                        charge
                    }
                    ("O", 1) => {
                        // COO- group, one C=O and one C-O bond
                        // assign the -1 charge to the singly bonded O
                        edges
                            .map(|e| {
                                let bond = e.weight().1;
                                if bond == 1 {
                                    -1
                                } else {
                                    tracing::debug!(
                                        "atom {} COO but not negative as bond is {}",
                                        atom_id,
                                        bond
                                    );
                                    0
                                }
                            })
                            .sum()
                    }
                    ("P", 4) => {
                        // PO4 group
                        // Rare case
                        unimplemented!()
                    }
                    ("C", 3) => {
                        // COO- groups but the C-O distances are the same, so negative charge placed on the carbon
                        let neighbors = graph.neighbors(node_idx);
                        let o_neighbors = neighbors.filter(|n| {
                            let (_, _, n_element) = &graph[*n];
                            let edge = graph[graph.find_edge(node_idx, *n).unwrap()];
                            n_element == "O" && edge.1 >= 2
                        });
                        if o_neighbors.clone().count() == 2 {
                            -1
                        } else {
                            tracing::debug!(
                                "atom {} C3 but not negative as neighbor count is {}",
                                atom_id,
                                o_neighbors.count()
                            );
                            0
                        }
                    }
                    _ => {
                        0
                        // ignored
                    }
                };
                (atom_id, charge)
            })
            .collect::<Vec<_>>();

        atom_charges.sort_by(|(id, _), (id2, _)| id.cmp(id2));

        let fragment_protons = self.fragment_protons();

        let frag_charges = self.topology.fragments.clone().map(|frags| {
            frags
                .into_iter()
                .enumerate()
                .map(|(f_id, atoms)| {
                    let frag_charge = atoms
                        .clone()
                        .into_iter()
                        .map(|aid| atom_charges[aid as usize].1)
                        .sum::<isize>();
                    if !uneven_ok && (frag_charge - fragment_protons[f_id] as isize) % 2 != 0 {
                        panic!(
                            "uneven electrons in fragment {}: charge {}, protons {}:\n{:?}",
                            f_id, frag_charge, fragment_protons[f_id], atoms,
                        )
                    };
                    frag_charge
                })
                .collect()
        });
        (
            frag_charges,
            atom_charges.into_iter().map(|(_, charge)| charge).collect(),
        )
    }

    /// Get number of protons in fragments
    pub fn fragment_protons(&self) -> Vec<usize> {
        let protons = self
            .topology
            .symbols
            .iter()
            .map(|atom| {
                periodic_table_on_an_enum::Element::from_symbol(atom)
                    .unwrap_or_else(|| panic!("Unknown symbol {atom}"))
                    .get_atomic_number()
            })
            .collect::<Vec<_>>();

        let broken_bonds = self.topology.broken_bonds();

        self.topology
            .fragments
            .as_ref()
            .unwrap_or(&vec![self
                .topology
                .symbols
                .iter()
                .enumerate()
                .map(|(i, _)| i as u32)
                .collect()])
            .iter()
            .map(|frag| {
                frag.iter()
                    .map(|atom| {
                        let p = protons[*atom as usize];
                        let hcaps = broken_bonds
                            .iter()
                            .filter(|pair| pair.0 == *atom || pair.1 == *atom)
                            .collect::<Vec<_>>()
                            .len();
                        p + hcaps
                    })
                    .sum::<usize>()
            })
            .collect()
    }

    pub fn ensure_no_missing_atoms(
        &mut self,
        strictness: AtomCheckStrictness,
    ) -> Result<(), Error> {
        if strictness == AtomCheckStrictness::None {
            return Ok(());
        }
        if let (Some(aas), Some(aa_seq), Some(atom_labels)) = (
            &self.amino_acids,
            &self.amino_acid_seq,
            &self.topology.atom_labels,
        ) {
            for (i, aa) in aas.iter().enumerate() {
                let aa_ref = aa_template_by_tok(aa_seq[i])
                    .ok_or(Error::MissingAminoAcidTemplate { aa: aa_seq[i] })?;
                // Make sure atom labels are unique
                let aa_atom_labels_iter = aa
                    .iter()
                    .map(|&atom_idx| atom_labels[atom_idx as usize].as_str());
                let aa_atom_labels = match aa_atom_labels_iter.clone().all_unique() {
                    true => Ok(aa_atom_labels_iter.collect::<HashSet<_>>()),
                    false => Err(Error::DuplicateAtomsInAminoAcid {
                        aa: aa_seq[i],
                        duplicate_atoms: aa_atom_labels_iter
                            .duplicates()
                            .map(|atom_label| atom_label.to_string())
                            .collect(),
                    }),
                }?;
                // Make sure all heavy atoms are present
                if strictness == AtomCheckStrictness::Heavy
                    || strictness == AtomCheckStrictness::All
                {
                    let mut missing_heavy_atoms = aa_ref
                        .heavy_atom_labels
                        .iter()
                        .filter(|&k| !aa_atom_labels.contains(k))
                        .peekable();
                    if missing_heavy_atoms.peek().is_some() {
                        return Err(Error::MissingAminoAcidHeavyAtoms {
                            aa: aa_seq[i],
                            missing_atoms: missing_heavy_atoms
                                .copied()
                                .map(str::to_string)
                                .collect(),
                        });
                    }
                }
                if (strictness == AtomCheckStrictness::Hydrogens
                    || strictness == AtomCheckStrictness::All)
                    && aa_ref.find_protonation_state(&aa_atom_labels).is_none()
                {
                    return Err(Error::BadProtonationState {
                        aa: aa_seq[i],
                        hydrogen_atoms: aa_atom_labels
                            .iter()
                            .filter_map(|l| l.starts_with('H').then(|| l.to_string()))
                            .collect(),
                    });
                }
            }
        }
        Ok(())
    }

    pub fn perceive_formal_charges(
        &mut self,
        missing_atom_strictness: AtomCheckStrictness,
    ) -> Result<(), Error> {
        // Make sure we have all the heavy atoms, if requested
        self.ensure_no_missing_atoms(missing_atom_strictness)?;
        // Assign charges for all atoms in all amino acids
        if let (
            Some(aas),
            Some(aa_seq),
            Some(connectivity),
            Some(atom_labels),
            Some(atom_charges),
        ) = (
            &self.amino_acids,
            &self.amino_acid_seq,
            &self.topology.connectivity,
            &self.topology.atom_labels,
            &mut self.topology.atom_charges,
        ) {
            for (aa_idx, aa) in aas.iter().enumerate() {
                let aa_ref = aa_template_by_tok(aa_seq[aa_idx])
                    .ok_or(Error::MissingAminoAcidTemplate { aa: aa_seq[aa_idx] })?;
                let aa_atom_labels = aa
                    .iter()
                    .map(|&atom_idx| atom_labels[atom_idx as usize].as_str())
                    .collect::<HashSet<_>>();
                let aa_heavy_atom_charges = aa_ref
                    .find_protonation_state(&aa_atom_labels)
                    .ok_or(Error::BadProtonationState {
                        aa: aa_seq[aa_idx],
                        hydrogen_atoms: aa_atom_labels
                            .iter()
                            .filter_map(|l| l.starts_with('H').then(|| l.to_string()))
                            .collect(),
                    })?
                    .heavy_atom_charges;
                // Maps the index [of the atom in ths instance of the aa] into its charge
                let aa_heavy_atom_map = aa
                    .iter()
                    .filter_map(|&atom_idx| {
                        let atom_label = atom_labels[atom_idx as usize].as_str();
                        if atom_label == "OXT" {
                            Some((atom_idx, i8::MIN))
                        } else {
                            aa_ref
                                .heavy_atom_labels
                                .iter()
                                .position(|ref_atom_label| ref_atom_label == &atom_label)
                                .map(|aa_ref_idx| (atom_idx, aa_heavy_atom_charges[aa_ref_idx]))
                        }
                    })
                    .collect::<HashMap<_, _>>();
                // Assign the heavy atom charges based on the identified protonation state
                let is_c_terminus = aa_ref.is_terminus(&aa_atom_labels, Terminus::C);
                let is_n_terminus = aa_ref.is_terminus(&aa_atom_labels, Terminus::N);
                for (&atom_idx, &atom_charge) in aa_heavy_atom_map.iter() {
                    let mut finalized_atom_charge = atom_charge;
                    if is_c_terminus && atom_labels[atom_idx as usize] == "OXT" {
                        // Handle c-terminus
                        finalized_atom_charge = aa_ref
                            .gen_termini_charge(&aa_atom_labels, Terminus::C)
                            .unwrap();
                        atom_charges[atom_idx as usize] = finalized_atom_charge;
                    }
                    if is_n_terminus && atom_labels[atom_idx as usize] == "N" {
                        // Handle n-terminus
                        finalized_atom_charge = aa_ref
                            .gen_termini_charge(&aa_atom_labels, Terminus::N)
                            .unwrap();
                        atom_charges[atom_idx as usize] = finalized_atom_charge;
                    }
                    if self.topology.symbols[atom_idx as usize] == "S"
                        && connectivity
                            .iter()
                            .filter(|bond| {
                                (bond.0 == atom_idx
                                    && self.topology.symbols[bond.1 as usize] == "S")
                                    || (bond.1 == atom_idx
                                        && self.topology.symbols[bond.0 as usize] == "S")
                            })
                            .peekable()
                            .peek()
                            .is_some()
                    {
                        // Correct the charge in the case of a disulfide bridge
                        finalized_atom_charge += 1;
                    }
                    atom_charges[atom_idx as usize] = finalized_atom_charge;
                }
                // Assign all hydrogens a charge of 0
                for &atom_idx in aa.iter().filter(|&&atom_idx| {
                    ["H", "1H", "2H", "3H"]
                        .iter()
                        .any(|prefix| atom_labels[atom_idx as usize].starts_with(prefix))
                }) {
                    atom_charges[atom_idx as usize] = 0;
                }
            }
        }
        Ok(())
    }

    pub fn perceive_bonds(
        &mut self,
        missing_atom_strictness: AtomCheckStrictness,
    ) -> Result<(), Error> {
        // Make sure we have all the heavy atoms, if requested
        self.ensure_no_missing_atoms(missing_atom_strictness)?;
        // Add bonds to each amino acid
        if let (Some(aas), Some(aa_seq), Some(atom_labels)) = (
            &self.amino_acids,
            &self.amino_acid_seq,
            &self.topology.atom_labels,
        ) {
            for (i, aa) in aas.iter().enumerate() {
                // Add inter amino acid bonds
                if i >= 1 {
                    if let (Some(&prev_c), Some(&curr_n)) = (
                        aas[i - 1]
                            .iter()
                            .find(|&&atom_idx| atom_labels[atom_idx as usize] == "C"),
                        aas[i]
                            .iter()
                            .find(|&&atom_idx| atom_labels[atom_idx as usize] == "N"),
                    ) {
                        // 2.0 is a lenient estimate for the size of a peptide bond.
                        // If the distance is smaller than this, a bond is guaranteed.
                        // If the distance is larger, a bond is nearly impossible.
                        // TODO: Check this against SEQRES, error on missing residues.
                        if self.topology.distance_between_atoms(prev_c, curr_n) < 2.0 {
                            self.topology
                                .connectivity
                                .as_mut()
                                .ok_or(Error::MissingAminoAcidConformerData)?
                                .push(Bond(
                                    prev_c.min(curr_n),
                                    prev_c.max(curr_n),
                                    BOND_ORDER_SINGLE,
                                ))
                        }
                    }
                }
                // Get the reference aa template for this aa instance in our structure
                let aa_ref = aa_template_by_tok(aa_seq[i])
                    .ok_or(Error::MissingAminoAcidTemplate { aa: aa_seq[i] })?;
                // Maps the label into the index of this instance of that atom for this aa
                let aa_atom_map = aa
                    .iter()
                    .map(|&atom_idx| (atom_labels[atom_idx as usize].as_str(), atom_idx))
                    .collect::<HashMap<_, _>>();
                // Construct the instance of the bonds for this aa using the instance atom idxs
                // NOTE: We use all+contains here intsead of forming a BTreeSet and using subset
                //       because we want to make fewer clones...
                //       comparing Container<T> to Container<&T> is a pain
                if aa_atom_map.keys().all(|k| {
                    aa_ref.heavy_atom_labels.contains(k)
                        || aa_ref.hydrogen_labels.contains(k)
                        || AminoAcidTemplate::TERMINI_ATOMS.contains(k)
                }) {
                    let new_connections = aa_ref
                        .bonds
                        .iter()
                        .filter_map(|BondTemplate(a1, a2, order)| {
                            match (aa_atom_map.get(a1), aa_atom_map.get(a2)) {
                                (Some(a_idx1), Some(a_idx2)) => {
                                    Some(Bond(*a_idx1.min(a_idx2), *a_idx1.max(a_idx2), *order))
                                }
                                _ => None,
                            }
                        })
                        .chain(aa_ref.gen_termini_bonds(&aa_atom_map));
                    self.topology
                        .connectivity
                        .as_mut()
                        .ok_or(Error::MissingAminoAcidConformerData)?
                        .extend(new_connections);
                } else {
                    let wrong_atoms: Vec<_> = aa_atom_map
                        .keys()
                        .filter(|&k| {
                            !aa_ref.heavy_atom_labels.contains(k)
                                && !aa_ref.hydrogen_labels.contains(k)
                                && !AminoAcidTemplate::TERMINI_ATOMS.contains(k)
                        })
                        .map(|atom_label| atom_label.to_string())
                        .collect();
                    return Err(Error::WrongAtomsInAminoAcid {
                        aa: aa_seq[i],
                        wrong_atoms,
                    });
                }
            }
        }
        Ok(())
    }
}
