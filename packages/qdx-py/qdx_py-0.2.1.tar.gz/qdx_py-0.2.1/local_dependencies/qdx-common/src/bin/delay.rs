use std::{env, error::Error, io, thread, time::Duration};

use qdx_common::{Setter, Stream};
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt, EnvFilter};

/// An example module definition that sleeps for a given number of milliseconds.
/// Once per second, it will emit the number of milliseconds that have elapsed.
/// It will also emit the total number of milliseconds that have elapsed once
/// the total delay time has elapsed.
///
/// Example usage:
///     cargo run --release --bin delay 60000 './path/to/output/file'
fn main() -> Result<(), Box<dyn Error>> {
    tracing_subscriber::registry()
        .with(EnvFilter::new(env::var("TRACE").unwrap_or_default()))
        .with(
            tracing_subscriber::fmt::layer()
                .with_writer(io::stderr)
                .compact()
                .without_time()
                .with_level(false),
        )
        .init();

    let (delay_in_millis, delay_progress, ..) = qdx_common::init::<u64, Stream<u64>>();

    let mut delay_progress = delay_progress.set(Stream::create()?)?;

    for i in 0..(delay_in_millis / 1_000) {
        thread::sleep(Duration::from_secs(1));
        delay_progress.send(&(1_000 * i))?;
    }

    thread::sleep(Duration::from_secs(delay_in_millis % 1_000));
    delay_progress.send(&delay_in_millis)?;

    Ok(())
}
