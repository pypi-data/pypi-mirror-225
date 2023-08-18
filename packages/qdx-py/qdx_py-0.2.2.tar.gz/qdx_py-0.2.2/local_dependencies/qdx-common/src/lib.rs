pub mod amino_acid;
pub mod bond;
pub mod conformer;
pub mod convert;
pub mod energy;
pub mod module;
pub mod qc;
#[cfg(test)]
mod test;
pub mod topology;
pub mod ts;
#[cfg(feature = "wasm")]
pub mod wasm;

pub use amino_acid::{AminoAcid, AminoAcidTemplate};
pub use bond::*;
pub use conformer::{AtomCheckStrictness, Conformer, Label};
pub use convert::*;
pub use energy::*;
pub use module::*;
pub use qc::*;
pub use topology::*;
pub use ts::*;

pub use qdx_derive::*;
pub use qdx_types::*;

pub fn init_built_in_types() {
    // Primitives
    ::qdx_types::register_built_in("Alt".to_string(), Alt::describe());
    ::qdx_types::register_built_in("Bond".to_string(), Bond::describe());
    ::qdx_types::register_built_in("AminoAcid".to_string(), AminoAcid::describe());
    ::qdx_types::register_built_in("Topology".to_string(), Topology::describe());
    // Basics
    ::qdx_types::register_built_in("Conformer".to_string(), Conformer::describe());
    ::qdx_types::register_built_in("MonomerEnergies".to_string(), MonomerEnergies::describe());
    ::qdx_types::register_built_in("DimerEnergies".to_string(), DimerEnergies::describe());
    ::qdx_types::register_built_in("TrimerEnergies".to_string(), TrimerEnergies::describe());
    ::qdx_types::register_built_in("Energy".to_string(), Energy::describe());
    ::qdx_types::register_built_in("Solvation".to_string(), Solvation::describe());
    ::qdx_types::register_built_in("Binding".to_string(), Binding::describe());

    // Module-specific
    ::qdx_types::register_built_in("QCParams".to_string(), qc::Params::describe());
    ::qdx_types::register_built_in("QCEnergyResults".to_string(), qc::EnergyResults::describe());
}
