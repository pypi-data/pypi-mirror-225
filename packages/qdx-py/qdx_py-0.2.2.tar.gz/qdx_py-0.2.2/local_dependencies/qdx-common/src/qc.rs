#[cfg(feature = "graphql")]
use async_graphql::{Enum, InputObject, SimpleObject};
use qdx_derive::Typedef;
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};

use crate::{
    energy::{DimerEnergies, Energy, MonomerEnergies, TrimerEnergies},
    topology::Topology,
};

#[derive(Copy, Clone, Debug, Default, PartialEq, Eq, PartialOrd, Ord, Typedef)]
#[cfg_attr(
    feature = "serde",
    derive(Deserialize, Serialize),
    serde(rename_all = "lowercase")
)]
#[cfg_attr(feature = "graphql", derive(Enum), graphql(rename_items = "lowercase"))]
pub enum Driver {
    #[default]
    Energy,
    Gradient,
}

/// Params attempts to follow the QC-JSON "standard" for configuring quantum chemistry calculations.
#[derive(Clone, Debug, Default, Typedef)]
#[cfg_attr(
    feature = "graphql",
    derive(InputObject, SimpleObject),
    graphql(
        input_name = "QCParamsInput",
        name = "QCParams",
        rename_fields = "snake_case"
    )
)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
pub struct Params {
    pub driver: Driver,
    pub model: Model,
    pub keywords: Keywords,
    pub topology: Topology,
    pub dry_run: Option<bool>,
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub title: Option<String>,

    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub use_spherical_sad_guess: Option<bool>,
}

#[derive(Copy, Clone, Debug, Default, PartialEq, Eq, PartialOrd, Ord, Typedef)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[cfg_attr(feature = "graphql", derive(Enum))]
pub enum Method {
    #[default]
    RHF,
    RIMP2,
}

/// Model configures the quantum energy calculation method and basis set.
#[derive(Clone, Debug, Typedef)]
#[cfg_attr(
    feature = "graphql",
    derive(InputObject, SimpleObject),
    graphql(
        input_name = "QCModelInput",
        name = "QCModel",
        rename_fields = "snake_case"
    )
)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
pub struct Model {
    #[cfg_attr(feature = "serde", serde(default))]
    pub method: Method,
    #[cfg_attr(feature = "serde", serde(default = "model_default_basis"))]
    pub basis: String,
    #[cfg_attr(feature = "serde", serde(default = "model_default_aux_basis"))]
    pub aux_basis: String,
    #[cfg_attr(feature = "serde", serde(default = "model_default_frag_enabled"))]
    pub frag_enabled: Option<bool>, // can't infer this: for validation sometimes don't want to perform frag calc for a multi-fragment topology
}

fn model_default_basis() -> String {
    "cc-pVDZ".into()
}

fn model_default_aux_basis() -> String {
    "cc-pVDZ-RIFIT".into()
}

fn model_default_frag_enabled() -> Option<bool> {
    Some(true)
}

impl Default for Model {
    fn default() -> Self {
        Self {
            method: Default::default(),
            basis: model_default_basis(),
            aux_basis: model_default_aux_basis(),
            frag_enabled: model_default_frag_enabled(),
        }
    }
}

/// Keywords are the "non-standard" QC-JSON configuration field.
#[derive(Clone, Debug, Default, Typedef)]
#[cfg_attr(
    feature = "graphql",
    derive(InputObject, SimpleObject),
    graphql(
        input_name = "QCKeywordsInput",
        name = "QCKeywords",
        rename_fields = "snake_case"
    )
)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
pub struct Keywords {
    #[cfg_attr(feature = "serde", serde(default))]
    pub scf: SCF,
    #[cfg_attr(feature = "serde", serde(default))]
    pub frag: Frag,
}

/// SCF configures the self-consistent field procedure.
#[derive(Clone, Debug, Typedef)]
#[cfg_attr(
    feature = "graphql",
    derive(InputObject, SimpleObject),
    graphql(
        input_name = "QCSCFInput",
        name = "QCSCF",
        rename_fields = "snake_case"
    )
)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
pub struct SCF {
    #[cfg_attr(feature = "serde", serde(default = "scf_default_niter"))]
    pub niter: u32,
    #[cfg_attr(feature = "serde", serde(default = "scf_default_ndiis"))]
    pub ndiis: u32,
    #[cfg_attr(feature = "serde", serde(default = "scf_default_scf_conv"))]
    pub scf_conv: f64,
    #[cfg_attr(
        feature = "serde",
        serde(default = "scf_default_dynamic_screening_threshold_exp")
    )]
    pub dynamic_screening_threshold_exp: u32,
    #[cfg_attr(feature = "serde", serde(default = "scf_default_convergence_metric"))]
    pub convergence_metric: String,
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub qnext: Option<bool>,
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub density_matrix_export: Option<bool>,
}

fn scf_default_niter() -> u32 {
    40
}

fn scf_default_ndiis() -> u32 {
    8
}

fn scf_default_scf_conv() -> f64 {
    6.0
}

fn scf_default_convergence_metric() -> String {
    "diis".into()
}

fn scf_default_dynamic_screening_threshold_exp() -> u32 {
    10
}

impl Default for SCF {
    fn default() -> Self {
        Self {
            niter: scf_default_niter(),
            ndiis: scf_default_ndiis(),
            scf_conv: scf_default_scf_conv(),
            dynamic_screening_threshold_exp: scf_default_dynamic_screening_threshold_exp(),
            convergence_metric: scf_default_convergence_metric(),
            qnext: Default::default(),
            density_matrix_export: Default::default(),
        }
    }
}

#[derive(Copy, Clone, Debug, Default, PartialEq, Eq, PartialOrd, Ord, Typedef)]
#[cfg_attr(
    feature = "serde",
    derive(Deserialize, Serialize),
    serde(rename_all = "lowercase")
)]
#[cfg_attr(feature = "graphql", derive(Enum), graphql(rename_items = "lowercase"))]
pub enum FragmentedEnergyType {
    #[default]
    #[cfg_attr(feature = "serde", serde(rename = "TotalEnergy"))]
    TotalEnergy,
    #[cfg_attr(feature = "serde", serde(rename = "InteractivityEnergy"))]
    InteractivityEnergy,
}

#[derive(Clone, Debug, Typedef)]
#[cfg_attr(
    feature = "graphql",
    derive(InputObject, SimpleObject),
    graphql(
        input_name = "QCFragInput",
        name = "QCFrag",
        rename_fields = "snake_case"
    )
)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
pub struct Frag {
    #[cfg_attr(feature = "serde", serde(default = "default_method"))]
    pub method: String,
    #[cfg_attr(feature = "serde", serde(default = "default_fragmentation_level"))]
    pub fragmentation_level: u8,
    #[cfg_attr(feature = "serde", serde(default = "default_ngpus_per_node"))]
    pub ngpus_per_node: u32,

    #[cfg_attr(
        feature = "serde",
        serde(
            default = "default_monomer_density_storage",
            skip_serializing_if = "Option::is_none"
        )
    )]
    pub monomer_density_storage: Option<bool>,

    #[cfg_attr(
        feature = "serde",
        serde(
            default = "default_monomer_cutoff",
            skip_serializing_if = "Option::is_none"
        )
    )]
    pub monomer_cutoff: Option<u32>,
    #[cfg_attr(feature = "graphql", graphql(name = "monomer_mp2_cutoff"))]
    #[cfg_attr(
        feature = "serde",
        serde(
            default = "default_monomer_mp2_cutoff",
            skip_serializing_if = "Option::is_none"
        )
    )]
    pub monomer_mp2_cutoff: Option<u32>,

    #[cfg_attr(
        feature = "serde",
        serde(
            default = "default_dimer_cutoff",
            skip_serializing_if = "Option::is_none"
        )
    )]
    pub dimer_cutoff: Option<u32>,
    #[cfg_attr(feature = "graphql", graphql(name = "dimer_mp2_cutoff"))]
    #[cfg_attr(
        feature = "serde",
        serde(
            default = "default_dimer_mp2_cutoff",
            skip_serializing_if = "Option::is_none"
        )
    )]
    pub dimer_mp2_cutoff: Option<u32>,

    #[cfg_attr(
        feature = "serde",
        serde(
            default = "default_trimer_cutoff",
            skip_serializing_if = "Option::is_none"
        )
    )]
    pub trimer_cutoff: Option<u32>,
    #[cfg_attr(feature = "graphql", graphql(name = "trimer_mp2_cutoff"))]
    #[cfg_attr(
        feature = "serde",
        serde(
            default = "default_trimer_mp2_cutoff",
            skip_serializing_if = "Option::is_none"
        )
    )]
    pub trimer_mp2_cutoff: Option<u32>,

    #[cfg_attr(
        feature = "serde",
        serde(default, skip_serializing_if = "Option::is_none")
    )]
    pub subset_of_fragments_to_calculate: Option<Vec<u32>>,

    #[cfg_attr(
        feature = "serde",
        serde(default, skip_serializing_if = "Option::is_none")
    )]
    pub reference_fragment: Option<u32>,

    // FIXME: remove this field once HERMES supports better energy calculation method definition
    #[cfg_attr(feature = "serde", serde(default))]
    pub fragmented_energy_type: FragmentedEnergyType,

    #[cfg_attr(
        feature = "serde",
        serde(default, skip_serializing_if = "Option::is_none")
    )]
    pub monolithic_density_matrix_export: Option<bool>,

    #[cfg_attr(
        feature = "serde",
        serde(
            default = "default_matrix_export_excludes_hydrogen_caps",
            skip_serializing_if = "Option::is_none"
        )
    )]
    pub matrix_export_excludes_hydrogen_caps: Option<bool>,
}
fn default_method() -> String {
    "MBE".into()
}

fn default_fragmentation_level() -> u8 {
    2
}

fn default_ngpus_per_node() -> u32 {
    1
}

fn default_monomer_density_storage() -> Option<bool> {
    Some(true)
}

fn default_monomer_cutoff() -> Option<u32> {
    Some(100)
}

fn default_monomer_mp2_cutoff() -> Option<u32> {
    Some(100)
}

fn default_dimer_cutoff() -> Option<u32> {
    Some(100)
}

fn default_dimer_mp2_cutoff() -> Option<u32> {
    Some(100)
}

fn default_trimer_cutoff() -> Option<u32> {
    Some(25)
}

fn default_trimer_mp2_cutoff() -> Option<u32> {
    Some(25)
}

fn default_matrix_export_excludes_hydrogen_caps() -> Option<bool> {
    Some(true)
}

impl Default for Frag {
    fn default() -> Self {
        Self {
            method: default_method(),
            fragmentation_level: default_fragmentation_level(),
            ngpus_per_node: default_ngpus_per_node(),
            monomer_density_storage: default_monomer_density_storage(),
            monomer_cutoff: default_monomer_cutoff(),
            monomer_mp2_cutoff: default_monomer_mp2_cutoff(),
            dimer_cutoff: default_dimer_cutoff(),
            dimer_mp2_cutoff: default_dimer_mp2_cutoff(),
            trimer_cutoff: default_trimer_cutoff(),
            trimer_mp2_cutoff: default_trimer_mp2_cutoff(),
            subset_of_fragments_to_calculate: Default::default(),
            reference_fragment: Default::default(),
            fragmented_energy_type: Default::default(),
            monolithic_density_matrix_export: Default::default(),
            matrix_export_excludes_hydrogen_caps: default_matrix_export_excludes_hydrogen_caps(),
        }
    }
}

#[derive(Clone, Debug, Default, Typedef)]
#[cfg_attr(
    feature = "graphql",
    derive(InputObject, SimpleObject),
    graphql(input_name = "SystemBasisInput", rename_fields = "snake_case")
)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
pub struct SystemBasis {
    pub n_occupied_basis_functions: u32,
    pub n_virtual_basis_functions: u32,
    pub total_n_basis_functions: u32,
}

#[derive(Clone, Debug, Default, Typedef)]
#[cfg_attr(
    feature = "graphql",
    derive(InputObject, SimpleObject),
    graphql(
        input_name = "QCEnergyResultsInput",
        name = "QCEnergyResults",
        rename_fields = "snake_case"
    )
)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
pub struct EnergyResults {
    /// Energy of the entire topology.
    pub energy: Energy,

    /// Energies for the various levels of fragmentation.
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub monomer_energies: Option<MonomerEnergies>,
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub dimer_energies: Option<DimerEnergies>,
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub trimer_energies: Option<TrimerEnergies>,

    // Basis Function Information
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub full_system_basis_functions: Option<SystemBasis>,
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub fragment_basis_functions: Option<Vec<SystemBasis>>,
}

// TODO: the internal state is similar to the checkpoint - we want to unify these and emit them during the run.
//       this will allow us to restore / view a calculation as it converges.
#[derive(Clone, Debug, Default, Typedef)]
#[cfg_attr(
    feature = "graphql",
    derive(InputObject, SimpleObject),
    graphql(
        input_name = "HermesInternalStateInput",
        name = "HermesInternalStateResults",
        rename_fields = "snake_case"
    )
)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
pub struct InternalState {
    /// Index of the fragments in the matrices
    pub fragment_groups: Vec<Vec<u32>>,
    /// Density Matrices
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub full_system_density_matrix: Option<Vec<f64>>,
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub fragment_density_matrices: Option<Vec<Vec<f64>>>,

    /// Coefficient and MO Matrices
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub fragment_coefficient_matrices: Option<Vec<Vec<f64>>>,
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub fragment_molecular_orbital_energies: Option<Vec<Vec<f64>>>,
}

/// This type is a compression-optimal representation of the internal state, used for isosurface rendering.
#[derive(Clone, Debug, Default)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
pub struct CompressedInternalState {
    /// Density Matrices
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub full_system_density_matrix: Option<Vec<half::f16>>,
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub fragment_density_matrices: Option<Vec<Vec<half::f16>>>,

    /// Coefficient and MO Matrices
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub fragment_coefficient_matrices: Option<Vec<Vec<half::f16>>>,
    #[cfg_attr(feature = "serde", serde(skip_serializing_if = "Option::is_none"))]
    pub fragment_molecular_orbital_energies: Option<Vec<Vec<half::f16>>>,
}

fn clamp_vec(vec: Vec<f64>, clamp: f64) -> Vec<half::f16>
where
{
    vec.into_iter()
        .map(|x| {
            if x > clamp {
                half::f16::from_f64(x - x % clamp)
            } else {
                half::f16::default()
            }
        })
        .collect()
}

impl InternalState {
    /// Reduce the size of the internal state by compressing the density matrices.
    /// We do this by setting all values below `clamp` to zero, and then incrementing
    /// the remaining values by `clamp` as a step size to increase the compression factor
    pub fn compress(self, clamp: f64) -> CompressedInternalState {
        CompressedInternalState {
            full_system_density_matrix: self
                .full_system_density_matrix
                .map(|x| clamp_vec(x, clamp)),
            fragment_density_matrices: self
                .fragment_density_matrices
                .map(|x| x.into_iter().map(|x| clamp_vec(x, clamp)).collect()),
            fragment_coefficient_matrices: self
                .fragment_coefficient_matrices
                .map(|x| x.into_iter().map(|x| clamp_vec(x, clamp)).collect()),
            fragment_molecular_orbital_energies: self
                .fragment_molecular_orbital_energies
                .map(|x| x.into_iter().map(|x| clamp_vec(x, clamp)).collect()),
        }
    }
}

#[cfg(all(feature = "serde", feature = "graphql"))]
#[cfg(test)]
mod tests {
    use super::*;

    // test that qc_params can be loaded from a json file
    #[test]
    fn load_qc_params() -> anyhow::Result<()> {
        serde_json::from_str::<Params>(crate::test::data::qc_json_w15::FILE)?;

        Ok(())
    }

    #[test]
    fn deserialize_default_model() -> anyhow::Result<()> {
        let model: Model = serde_json::from_str("{}")?;
        println!("{model:?}");
        assert_eq!(model.basis, Model::default().basis);
        assert_eq!(model.method, Model::default().method);
        assert_eq!(model.aux_basis, Model::default().aux_basis);
        assert_eq!(model.frag_enabled, Model::default().frag_enabled);

        Ok(())
    }

    #[test]
    fn deserialize_default_scf() -> anyhow::Result<()> {
        let scf: SCF = serde_json::from_str("{}")?;
        println!("{scf:?}");
        assert_eq!(scf.convergence_metric, SCF::default().convergence_metric);
        assert_eq!(
            scf.dynamic_screening_threshold_exp,
            SCF::default().dynamic_screening_threshold_exp
        );
        assert_eq!(scf.ndiis, SCF::default().ndiis);
        assert_eq!(scf.niter, SCF::default().niter);
        assert_eq!(scf.scf_conv, SCF::default().scf_conv);

        Ok(())
    }

    #[test]
    fn deserialize_default_frag() -> anyhow::Result<()> {
        let frag: Frag = serde_json::from_str("{}")?;
        println!("{frag:?}");
        assert_eq!(frag.method, Frag::default().method);
        assert_eq!(
            frag.fragmentation_level,
            Frag::default().fragmentation_level
        );
        assert_eq!(frag.ngpus_per_node, Frag::default().ngpus_per_node);
        assert_eq!(frag.monomer_cutoff, Frag::default().monomer_cutoff);
        assert_eq!(frag.monomer_mp2_cutoff, Frag::default().monomer_mp2_cutoff);
        assert_eq!(frag.dimer_cutoff, Frag::default().dimer_cutoff);
        assert_eq!(frag.dimer_mp2_cutoff, Frag::default().dimer_mp2_cutoff);
        assert_eq!(frag.trimer_cutoff, Frag::default().trimer_cutoff);
        assert_eq!(frag.trimer_mp2_cutoff, Frag::default().trimer_mp2_cutoff);
        assert_eq!(
            frag.subset_of_fragments_to_calculate,
            Frag::default().subset_of_fragments_to_calculate
        );
        assert_eq!(frag.reference_fragment, Frag::default().reference_fragment);
        assert_eq!(
            frag.fragmented_energy_type,
            Frag::default().fragmented_energy_type
        );
        Ok(())
    }

    // TODO: figure out how to compare equivalent json objects
    // test that qc_params can be serialized to a json string correctly
    // #[test]
    // fn serialize_qc_params() -> anyhow::Result<()> {
    //     let orig = include_str!("../tests/data/w15.json.toml")
    //         .replace(" ", "")
    //         .replace("\n", "");
    //     let json = serde_json::from_str::<serde_json::Value>(&orig)?;
    //     let params = serde_json::from_str::<Params>(&orig)?;
    //     assert_eq!(
    //         json,
    //         serde_json::from_str::<serde_json::Value>(&serde_json::to_string(&params)?)?
    //     );

    //     Ok(())
    // }
}
