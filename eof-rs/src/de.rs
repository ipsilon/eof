use super::error::{Error, Result};
use super::types::*;

use std::io::Read;

// TODO: implement complete serde serialiser (see ciborium for an example)

trait ExactReader {
    fn read_u8(&mut self) -> Result<u8>;
    fn read_u16(&mut self) -> Result<u16>;
    fn read_bytes(&mut self, len: usize) -> Result<Vec<u8>>;
}

impl ExactReader for [u8] {
    fn read_u8(&mut self) -> Result<u8> {
        let mut tmp = [0u8];
        self.read_exact(&mut tmp)?;
        Ok(tmp[0])
    }

    fn read_u16(&mut self) -> Result<u16> {
        let mut tmp = [0u8; 2];
        self.read_exact(&mut tmp)?;
        Ok(((tmp[0] << 8) | tmp[1]) as u16)
    }

    fn read_bytes(&mut self, len: usize) -> Result<Vec<u8>> {
        let mut tmp = Vec::with_capacity(len);
        self.read_exact(&mut tmp)?;
        Ok(tmp)
    }
}


/*
fn read_exact(&mut self, buf: &mut [u8]) -> Result<()> { ... }

struct ExactReader<'a>(&'a [u8]);

impl<'a> ExactReader<'a> {
    fn read_u8(&'a mut self) -> Result<u8> {
        let mut tmp = [0u8];
        self.0.read_exact(&mut tmp)?;
        Ok(tmp[0])
    }

    fn read_u16(&'a mut self) -> Result<u16> {
        let mut tmp = [0u8; 2];
        self.0.read_exact(&mut tmp)?;
        Ok(((tmp[0] << 8) | tmp[1]) as u16)
    }

    fn read_bytes(&'a mut self, len: u16) -> Result<Vec<u8>> {
        let mut tmp = Vec::with_capacity(len as usize);
        self.0.read_exact(&mut tmp)?;
        Ok(tmp)
    }
}
*/

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
        let mut reader = ExactReader(&v);
        if (reader.read_u16()?) != 0xef00 {
            return Err(Error::InvalidMagic);
        }
        if (reader.read_u8()?) != 1 {
            return Err(Error::UnsupportedVersion);
        }
        let container = EOFContainer {
            version: 1,
            sections: vec![],
        };
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
        for i in 1..self.headers.len() {
            self.contents.push(reader.read_bytes(self.headers[i].size)?);
        }
        /*
                    if section_kind == 1 {
                    container.sections.push(read_code_section(&mut self));
                    } else if section_kind == 2 {
                    container.sections.push(read_code_section(&mut self));
                    } else if section_kind == 3 {
                    container.sections.push(read_code_section(&mut self));
                    } else {
                        return Err(Error::UnsupportedSectionKind);
                    }
                }
        */
        Ok(())
    }

    pub fn finalize(self) -> Result<EOFContainer> {
        unimplemented!()
    }
}

pub fn from_slice(value: &[u8]) -> Result<EOFContainer> {
    let mut decoder = Decoder::new();
    decoder.read(value);
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
