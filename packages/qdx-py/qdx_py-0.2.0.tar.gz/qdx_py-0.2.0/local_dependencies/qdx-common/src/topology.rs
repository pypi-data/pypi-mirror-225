use std::io::Write;
use std::{collections::HashMap, fs::File};

use anyhow::anyhow;
#[cfg(feature = "graphql")]
use async_graphql::{InputObject, SimpleObject};
use euclid::default::Point3D;
use itertools::Itertools;
use periodic_table_on_an_enum::ElectronicConfiguration;
use petgraph::{dot::Dot, prelude::UnGraph};
use qdx_derive::Typedef;
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};

use crate::bond::{
    Bond, BondOrder, BondOrders, RingResolver, BOND_ORDER_ONEANDAHALF, BOND_ORDER_RING,
};

#[derive(Clone, Debug, Eq, PartialEq, Typedef)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
pub struct Alt(pub u32, pub Vec<u32>);

#[cfg(feature = "graphql")]
async_graphql::scalar!(Alt);

fn with_index<T, F>(mut f: F) -> impl FnMut(&T) -> bool
where
    F: FnMut(usize, &T) -> bool,
{
    let mut i = 0;
    move |item| (f(i, item), i += 1).0
}

#[derive(Clone, Debug, Default, PartialEq, Typedef)]
#[cfg_attr(
    feature = "graphql",
    derive(InputObject, SimpleObject),
    graphql(rename_fields = "snake_case", input_name = "TopologyInput")
)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
pub struct Topology {
    pub symbols: Vec<String>,
    pub geometry: Vec<f32>,
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub connectivity: Option<Vec<Bond>>,
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub atom_charges: Option<Vec<i8>>,
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub partial_charges: Option<Vec<f32>>,
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub atom_labels: Option<Vec<String>>,
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub fragments: Option<Vec<Vec<u32>>>,
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub fragment_charges: Option<Vec<i8>>,
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub alts: Option<Vec<Alt>>,
}

pub struct TopologyIter<'a> {
    topology: &'a Topology,
    index: usize,
}

impl<'a> IntoIterator for &'a Topology {
    type Item = (
        &'a str,
        &'a [f32; 3],
        Option<i8>,
        Option<f32>,
        Option<&'a str>,
    );
    type IntoIter = TopologyIter<'a>;

    fn into_iter(self) -> Self::IntoIter {
        TopologyIter {
            topology: self,
            index: 0,
        }
    }
}

impl<'a> Iterator for TopologyIter<'a> {
    type Item = (
        &'a str,
        &'a [f32; 3],
        Option<i8>,
        Option<f32>,
        Option<&'a str>,
    );

    fn next(&mut self) -> Option<Self::Item> {
        if self.index < self.topology.symbols.len() {
            let symbol = self.topology.symbols[self.index].as_str();
            let geometry = self.topology.geometry[self.index * 3..self.index * 3 + 3]
                .try_into()
                .unwrap();
            let atom_charge = self
                .topology
                .atom_charges
                .as_ref()
                .and_then(|atom_charges| atom_charges.get(self.index).copied());
            let partial_charge = self
                .topology
                .partial_charges
                .as_ref()
                .and_then(|partial_charges| partial_charges.get(self.index).copied());
            let atom_label = self
                .topology
                .atom_labels
                .as_ref()
                .and_then(|labels| labels.get(self.index))
                .map(|x| x.as_str());
            self.index += 1;
            Some((symbol, geometry, atom_charge, partial_charge, atom_label))
        } else {
            None
        }
    }
}

type Node = (usize, Point3D<f32>, String);

impl Topology {
    pub fn center(&self) -> (f32, f32, f32) {
        assert_eq!(self.geometry.len() % 3, 0);

        let mut avg_x = 0.0;
        let mut avg_y = 0.0;
        let mut avg_z = 0.0;
        for i in 0..self.geometry.len() / 3 {
            avg_x += unsafe { self.geometry.get_unchecked(3 * i) };
            avg_y += unsafe { self.geometry.get_unchecked(3 * i + 1) };
            avg_z += unsafe { self.geometry.get_unchecked(3 * i + 2) };
        }
        avg_x /= self.geometry.len() as f32;
        avg_y /= self.geometry.len() as f32;
        avg_z /= self.geometry.len() as f32;

        (avg_x, avg_y, avg_z)
    }

    pub fn bounding_box(&self) -> ((f32, f32, f32), (f32, f32, f32)) {
        let min @ (mut min_x, mut min_y, mut min_z) = (f32::MAX, f32::MAX, f32::MAX);
        let max @ (mut max_x, mut max_y, mut max_z) = (f32::MIN, f32::MIN, f32::MIN);
        for chunk in self.geometry.chunks(3) {
            match chunk {
                [x, y, z] => {
                    min_x = x.min(min_x);
                    min_y = y.min(min_y);
                    min_z = z.min(min_z);

                    max_x = x.max(max_x);
                    max_y = y.max(max_y);
                    max_z = z.max(max_z);
                }
                _ => panic!("`Topology::geometry` is malformed: `len` must be a multiple of 3"),
            }
        }
        (min, max)
    }

    pub fn broken_bonds(&self) -> Vec<Bond> {
        let mut broken_bonds = Vec::new();

        let empty_frag = vec![]; // Needed for lifetimes

        for bond in self.connectivity.as_ref().unwrap_or(&vec![]).iter() {
            let begin_frag = self
                .fragments
                .as_ref()
                .unwrap_or(&empty_frag)
                .iter()
                .find_position(|frag| frag.contains(&bond.0));
            let end_frag = self
                .fragments
                .as_ref()
                .unwrap_or(&empty_frag)
                .iter()
                .find_position(|frag| frag.contains(&bond.1));
            match (begin_frag, end_frag) {
                (Some((i, _)), Some((j, _))) if i != j => {
                    broken_bonds.push(*bond);
                }
                (Some(_), None) => {
                    broken_bonds.push(*bond);
                }
                (None, Some(_)) => {
                    broken_bonds.push(*bond);
                }
                _ => { /* Do nothing */ }
            }
        }

        broken_bonds
    }

    pub fn drop_atoms(&mut self, atoms_to_drop: &[u32]) {
        debug_assert!(self.is_valid());

        // Filter dropped atoms from fragments; comes first because it uses atom_charges
        if let Some(fragments) = &mut self.fragments {
            for (i, f) in fragments.iter_mut().enumerate() {
                // Update the charges by subtracting out the charge of any removed atoms
                if let (Some(fragment_charges), Some(atom_charges)) =
                    (&mut self.fragment_charges, &self.atom_charges)
                {
                    fragment_charges[i] -= f
                        .iter()
                        .filter_map(|&x| {
                            atoms_to_drop
                                .contains(&x)
                                .then_some(atom_charges[x as usize])
                        })
                        .sum::<i8>();
                }
                // Remove atoms that are to be dropped and are thus no longer around
                f.retain(|x| !atoms_to_drop.contains(x));
                // Reindex atoms that came after the dropped ones
                for atom_i in f.iter_mut() {
                    *atom_i -= atoms_to_drop
                        .iter()
                        .filter(|&atom_j| *atom_j < *atom_i)
                        .count() as u32;
                }
            }
            // Remove any fragments that became empty due to the above
            if let Some(fragment_charges) = &mut self.fragment_charges {
                fragment_charges.retain(with_index(|i, _| !fragments[i].is_empty()));
            }
            fragments.retain(|f| !f.is_empty());
        }

        // Drop atom-wise data
        self.symbols
            .retain(with_index(|i, _| !atoms_to_drop.contains(&(i as u32))));
        self.geometry.retain(with_index(|i, _| {
            !atoms_to_drop.contains(&((i as u32) / 3))
        }));
        if let Some(atom_charges) = &mut self.atom_charges {
            atom_charges.retain(with_index(|i, _| !atoms_to_drop.contains(&(i as u32))));
        }
        self.partial_charges = None;
        if let Some(atom_labels) = &mut self.atom_labels {
            atom_labels.retain(with_index(|i, _| !atoms_to_drop.contains(&(i as u32))));
        }

        // Drop unneeded bonds and reindex atoms in still-present bonds
        if let Some(connectivity) = &mut self.connectivity {
            connectivity.retain(|x| !atoms_to_drop.contains(&x.0) && !atoms_to_drop.contains(&x.1));
            for bond in connectivity.iter_mut() {
                bond.0 -= atoms_to_drop
                    .iter()
                    .filter(|&atom_j| *atom_j < bond.0)
                    .count() as u32;
                bond.1 -= atoms_to_drop
                    .iter()
                    .filter(|&atom_j| *atom_j < bond.1)
                    .count() as u32;
            }
        }
        debug_assert!(self.is_valid());
    }

    /// Remove a fragment and all the atoms it references from a topology
    ///
    /// # Example
    /// ```
    /// use qdx_common::topology::Topology;
    /// let mut topology = Topology {
    ///     symbols: vec!["C".into(), "H".into(), "O".into()],
    ///     geometry: vec![1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0],
    ///     connectivity: None,
    ///     fragments: Some(vec![vec![0], vec![1], vec![2]]),
    ///     fragment_charges: Some(vec![0, 0, 0]),
    ///     atom_charges: Some(vec![0, 0, 0]),
    ///     partial_charges: Some(vec![0.0, 0.0, 0.0]),
    ///     atom_labels: None,
    ///     alts: None,
    /// };
    /// topology.drop_fragments(&vec![1]);
    /// assert_eq!(topology.fragments.as_ref().map(|l| l.len()), Some(2));
    /// assert_eq!(topology.symbols.len(), 2);
    /// assert_eq!(topology.symbols, vec!["C", "O"]);
    /// assert_eq!(topology.geometry.len(), 6);
    /// topology.drop_fragments(&vec![1]);
    /// assert_eq!(topology.fragments.as_ref().map(|l| l.len()), Some(1));
    /// assert_eq!(topology.symbols.len(), 1);
    /// assert_eq!(topology.symbols, vec!["C"]);
    /// assert_eq!(topology.geometry.len(), 3);
    /// let mut topology2 = Topology {
    ///     symbols: vec!["C".into(), "H".into(), "O".into()],
    ///     geometry: vec![1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0],
    ///     connectivity: None,
    ///     fragments: Some(vec![vec![0], vec![1], vec![2]]),
    ///     fragment_charges: None,
    ///     atom_charges: None,
    ///     partial_charges: None,
    ///     atom_labels: None,
    ///     alts: None,
    /// };
    /// topology2.drop_fragments(&vec![1]);
    /// assert_eq!(topology2.fragments.as_ref().map(|l| l.len()), Some(2));
    /// topology2.drop_fragments(&vec![1]);
    /// assert_eq!(topology2.fragments.as_ref().map(|l| l.len()), Some(1));
    /// topology2.drop_fragments(&vec![0]);
    /// assert_eq!(topology2.fragments.as_ref().map(|l| l.len()), Some(0));
    /// ```
    pub fn drop_fragments(&mut self, frags_to_drop: &[usize]) {
        debug_assert!(self.is_valid());

        // Clear and obtain the existing fragments (if any are there)
        if let Some(fragments) = &mut self.fragments {
            // Get the atoms in the fragment to drop
            let atoms_to_drop = frags_to_drop
                .iter()
                .flat_map(|&frag_to_drop| &fragments[frag_to_drop])
                .copied()
                .collect::<Vec<_>>();

            // Drop the fragment itself as requested (not necessary, but a small optimization)
            if let Some(fragment_charges) = &mut self.fragment_charges {
                fragment_charges.retain(with_index(|i, _| !frags_to_drop.contains(&i)))
            }
            fragments.retain(with_index(|i, _| !frags_to_drop.contains(&i)));

            // Remove all the atoms from the Topology
            self.drop_atoms(&atoms_to_drop);
        }
        debug_assert!(self.is_valid());
    }

    /// Extend this topology with another topology.
    /// # Example
    /// ```
    /// use qdx_common::topology::Topology;
    /// let mut topology = Topology {
    ///    symbols: vec!["C".into(),"H".into(),"O".into()],
    ///    geometry: vec![1.0,1.0,1.0,2.0,2.0,2.0,3.0,3.0,3.0],
    ///    connectivity: None,
    ///    fragments: Some(vec![vec![0], vec![1], vec![2]]),
    ///    fragment_charges: Some(vec![0,0,0]),
    ///    atom_charges: Some(vec![0,0,0]),
    ///    partial_charges: Some(vec![0.0,0.0,0.0]),
    ///    atom_labels: None,
    ///    ..Default::default()
    /// };
    /// let mut other = Topology {
    ///   symbols: vec!["C".into(),"H".into(),"O".into()],
    ///   geometry: vec![1.0,1.0,1.0,2.0,2.0,2.0,3.0,3.0,3.0],
    ///   connectivity: None,
    ///   fragments: Some(vec![vec![0], vec![1], vec![2]]),
    ///   fragment_charges: Some(vec![0,0,0]),
    ///   atom_charges: Some(vec![0,0,0]),
    ///   partial_charges: Some(vec![0.0,0.0,0.0]),
    ///   atom_labels: None,
    ///   ..Default::default()
    /// };
    /// topology.extend(other);
    /// assert_eq!(topology.symbols.len(), 6);
    /// assert_eq!(topology.symbols, vec!["C","H","O","C","H","O"]);
    /// assert_eq!(topology.geometry.len(), 18);
    /// assert_eq!(topology.fragments, Some(vec![vec![0], vec![1], vec![2], vec![3], vec![4], vec![5]]));
    /// assert_eq!(topology.fragment_charges, Some(vec![0,0,0,0,0,0]));
    /// assert_eq!(topology.atom_charges, Some(vec![0,0,0,0,0,0]));
    /// assert_eq!(topology.partial_charges, Some(vec![0.0,0.0,0.0,0.0,0.0,0.0]));
    ///
    /// let mut other_unfragmented = Topology {
    ///   symbols: vec!["C".into(),"H".into(),"O".into()],
    ///   geometry: vec![1.0,1.0,1.0,2.0,2.0,2.0,3.0,3.0,3.0],
    ///   ..Default::default()
    /// };
    /// topology.extend(other_unfragmented);
    /// assert_eq!(topology.symbols.len(), 9);
    /// assert_eq!(topology.symbols, vec!["C","H","O","C","H","O","C","H","O"]);
    /// assert_eq!(topology.geometry.len(), 27);
    /// assert_eq!(topology.fragments, Some(vec![vec![0], vec![1], vec![2], vec![3], vec![4], vec![5], vec![6, 7, 8]]));
    /// assert_eq!(topology.fragment_charges, Some(vec![0,0,0,0,0,0,0]));
    /// ```
    pub fn extend(&mut self, mut other: Self) {
        debug_assert!(self.is_valid() && other.is_valid());

        let offset = self.symbols.len() as u32;
        let other_len = other.symbols.len() as u32;

        // Extend symbols
        self.symbols.append(&mut other.symbols);

        // Extend geometry
        self.geometry.append(&mut other.geometry);

        // Extend the atom charges
        match (&mut self.atom_charges, &mut other.atom_charges) {
            (Some(atom_charges), Some(other_atom_charges)) => {
                atom_charges.append(other_atom_charges)
            }
            (Some(atom_charges), None) => {
                atom_charges.extend((0..other_len).map(|_| 0));
            }
            (None, Some(other_atom_charges)) => {
                let mut atom_charges = (0..offset).map(|_| 0).collect::<Vec<_>>();
                atom_charges.append(other_atom_charges);
                self.atom_charges = Some(atom_charges);
            }
            _ => { /* Do nothing */ }
        }
        // Extend the partial charges
        match (&mut self.partial_charges, &mut other.partial_charges) {
            (Some(partial_charges), Some(other_partial_charges)) => {
                partial_charges.append(&mut *other_partial_charges);
            }
            (Some(partial_charges), None) => {
                partial_charges.extend((0..other_len).map(|_| 0.0));
            }
            (None, Some(other_partial_charges)) => {
                let mut partial_charges = (0..offset).map(|_| 0.0).collect::<Vec<_>>();
                partial_charges.append(&mut *other_partial_charges);
                self.partial_charges = Some(partial_charges);
            }
            _ => { /* Do nothing */ }
        }

        // Extend the atom labels
        match (&mut self.atom_labels, &mut other.atom_labels) {
            (Some(atom_labels), Some(other_atom_labels)) => atom_labels.append(other_atom_labels),
            (Some(atom_labels), None) => {
                atom_labels.extend((0..other_len).map(|_| String::new()));
            }
            (None, Some(other_atom_labels)) => {
                let mut atom_labels = self
                    .symbols
                    .iter()
                    .map(|_| String::new())
                    .collect::<Vec<_>>();
                atom_labels.append(other_atom_labels);
                self.atom_labels = Some(atom_labels);
            }
            _ => { /* Do nothing */ }
        }

        // Extend connectivity
        let offset_connectivity = other.connectivity.map(|connectivity| {
            connectivity
                .iter()
                .map(|bond| Bond(bond.0 + offset, bond.1 + offset, bond.2))
                .collect::<Vec<_>>()
        });
        if let Some(connectivity) = &mut self.connectivity {
            if let Some(offset_connectivity) = offset_connectivity {
                connectivity.extend(offset_connectivity);
            }
        } else {
            self.connectivity = offset_connectivity;
        }

        let offset_fragments = match other.fragments {
            Some(frags) => frags
                .into_iter()
                .map(|frag| frag.into_iter().map(|i| i + offset).collect::<Vec<_>>())
                .collect::<Vec<_>>(),
            None => vec![(offset..other_len + offset).collect::<Vec<_>>()],
        };

        // Extend fragment charges before extending fragments
        // to prevent problems caused by pre-emptively modifying the fragements
        match (&mut self.fragment_charges, &mut other.fragment_charges) {
            (Some(fragment_charges), Some(other_fragment_charges)) => {
                fragment_charges.append(other_fragment_charges)
            }
            (Some(fragment_charges), None) => {
                // if we have fragments,
                // we should always have fragments for the other topology default to zero.
                fragment_charges.extend(offset_fragments.iter().map(|_| 0));
            }
            (None, Some(other_fragment_charges)) => {
                let mut fragment_charges = vec![];
                if let Some(fragments) = &self.fragments {
                    // If these fragments are present (but not charged),
                    // then default to zero.
                    fragment_charges.extend(fragments.iter().map(|_| 0));
                }
                fragment_charges.append(other_fragment_charges);
                self.fragment_charges = Some(fragment_charges);
            }
            _ => { /* Do nothing */ }
        }

        match &mut self.fragments {
            Some(frags) => {
                // If other fragments are present, and there are fragments on self,
                // then we add the other fragments to self
                frags.extend(offset_fragments);
            }
            None => {
                // If other fragments are present, but there are no fragments on self,
                // then we put all current atoms in a single fragment
                let mut fragments = vec![vec![]];
                for i in 0..offset {
                    fragments[0].push(i);
                }
                fragments.extend(offset_fragments);
                self.fragments = Some(fragments);
            }
        }

        debug_assert!(self.is_valid());
    }

    /// Compute the distance from the reference point to an atom identified by its index.
    pub fn distance_to_atom(&self, reference_point: &[f32; 3], atom_idx: u32) -> f32 {
        Point3D::new(reference_point[0], reference_point[1], reference_point[2]).distance_to(
            Point3D::new(
                self.geometry[atom_idx as usize * 3],
                self.geometry[atom_idx as usize * 3 + 1],
                self.geometry[atom_idx as usize * 3 + 2],
            ),
        )
    }

    /// Compute the distance between two atoms identified by their indices.
    pub fn distance_between_atoms(&self, atom1_idx: u32, atom2_idx: u32) -> f32 {
        Point3D::new(
            self.geometry[atom1_idx as usize * 3],
            self.geometry[atom1_idx as usize * 3 + 1],
            self.geometry[atom1_idx as usize * 3 + 2],
        )
        .distance_to(Point3D::new(
            self.geometry[atom2_idx as usize * 3],
            self.geometry[atom2_idx as usize * 3 + 1],
            self.geometry[atom2_idx as usize * 3 + 2],
        ))
    }

    /// Create a vector of indices based on whether any atom in the corresponding atom set is
    /// within the threshold of the reference point. The u32s in the atom_sets parameter should be
    /// valid indices into the atoms in the topology.
    pub fn get_atom_sets_near_point(
        &self,
        reference_point: &[f32; 3],
        threshold: f32,
        atom_sets: &Option<Vec<Vec<u32>>>,
    ) -> Vec<usize> {
        if let Some(atom_sets) = atom_sets {
            return atom_sets
                .iter()
                .enumerate()
                .filter_map(|(idx, atom_set)| {
                    atom_set
                        .iter()
                        .any(|&a| self.distance_to_atom(reference_point, a) <= threshold)
                        .then_some(idx)
                })
                .collect();
        }
        vec![]
    }

    /// Create a vector of fragment indices based on whether any atom in that fragment is within
    /// the threshold of the reference point.
    pub fn get_fragments_near_point(
        &self,
        reference_point: &[f32; 3],
        threshold: f32,
    ) -> Vec<usize> {
        self.get_atom_sets_near_point(reference_point, threshold, &self.fragments)
    }

    /// Get the coordinates of a specific atom. (could this be renamed to get_coords()?)
    pub fn coord(&self, atom_idx: u32) -> (f32, f32, f32) {
        let atom_idx = atom_idx as usize;
        (
            self.geometry[atom_idx * 3],
            self.geometry[atom_idx * 3 + 1],
            self.geometry[atom_idx * 3 + 2],
        )
    }

    /// Set the coordinates of a specific atom
    pub fn set_coords(&mut self, atom_idx: u32, new_coords: (f32, f32, f32)) {
        let atom_idx = atom_idx as usize;
        self.geometry[atom_idx * 3] = new_coords.0;
        self.geometry[atom_idx * 3 + 1] = new_coords.1;
        self.geometry[atom_idx * 3 + 2] = new_coords.2;
    }

    pub fn to_xyz_format(&self) -> String {
        let xyz = format!(
            " {}\n qdx molecule \n {}",
            self.symbols.len(),
            self.geometry
                .chunks(3)
                .zip(self.symbols.clone())
                .map(|a| format!("{} {} {} {}", a.1, a.0[0], a.0[1], a.0[2]))
                .collect::<Vec<String>>()
                .join("\n")
        );
        xyz
    }

    pub fn to_xyz_format_fragments(&self) -> Option<Vec<String>> {
        let bind = self.to_xyz_format();
        let mut xyzs = bind.split('\n').collect::<Vec<_>>();
        // drop the inherent label
        xyzs.drain(..2);
        self.fragments.as_ref().map(|fragments| {
            fragments
                .iter()
                .enumerate()
                .map(|(id, frag)| {
                    format!(
                        "{}\nfragment {} charge {:?} \n{}",
                        frag.len(),
                        id,
                        self.fragment_charges.clone().map(|fc| fc[id]),
                        frag.iter()
                            .map(|atom| xyzs[*atom as usize])
                            .collect::<Vec<_>>()
                            .join("\n")
                    )
                })
                .collect::<Vec<_>>()
        })
    }

    /// Use charges on atoms to determine charges of fragments
    pub fn explicit_fragment_charges(&self) -> Option<Vec<i8>> {
        self.fragments.as_ref().map(|x| {
            x.iter()
                .map(|x| {
                    if let Some(atom_charges) = self.atom_charges.clone() {
                        x.iter().map(|x| atom_charges[*x as usize]).sum()
                    } else {
                        0
                    }
                })
                .collect()
        })
    }

    /// In theory, this should work;
    /// however, knowing the exact bond-orders of atom pairs is easier said than done
    /// This code is deprecated
    /// until we can be sure that the correct bond orders are being assigned to each atom pair
    pub fn implicit_fragment_charges(&self) -> anyhow::Result<Option<Vec<isize>>> {
        let parts = self
            .symbols
            .iter()
            .enumerate()
            .map(|(a_id, atom)| {
                let element = periodic_table_on_an_enum::Element::from_symbol(atom)
                    .unwrap_or_else(|| panic!("Unknown symbol {atom}"));
                let valence_electrons: isize = element
                    .get_electronic_configuration_str()
                    .split(']')
                    .last()
                    .expect("no orbitals")
                    .split(' ')
                    .map(|orbital| {
                        orbital
                            .chars()
                            .last()
                            .unwrap_or('0')
                            .to_string()
                            .parse::<isize>()
                            .unwrap()
                    })
                    .sum();

                let electrons_to_form_stable_shell = match element.get_electronic_configuration() {
                    ElectronicConfiguration { s: _, p, d, f }
                        if f == [0, 0] && d == [0; 4] && p == [0u8; 6] =>
                    {
                        2
                    }
                    ElectronicConfiguration { s: _, p, d, f }
                        if f == [0, 0] && d == [0; 4] && p != [0u8; 6] =>
                    {
                        8
                    }
                    ElectronicConfiguration { s: _, p, d, f }
                        if f == [0, 0] && d != [0; 4] && p != [0u8; 6] =>
                    {
                        8
                    }
                    ElectronicConfiguration { .. } => panic!("unsupported"),
                };

                let bonds: usize = self
                    .connectivity
                    .clone()
                    .expect("need bonds to get charges")
                    .iter()
                    .map(|pair| {
                        if pair.0 == a_id as u32 || pair.1 == a_id as u32 {
                            pair.2 as usize
                        } else {
                            0
                        }
                    })
                    .sum();
                if atom == "C" && bonds != 4 {
                    // println!("C has wrong bonds {}", bonds)
                }

                let protons = element.get_atomic_number() as isize;

                // TODO: nbe = spdf fill stable outer shell
                // let nbe = (protons - valence_electrons) - bonds as isize;
                let nbe = electrons_to_form_stable_shell - 2 * bonds as isize;
                let charge = valence_electrons - nbe - bonds as isize;
                (protons, charge)
            })
            .collect::<Vec<_>>();

        Ok(match &self.fragments {
            Some(fragments) => Some(
                fragments
                    .iter()
                    .enumerate()
                    .map(|(id, fragment)| {
                        let mut charge = 0;
                        let mut protons = 0;
                        for atom in fragment {
                            let comp = parts[*atom as usize];
                            protons += comp.0;
                            charge += comp.1;
                        }
                        if (protons + charge) % 2 != 0 {
                            let mut file = File::create("/tmp/problem_frag.dot").unwrap();
                            write!(file, "{:?}", Dot::new(&self.fragment_to_graph(id)))?;
                            return Err(anyhow!(
                                "Uneven number of electrons in frag {}: protons {} charge {}",
                                id,
                                protons,
                                charge
                            ));
                        }
                        Ok(charge)
                    })
                    .collect::<Result<Vec<isize>, _>>()?,
            ),
            None => None,
        })
    }

    pub fn to_graph(&self) -> UnGraph<Node, (f32, BondOrder)> {
        // TODO: return fragmented graph if fragmentation is present
        let mut graph = UnGraph::default();
        let idxs = self
            .geometry
            .chunks(3)
            .zip(self.symbols.clone())
            .enumerate()
            .map(|a| graph.add_node((a.0, Point3D::new(a.1 .0[0], a.1 .0[1], a.1 .0[2]), a.1 .1)))
            .collect::<Vec<_>>();

        if let Some(connectivity) = self.connectivity.clone() {
            for bond in connectivity {
                let i1 = idxs[bond.0 as usize];
                let i2 = idxs[bond.1 as usize];
                graph.add_edge(i1, i2, (graph[i1].1.distance_to(graph[i2].1), bond.2));
            }
        }
        graph
    }

    pub fn fragment_to_graph(&self, frag_id: usize) -> UnGraph<Node, (f32, BondOrder)> {
        // TODO: return fragmented graph if fragmentation is present
        let mut graph = UnGraph::default();
        if let Some(fragments) = self.fragments.clone() {
            let idxs = self
                .geometry
                .chunks(3)
                .zip(self.symbols.clone())
                .enumerate()
                .filter_map(|(atom_id, (geometry, symbol))| {
                    if fragments[frag_id].contains(&(atom_id as u32)) {
                        Some((
                            atom_id,
                            graph.add_node((
                                atom_id,
                                Point3D::new(geometry[0], geometry[1], geometry[2]),
                                symbol,
                            )),
                        ))
                    } else {
                        None
                    }
                })
                .collect::<HashMap<usize, _>>();

            if let Some(connectivity) = self.connectivity.clone() {
                for bond in connectivity {
                    if fragments[frag_id].contains(&bond.0) && fragments[frag_id].contains(&bond.1)
                    {
                        let i1 = idxs[&(bond.0 as usize)];
                        let i2 = idxs[&(bond.1 as usize)];
                        graph.add_edge(i1, i2, (graph[i1].1.distance_to(graph[i2].1), bond.2));
                    }
                }
            }
        }
        graph
    }

    /// Infer bonds and their orders based on geometry.
    /// Will only check for bonds inside fragments and between neighboring fragments.
    pub fn implicit_connectivity(&self, tolerance: f32) -> Vec<Bond> {
        let points = self
            .geometry
            .chunks(3)
            .zip(self.symbols.clone())
            .map(|(geom, symbol)| (symbol, Point3D::new(geom[0], geom[1], geom[2])))
            .collect::<Vec<_>>();

        let bond_orders = BondOrders::default();

        let mut ring_resolver = RingResolver::new();

        self.fragments
            .as_ref()
            .expect("must be fragmented")
            .windows(2) // compare two fragments at a time
            .flat_map(|x| {
                x.iter()
                    .flatten()
                    .combinations(2)
                    .filter_map(|atom_ids| match atom_ids[..] {
                        [i, j] => {
                            let a1 = &points[*i as usize];
                            let a2 = &points[*j as usize];
                            let distance = a1.1.distance_to(a2.1);
                            let order = bond_orders
                                .max_bond_order(&a1.0, &a2.0, distance, tolerance)
                                .unwrap_or_else(|| {
                                    panic!("no known bond orders between {} and {}", a1.0, a2.0)
                                });

                            if order == 0 {
                                if distance < 2.5 {
                                    tracing::debug!(
                                        "Not connecting {}{}  {}{} even though close: {}A",
                                        a1.0,
                                        i,
                                        a2.0,
                                        j,
                                        distance
                                    );
                                }
                                None
                            } else {
                                Some((i, j, order))
                            }
                        }
                        _ => panic!("invalid"),
                    })
            })
            .map(|(a, b, order)| (a.min(b), a.max(b), order))
            .sorted()
            .dedup_by(|(a1, a2, _), (b1, b2, _)| {
                (*a1 == *b1 && *a2 == *b2) || (*a1 == *b2 && *a2 == *b1)
            }) // Remove duplicate inter-fragment bonds
            .map(|x| Bond(*x.0, *x.1, ring_resolver.step(x.2))) // Apply aromatic-ring fix
            .collect()
    }

    pub fn is_valid(&self) -> bool {
        if self.geometry.len() % 3 != 0 {
            eprintln!(
                "Geometry length must be a multiple of 3 but is {}",
                self.geometry.len()
            );
            return false;
        }
        if self.geometry.len() != self.symbols.len() * 3 {
            eprintln!(
                "Geometry length must be 3 times the number of symbols ({}) but is {}",
                self.symbols.len(),
                self.geometry.len()
            );
            return false;
        }
        if let Some(atom_charges) = &self.atom_charges {
            if atom_charges.len() != self.symbols.len() {
                eprintln!(
                    "Atom charges length must be the same as the number of symbols ({}) but is {}",
                    self.symbols.len(),
                    atom_charges.len()
                );
                return false;
            }
        }
        if let Some(partial_charges) = &self.partial_charges {
            if partial_charges.len() != self.symbols.len() {
                eprintln!(
                    "Atom charges length must be the same as the number of symbols ({}) but is {}",
                    self.symbols.len(),
                    partial_charges.len()
                );
                return false;
            }
        }
        if let Some(atom_labels) = &self.atom_labels {
            if atom_labels.len() != self.symbols.len() {
                eprintln!(
                    "Atom labels length must be the same as the number of symbols ({}) but is {}",
                    self.symbols.len(),
                    atom_labels.len()
                );
                return false;
            }
        }
        if let Some(fragments) = &self.fragments {
            // An atom cannot be in multiple fragments
            for (i, i_frag) in fragments.iter().enumerate() {
                for (j, j_frag) in fragments.iter().enumerate() {
                    if i == j {
                        continue;
                    }
                    for i_atom in i_frag {
                        for j_atom in j_frag {
                            if i_atom == j_atom {
                                eprintln!("Atom {i_atom} is in both fragments {i} and {j}");
                                return false;
                            }
                        }
                    }
                }
            }
            // An atom cannot be in the same fragment multiple times
            for frag in fragments {
                for (i, i_atom) in frag.iter().enumerate() {
                    for (j, j_atom) in frag.iter().enumerate() {
                        if i == j {
                            continue;
                        }
                        if i_atom == j_atom {
                            eprintln!("Atom {i_atom} is in fragment {i} multiple times");
                            return false;
                        }
                    }
                }
            }
        }
        if let Some(fragment_charges) = &self.fragment_charges {
            if self.fragments.is_none() {
                eprintln!("Fragment charges cannot be set without fragments");
                return false;
            }
            if fragment_charges.len() != self.fragments.as_ref().unwrap().len() {
                eprintln!(
                    "Fragment charges length must be the same as the number of fragments ({}) but is {}",
                    self.fragments.as_ref().unwrap().len(),
                    fragment_charges.len()
                );
                return false;
            }
        }
        if let Some(connectivity) = &self.connectivity {
            for Bond(i, j, order) in connectivity {
                // An atom cannot be bonded to itself
                if i == j {
                    eprintln!("Atom {i} is bonded to itself");
                    return false;
                }
                // An atom cannot have greater than triple bonds
                if *order > 3 && *order != BOND_ORDER_ONEANDAHALF && *order != BOND_ORDER_RING {
                    eprintln!("Atom {i} has a bond of order {order}");
                    return false;
                }
            }
        }
        true
    }
}
