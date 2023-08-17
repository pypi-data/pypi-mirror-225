use std::{
    fs::{File, OpenOptions},
    io,
    marker::PhantomData,
    path::PathBuf,
};

#[cfg(feature = "serde")]
use serde::{Deserialize, Deserializer, Serialize, Serializer};

use crate::{Bytes, Object, Typedef};

pub trait Getter<T> {
    fn get(self) -> io::Result<T>;
}

pub trait Setter<T> {
    fn set(self, t: T) -> io::Result<T>;
}

pub struct Mutable<T> {
    _t: PhantomData<T>,
    fd: String,
    f: File,
}

#[cfg(feature = "serde")]
impl<T> Mutable<T>
where
    T: Serialize + Typedef,
{
    pub fn create(self) -> io::Result<Object<T>> {
        let obj = Object::with_fd(
            self.fd
                .parse::<PathBuf>()
                .unwrap()
                .file_stem()
                .unwrap()
                .to_str()
                .unwrap()
                .to_string(),
        )?;
        serde_json::to_writer(self.f, &obj)?;
        Ok(obj)
    }
}

#[cfg(feature = "serde")]
impl<T> Setter<T> for Mutable<T>
where
    T: Serialize + Typedef,
{
    fn set(self, t: T) -> io::Result<T> {
        serde_json::to_writer(self.f, &t)?;
        Ok(t)
    }
}

#[cfg(feature = "serde")]
impl Setter<Bytes> for Mutable<Bytes> {
    fn set(mut self, bytes: Bytes) -> io::Result<Bytes> {
        use std::io::Write;
        self.f.write_all(&bytes)?;
        Ok(bytes)
    }
}

#[cfg(feature = "serde")]
impl<'de, T> Deserialize<'de> for Mutable<T> {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        use serde::de::Error;

        let fd = String::deserialize(deserializer)?;
        let f = OpenOptions::new()
            .create(false)
            .read(false)
            .write(true)
            .truncate(true)
            .open(&fd)
            .map_err(|e| D::Error::custom(format!("cannot open {fd} for reading: {e}")))?;
        Ok(Self {
            _t: PhantomData,
            fd,
            f,
        })
    }
}

#[cfg(feature = "serde")]
impl<T> Serialize for Mutable<T> {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        serializer.serialize_str(&self.fd)
    }
}
