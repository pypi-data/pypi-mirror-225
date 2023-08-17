use std::{
    fs::{File, OpenOptions},
    io,
    marker::PhantomData,
};

#[cfg(feature = "serde")]
use serde::{Deserialize, Deserializer, Serialize, Serializer};
use uuid::Uuid;

use crate::{Bytes, Getter, Setter, Type, Typedef};

pub struct Object<T> {
    _t: PhantomData<T>,
    fd: String,
    f: File,
}

impl<T> Object<T> {
    pub fn new() -> io::Result<Self> {
        let fd = Uuid::new_v4().to_string();
        let f = OpenOptions::new()
            .create(true)
            .read(true)
            .write(true)
            .truncate(true)
            .open(&fd)?;
        Ok(Self {
            _t: PhantomData,
            fd,
            f,
        })
    }

    pub fn with_fd(fd: String) -> io::Result<Self> {
        let f = OpenOptions::new()
            .create(true)
            .read(true)
            .write(true)
            .truncate(true)
            .open(&fd)?;
        Ok(Self {
            _t: PhantomData,
            fd,
            f,
        })
    }
}

impl<T> Typedef for Object<T>
where
    T: Typedef,
{
    fn describe() -> Type {
        Type::Object(Box::new(T::describe()))
    }
}

#[cfg(feature = "serde")]
impl<T> Getter<T> for Object<T>
where
    for<'de> T: Deserialize<'de> + Typedef,
{
    fn get(self) -> io::Result<T> {
        Ok(serde_json::from_reader(self.f)?)
    }
}

#[cfg(feature = "serde")]
impl Getter<Bytes> for Object<Bytes> {
    fn get(mut self) -> io::Result<Bytes> {
        use std::io::Read;
        let mut buf = Vec::new();
        self.f.read_to_end(&mut buf)?;
        Ok(Bytes::from(buf))
    }
}

#[cfg(feature = "serde")]
impl<T> Setter<T> for Object<T>
where
    T: Serialize + Typedef,
{
    fn set(self, t: T) -> io::Result<T> {
        // NOTE: It might be best to open here instead of at the serialize call
        serde_json::to_writer(self.f, &t)?;
        Ok(t)
    }
}

#[cfg(feature = "serde")]
impl Setter<Bytes> for Object<Bytes> {
    fn set(mut self, bytes: Bytes) -> io::Result<Bytes> {
        use std::io::Write;
        self.f.write_all(&bytes)?;
        Ok(bytes)
    }
}

#[cfg(feature = "serde")]
impl<'de, T> Deserialize<'de> for Object<T> {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        use serde::de::Error;

        let fd = String::deserialize(deserializer)?;
        let f = OpenOptions::new()
            .create(false)
            .read(true)
            .write(true)
            .truncate(false)
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
impl<T> Serialize for Object<T> {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        serializer.serialize_str(&self.fd)
    }
}
