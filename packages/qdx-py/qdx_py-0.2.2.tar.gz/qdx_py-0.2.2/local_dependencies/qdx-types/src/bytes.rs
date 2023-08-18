use std::ops::{Deref, DerefMut};

use crate::{Type, Typedef};

pub struct Bytes(Vec<u8>);

impl Bytes {
    pub fn new(v: Vec<u8>) -> Self {
        Self(v)
    }
}

impl From<Vec<u8>> for Bytes {
    fn from(v: Vec<u8>) -> Self {
        Self(v)
    }
}

impl Typedef for Bytes {
    fn describe() -> Type {
        Type::Bytes
    }
}

impl Deref for Bytes {
    type Target = Vec<u8>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Bytes {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}
