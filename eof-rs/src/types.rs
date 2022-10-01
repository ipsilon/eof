// TODO use serde
use serde::{Deserialize, Serialize, Serializer};
use serde_bytes_repr::{ByteFmtDeserializer, ByteFmtSerializer};

pub type EOFVersion = u8;

fn serialize_bytes<S, T>(x: T, s: S) -> Result<S::Ok, S::Error>
where
    S: Serializer,
    T: AsRef<[u8]>,
{
    s.serialize_str(&hex::encode(x.as_ref()))
}

#[derive(Eq, PartialEq, Debug, Clone, Serialize, Deserialize)]
pub struct EOFContainer {
    pub version: EOFVersion,
    pub sections: Vec<EOFSection>,
}

#[derive(Eq, PartialEq, Debug, Clone, Serialize, Deserialize)]
pub enum EOFSection {
    #[serde(serialize_with = "serialize_bytes")]
    Code(Vec<u8>),
    Data(Vec<u8>),
    Type(Vec<EOFTypeSectionEntry>),
}

#[derive(Eq, PartialEq, Debug, Clone, Serialize, Deserialize)]
pub struct EOFTypeSectionEntry {
    pub inputs: u8,
    pub outputs: u8,
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
    pub fn serialize_eof(&self) -> Result<Vec<u8>, ()> {
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
