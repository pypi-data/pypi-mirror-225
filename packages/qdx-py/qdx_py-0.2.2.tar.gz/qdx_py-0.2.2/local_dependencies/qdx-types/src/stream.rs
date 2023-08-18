use std::{
    fs::{File, OpenOptions},
    io::{self, Read, Seek, Write},
    marker::PhantomData,
};

use file_rotate::{
    suffix::{AppendTimestamp, FileLimit},
    FileRotate,
};
#[cfg(feature = "serde")]
use serde::{Deserialize, Deserializer, Serialize, Serializer};
use uuid::Uuid;

use crate::{Type, Typedef};

pub struct Stream<T> {
    _t: PhantomData<T>,
    fd: String,
    fr: FileRotate<AppendTimestamp>,
    fr_idx: usize, // which file in the rotation are we on?
    i_idx: usize,  // which byte in the file are we on?
    f: Option<File>,
}

impl<T> Stream<T> {
    pub fn with_fd(fd: String) -> io::Result<Self> {
        let f = file_rotate::FileRotate::new(
            format!("{fd}_stream/stream"),
            AppendTimestamp::default(FileLimit::MaxFiles(9999)),
            file_rotate::ContentLimit::Lines(1000),
            file_rotate::compression::Compression::None,
            None,
        );
        Ok(Self {
            _t: PhantomData,
            fd,
            fr: f,
            fr_idx: 0,
            i_idx: 0,
            f: None,
        })
    }

    pub fn create() -> io::Result<Self> {
        let fd = Uuid::new_v4().to_string();

        let f = file_rotate::FileRotate::new(
            format!("{fd}_stream/stream"),
            AppendTimestamp::default(FileLimit::MaxFiles(9999)),
            file_rotate::ContentLimit::Lines(1000),
            file_rotate::compression::Compression::None,
            None,
        );
        Ok(Self {
            _t: PhantomData,
            fd,
            fr: f,
            fr_idx: 0,
            i_idx: 0,
            f: None,
        })
    }

    /// Streams have parts. This will increment the part number and open the file for that part
    fn rotate(&mut self) -> io::Result<()> {
        self.fr.rotate()?; // ensure that all existing files are closed, and increment the file rotation
        let paths = self.fr.log_paths();
        self.f = if let Some(file) = paths.get(self.fr_idx) {
            let f = OpenOptions::new().read(true).open(file)?;
            if f.metadata()?.len() == 0 {
                // file is empty, so stop here
                return Err(io::ErrorKind::UnexpectedEof.into());
            }
            Some(f)
        } else {
            return Err(io::ErrorKind::AddrNotAvailable.into());
        };
        Ok(())
    }
}

impl<T> Typedef for Stream<T>
where
    T: Typedef,
{
    fn describe() -> Type {
        Type::Stream(Box::new(T::describe()))
    }
}

#[cfg(feature = "serde")]
impl<T> Stream<T>
where
    for<'de> T: Deserialize<'de> + Typedef,
{
    pub fn recv(&mut self) -> io::Result<Option<T>> {
        let f = match self.f {
            Some(ref mut f) => f,
            None => {
                match self.rotate() {
                    Err(e) if e.kind() == io::ErrorKind::UnexpectedEof => {
                        return Ok(None);
                    }
                    Err(e) => return Err(e),
                    Ok(_) => {}
                };
                self.f.as_mut().ok_or(io::ErrorKind::AddrNotAvailable)?
            }
        };
        // we use self.i_idx to keep track of where we are in the file
        let mut i = self.i_idx;
        f.seek(std::io::SeekFrom::Start(self.i_idx as u64))?;

        // We will read one byte at a time. If it is a RS (30), then we will
        // read until the LS (10) byte is found, and parse everything inbetween
        // as a JSON value.
        let mut buf = [0u8; 1];

        // If we reach the end of the reader, we will return None.
        match f.read_exact(&mut buf) {
            Ok(_) => {}
            Err(e) if e.kind() == io::ErrorKind::UnexpectedEof => {
                // close the current file and increment the file rotation
                self.f = None;
                self.i_idx = 0;
                self.fr_idx += 1;
                return self.recv();
            }
            Err(e) => return Err(e),
        }

        // Otherwise, if the byte is RS (30), we will read until the LS (10).
        if buf[0] == 30 {
            let mut str = String::new();
            loop {
                i += 1;
                // We do not expect any errors until LS (10) has been found.
                f.read_exact(&mut buf)?;
                if buf[0] == 10 {
                    break;
                }
                str.push(buf[0] as char);
            }
            self.i_idx = i + 1;
            return Ok(Some(serde_json::from_str(&str)?));
        }
        Err(io::Error::new(
            io::ErrorKind::InvalidData,
            format!("expected RS or EOF, got {:?}", buf[0]),
        ))
    }

    pub fn send(&mut self, t: &T) -> io::Result<()>
    where
        T: Serialize,
    {
        let str = serde_json::to_string(t)?;
        self.fr.write_all(&[30])?;
        self.fr.write_all(str.as_bytes())?;
        self.fr.write_all(&[10])?;
        self.fr.flush()?;
        Ok(())
    }
}

#[cfg(feature = "serde")]
impl<'de, T> Deserialize<'de> for Stream<T> {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        let fd = String::deserialize(deserializer)?;

        let f = file_rotate::FileRotate::new(
            format!("{fd}_stream/stream"),
            AppendTimestamp::default(FileLimit::MaxFiles(9999)),
            file_rotate::ContentLimit::Lines(1000),
            file_rotate::compression::Compression::None,
            None,
        );
        Ok(Self {
            _t: PhantomData,
            fd,
            fr: f,
            fr_idx: 0,
            i_idx: 0,
            f: None,
        })
    }
}

#[cfg(feature = "serde")]
impl<T> Serialize for Stream<T> {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        serializer.serialize_str(&self.fd)
    }
}

#[cfg(test)]
mod tests {

    #[test]
    fn test_new_stream() -> Result<(), Box<dyn std::error::Error>> {
        let mut stream = crate::Stream::<String>::create()?;
        stream.send(&"Hello World".to_string())?;
        stream.send(&"Hello World 2".to_string())?;
        let msg = stream.recv()?;
        assert_eq!(msg, Some("Hello World".to_string()));
        let msg = stream.recv()?;
        assert_eq!(msg, Some("Hello World 2".to_string()));
        stream.send(&"Hello World 3".to_string())?;
        let msg = stream.recv()?;
        assert_eq!(msg, Some("Hello World 3".to_string()));

        let msg = stream.recv()?;
        assert_eq!(msg, None);
        // // cleanup
        std::fs::remove_dir_all(format!("{}_stream", stream.fd))?;
        Ok(())
    }

    #[test]
    fn test_new_stream_with_fd() -> Result<(), Box<dyn std::error::Error>> {
        let mut stream = crate::Stream::<String>::with_fd(uuid::Uuid::new_v4().to_string())?;
        stream.send(&"Hello World".to_string())?;
        stream.send(&"Hello World 2".to_string())?;
        let msg = stream.recv()?;
        assert_eq!(msg, Some("Hello World".to_string()));
        let msg = stream.recv()?;
        assert_eq!(msg, Some("Hello World 2".to_string()));
        stream.send(&"Hello World 3".to_string())?;
        let msg = stream.recv()?;
        assert_eq!(msg, Some("Hello World 3".to_string()));

        let msg = stream.recv()?;
        assert_eq!(msg, None);

        std::fs::remove_dir_all(format!("{}_stream", stream.fd))?;
        Ok(())
    }
}
