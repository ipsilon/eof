// TODO use serde
use serde::{Deserialize, Serialize};
use serde_json::Result;
use serde::ser::Error;

pub type EOFVersion = u8;

#[derive(Eq, PartialEq, Debug, Clone, Serialize, Deserialize)]
pub struct EOFContainer {
    version: EOFVersion,
    sections: Vec<EOFSection>,
}

#[derive(Eq, PartialEq, Debug, Clone, Serialize, Deserialize)]
pub enum EOFSection {
    Code(Vec<u8>),
    Data(Vec<u8>),
    Type(Vec<EOFTypeSectionEntry>),
}

#[derive(Eq, PartialEq, Debug, Clone, Serialize, Deserialize)]
pub struct EOFTypeSectionEntry {
    inputs: u8,
    outputs: u8,
}

impl EOFSection {
    fn kind(&self) -> u8 {
        match self {
            EOFSection::Code(_) => 1,
            EOFSection::Data(_) => 2,
            EOFSection::Type(_) => 3,
        }
    }
}

impl EOFContainer {
    pub fn serialize_eof(&self) -> Result<Vec<u8>> {
        let mut ret = vec![1u8];
        
        Ok(ret)
    }
}

#[cfg(test)]
mod tests {
    use crate::*;

    #[test]
    fn encode_json() {
        let container = EOFContainer {
            version: 1,
            sections: vec![EOFSection::Code(vec![00])],
        };

        let serialized = serde_json::to_string(&container).unwrap();
        println!("{}", serialized);
        assert_eq!(serialized, "{\"version\":1,\"sections\":[{\"Code\":[0]}]}");
    }

    #[test]
    fn encode_eof() {
        let container = EOFContainer {
            version: 1,
            sections: vec![EOFSection::Code(vec![00])],
        };

        let serialized = container.serialize_eof().unwrap();
        println!("{:?}", serialized);
        assert_eq!(serialized, vec![1u8]);
    }
}
