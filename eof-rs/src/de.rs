use super::error::{Error, Result};
use super::types::*;

use std::io::Read;

// TODO: implement complete serde serialiser (see ciborium for an example)

trait ExactReader {
    fn read_u8(&mut self) -> std::io::Result<u8>;
    fn read_u16(&mut self) -> std::io::Result<u16>;
    fn read_bytes(&mut self, len: usize) -> std::io::Result<Vec<u8>>;
}

impl ExactReader for &[u8] {
    fn read_u8(&mut self) -> std::io::Result<u8> {
        let mut tmp = [0u8];
        self.read_exact(&mut tmp)?;
        Ok(tmp[0])
    }

    fn read_u16(&mut self) -> std::io::Result<u16> {
        let mut tmp = [0u8; 2];
        self.read_exact(&mut tmp)?;
        Ok(u16::from_be_bytes(tmp))
    }

    fn read_bytes(&mut self, len: usize) -> std::io::Result<Vec<u8>> {
        let mut tmp = Vec::with_capacity(len);
        unsafe { tmp.set_len(len) };
        self.read_exact(&mut tmp[..])?;
        Ok(tmp)
    }
}

struct HeaderEntry {
    pub kind: u8,
    pub size: u16,
}

struct Decoder {
    version: u8,
    headers: Vec<HeaderEntry>,
    contents: Vec<Vec<u8>>,
}

impl Decoder {
    pub fn new() -> Self {
        Self {
            version: 1,
            headers: vec![],
            contents: vec![],
        }
    }

    pub fn read(&mut self, v: &[u8]) -> Result<()> {
        let mut reader = v;
        if (reader.read_u16()?) != 0xef00 {
            return Err(Error::InvalidMagic);
        }
        if (reader.read_u8()?) != 1 {
            return Err(Error::UnsupportedVersion);
        }
        // TODO: rewrite this to be more idiomatic
        loop {
            let section_kind = reader.read_u8()?;
            if section_kind == 0 {
                break;
            }
            let section_size = reader.read_u16()?;
            self.headers.push(HeaderEntry {
                kind: section_kind,
                size: section_size,
            });
        }
        for i in 0..self.headers.len() {
            self.contents
                .push(reader.read_bytes(self.headers[i].size as usize)?);
        }
        Ok(())
    }

    pub fn finalize(self) -> Result<EOFContainer> {
        let mut container = EOFContainer {
            version: self.version,
            sections: vec![],
        };
        // TODO: make this idiomatic
        for i in 0..self.headers.len() {
            let kind = self.headers[i].kind;
            if kind == 1 {
                container
                    .sections
                    .push(EOFSection::Code(self.contents[i].to_vec()));
            } else if kind == 2 {
                container
                    .sections
                    .push(EOFSection::Data(self.contents[i].to_vec()));
            } else if kind == 3 {
                let mut reader = &self.contents[i][..];
                let mut tmp: Vec<EOFTypeSectionEntry> = vec![];
                for _ in 0..(reader.len() / 2) {
                    tmp.push(EOFTypeSectionEntry {
                        inputs: reader.read_u8()?,
                        outputs: reader.read_u8()?,
                    });
                }
                container.sections.push(EOFSection::Type(tmp));
            } else {
                return Err(Error::UnsupportedSectionKind);
            }
        }
        Ok(container)
    }
}

pub fn from_slice(value: &[u8]) -> Result<EOFContainer> {
    let mut decoder = Decoder::new();
    decoder.read(value)?;
    decoder.finalize()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn decode_eof_bytes() {
        let input = hex::decode("ef00010300040100010100010200050000000101fefe0001020304").unwrap();
        let container = EOFContainer {
            version: 1,
            sections: vec![
                EOFSection::Type(vec![
                    EOFTypeSectionEntry {
                        inputs: 0,
                        outputs: 0,
                    },
                    EOFTypeSectionEntry {
                        inputs: 1,
                        outputs: 1,
                    },
                ]),
                EOFSection::Code(vec![0xfe]),
                EOFSection::Code(vec![0xfe]),
                EOFSection::Data(vec![0, 1, 2, 3, 4]),
            ],
        };

        let deserialized = from_slice(&input[..]).unwrap();

        println!("{:?}", container);
        assert_eq!(deserialized, container);
    }
}
