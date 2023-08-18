use std::{env, process, str::FromStr};

#[cfg(feature = "graphql")]
use async_graphql::{InputObject, SimpleObject};
use qdx_derive::Typedef;
use qdx_types::{Mutable, Stream, Tuple, Type, Typedef};
use serde::{Deserialize, Serialize};

use crate::init_built_in_types;

/// Explicit resources required for an instance.
/// Will fall back to the hint value if not specified.
#[derive(Serialize, Deserialize, Debug, Clone)]
#[cfg_attr(
    feature = "graphql",
    derive(InputObject, SimpleObject),
    graphql(
        input_name = "ResourcesInput",
        name = "Resources",
        rename_fields = "snake_case"
    )
)]
pub struct Resources {
    pub gpus: Option<u8>,
    pub nodes: Option<u32>,
    pub mem: Option<u32>,
    pub storage: Option<u32>,
    pub walltime: Option<u32>, // in minutes
}

/// Resource utilization of an instance reported post run.
#[derive(Serialize, Deserialize, Debug, Clone)]
#[cfg_attr(
    feature = "graphql",
    derive(InputObject, SimpleObject),
    graphql(
        input_name = "UtilizationInput",
        name = "Utilization",
        rename_fields = "snake_case"
    )
)]
pub struct Utilization {
    pub gpu: Option<f32>, // in % - where 100% = 1 gpu fully utilized
    pub mem: Option<f32>, // in GB
    pub storage: f32,     // size of run directory after run
    pub walltime: f32,    // in minutes
    pub cputime: f32,     // in minutes
    pub inodes: f32,      // number of inodes used by run directory after run
    pub sus: Option<u64>, // number of gadi sus used
}

//TODO: Do we want to allow developers to a way for developers to document resource requirements?
//      eg - "if you have 100 atoms, you should use 1 gpu with 32 gb memory"
/// Validation and hints to resources to use for an instance.
#[derive(Serialize, Deserialize, Debug)]
pub struct ResourceBounds {
    pub gpu_min: u8,  // 0 means no gpu required.
    pub gpu_max: u8,  // 0 means no gpu used
    pub gpu_hint: u8, // most optimal gpu count

    pub node_min: u32,  // minimum node count
    pub node_max: u32,  // maximum node count (e.g. maximum node parallelism)
    pub node_hint: u32, // most optimal node count

    pub mem_min: u32, // in MB
    pub mem_max: u32, // in MB (0 means no limit)

    pub storage_min: u32, // in MB
    pub storage_max: u32, // in MB (0 means no limit)
}

impl Default for ResourceBounds {
    fn default() -> Self {
        Self {
            gpu_min: Default::default(),
            gpu_max: Default::default(),
            gpu_hint: Default::default(),

            node_min: 1,
            node_max: 1,
            node_hint: 1,

            mem_min: Default::default(),
            mem_max: Default::default(),

            storage_min: Default::default(),
            storage_max: Default::default(),
        }
    }
}

//TODO: Do we want "description", "usage" etc here?
#[derive(Serialize, Deserialize, Debug)]
pub struct Manifest {
    pub name: String,
    pub ins: Vec<Type>,
    pub outs: Vec<Type>,
    pub resource_bounds: ResourceBounds,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct ModuleDescriptor {
    pub host: String,
    pub owner: String,
    pub repo: String,
    pub name: String,
    pub version: String,
}

impl FromStr for ModuleDescriptor {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // Format is as follows:
        // for remote: host:owner/repo/version#name
        // for local: ./path/to/module#name - version, repo and host is always "local"
        let mut parts = s.split('#');
        let module = parts.next().ok_or("No module part")?;
        if module.starts_with('.') {
            return Ok(ModuleDescriptor {
                host: "local".to_string(),
                owner: "local".to_string(),
                repo: "local".to_string(),
                name: parts.next().ok_or("No module name")?.to_string(),
                version: "local".to_string(),
            });
        }
        let name = parts.next().ok_or("No name part")?;

        let mut parts = module.split(':');
        let host = parts.next().ok_or("No host part")?;

        let mut parts = parts.next().ok_or("No repo part")?.split('/');
        let owner = parts.next().ok_or("No owner part")?;
        let repo = parts.next().ok_or("No repo part")?;
        let version = parts.next().unwrap_or("latest");

        Ok(ModuleDescriptor {
            host: host.to_string(),
            owner: owner.to_string(),
            repo: repo.to_string(),
            name: name.to_string(),
            version: version.to_string(),
        })
    }
}

#[derive(Serialize, Deserialize, Debug, Typedef, Clone)]
pub enum RuntimeEvent {
    Progress(ProgressEvent),
}

#[derive(Serialize, Deserialize, Debug, Typedef, Clone)]
pub struct ProgressEvent {
    pub n: u64,
    pub n_expected: u64,
    pub n_max: u64,
    pub done: bool,
}

/// Initialize the tengu module with the default resources.
pub fn init<In, Out>() -> (In, Mutable<Out>, (Mutable<Stream<ProgressEvent>>,))
where
    for<'de> In: Deserialize<'de> + Typedef,
    for<'de> Out: Deserialize<'de> + Typedef,
{
    init_with_resources(ResourceBounds::default())
}

/// Initialize the tengu module. The input parameter type and the output
/// parameter type are used to automatically generate the required tengu
/// manifest. Modules that consume multiple input parameters or produce output
/// parameters should use a tuple type.
pub fn init_with_resources<In, Out>(
    resource_bounds: ResourceBounds,
) -> (In, Mutable<Out>, (Mutable<Stream<ProgressEvent>>,))
where
    for<'de> In: Deserialize<'de> + Typedef,
    for<'de> Out: Deserialize<'de> + Typedef,
{
    init_built_in_types();

    let mut args = env::args();
    let name = args.next().unwrap();

    let first = args
        .next()
        .expect("first argument must be 'manifest' or data");

    if first == "manifest" {
        let ins = if let Type::Tuple(Tuple(tuple)) = In::describe() {
            tuple
        } else {
            vec![In::describe()]
        };
        let outs = if let Type::Tuple(Tuple(tuple)) = Out::describe() {
            tuple
        } else {
            vec![Out::describe()]
        };
        println!(
            "{}",
            serde_json::to_string_pretty(&Manifest {
                name,
                ins,
                outs,
                resource_bounds,
            })
            .expect("manifest is valid json")
        );
        process::exit(0);
    }
    let mut args = env::args().skip(1);

    let input = if let Type::Tuple(Tuple(tuple)) = In::describe() {
        let mut inputs = Vec::with_capacity(tuple.len());
        for _ in 0..tuple.len() {
            inputs.push(args.next().expect("missing input argument"));
        }
        serde_json::from_str(&format!("[{}]", inputs.join(",")))
            .unwrap_or_else(|_| panic!("incompatible input arguments {inputs:?}"))
    } else {
        serde_json::from_str(&args.next().expect("missing input argument"))
            .expect("incompatible input arguments")
    };

    let output = serde_json::from_str(&args.next().expect("missing output argument"))
        .expect("incompatible output arguments");

    let progress_stream = serde_json::from_str(&args.next().expect("missing stream argument"))
        .expect("missing stream fd");

    (input, output, (progress_stream,))
}
