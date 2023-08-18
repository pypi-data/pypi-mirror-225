use std::error::Error;

use qdx_common::{Object, Setter};

/// Echo the input to the output.
/// Example usage:
///    cargo run --release --bin qdx-convert '"pdb"' '"input.pdb"' '"output.qdx.json"'
fn main() -> Result<(), Box<dyn Error>> {
    //let (delay_in_millis, delay_progress, ..) = qdx_common::init::<u64, Stream<u64>>();
    let (input, output, ..) =
        qdx_common::init::<(u8, f32, String, Object<u8>), (u8, f32, String, Object<u8>)>();
    output.set((input.0, input.1, input.2, input.3))?;
    Ok(())
}
