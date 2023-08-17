use std::{
    cmp::Ordering,
    collections::{BTreeMap, BTreeSet, HashMap, HashSet},
    fmt::{self, Display, Formatter},
    ops::AddAssign,
};

use itertools::Itertools;
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};

use crate::{
    amino_acid::AminoAcid,
    bond::Bond,
    conformer::{Conformer, Label},
    topology::{Alt, Topology},
};

#[derive(thiserror::Error, Debug)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
pub enum Error {
    #[error("invalid line length, expected '> {expected}', found '{found}'")]
    InvalidLineLength { expected: usize, found: usize },
    #[error("invalid line, expected '{expected}', found '{found}'")]
    InvalidLine { expected: String, found: String },
    #[error(
        "invalid connection for atom index {atom_idx} references and atom that does not exist"
    )]
    InvalidConnection { atom_idx: u32 },
    #[error("invalid bond order between {origin_element} {origin} and {target_element} {target} {distance}")]
    InvalidBondOrder {
        origin: String,
        origin_element: String,
        target: String,
        target_element: String,
        distance: f32,
    },
    #[error("expected int at {line}:{start}-{end}")]
    ExpectedInt {
        line: usize,
        start: usize,
        end: usize,
    },
    #[error("expected float at {line}:{start}-{end}")]
    ExpectedFloat {
        line: usize,
        start: usize,
        end: usize,
    },
}

#[derive(Clone, Eq, PartialEq, Ord, PartialOrd)]
struct ResidueId {
    chain_id: String,
    sequence_number: i32,
    insertion_code: String,
    residue_name: String,
}

impl Display for ResidueId {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "{}_{:…>9}_{}_{}",
            self.chain_id, self.sequence_number, self.insertion_code, self.residue_name
        )?;
        Ok(())
    }
}

enum Line {
    Seqres(Seqres),
    Atom(Atom),
    Conect(Conect),
    Ter(Ter),
    Ignored(String),
    Model,
    EndModel,
    End,
}

struct Seqres {
    ser_num: u32,
    chain_id: String,
    num_res: u32,
    seq: Vec<String>,
}

struct Atom {
    atom_idx: u32,
    atom_name: String,
    alternate_location: Option<String>,
    residue_name: String,
    chain_id: String,
    sequence_number: i32,
    residue_insertion: Option<String>,
    atom_x: f32,
    atom_y: f32,
    atom_z: f32,
    occupancy: f32,
    temperature_factor: f32,
    segment_id: Option<String>,
    element_symbol: String,
    charge: i8,
    is_het_atom: bool,
}

#[derive(Debug)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
pub struct Conect {
    atom_idxs: Vec<u32>,
}

struct Ter {
    atom_idx: u32,
    residue_name: String,
    chain_id: String,
    residue_idx: i32,
}

impl Display for Line {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::Seqres(seqres) => Self::fmt_seqres(seqres, f),
            Self::Atom(atom) => Self::fmt_atom(atom, f),
            Self::Conect(conect) => Self::fmt_conect(conect, f),
            Self::Ter(ter) => Self::fmt_ter(ter, f),
            Self::Ignored(ignored) => ignored.fmt(f),
            Self::End => "END".fmt(f),
            Self::Model => "MODEL ".fmt(f), // FIXME: Figure out model indices
            Self::EndModel => "ENDMDL".fmt(f),
        }
    }
}

impl Line {
    fn try_from(value: &str, line: usize) -> Result<Self, Error> {
        if value.len() < 3 {
            return Err(Error::InvalidLineLength {
                expected: 3,
                found: value.len(),
            });
        }
        // In an ideal world, yes, but remark records sometimes exceeds it
        // if value.len() > 80 {
        //     return Err(Error::InvalidLineLength {
        //         expected: 80,
        //         found: value.len(),
        //     });
        // }
        if value.len() == 3 {
            if value == "END" {
                return Ok(Self::End);
            } else if value == "TER" {
                return Ok(Self::Ignored(value.to_string()));
            } else {
                return Err(Error::InvalidLine {
                    expected: "END".to_string(),
                    found: value.to_string(),
                });
            }
        }
        if value.len() < 6 {
            return Err(Error::InvalidLineLength {
                expected: 6,
                found: value.len(),
            });
        }
        let value = format!("{value:<80}");
        let line_id = &value[0..6];
        match line_id {
            "SEQRES" => Self::try_from_seqres(&value, line),
            "ATOM  " => Self::try_from_atom(&value, line),
            "HETATM" => Self::try_from_hetatm(&value, line),
            "CONECT" => Self::try_from_conect(&value, line),
            "TER   " => Self::try_from_ter(&value, line),
            "MODEL " => Ok(Self::Model),
            "ENDMDL" => Ok(Self::EndModel),
            "END   " => Ok(Self::End),
            _ => Ok(Self::Ignored(value.to_string())),
        }
    }

    fn try_from_seqres(value: &str, line: usize) -> Result<Self, Error> {
        Ok(Self::Seqres(Seqres {
            ser_num: Self::parse_u32(value, 7, 10, line)?,
            chain_id: Self::parse_str(value, 11, 12, line),
            num_res: Self::parse_u32(value, 13, 17, line)?,
            seq: vec![
                Self::parse_str(value, 7, 10, line),
                Self::parse_str(value, 19, 22, line),
                Self::parse_str(value, 23, 26, line),
                Self::parse_str(value, 27, 30, line),
                Self::parse_str(value, 31, 34, line),
                Self::parse_str(value, 35, 38, line),
                Self::parse_str(value, 39, 42, line),
                Self::parse_str(value, 43, 46, line),
                Self::parse_str(value, 47, 50, line),
                Self::parse_str(value, 51, 54, line),
                Self::parse_str(value, 55, 58, line),
                Self::parse_str(value, 59, 62, line),
                Self::parse_str(value, 63, 66, line),
                Self::parse_str(value, 67, 70, line),
            ],
        }))
    }

    fn fmt_seqres(seqres: &Seqres, f: &mut Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "SEQRES {:>3} {:>1} {:>4} ",
            seqres.ser_num, seqres.chain_id, seqres.num_res,
        )?;
        for seq_elem in &seqres.seq {
            write!(f, " {seq_elem}")?;
        }
        write!(f, "          ")
    }

    fn try_from_atom(value: &str, line: usize) -> Result<Self, Error> {
        Ok(Self::Atom(Atom {
            // LINE_ID [0 .. 6)
            atom_idx: Self::parse_u32(value, 6, 11, line)?,
            // UNUSED [11 .. 12)
            atom_name: Self::parse_str(value, 12, 16, line),
            alternate_location: Self::parse_opt_str(value, 16, 17, line),
            residue_name: Self::parse_str(value, 17, 20, line),
            // UNUSED [20 .. 21)
            chain_id: Self::parse_str(value, 21, 22, line),
            sequence_number: Self::parse_i32(value, 22, 26, line)?,
            residue_insertion: Self::parse_opt_str(value, 26, 27, line),
            // UNUSED [27 .. 30)
            atom_x: Self::parse_f32(value, 30, 38, line)?,
            atom_y: Self::parse_f32(value, 38, 46, line)?,
            atom_z: Self::parse_f32(value, 46, 54, line)?,
            occupancy: Self::parse_f32(value, 54, 60, line)?,
            temperature_factor: Self::parse_f32(value, 60, 66, line)?,
            // UNUSED [66 .. 72)
            segment_id: Self::parse_opt_str(value, 72, 76, line),
            element_symbol: Self::parse_str(value, 76, 78, line),
            charge: Self::parse_opt_charge(value, 78, 80, line)?.unwrap_or_default(),
            is_het_atom: false,
        }))
    }

    fn fmt_atom(atom: &Atom, f: &mut Formatter<'_>) -> fmt::Result {
        // the formatting behaviour is strange - not quite left or right aligned depending
        // on the name length
        // ATOM     14  CD1 ILE H  16       5.687  -5.180  20.042  1.00 16.16           C
        // ATOM     15  H   ILE H  16       5.719  -8.041  17.843  1.00 15.91           H
        // ATOM     16  HA  ILE H  16       5.011  -8.089  19.908  1.00 14.62           H
        // ATOM     17  HB  ILE H  16       2.748  -6.457  18.674  1.00 16.05           H
        // ATOM     18 HG13 ILE H  16       3.987  -4.470  18.959  1.00 14.52           H
        // ATOM     19 HG12 ILE H  16       4.979  -5.543  18.043  1.00 14.52           H
        // ATOM     20 HG21 ILE H  16       2.577  -5.253  20.823  1.00 16.45           H
        // ATOM     21 HG22 ILE H  16       2.045  -6.916  20.934  1.00 16.45           H
        // ATOM     22 HG23 ILE H  16       3.626  -6.474  21.558  1.00 16.45           H
        // ATOM     23 HD11 ILE H  16       6.596  -4.859  19.533  1.00 16.16           H
        // ATOM     24 HD12 ILE H  16       5.417  -4.409  20.763  1.00 16.16           H
        let atom_name = match atom.atom_name.len() {
            0 => format!(" {}", atom.atom_name),
            1 => format!(" {}", atom.atom_name),
            2 => format!(" {}", atom.atom_name),
            3 => format!(" {}", atom.atom_name),
            4 => atom.atom_name.clone(),
            _ => {
                // invalid name
                return Err(fmt::Error);
            }
        };
        write!(
            f,
            "{:<6}{:>5} {:<4}{:<1}{:>3} {:>1}{:>4}{:>1}   {:>8.3}{:>8.3}{:>8.3}{:>6.2}{:>6.2}      {:<4}{:>2}{:>2}",
            if atom.is_het_atom { "HETATM" } else { "ATOM" },
            atom.atom_idx,
            atom_name,
            atom.alternate_location.clone().unwrap_or_default(),
            atom.residue_name,
            atom.chain_id,
            atom.sequence_number,
            atom.residue_insertion.clone().unwrap_or_default(),
            atom.atom_x,
            atom.atom_y,
            atom.atom_z,
            atom.occupancy,
            atom.temperature_factor,
            atom.segment_id.clone().unwrap_or_default(),
            atom.element_symbol,
            match atom.charge.cmp(&0) {
                Ordering::Greater => format!("{}+", atom.charge),
                Ordering::Less => format!("{}-", -atom.charge),
                Ordering::Equal => "".to_string()
            }
        )
    }

    fn try_from_hetatm(value: &str, line: usize) -> Result<Self, Error> {
        Self::try_from_atom(value, line).map(|line| match line {
            Self::Atom(atom) => Self::Atom(Atom {
                is_het_atom: true,
                ..atom
            }),
            x => x,
        })
    }

    fn try_from_conect(value: &str, line: usize) -> Result<Self, Error> {
        let mut atom_idxs = Vec::with_capacity(15); // 15 is the maximum number of connections that fit in a single line

        let mut start = 6;
        let mut end = 11;
        while start < value.len() && end <= value.len() {
            let opt_atom_idx = Self::parse_opt_u32(value, start, end, line)?;
            match opt_atom_idx {
                Some(atom_idx) => atom_idxs.push(atom_idx),
                _ => break,
            }
            start += 5;
            end += 5;
        }

        Ok(Self::Conect(Conect { atom_idxs }))
    }

    fn fmt_conect(conect: &Conect, f: &mut Formatter<'_>) -> fmt::Result {
        if conect.atom_idxs.len() < 2 {
            panic!("CONECT with less than 2 atoms not supported")
        } else if conect.atom_idxs.len() == 2 {
            write!(
                f,
                "CONECT{:>5}{:>5}",
                conect.atom_idxs[0], conect.atom_idxs[1],
            )
        } else if conect.atom_idxs.len() == 3 {
            write!(
                f,
                "CONECT{:>5}{:>5}{:>10}",
                conect.atom_idxs[0], conect.atom_idxs[1], conect.atom_idxs[2],
            )
        } else if conect.atom_idxs.len() == 4 {
            write!(
                f,
                "CONECT{:>5}{:>5}{:>10}{:>5}",
                conect.atom_idxs[0], conect.atom_idxs[1], conect.atom_idxs[2], conect.atom_idxs[3],
            )
        } else {
            panic!("CONECT with more than 4 atoms not supported")
        }
    }

    fn try_from_ter(value: &str, line: usize) -> Result<Self, Error> {
        Ok(Self::Ter(Ter {
            // LINE_ID [0 .. 6)
            // Not used for anything and some underlying tooling just prints TER                    243
            // so we can default it
            atom_idx: Self::parse_u32(value, 6, 11, line).unwrap_or_default(),
            // UNUSED [11 .. 17)
            residue_name: Self::parse_str(value, 17, 20, line),
            // UNUSED [20 .. 21)
            chain_id: Self::parse_str(value, 21, 22, line),
            residue_idx: Self::parse_i32(value, 22, 26, line).unwrap_or_default(),
            // UNUSED [26 .. 80)
        }))
    }

    fn fmt_ter(ter: &Ter, f: &mut Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "TER   {:>5}      {:>3} {:>1}{:>4}",
            ter.atom_idx, ter.residue_name, ter.chain_id, ter.residue_idx
        )
    }

    fn parse_opt_charge(
        value: &str,
        start: usize,
        end: usize,
        line: usize,
    ) -> Result<Option<i8>, Error> {
        #[cfg(feature = "debug")]
        Self::trace_parser(value, start, end);

        let trimmed = value[start..end].trim();
        if trimmed.is_empty() {
            return Ok(None);
        }

        if trimmed.ends_with('+') || trimmed.ends_with('-') {
            trimmed[..trimmed.len() - 1]
                .parse::<i8>()
                .map(|v| Some(v * if trimmed.ends_with('-') { -1 } else { 1 }))
                .map_err(|_source| Error::ExpectedInt { line, start, end })
        } else {
            trimmed
                .parse()
                .map(Some)
                .map_err(|_source| Error::ExpectedInt { line, start, end })
        }
    }

    fn parse_u32(value: &str, start: usize, end: usize, line: usize) -> Result<u32, Error> {
        #[cfg(feature = "debug")]
        Self::trace_parser(value, start, end);

        value[start..end]
            .trim()
            .parse()
            .map_err(|_source| Error::ExpectedInt { line, start, end })
    }

    fn parse_i32(value: &str, start: usize, end: usize, line: usize) -> Result<i32, Error> {
        #[cfg(feature = "debug")]
        Self::trace_parser(value, start, end);

        value[start..end]
            .trim()
            .parse()
            .map_err(|_source| Error::ExpectedInt { line, start, end })
    }

    fn parse_opt_u32(
        value: &str,
        start: usize,
        end: usize,
        line: usize,
    ) -> Result<Option<u32>, Error> {
        #[cfg(feature = "debug")]
        Self::trace_parser(value, start, end);

        if value[start..end].trim() == "" {
            return Ok(None);
        }
        value[start..end]
            .trim()
            .parse()
            .map(Some)
            .map_err(|_source| Error::ExpectedInt { line, start, end })
    }

    fn parse_f32(value: &str, start: usize, end: usize, line: usize) -> Result<f32, Error> {
        #[cfg(feature = "debug")]
        Self::trace_parser(value, start, end);

        value[start..end]
            .trim()
            .parse()
            .map_err(|_source| Error::ExpectedFloat { line, start, end })
    }

    fn parse_str(value: &str, start: usize, end: usize, _line: usize) -> String {
        #[cfg(feature = "debug")]
        Self::trace_parser(value, start, end);

        value[start..end].trim().to_string()
    }

    fn parse_opt_str(value: &str, start: usize, end: usize, _line: usize) -> Option<String> {
        #[cfg(feature = "debug")]
        Self::trace_parser(value, start, end);

        if value[start..end].trim() == "" {
            return None;
        }
        Some(value[start..end].trim().to_string())
    }

    #[cfg(feature = "debug")]
    fn trace_parser(value: &str, start: usize, end: usize) {
        tracing::debug!("{:<80}", value);
        if end > start + 1 {
            tracing::debug!("{:>2$}{:^>3$}", "^", "^", start + 1, end - start - 1);
        } else {
            tracing::debug!("{:>1$}", "^", start + 1);
        }
        tracing::debug!("{:>1$}", &value[start..end], end);
    }
}

pub fn from_pdb(
    pdb_contents: impl AsRef<str>,
    keep_residues: Option<HashSet<String>>,
    skip_residues: Option<HashSet<String>>,
) -> Result<Vec<Conformer>, Error> {
    let mut global_connectivity = Vec::<(u32, u32, u8)>::new();
    let mut conformers = Vec::new();
    let mut conformer_atom_ids = Vec::new();

    let mut lines = pdb_contents.as_ref().lines().enumerate();
    loop {
        let mut topology = Topology::default();

        // Set of amino acid identities. An identity is guaranteed to be unique
        // within a model.
        let mut amino_acid_ids = BTreeSet::new();
        // Mapping of amino acid identities to the type of amino acid.
        let mut amino_acid_seq = BTreeMap::new();
        // Mapping of amino acid identities to a vector of atom indices (referencing
        // the `atoms` vector) that are part of the amino acid.
        let mut amino_acids = BTreeMap::<_, Vec<_>>::new();
        // Mapping of amino acid identities to their sequence identifiers (which are
        // assumed to be the residue number in the PDB).
        // WARN: This is probably not the best way to define sequence identifiers.
        let mut amino_acid_seq_ids = BTreeMap::new();
        let mut amino_acid_insertion_codes = BTreeMap::new();
        let mut amino_acid_labels = BTreeMap::new();

        // Vector of atom identities that zips with the `atoms` vector.
        let mut atom_ids = Vec::new();
        // Vector of atom names. An atom name identifies the element symbol and
        // (optionally) its position within an amino acid.
        let mut atom_labels = Vec::new();
        // Vector of atom symbols that zips with the `atoms` vector.
        let mut atom_symbols = Vec::new();
        // Vector of atom charges that zips with the `atoms` vector.
        let mut atom_formal_charges = Vec::new();
        // Mapping of atom identities to a vector of alternative xyz coordinates for
        // that atom. This does not include the canonical coordinates.
        let mut alts = BTreeMap::<_, Vec<_>>::new();

        // Set of residue identities. An identity is guaranteed to be unique within
        // a model.
        let mut residue_ids = BTreeSet::new();
        // Mapping of residue identities to residue names. A residue name identifies
        // the type of residue (e.g. "LIG" for ligand).
        let mut residue_seq = BTreeMap::new();
        // Mapping of residue identities to a vector of atom indices (referenceing
        // the `atoms` vector) that are part of the residue.
        let mut residues = BTreeMap::<_, Vec<_>>::new();
        let mut residue_seq_ids = BTreeMap::new();
        let mut residue_insertion_codes = BTreeMap::new();
        let mut residue_labels = BTreeMap::new();

        // Mapping of chain identities (a.k.a. subunits and substructures) to a
        // vector of atom indices (referencing the `atoms` vector) that are part of
        // the chain.
        let mut chains = BTreeMap::<_, Vec<_>>::new();

        let mut connectivity = Vec::<(u32, u32, u8)>::new();

        let mut in_model = false;
        let mut eof = false;
        loop {
            // Load the next line and exit from the inner loop if there is no
            // next line. The outer loop with then attempt to finalize the
            // processing of any model that was being built, and then exit the
            // outer loop.
            let line = lines.next();
            if line.is_none() {
                eof = true;
                break;
            }
            let (i, line) = line.unwrap();
            let line = Line::try_from(line, i + 1)?;

            match line {
                Line::Model => {
                    in_model = true;
                }
                Line::EndModel => {
                    break;
                }
                Line::Seqres(_seqres) => {
                    // TODO: The SEQRES should match the stuff that's present,
                    //       but it should also include any gaps in the residues
                    //       as presented in the ATOM lines. Though, it may not
                    //       include atoms at the beginning and end of the
                    //       chain, that is, the first sequence number may not
                    //       be 1, and the last one may not be equal to the
                    //       length of the full chain.
                }
                Line::Atom(atom) => {
                    in_model = true;

                    if let Some(keep_residues) = &keep_residues {
                        if !keep_residues.contains(&atom.residue_name) {
                            continue;
                        }
                    }

                    if let Some(skip_residues) = &skip_residues {
                        if skip_residues.contains(&atom.residue_name) {
                            continue;
                        }
                    }

                    // To have a unique identifier for the residue, we need to
                    // combine:
                    //   - chain ID (indices can reset between chains)
                    //   - the sequence number
                    //   - the insertion code (disambiguates between residues
                    //     with the same sequence number)
                    //   - the residue name (yes, all the above still be the
                    //     same if the residue name differs)
                    //
                    // "Together, columns 23-27 make a sequence ID, which is a
                    //  mostly-numeric ID of the residue position.
                    //
                    //  Note: It's not a full ID of the residue. When you have a
                    //  point mutation (a.k.a. microheterogeneity) you have 2+
                    //  residues with partial occupancy at the same position. To
                    //  fully identify a residue both the sequence ID and
                    //  residue name are needed." ―
                    //  https://bioinformatics.stackexchange.com/a/11590
                    let residue_id = ResidueId {
                        chain_id: atom.chain_id.clone(),
                        sequence_number: atom.sequence_number,
                        insertion_code: atom.residue_insertion.clone().unwrap_or("~".to_string()),
                        residue_name: atom.residue_name.clone(),
                    };

                    match atom.alternate_location.as_deref() {
                        Some("A") | None => {
                            topology.symbols.push(atom.element_symbol.clone());
                            topology.geometry.extend_from_slice(&[
                                atom.atom_x,
                                atom.atom_y,
                                atom.atom_z,
                            ]);

                            match AminoAcid::from_pdb_std_name(&atom.residue_name) {
                                Ok(amino_acid) => {
                                    amino_acid_ids.insert(residue_id.clone());
                                    amino_acid_seq.insert(residue_id.clone(), amino_acid);
                                    amino_acids
                                        .entry(residue_id.clone())
                                        .or_default()
                                        .push((topology.symbols.len() - 1) as u32);
                                    amino_acid_seq_ids
                                        .insert(residue_id.clone(), atom.sequence_number);
                                    amino_acid_insertion_codes.insert(
                                        residue_id.clone(),
                                        atom.residue_insertion.clone().unwrap_or_default(),
                                    );
                                    amino_acid_labels.insert(
                                        residue_id.clone(),
                                        format!(
                                            "{}{}",
                                            atom.sequence_number,
                                            atom.residue_insertion.unwrap_or_default()
                                        ),
                                    );
                                }
                                Err(_) => {
                                    residue_ids.insert(residue_id.clone());
                                    residue_seq.insert(residue_id.clone(), atom.residue_name);
                                    residues
                                        .entry(residue_id.clone())
                                        .or_default()
                                        .push((topology.symbols.len() - 1) as u32);
                                    residue_seq_ids
                                        .insert(residue_id.clone(), atom.sequence_number);
                                    residue_insertion_codes.insert(
                                        residue_id.clone(),
                                        atom.residue_insertion.clone().unwrap_or_default(),
                                    );
                                    residue_labels.insert(
                                        residue_id.clone(),
                                        format!(
                                            "{}{}",
                                            atom.sequence_number,
                                            atom.residue_insertion.unwrap_or_default()
                                        ),
                                    );
                                }
                            }

                            atom_ids.push(atom.atom_idx);
                            atom_labels.push(atom.atom_name);
                            atom_symbols.push(atom.element_symbol);
                            atom_formal_charges.push(atom.charge);
                            // We do not need to push any information. We abuse this
                            // notation to initialise the entry *only* in the instance
                            // that it is not already present.
                            alts.entry(atom.atom_idx).or_default();

                            chains
                                .entry(atom.chain_id)
                                .or_default()
                                .push((atom_labels.len() - 1) as u32);
                        }
                        _ => {
                            alts.entry(atom.atom_idx)
                                .or_default()
                                .push(([atom.atom_x, atom.atom_y, atom.atom_z], atom.charge));
                        }
                    }
                }
                Line::Conect(conect) => {
                    let origin = conect.atom_idxs[0];
                    for target in conect.atom_idxs.into_iter().skip(1) {
                        if in_model {
                            connectivity.push((origin, target, 1));
                        } else {
                            global_connectivity.push((origin, target, 1));
                        }
                    }
                }
                _ => {
                    // TOOD: Support for other lines.
                }
            }
        }

        if !in_model {
            if eof {
                // No model was found and the end of the file was reached. Exit
                // the outer loop.
                break;
            }
            // No model was found but we are not at the end of the file, so we
            // must re-enter the inner loop.
            continue;
        }

        let mut conformer = Conformer {
            topology,
            // NOTE: We are dependent on the BTreeMap visiting its elements in order.
            amino_acid_seq: Some(amino_acid_seq.into_values().collect()),
            // NOTE: We are dependent on the BTreeMap visiting its elements in order.
            amino_acids: Some(amino_acids.into_values().collect()),
            amino_acid_seq_ids: Some(amino_acid_seq_ids.into_values().collect()),
            amino_acid_insertion_codes: Some(amino_acid_insertion_codes.into_values().collect()),
            amino_acid_labels: Some(
                amino_acid_labels
                    .into_values()
                    .enumerate()
                    .map(|(i, label)| Label(i as u32, label))
                    .collect(),
            ),
            // NOTE: We are implicitly dependent on the BTreeSet visiting its elements in order.
            residue_seq: Some(residue_seq.into_values().collect()),
            residue_seq_ids: Some(residue_seq_ids.into_values().collect()),
            residue_insertion_codes: Some(residue_insertion_codes.into_values().collect()),
            residue_labels: Some(
                residue_labels
                    .into_values()
                    .enumerate()
                    .map(|(i, label)| Label(i as u32, label))
                    .collect(),
            ),
            // NOTE: We are implicitly dependent on the BTreeSet visiting its elements in order.
            residues: Some(residues.into_values().collect()),
            subunits: Some(chains.into_values().collect()),
        };

        conformer.topology.atom_labels = Some(atom_labels);

        // We store amino acids as the "default" fragments so that we
        // can generalize fast implicit connectvity searches
        conformer.topology.fragments = Some(
            conformer
                .amino_acids
                .clone()
                .unwrap()
                .into_iter()
                .chain(conformer.residues.clone().unwrap().into_iter())
                .collect(),
        );

        let mut connectivity_deduper = BTreeMap::<(usize, usize), u8>::new();
        for (origin, target, order) in connectivity {
            let (origin, _) = atom_ids
                .iter()
                .find_position(|x| *x == &origin)
                .ok_or(Error::InvalidConnection { atom_idx: origin })?;
            let (target, _) = atom_ids
                .iter()
                .find_position(|x| *x == &target)
                .ok_or(Error::InvalidConnection { atom_idx: target })?;

            if connectivity_deduper.contains_key(&(target, origin)) {
                // Dedup CONECT records are that entered in reverse, because this it
                // is common for PDBs to describe one bond in both directions.
                continue;
            }
            match connectivity_deduper.get_mut(&(origin, target)) {
                Some(order) => {
                    // However, if the bond is explicitly entered twice in the same
                    // direction, this usually signifies that the bond is a double
                    // bond.
                    order.add_assign(1);
                }
                None => {
                    connectivity_deduper.insert((origin, target), order);
                }
            }
        }
        conformer.topology.connectivity = Some(
            connectivity_deduper
                .into_iter()
                .map(|((i, j), order)| Bond(i.min(j) as u32, i.max(j) as u32, order))
                .collect::<Vec<_>>(),
        );

        conformer.topology.fragment_charges = Some(
            conformer
                .amino_acids
                .iter()
                .flatten()
                .chain(conformer.residues.iter().flatten())
                .enumerate()
                .map(|(_, atoms)| {
                    atoms
                        .iter()
                        .map(|i| {
                            *atom_formal_charges
                                .get(*i as usize)
                                .expect("atom charges should zip with atoms")
                                as isize
                        })
                        .sum::<isize>() as i8
                })
                .collect(),
        );

        // Add atom charges
        conformer.topology.atom_charges = Some(atom_formal_charges);

        // Add the alts to the topology.
        let alts = alts
            .into_iter()
            .map(|(i, is)| {
                Alt(
                    i,
                    is.into_iter()
                        .map(|(xyz, atom_charge)| {
                            let alt_i = conformer.topology.symbols.len();
                            conformer
                                .topology
                                .symbols
                                .push(conformer.topology.symbols[i as usize].clone());
                            conformer.topology.geometry.push(xyz[0]);
                            conformer.topology.geometry.push(xyz[1]);
                            conformer.topology.geometry.push(xyz[2]);
                            if let Some(atom_charges) = &mut conformer.topology.atom_charges {
                                atom_charges.push(atom_charge);
                            } else {
                                panic!("cannot have alternate charges without charges");
                            }
                            alt_i as u32
                        })
                        .collect_vec(),
                )
            })
            .collect();
        conformer.topology.alts = Some(alts);

        // Store the model alongside the metadata required for parsing global
        // connectivity information
        conformers.push(conformer);
        conformer_atom_ids.push(atom_ids);

        if eof {
            break;
        }
    }

    // CONECT records can appear outside of model definitions even in PDBs that
    // define multiple models. The only reasonable interpretation is that these
    // CONECT records apply to all models.
    for (conformer, atom_ids) in conformers.iter_mut().zip(conformer_atom_ids.iter()) {
        let mut connectivity_deduper = HashMap::<(usize, usize), u8>::new();
        for (origin, target, order) in global_connectivity.iter() {
            let (origin, _) = atom_ids
                .iter()
                .find_position(|x| *x == origin)
                .ok_or(Error::InvalidConnection { atom_idx: *origin })?;
            let (target, _) = atom_ids
                .iter()
                .find_position(|x| *x == target)
                .ok_or(Error::InvalidConnection { atom_idx: *target })?;

            if connectivity_deduper.contains_key(&(target, origin)) {
                // Dedup CONECT records are that entered in reverse, because this it
                // is common for PDBs to describe one bond in both directions.
                continue;
            }
            match connectivity_deduper.get_mut(&(origin, target)) {
                Some(order) => {
                    // However, if the bond is explicitly entered twice in the same
                    // direction, this usually signifies that the bond is a double
                    // bond.
                    order.add_assign(1);
                }
                None => {
                    connectivity_deduper.insert((origin, target), *order);
                }
            }
        }
        let additional_connectivity = connectivity_deduper
            .iter()
            .map(|((i, j), order)| Bond(*i.min(j) as u32, *i.max(j) as u32, *order))
            .collect::<Vec<_>>();
        match &mut conformer.topology.connectivity {
            Some(connectivity) => {
                connectivity.extend(additional_connectivity);
            }
            None => {
                conformer.topology.connectivity = Some(additional_connectivity);
            }
        }
    }

    Ok(conformers)
}

pub fn to_pdb(conformer: Conformer) -> String {
    let mut pdb = String::new();

    let mut atom_idx_to_chain_id = HashMap::new();
    for (i, subunit) in conformer
        .subunits
        .unwrap_or_default()
        .into_iter()
        .enumerate()
    {
        for atom_idx in subunit {
            atom_idx_to_chain_id.insert(atom_idx, i);
        }
    }

    let mut amino_acid_i_to_label = HashMap::new();
    if let Some(amino_acid_labels) = &conformer.amino_acid_labels {
        for Label(i, label) in amino_acid_labels {
            amino_acid_i_to_label.insert(*i, label.clone());
        }
    }

    let mut residue_i_to_label = HashMap::new();
    if let Some(residue_labels) = &conformer.residue_labels {
        for Label(i, label) in residue_labels {
            residue_i_to_label.insert(*i, label.clone());
        }
    }

    if let (
        Some(amino_acids),
        Some(amino_acid_seq),
        Some(amino_acid_seq_ids),
        Some(amino_acid_labels),
    ) = (
        conformer.amino_acids,
        conformer.amino_acid_seq,
        conformer.amino_acid_seq_ids,
        conformer.amino_acid_labels,
    ) {
        assert_eq!(amino_acids.len(), amino_acid_seq.len());
        assert_eq!(amino_acids.len(), amino_acid_seq_ids.len());
        assert_eq!(amino_acids.len(), amino_acid_labels.len());

        for i in 0..amino_acids.len() {
            for atom_idx in &amino_acids[i] {
                let atom = Atom {
                    atom_idx: *atom_idx,
                    atom_name: conformer
                        .topology
                        .atom_labels
                        .as_ref()
                        .and_then(|atom_labels| atom_labels.get(*atom_idx as usize).cloned())
                        .or_else(|| conformer.topology.symbols.get(*atom_idx as usize).cloned())
                        .unwrap_or_default(),
                    alternate_location: None, // TODO: Support altlocs
                    residue_name: amino_acid_seq[i].to_pdb_std_name().to_string(),
                    chain_id: format!(
                        "{}",
                        (atom_idx_to_chain_id
                            .get(atom_idx)
                            .cloned()
                            .unwrap_or_default() as u8
                            + 65) as char
                    ),
                    sequence_number: amino_acid_seq_ids[i],
                    residue_insertion: Some(
                        conformer
                            .amino_acid_insertion_codes
                            .as_ref()
                            .and_then(|xs| xs.get(i))
                            .cloned()
                            .unwrap_or("".to_string()),
                    ),
                    atom_x: conformer.topology.geometry[3 * *atom_idx as usize],
                    atom_y: conformer.topology.geometry[3 * *atom_idx as usize + 1],
                    atom_z: conformer.topology.geometry[3 * *atom_idx as usize + 2],
                    occupancy: 1.0, // TODO: Support altlocs
                    temperature_factor: 0.0,
                    segment_id: None,
                    element_symbol: conformer.topology.symbols[*atom_idx as usize].clone(),
                    charge: conformer
                        .topology
                        .atom_charges
                        .as_ref()
                        .and_then(|atom_charges| atom_charges.get(*atom_idx as usize).cloned())
                        .unwrap_or_default(),
                    is_het_atom: false,
                };

                pdb += &format!("{}\n", Line::Atom(atom));
            }
        }
    }

    if let (Some(residues), Some(residue_seq), Some(residue_seq_ids), Some(residue_labels)) = (
        conformer.residues,
        conformer.residue_seq,
        conformer.residue_seq_ids,
        conformer.residue_labels,
    ) {
        assert_eq!(residues.len(), residue_seq.len());
        assert_eq!(residues.len(), residue_seq_ids.len());
        assert_eq!(residues.len(), residue_labels.len());

        for i in 0..residues.len() {
            for atom_idx in &residues[i] {
                let atom = Atom {
                    atom_idx: *atom_idx,
                    atom_name: conformer
                        .topology
                        .atom_labels
                        .as_ref()
                        .and_then(|atom_labels| atom_labels.get(*atom_idx as usize).cloned())
                        .or_else(|| conformer.topology.symbols.get(*atom_idx as usize).cloned())
                        .unwrap_or_default(),
                    alternate_location: None, // TODO: Support altlocs
                    residue_name: residue_seq[i].clone(),
                    chain_id: format!(
                        "{}",
                        (atom_idx_to_chain_id
                            .get(atom_idx)
                            .cloned()
                            .unwrap_or_default() as u8
                            + 65) as char
                    ),
                    sequence_number: residue_seq_ids[i],
                    residue_insertion: Some(
                        conformer
                            .residue_insertion_codes
                            .as_ref()
                            .and_then(|xs| xs.get(i))
                            .cloned()
                            .unwrap_or("".to_string()),
                    ),
                    atom_x: conformer.topology.geometry[3 * *atom_idx as usize],
                    atom_y: conformer.topology.geometry[3 * *atom_idx as usize + 1],
                    atom_z: conformer.topology.geometry[3 * *atom_idx as usize + 2],
                    occupancy: 1.0, // TODO: Support altlocs
                    temperature_factor: 0.0,
                    segment_id: None,
                    element_symbol: conformer.topology.symbols[*atom_idx as usize].clone(),
                    charge: conformer
                        .topology
                        .atom_charges
                        .as_ref()
                        .and_then(|atom_charges| atom_charges.get(*atom_idx as usize).cloned())
                        .unwrap_or_default(),
                    is_het_atom: true,
                };

                pdb += &format!("{}\n", Line::Atom(atom));
            }
        }
    }

    for bond in conformer.topology.connectivity.unwrap_or_default() {
        // for _ in 0..bond.2 {
        pdb += &format!(
            "{}\n",
            Line::Conect(Conect {
                atom_idxs: vec![bond.0, bond.1],
            })
        );
        // }
    }

    pdb
}

#[cfg(all(feature = "serde", feature = "graphql"))]
#[cfg(test)]
mod tests {
    use std::{
        fs::File,
        io::Write,
        {env, error},
    };

    use petgraph::dot::Dot;
    use serde_json;
    use tracing_subscriber::prelude::*;
    use tracing_subscriber::EnvFilter;

    use crate::{amino_acid::AminoAcid, pdb::from_pdb, test, Conformer};

    use super::to_pdb;

    //#[cfg(feature = "serde")]
    #[test]
    fn test_to_protein() -> anyhow::Result<()> {
        // TODO: test multiple pdb files
        //let pdb = read(Path::new("./tests/data/akt1_active_complex_last_frame.pdb"))?;
        // let pdb = read(Path::new(
        //     "./tests/data/hivpr_active_complex_last_frame.pdb",
        // ))?;

        let pdb = crate::test::data::pdb_1fcx::FILE;
        let mut parsed = super::from_pdb(pdb, None, None)?[0].clone();
        parsed.topology.connectivity = Some(parsed.topology.implicit_connectivity(0.0));
        let fragmented = parsed.fragment(10, None);
        parsed.topology.fragments = Some(fragmented);
        assert!(
            parsed.topology.geometry.len() == 3 * parsed.topology.symbols.len(),
            "{} != {}",
            parsed.topology.geometry.len(),
            3 * parsed.topology.symbols.len()
        );
        assert!(
            parsed.topology.atom_labels.clone().unwrap().len() == parsed.topology.symbols.len()
        );

        for (id, xyz) in parsed
            .topology
            .to_xyz_format_fragments()
            .unwrap()
            .iter()
            .enumerate()
        {
            let mut file = File::create(format!("/tmp/{id}_fragment.xyz")).unwrap();

            write!(file, "{xyz}")?;
        }

        let mut file = File::create("/tmp/whole_mol.xyz").unwrap();

        write!(file, "{}", parsed.topology.to_xyz_format())?;

        let mut dotfile = File::create("/tmp/whole_mol.dot").unwrap();

        write!(dotfile, "{:?}", Dot::new(&parsed.topology.to_graph()))?;

        parsed.topology.fragment_charges = parsed
            .substructure_charges(true)
            .0
            .map(|x| x.iter().map(|x| *x as i8).collect());

        let mut file = File::create("/tmp/test_topology.json").unwrap();

        write!(file, "{}", serde_json::to_string_pretty(&parsed.topology)?)?;

        Ok(())
    }

    #[test]
    fn load_4hhb() -> Result<(), Box<dyn error::Error>> {
        tracing_subscriber::registry()
            .with(EnvFilter::new(env::var("TRACE").unwrap_or_default()))
            .with(tracing_subscriber::fmt::layer())
            .init();

        // Load the PDB from the test string.
        let pdb = test::data::pdb_4hhb::FILE;
        let complex = super::from_pdb(pdb, None, None)?[0].clone();

        // Assert expected sizes for the topology.
        let n_expected_symbols = 4779;
        let n_expected_geometry = 3 * n_expected_symbols;
        assert_eq!(
            complex.topology.symbols.len(),
            n_expected_symbols,
            "expected {n_expected_symbols} symbols"
        );
        assert_eq!(
            complex.topology.geometry.len(),
            n_expected_geometry,
            "expected {n_expected_geometry} geometry coords"
        );

        // Assert expected sizes for the amino acids.
        let n_expected_amino_acids = 574;
        let n_expected_amino_acid_atoms = 4384;
        assert_eq!(
            complex.amino_acid_seq.clone().unwrap().len(),
            n_expected_amino_acids,
            "expected {n_expected_amino_acids} amino acids"
        );
        assert_eq!(
            complex.amino_acids.clone().unwrap().len(),
            complex.amino_acid_seq.clone().unwrap().len(),
            "expected amino acid atoms to match amino acids"
        );
        assert_eq!(
            complex
                .amino_acids
                .clone()
                .unwrap()
                .iter()
                .fold(0, |accum, atoms| accum + atoms.len()),
            n_expected_amino_acid_atoms,
            "expected {n_expected_amino_acid_atoms} amino acid atoms"
        );

        // Assert expected sizes for the atoms.
        assert_eq!(
            complex.topology.atom_labels.clone().unwrap().len(),
            n_expected_symbols,
            "expected atom names to match topology"
        );

        // Assert the expected sizes for the residues.
        let n_expected_residues = 227;
        let n_expected_residue_atoms = 395;
        assert_eq!(
            complex.residue_seq.clone().unwrap().len(),
            n_expected_residues,
            "expected {n_expected_residues} residues"
        );
        assert_eq!(
            complex.residues.clone().unwrap().len(),
            complex.residue_seq.unwrap().len(),
            "expected residue atoms to match residues"
        );
        assert_eq!(
            complex
                .residues
                .clone()
                .unwrap()
                .iter()
                .fold(0, |accum, atoms| accum + atoms.len()),
            n_expected_residue_atoms,
            "expected {n_expected_residue_atoms} residue atoms"
        );

        let subunits = complex.subunits.clone().unwrap();
        // Assert the expected sizes for the subunits.
        let n_expected_subunits = 4;
        assert_eq!(
            subunits.len(),
            n_expected_subunits,
            "expected {n_expected_subunits} subunits"
        );
        assert_eq!(
            complex
                .subunits
                .clone()
                .unwrap()
                .iter()
                .fold(0, |accum, subunit| accum + subunit.len()),
            n_expected_symbols,
            "expected {n_expected_symbols} subunit atoms"
        );
        assert_eq!(
            subunits[0].len(),
            1168,
            "expected 1168 atoms in the 1st subunit"
        );
        assert_eq!(
            subunits[1].len(),
            1224,
            "expected 1224 atoms in the 2nd subunit"
        );
        assert_eq!(
            subunits[2].len(),
            1171,
            "expected 1171 atoms in the 3rd subunit"
        );
        assert_eq!(
            subunits[3].len(),
            1216,
            "expected 1216 atoms in the 4th subunit"
        );

        // Assert the values of some atoms.
        assert_eq!(
            complex.topology.symbols[0], "N",
            "expected first atom to be N"
        );
        assert_eq!(
            complex.topology.geometry[..3],
            [6.204, 16.869, 4.854],
            "expected first atom to be at x=6.204, y=16.869, z=4.854"
        );
        assert_eq!(
            complex.topology.symbols[complex.topology.symbols.len() - 1],
            "O",
            "expected last atom to be O"
        );
        assert_eq!(
            complex.topology.geometry[complex.topology.geometry.len() - 3..],
            [-1.263, -2.837, -21.251],
            "expected first atom to be at x=-1.263, y=-2.837, z=-21.251"
        );

        // Assert the value of some residues.
        assert_eq!(
            complex.amino_acid_seq.unwrap()[0],
            AminoAcid::VAL,
            "expected first amino acid to be VAL"
        );
        assert_eq!(
            complex.amino_acids.unwrap()[0],
            [0, 1, 2, 3, 4, 5, 6],
            "expected first amino acid to contain atoms 0, 1, 2, 3, 4, 5, and 6"
        );

        Ok(())
    }

    #[test]
    fn test_to_pdb() {
        let isoprophyl: Conformer = serde_json::from_str(
            r#"
{"topology":
{"symbols":["C","C","C","O","H","H","H","H","H","H","H","H"],
"geometry":[-0.622,1.298,0.111,0.01,-0.007,-0.379,1.459,-0.085,0.105,-0.726,-1.116,0.138,-0.06,2.145,-0.284,-1.654,1.354,-0.234,-0.601,1.325,1.2,-0.011,-0.033,-1.469,1.48,-0.058,1.195,1.909,-1.014,-0.244,2.021,0.762,-0.289,-1.655,-1.131,-0.129],
"connectivity":[[0,1,1],[0,4,1],[0,5,1],[0,6,1],[1,2,1],[1,3,1],[1,7,1],[2,8,1],[2,9,1],[2,10,1],[3,11,1]],
"atom_charges":[0,0,0,0,0,0,0,0,0,0,0,0],"fragments":[[0,1,2,3,4,5,6,7,8,9,10,11]],
"fragment_charges":[0]},
"residues":[[0,1,2,3,4,5,6,7,8,9,10,11]],"residue_seq":["LIG"],
"residue_seq_ids": [0],
"residue_labels":[[0,"IPA"]],
"residue_insertion_codes": [""]}

    "#,
        )
        .unwrap();

        let parsed_pdb1 = from_pdb(to_pdb(isoprophyl), None, None).unwrap();
        assert_eq!(parsed_pdb1.len(), 1);

        let parsed_pdb2 = from_pdb(to_pdb(parsed_pdb1[0].clone()), None, None).unwrap();
        assert_eq!(parsed_pdb2.len(), 1);

        assert_eq!(parsed_pdb1[0], parsed_pdb2[0]);
    }
}
