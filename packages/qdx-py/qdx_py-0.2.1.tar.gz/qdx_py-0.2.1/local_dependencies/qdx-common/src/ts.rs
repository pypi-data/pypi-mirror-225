use std::time::SystemTime;

/// Returns the number of nanoseconds since Unix epoch. The signed integer is
/// enough for 2^63 / 10^9 / 60 / 60 / 24 / 365 = ~292 years worth of
/// nanoseconds. This is sufficient for our use case; hopefully humanity writes
/// better technology within the next 300 years.
pub fn now() -> i64 {
    SystemTime::now()
        .duration_since(SystemTime::UNIX_EPOCH)
        .expect("`SystemTime::now()` should be after `SystemTime::UNIX_EPOCH`")
        .as_nanos() as i64
}
