use serde::{Deserialize, Serialize, Serializer};

pub const EOF_MAGIC: u16 = 0xef00;
pub const EOF_VERSION_1: u8 = 1;
pub const EOF_SECTION_TERMINATOR: u8 = 0;
pub const EOF_SECTION_CODE: u8 = 1;
pub const EOF_SECTION_DATA: u8 = 2;
pub const EOF_SECTION_TYPE: u8 = 3;

pub type EOFVersion = u8;

#[derive(Eq, PartialEq, Debug, Clone, Serialize, Deserialize)]
pub struct EOFContainer {
    pub version: EOFVersion,
    pub sections: Vec<EOFSection>,
}

#[derive(Eq, PartialEq, Debug, Clone, Serialize, Deserialize)]
pub enum EOFSection {
    #[serde(serialize_with = "serialize_bytes")]
    Code(Vec<u8>),
    #[serde(serialize_with = "serialize_bytes")]
    Data(Vec<u8>),
    Type(Vec<EOFTypeSectionEntry>),
}

#[derive(Eq, PartialEq, Debug, Clone, Serialize, Deserialize)]
pub struct EOFTypeSectionEntry {
    pub inputs: u8,
    pub outputs: u8,
}

impl EOFSection {
    pub fn kind(&self) -> u8 {
        match self {
            EOFSection::Code(_) => EOF_SECTION_CODE,
            EOFSection::Data(_) => EOF_SECTION_DATA,
            EOFSection::Type(_) => EOF_SECTION_TYPE,
        }
    }

    pub(crate) fn priority(&self) -> u8 {
        match self {
            EOFSection::Code(_) => 2,
            EOFSection::Data(_) => 3,
            EOFSection::Type(_) => 1,
        }
    }
}

fn serialize_bytes<S, T>(x: T, s: S) -> Result<S::Ok, S::Error>
where
    S: Serializer,
    T: AsRef<[u8]>,
{
    s.serialize_str(&hex::encode(x.as_ref()))
}

#[cfg(test)]
mod tests {
    use crate::*;

    #[test]
    fn encode_json() {
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
        let serialized = serde_json::to_string(&container).unwrap();
        println!("{}", serialized);
        assert_eq!(
            serialized,
            "{\"version\":1,\"sections\":[{\"Type\":[{\"inputs\":0,\"outputs\":0},{\"inputs\":1,\"outputs\":1}]},{\"Code\":\"fe\"},{\"Code\":\"fe\"},{\"Data\":\"0001020304\"}]}"
        );
    }
}
