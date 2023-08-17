use crate::bond;
use crate::conformer::{Conformer, Label};
use std::collections::HashMap;

#[derive(Debug)]
struct Atom {
    x: f64,
    y: f64,
    z: f64,
    symbol: String,
    _mass_difference: i32,
    charge: i32,
    _atom_atom_mapping_number: Option<u32>,
}

#[derive(Debug)]
struct Bond {
    atom1: usize,
    atom2: usize,
    bond_type: u32,
    _bond_stereo: u32,
}

#[derive(Debug)]
struct Molecule {
    name: String,
    atoms: Vec<Atom>,
    bonds: Vec<Bond>,
    associated_data: HashMap<String, String>,
}

#[derive(Debug, Copy, Clone)]
pub enum SDFParseState {
    HeaderBlock,
    CountsLine,
    AtomBlock,
    BondBlock,
    PropertiesBlock,
    DataItems,
}

impl std::fmt::Display for SDFParseState {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        use SDFParseState::*;

        match self {
            HeaderBlock => write!(f, "HeaderBlock"),
            CountsLine => write!(f, "CountsLine"),
            AtomBlock => write!(f, "AtomBlock"),
            BondBlock => write!(f, "BondBlock"),
            PropertiesBlock => write!(f, "PropertiesBlock"),
            DataItems => write!(f, "DataItems"),
        }
    }
}

#[derive(Debug, Copy, Clone)]
pub enum SDFPropertyType {
    Charge,
    End,
}

impl std::fmt::Display for SDFPropertyType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        use SDFPropertyType::*;

        match self {
            Charge => write!(f, "CHG"),
            End => write!(f, "END"),
        }
    }
}

impl std::str::FromStr for SDFPropertyType {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        use SDFPropertyType::*;

        match s {
            "CHG" => Ok(Charge),
            "END" => Ok(End),
            _ => Err(()),
        }
    }
}

#[derive(Debug, Copy, Clone, thiserror::Error)]
pub enum SDFErrorType {
    FormatCharge,
    HeaderLine,
    ParseNumAtoms,
    ParseNumBonds,
    ParseX,
    ParseY,
    ParseZ,
    ParseCharge,
    ParseAtomAtomMappingNumber,
    ParseBondAtom1,
    ParseBondAtom2,
    ParseBondType,
    ParsePropertyType,
    ParsePropertyCHGCount,
    ParsePropertyCHGIndex,
    ParsePropertyCHGCharge,
    PropertyCHGCount,
    PropertyCHGIndex,
    PropertyCHGCharge,
    ParseDataKey,
}

impl std::fmt::Display for SDFErrorType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        use SDFErrorType::*;

        match self {
            FormatCharge => write!(f, "could not format charge"),
            HeaderLine => write!(f, "missing header line"),
            ParseNumAtoms => write!(f, "could not parse number of atoms"),
            ParseNumBonds => write!(f, "could not parse number of bonds"),
            ParseX => write!(f, "could not parse x coordinate"),
            ParseY => write!(f, "could not parse y coordinate"),
            ParseZ => write!(f, "could not parse z coordinate"),
            ParseCharge => write!(f, "could not parse charge"),
            ParseAtomAtomMappingNumber => write!(f, "could not parse atom-atom mapping number"),
            ParseBondAtom1 => write!(f, "could not parse first bond atom index"),
            ParseBondAtom2 => write!(f, "could not parse second bond atom index"),
            ParseBondType => write!(f, "could not parse bond type"),
            ParsePropertyType => write!(f, "could not parse property type"),
            ParsePropertyCHGCount => write!(f, "could not parse CHG count"),
            ParsePropertyCHGIndex => write!(f, "could not parse CHG index"),
            ParsePropertyCHGCharge => write!(f, "could not parse CHG charge"),
            PropertyCHGCount => write!(f, "HG count out of range"),
            PropertyCHGIndex => write!(f, "CHG index out of range"),
            PropertyCHGCharge => write!(f, "CHG charge out of range"),
            ParseDataKey => write!(f, "could not parse data item key"),
        }
    }
}

#[derive(Debug)]
pub struct SDFParseError {
    line_number: usize,
    state: SDFParseState,
    ty: SDFErrorType,
}

impl std::fmt::Display for SDFParseError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "line {} state {}: {}",
            self.line_number, self.state, self.ty
        )
    }
}

impl std::error::Error for SDFParseError {}

fn charge_field_to_charge(c: i32) -> Option<i32> {
    match c {
        0 => Some(0),
        1 => Some(3),
        2 => Some(2),
        3 => Some(1),
        // TODO: This apparently represents a "doublet radical", but I don't know what we want to
        // do aobut this.
        4 => unimplemented!(),
        5 => Some(-1),
        6 => Some(-2),
        7 => Some(-3),
        _ => None,
    }
}

fn charge_to_charge_field(c: Option<i8>) -> Result<i32, SDFErrorType> {
    Ok(match c {
        Some(0) => 0,
        Some(3) => 1,
        Some(2) => 2,
        Some(1) => 3,
        Some(-1) => 5,
        Some(-2) => 6,
        Some(-3) => 7,
        _ => {
            return Err(SDFErrorType::FormatCharge);
        }
    })
}

fn parse_sdf(content: &str) -> Result<Vec<Molecule>, SDFParseError> {
    use SDFErrorType::*;
    use SDFParseState::*;

    let mut state = SDFParseState::HeaderBlock;
    let mut seen_chg_property = false;

    let mut molecules: Vec<Molecule> = Vec::new();

    let mut lines = content.lines().enumerate();

    while let Some((line_number, line)) = lines.next() {
        if line.trim().is_empty() {
            continue; // Handle empty lines
        }

        let line_number = line_number + 1;

        match state {
            HeaderBlock => {
                molecules.push(Molecule {
                    name: line.to_string(),
                    atoms: Vec::new(),
                    bonds: Vec::new(),
                    associated_data: HashMap::<String, String>::new(),
                });

                lines.next().ok_or(SDFParseError {
                    line_number: line_number + 1,
                    state,
                    ty: HeaderLine,
                })?;
                lines.next().ok_or(SDFParseError {
                    line_number: line_number + 2,
                    state,
                    ty: HeaderLine,
                })?;

                state = CountsLine;
            }
            CountsLine => {
                let num_atoms: usize = line[..3].trim().parse().map_err(|_| SDFParseError {
                    line_number,
                    state,
                    ty: ParseNumAtoms,
                })?;
                let num_bonds: usize = line[3..6].trim().parse().map_err(|_| SDFParseError {
                    line_number,
                    state,
                    ty: ParseNumBonds,
                })?;

                molecules.last_mut().unwrap().atoms.reserve(num_atoms);
                molecules.last_mut().unwrap().bonds.reserve(num_bonds);

                state = AtomBlock;
            }
            AtomBlock => {
                molecules.last_mut().unwrap().atoms.push(Atom {
                    x: line[..10].trim().parse().map_err(|_| SDFParseError {
                        line_number,
                        state,
                        ty: ParseX,
                    })?,
                    y: line[10..20].trim().parse().map_err(|_| SDFParseError {
                        line_number,
                        state,
                        ty: ParseY,
                    })?,
                    z: line[20..30].trim().parse().map_err(|_| SDFParseError {
                        line_number,
                        state,
                        ty: ParseZ,
                    })?,
                    symbol: line[30..34].trim().to_string(),
                    _mass_difference: line[34..36].trim().parse().unwrap_or(0),
                    charge: line[36..39]
                        .trim()
                        .parse()
                        .map_err(|_| SDFParseError {
                            line_number,
                            state,
                            ty: ParseZ,
                        })
                        .map(|c| {
                            charge_field_to_charge(c).ok_or(SDFParseError {
                                line_number,
                                state,
                                ty: ParseZ,
                            })
                        })??,
                    _atom_atom_mapping_number: {
                        if line.len() < 57 {
                            None
                        } else {
                            let substr = line[54..57].trim();
                            if !substr.is_empty() {
                                let index: u32 = substr.parse().map_err(|_| SDFParseError {
                                    line_number,
                                    state,
                                    ty: ParseAtomAtomMappingNumber,
                                })?;
                                if index != 0 {
                                    panic!("unimplemented");
                                }
                            }

                            None
                        }
                    },
                });

                if molecules.last().unwrap().atoms.len()
                    == molecules.last().unwrap().atoms.capacity()
                {
                    state = BondBlock;
                }
            }
            BondBlock => {
                molecules.last_mut().unwrap().bonds.push(Bond {
                    atom1: line[..3]
                        .trim()
                        .parse()
                        .map_err(|_| SDFParseError {
                            line_number,
                            state,
                            ty: ParseBondAtom1,
                        })
                        .map(|index: usize| index - 1)?,
                    atom2: line[3..6]
                        .trim()
                        .parse()
                        .map_err(|_| SDFParseError {
                            line_number,
                            state,
                            ty: ParseBondAtom2,
                        })
                        .map(|index: usize| index - 1)?,
                    bond_type: line[6..9].trim().parse().map_err(|_| SDFParseError {
                        line_number,
                        state,
                        ty: ParseBondType,
                    })?,
                    _bond_stereo: line[9..12].trim().parse().unwrap_or(0),
                });

                if molecules.last().unwrap().bonds.len()
                    == molecules.last().unwrap().bonds.capacity()
                {
                    state = PropertiesBlock;
                }
            }
            PropertiesBlock => {
                let property_type: SDFPropertyType =
                    line[3..6].trim().parse().map_err(|_| SDFParseError {
                        line_number,
                        state,
                        ty: ParsePropertyType,
                    })?;

                match property_type {
                    SDFPropertyType::Charge => {
                        if !seen_chg_property {
                            if let Some(molecule) = molecules.last_mut() {
                                molecule.atoms.iter_mut().for_each(|atom| atom.charge = 0)
                            }

                            seen_chg_property = true;
                        }
                        // apparently, the count block is 6..9 in some standards, and 6..8 in others
                        // lets determine this by checking if 9 is a space or not
                        let count_end = if line[8..9].trim().is_empty() { 8 } else { 9 };

                        let count: u32 =
                            line[6..count_end]
                                .trim()
                                .parse()
                                .map_err(|_| SDFParseError {
                                    line_number,
                                    state,
                                    ty: ParsePropertyCHGCount,
                                })?;

                        if count == 0 || count > 8 {
                            return Err(SDFParseError {
                                line_number,
                                state,
                                ty: PropertyCHGCount,
                            });
                        }

                        for i in 0..count {
                            let start = count_end + 8 * i as usize;
                            let end = count_end + 4 + 8 * i as usize;

                            let index: u32 =
                                line[start..end].trim().parse().map_err(|_| SDFParseError {
                                    line_number,
                                    state,
                                    ty: ParsePropertyCHGIndex,
                                })?;

                            let start = count_end + 4 + 8 * i as usize;
                            let end = count_end + 8 + 8 * i as usize;

                            let charge: i32 =
                                line[start..end].trim().parse().map_err(|_| SDFParseError {
                                    line_number,
                                    state,
                                    ty: ParsePropertyCHGCharge,
                                })?;

                            molecules.last_mut().unwrap().atoms[index as usize - 1].charge = charge;
                        }
                    }
                    SDFPropertyType::End => state = DataItems,
                }
            }
            DataItems => {
                if line == "$$$$" {
                    state = HeaderBlock;
                    seen_chg_property = false;
                } else {
                    if !line.starts_with('>') {
                        return Err(SDFParseError {
                            line_number,
                            state,
                            ty: ParseDataKey,
                        });
                    }

                    // Associated data entry.
                    let start = line.find('<').ok_or(SDFParseError {
                        line_number,
                        state,
                        ty: ParseDataKey,
                    })?;
                    let offset = line[start..].find('>').ok_or(SDFParseError {
                        line_number,
                        state,
                        ty: ParseDataKey,
                    })?;

                    let key = line[start + 1..start + offset].to_string();
                    if let Some((_, line)) = lines.next() {
                        let value = line.trim().to_string();
                        molecules
                            .last_mut()
                            .unwrap()
                            .associated_data
                            .insert(key, value);

                        lines.next();
                    }
                }
            }
        }
    }

    Ok(molecules)
}

pub fn from_sdf(content: &str) -> Result<Vec<Conformer>, SDFParseError> {
    Ok(parse_sdf(content)?
        .into_iter()
        .map(|molecule| {
            let mut conformer = Conformer {
                residues: Some(vec![molecule
                    .atoms
                    .iter()
                    .enumerate()
                    .map(|(i, _)| i as u32)
                    .collect()]),
                residue_labels: Some(vec![Label(0, molecule.name)]),
                residue_seq: Some(vec!["LIG".to_string()]),
                ..Default::default()
            };

            conformer.topology.fragments = conformer.residues.clone();

            conformer.topology.connectivity = Some(vec![]);
            for bond in molecule.bonds {
                if let Some(x) = conformer.topology.connectivity.as_mut() {
                    x.push(bond::Bond(
                        (bond.atom1 + conformer.topology.symbols.len()) as u32,
                        (bond.atom2 + conformer.topology.symbols.len()) as u32,
                        bond.bond_type as u8,
                    ))
                }
            }

            conformer.topology.atom_charges = Some(
                molecule
                    .atoms
                    .iter()
                    .map(|atom| atom.charge as i8)
                    .collect(),
            );

            conformer.topology.fragment_charges = conformer.topology.explicit_fragment_charges();

            conformer.topology.geometry = molecule
                .atoms
                .iter()
                .flat_map(|atom| [atom.x as f32, atom.y as f32, atom.z as f32])
                .collect();

            conformer.topology.symbols =
                molecule.atoms.into_iter().map(|atom| atom.symbol).collect();

            conformer
        })
        .collect())
}

/// Convert a Complex to a SDF file
pub fn to_sdf(c: &Conformer) -> Result<String, SDFErrorType> {
    let mut sdf = String::new();
    for (i, _) in c.residues.as_ref().unwrap().iter().enumerate() {
        sdf.push_str(&format!(
            "{}\n     QDXF           3D\n\n",
            c.residue_labels.as_ref().unwrap()[i].1
        ));
        sdf.push_str(&format!(
            " {} {}  0  0  0  0  0  0  0  0999 V2000\n",
            c.topology.symbols.len(),
            c.topology.connectivity.as_ref().unwrap().len()
        ));
        for (j, atom) in c.topology.symbols.iter().enumerate() {
            sdf.push_str(&format!(
                "{:10.4}{:10.4}{:10.4} {:3} 0  {}  0  0  0  0  0  0  0  0  0  0\n",
                c.topology.geometry[3 * j],
                c.topology.geometry[3 * j + 1],
                c.topology.geometry[3 * j + 2],
                atom,
                charge_to_charge_field(c.topology.atom_charges.as_ref().map(|x| x[j]))?,
            ));
        }

        for con in c.topology.connectivity.as_ref().unwrap().iter() {
            sdf.push_str(&format!("{:3}{:3}{:3}  0\n", con.0 + 1, con.1 + 1, con.2));
        }
        // do charge properties
        // After the M  CHG, the first number defines the number of charges defined on this line (up to 8).
        // If the compound has more than this, they can go on additional M  CHG lines.
        // Each charge entry consists of two four-character fields -
        // the first is the index of the charged atom (starting from one), and the second is the charge.
        // The below means "add a charge to the first atom of +2".
        // M  CHG  1   1   2
        let charges = c.topology.atom_charges.as_ref().map(|x| {
            x.chunks(8)
                .enumerate()
                .map(|(i, x)| {
                    let mut s = format!("M  CHG{:3}", x.len());
                    for (j, charge) in x.iter().enumerate() {
                        s.push_str(&format!("{:4}{:4}", (i * 8) + j + 1, charge));
                    }
                    s
                })
                .collect::<Vec<_>>()
        });
        if let Some(charges) = charges {
            for charge in charges {
                sdf.push_str(&format!("{charge}\n"));
            }
        }

        sdf.push_str("M  END\n$$$$"); // The 'M END' marker is added to signify the end of an SDF record
    }
    Ok(sdf)
}

#[cfg(test)]
mod tests {
    use crate::test;

    use super::{from_sdf, to_sdf};

    #[test]
    fn parse_basic_ligand_1() -> Result<(), Box<dyn std::error::Error>> {
        let input_contents = crate::test::data::sdf_1a30_ligand()?;

        let molecules = super::parse_sdf(&input_contents)?;

        assert_eq!(molecules.len(), 1);

        let molecule = &molecules[0];

        assert_eq!(molecule.atoms.len(), 49);
        assert_eq!(molecule.bonds.len(), 48);

        assert_eq!(molecule.atoms[0].x, 4.8410);
        assert_eq!(molecule.atoms[0].y, 27.5760);
        assert_eq!(molecule.atoms[0].z, 5.3100);
        assert_eq!(molecule.atoms[0].symbol, "N");
        assert_eq!(molecule.atoms[0]._mass_difference, 0);
        assert_eq!(molecule.atoms[0].charge, 1);

        assert_eq!(molecule.atoms[20].x, 13.7840);
        assert_eq!(molecule.atoms[20].y, 23.4420);
        assert_eq!(molecule.atoms[20].z, 4.1920);
        assert_eq!(molecule.atoms[20].symbol, "O");
        assert_eq!(molecule.atoms[20]._mass_difference, 0);
        assert_eq!(molecule.atoms[20].charge, 0);

        assert_eq!(molecule.atoms[48].x, 8.4734);
        assert_eq!(molecule.atoms[48].y, 21.6232);
        assert_eq!(molecule.atoms[48].z, 2.6515);
        assert_eq!(molecule.atoms[48].symbol, "H");
        assert_eq!(molecule.atoms[48]._mass_difference, 0);
        assert_eq!(molecule.atoms[48].charge, 0);

        assert_eq!(molecule.bonds[0].atom1, 2);
        assert_eq!(molecule.bonds[0].atom2, 1);
        assert_eq!(molecule.bonds[0].bond_type, 1);
        assert_eq!(molecule.bonds[0]._bond_stereo, 0);

        assert_eq!(molecule.bonds[18].atom1, 21);
        assert_eq!(molecule.bonds[18].atom2, 22);
        assert_eq!(molecule.bonds[18].bond_type, 1);
        assert_eq!(molecule.bonds[18]._bond_stereo, 0);

        assert_eq!(molecule.bonds[47].atom1, 24);
        assert_eq!(molecule.bonds[47].atom2, 48);
        assert_eq!(molecule.bonds[47].bond_type, 1);
        assert_eq!(molecule.bonds[47]._bond_stereo, 0);

        assert_eq!(molecule.associated_data.len(), 5);

        assert_eq!(
            molecule.associated_data.get("MOLECULAR_FORMULA"),
            Some(&"C15H23N3O8".to_string())
        );
        assert_eq!(
            molecule.associated_data.get("MOLECULAR_WEIGHT"),
            Some(&"373.2".to_string())
        );
        assert_eq!(
            molecule.associated_data.get("NUM_HB_ATOMS"),
            Some(&"11".to_string())
        );
        assert_eq!(
            molecule.associated_data.get("NUM_ROTOR"),
            Some(&"9".to_string())
        );
        assert_eq!(
            molecule.associated_data.get("XLOGP2"),
            Some(&"-2.04".to_string())
        );

        Ok(())
    }

    #[test]
    fn parse_basic_ligand_2() -> Result<(), Box<dyn std::error::Error>> {
        let input_contents = test::data::sdf_rank_1()?;

        let molecules = super::parse_sdf(&input_contents)?;

        assert_eq!(molecules.len(), 1);

        let molecule = &molecules[0];

        assert_eq!(molecule.atoms.len(), 26);
        assert_eq!(molecule.bonds.len(), 25);

        assert_eq!(molecule.atoms[0].x, 4.5505);
        assert_eq!(molecule.atoms[0].y, 28.0991);
        assert_eq!(molecule.atoms[0].z, 4.6360);
        assert_eq!(molecule.atoms[0].symbol, "N");
        assert_eq!(molecule.atoms[0]._mass_difference, 0);
        assert_eq!(molecule.atoms[0].charge, 1);

        assert_eq!(molecule.atoms[20].x, 13.0946);
        assert_eq!(molecule.atoms[20].y, 23.4684);
        assert_eq!(molecule.atoms[20].z, 4.2770);
        assert_eq!(molecule.atoms[20].symbol, "O");
        assert_eq!(molecule.atoms[20]._mass_difference, 0);
        assert_eq!(molecule.atoms[20].charge, -1);

        assert_eq!(molecule.bonds[0].atom1, 2);
        assert_eq!(molecule.bonds[0].atom2, 1);
        assert_eq!(molecule.bonds[0].bond_type, 1);
        assert_eq!(molecule.bonds[0]._bond_stereo, 0);

        assert_eq!(molecule.bonds[18].atom1, 21);
        assert_eq!(molecule.bonds[18].atom2, 22);
        assert_eq!(molecule.bonds[18].bond_type, 1);
        assert_eq!(molecule.bonds[18]._bond_stereo, 0);

        assert_eq!(molecule.associated_data.len(), 1);

        assert_eq!(
            molecule.associated_data.get("_TriposChargeType"),
            Some(&"MMFF94_CHARGES".to_string())
        );

        Ok(())
    }

    #[test]
    fn from_to_rank1() -> Result<(), Box<dyn std::error::Error>> {
        let input_contents = test::data::sdf_rank_1()?;
        let res1 = from_sdf(&input_contents)?;
        let sdf1 = to_sdf(&res1[0])?;
        let res2 = from_sdf(&sdf1)?;
        assert_eq!(res1, res2);
        let sdf2 = to_sdf(&res2[0])?;
        assert_eq!(sdf1, sdf2);

        Ok(())
    }

    #[test]
    fn from_to_alt_charge_format() -> Result<(), Box<dyn std::error::Error>> {
        let input_contents = test::data::sdf_alt_charge()?;
        let res1 = from_sdf(&input_contents)?;
        let sdf1 = to_sdf(&res1[0])?;
        let res2 = from_sdf(&sdf1)?;
        assert_eq!(res1, res2);
        let sdf2 = to_sdf(&res2[0])?;
        assert_eq!(sdf1, sdf2);

        Ok(())
    }

    #[test]
    fn from_to_1a30() -> Result<(), Box<dyn std::error::Error>> {
        let input_contents = test::data::sdf_1a30_ligand()?;
        let res1 = from_sdf(&input_contents)?;
        let sdf1 = to_sdf(&res1[0])?;
        let res2 = from_sdf(&sdf1)?;
        assert_eq!(res1, res2);
        let sdf2 = to_sdf(&res2[0])?;
        assert_eq!(sdf1, sdf2);

        Ok(())
    }

    #[test]
    fn isopropyl() -> Result<(), Box<dyn std::error::Error>> {
        let input_contents = test::data::sdf_isopropyl()?;

        let molecules = super::from_sdf(&input_contents)?;

        assert_eq!(molecules.len(), 1);
        assert_eq!(molecules[0].topology.symbols.len(), 12);
        assert_eq!(molecules[0].topology.geometry.len(), 36);
        assert_eq!(
            molecules[0].topology.connectivity.as_ref().unwrap().len(),
            11
        );

        println!("{:?}", molecules[0]);

        Ok(())
    }
}
