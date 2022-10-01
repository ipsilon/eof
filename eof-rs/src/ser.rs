use super::error::{Error, Result};
use serde::ser;

// TODO: implement complete serde serialiser (see ciborium for an example)

use crate::types::*;

struct HeaderEntry {
    pub kind: u8,
    pub size: u16,
}

struct Encoder {
    version: u8,
    headers: Vec<HeaderEntry>,
    contents: Vec<Vec<u8>>,
}

impl Encoder {
    pub fn push_section(&mut self, section: EOFSection) -> Result<()> {
        let section_kind = section.kind();

        // Encode content
        let content = match section {
            EOFSection::Code(code) => code,
            EOFSection::Data(data) => data,
            EOFSection::Type(types) => unimplemented!(),
            _ => unimplemented!(),
        };
        let content_len = content.len();
        self.contents.push(content);

        // Store header
        self.headers.push(HeaderEntry {
            kind: section_kind,
            size: content_len as u16,
            //       size: u16::try_from(content.len())?
        });

        Ok(())
    }

    pub fn finalize(self) -> Result<Vec<u8>> {
        let mut encoded_headers: Vec<u8> = self
            .headers
            .iter()
            .map(|header| {
                vec![
                    header.kind,
                    (header.size >> 8) as u8,
                    (header.size & 0xff) as u8,
                ]
            })
            .flatten()
            .collect();
        let mut encoded_contents: Vec<u8> = self.contents.into_iter().flatten().collect();

        let mut ret = vec![0xef, 0x00, self.version];
        ret.append(&mut encoded_headers);
        ret.push(0); // terminator
        ret.append(&mut encoded_contents);

        Ok(ret)
    }
}

pub fn to_bytes(value: EOFContainer) -> Result<Vec<u8>> {
    let mut encoder = Encoder {
        version: value.version,
        headers: vec![],
        contents: vec![],
    };
    for section in value.sections {
        encoder.push_section(section);
    }
    encoder.finalize()
}

#[cfg(test)]
mod tests {
    use crate::*;

    #[test]
    fn encode_eof_bytes() {
        let container = EOFContainer {
            version: 1,
            sections: vec![
                EOFSection::Code(vec![0xfe]),
                EOFSection::Data(vec![0, 1, 2, 3, 4]),
            ],
        };

        let serialized = to_bytes(container).unwrap();
        println!("{:?}", serialized);
        assert_eq!(hex::encode(serialized), hex::encode("00")); //"{\"version\":1,\"sections\":[{\"Code\":[0]}]}");
    }
}
