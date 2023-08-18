#[cfg(feature = "graphql")]
use async_graphql::{InputObject, SimpleObject};
use qdx_derive::Typedef;
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Default, Typedef)]
#[cfg_attr(
    feature = "graphql",
    derive(InputObject, SimpleObject),
    graphql(input_name = "EnergyInput", rename_fields = "snake_case")
)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
pub struct Energy {
    /// HF energy of the entire topology.
    pub hf: f64,
    /// MP2 same-spin energy correction for the entire topology.
    pub mp2_ss: Option<f64>,
    /// MP2 opposite-spin energy correction for the entire topology.
    pub mp2_os: Option<f64>,
}

#[derive(Clone, Debug, Default, Typedef)]
#[cfg_attr(
    feature = "graphql",
    derive(InputObject, SimpleObject),
    graphql(input_name = "MonomerEnergiesInput", rename_fields = "snake_case")
)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
pub struct MonomerEnergies {
    /// HF energy of each fragment.
    pub hf: Vec<f64>,
    /// MP2 opposite-spin correction for each fragment.
    pub mp2_os: Vec<Option<f64>>,
    /// MP2 same-spin correction for each fragment.
    pub mp2_ss: Vec<Option<f64>>,
}

#[derive(Clone, Debug, Default, Typedef)]
#[cfg_attr(
    feature = "graphql",
    derive(InputObject, SimpleObject),
    graphql(input_name = "DimerEnergiesInput", rename_fields = "snake_case")
)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
pub struct DimerEnergies {
    /// 2-tuple indexes into the fragment list to define dimers.
    pub dimers: Vec<Vec<u32>>,
    /// Zips with dimers to define the distance between dimers (this is temporary
    /// until the distance calculation is ripped from the QC algorithm and put
    /// into a stand-alone library). Thus, it is optional.
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub dimer_distances: Option<Vec<f64>>,
    /// Zips with dimers to define the MBE2 corrections to the HF energy.
    pub hf: Vec<f64>,
    /// Zips with dimers to define the contribution to the HF interaction energy.
    pub hf_interaction: Vec<f64>,
    /// Zips with dimers to define the MBE2 corrections to the MP2 opposite-spin energy.
    pub mp2_os: Vec<Option<f64>>,
    /// Zips with dimers to define the contribution to the MP2 opposite-spin interaction energy.
    pub mp2_os_interaction: Vec<Option<f64>>,
    /// Zips with dimers to define the MBE2 corrections to the MP2 same-spin energy.
    pub mp2_ss: Vec<Option<f64>>,
    /// Zips with dimers to define the contribution to the MP2 same-spin interaction energy.
    pub mp2_ss_interaction: Vec<Option<f64>>,
}

#[derive(Clone, Debug, Default, Typedef)]
#[cfg_attr(
    feature = "graphql",
    derive(InputObject, SimpleObject),
    graphql(input_name = "TrimerEnergiesInput", rename_fields = "snake_case")
)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
pub struct TrimerEnergies {
    /// 3-tuple indexes into the fragment list to define dimers.
    pub trimers: Vec<Vec<u32>>,
    /// Zips with trimers to define the MBE3 corrections to the HF energy.
    pub hf: Vec<f64>,
    /// Zips with trimes to define the contribution to the HF interaction energy.
    pub hf_interaction: Vec<f64>,
    /// Zips with trimers to define the MBE3 corrections to the MP2 same-spin energy.
    pub mp2_ss: Vec<Option<f64>>,
    /// Zips with trimers to define the contribution to the MP2 same-spin interaction energy.
    pub mp2_ss_interaction: Vec<Option<f64>>,
    /// Zips with trimers to define the MBE3 corrections to the MP2 opposite-spin energy.
    pub mp2_os: Vec<Option<f64>>,
    /// Zip with trimers to define the contribution to the MP2 opposite-spin interaction energy.
    pub mp2_os_interaction: Vec<Option<f64>>,
}

#[derive(Clone, Debug, Default, Typedef)]
#[cfg_attr(
    feature = "graphql",
    derive(InputObject, SimpleObject),
    graphql(input_name = "SingleSolv", rename_fields = "snake_case")
)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
pub struct SingleSolv {
    // The solvent.
    pub solvent: String,
    // The method by which the solvation energy is computed.
    pub method: String,
    // The solvation free energy.
    pub delta_g: Option<f64>,
    // The polar energy in vacuum.
    pub polar_vacuum: Option<f64>,
    // The polar energy in solvent.
    pub polar_solvent: Option<f64>,
    // The nonpolar energy in solvent.
    pub nonpolar_solvent: Option<f64>,
}

#[derive(Clone, Debug, Default, Typedef)]
#[cfg_attr(
    feature = "graphql",
    derive(InputObject, SimpleObject),
    graphql(input_name = "SingleBind", rename_fields = "snake_case")
)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
// Stores a single experimental or calculated value of binding energy of a complex.
pub struct SingleBind {
    // The method by which the binding energy is computed. This
    // can be experimental - e.g. IC50, K_d - or calculated, e.g.,
    // MMPBSA.
    pub method: String,
    // The binding energy.
    pub delta_g: Option<f64>,
    // Units of the binding energy.
    pub units: Option<String>,
}

#[derive(Clone, Debug, Default, Typedef)]
#[cfg_attr(
    feature = "graphql",
    derive(InputObject, SimpleObject),
    graphql(input_name = "Solvation", rename_fields = "snake_case")
)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
pub struct Solvation {
    pub solvation: Vec<SingleSolv>,
}

#[derive(Clone, Debug, Default, Typedef)]
#[cfg_attr(
    feature = "graphql",
    derive(InputObject, SimpleObject),
    graphql(input_name = "Binding", rename_fields = "snake_case")
)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
// Stores the values of binding energy of a complex.
pub struct Binding {
    pub binding: Vec<SingleBind>,
}
