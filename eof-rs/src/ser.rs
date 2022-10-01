use super::error::{Error, Result};
use serde::ser;

pub struct Serializer;

pub enum GuraType {
  Object,
  Array,
}


impl ser::Serializer for Serializer {
    type Ok = GuraType;
    type Error = Error;

    type SerializeSeq = SerializeArray;
    type SerializeTuple = SerializeArray;
    type SerializeTupleStruct = SerializeArray;
    type SerializeTupleVariant = SerializeTupleVariant;
    type SerializeMap = SerializeMap;
    type SerializeStruct = SerializeStruct;
    type SerializeStructVariant = SerializeStructVariant;

    fn serialize_bool(self, v: bool) -> Result<GuraType> {
        unimplemented!()
    }

    fn serialize_i8(self, v: i8) -> Result<GuraType> {
        self.serialize_i64(v as i64)
    }

    fn serialize_i16(self, v: i16) -> Result<GuraType> {
        self.serialize_i64(v as i64)
    }

    fn serialize_i32(self, v: i32) -> Result<GuraType> {
        self.serialize_i64(v as i64)
    }

    fn serialize_i64(self, v: i64) -> Result<GuraType> {
//        Ok(GuraType::Integer(v as isize))
unimplemented!()
    }

    fn serialize_u8(self, v: u8) -> Result<GuraType> {
        self.serialize_i64(v as i64)
    }

    fn serialize_u16(self, v: u16) -> Result<GuraType> {
        self.serialize_i64(v as i64)
    }

    fn serialize_u32(self, v: u32) -> Result<GuraType> {
        self.serialize_i64(v as i64)
    }

    fn serialize_u64(self, v: u64) -> Result<GuraType> {
//        Ok(GuraType::Integer(v as isize))
unimplemented!()
    }

    fn serialize_f32(self, v: f32) -> Result<GuraType> {
        self.serialize_f64(v as f64)
    }

    fn serialize_f64(self, v: f64) -> Result<GuraType> {
//        Ok(GuraType::Float(v))
unimplemented!()
    }

    fn serialize_char(self, value: char) -> Result<GuraType> {
        self.serialize_str(&value.to_string())
    }

    fn serialize_str(self, value: &str) -> Result<GuraType> {
//        Ok(GuraType::String(value.to_string()))
unimplemented!()
    }

    fn serialize_bytes(self, value: &[u8]) -> Result<GuraType> {
unimplemented!()
//        let vec = value
//            .iter()
//            .map(|&b| GuraType::Integer(b as isize))
//            .collect();
//        Ok(GuraType::Array(vec))
    }

    fn serialize_unit(self) -> Result<GuraType> {
unimplemented!()
//        Ok(GuraType::Null)
    }

    fn serialize_unit_struct(self, _name: &'static str) -> Result<GuraType> {
        self.serialize_unit()
    }

    fn serialize_unit_variant(
        self,
        _name: &str,
        _variant_index: u32,
        variant: &str,
    ) -> Result<GuraType> {
//        Ok(GuraType::String(variant.to_owned()))
unimplemented!()
    }

    fn serialize_newtype_struct<T: ?Sized>(self, _name: &'static str, value: &T) -> Result<GuraType>
    where
        T: ser::Serialize,
    {
        value.serialize(self)
    }

    fn serialize_newtype_variant<T: ?Sized>(
        self,
        _name: &str,
        _variant_index: u32,
        variant: &str,
        value: &T,
    ) -> Result<GuraType>
    where
        T: ser::Serialize,
    {
//        Ok(singleton_hash(variant.to_string(), to_gura_type(value)?))
unimplemented!()
    }

    fn serialize_none(self) -> Result<GuraType> {
        self.serialize_unit()
    }

    fn serialize_some<V: ?Sized>(self, value: &V) -> Result<GuraType>
    where
        V: ser::Serialize,
    {
        value.serialize(self)
    }

    fn serialize_seq(self, len: Option<usize>) -> Result<SerializeArray> {
//        let array = match len {
//            None => Vec::new(),
//            Some(len) => Vec::with_capacity(len),
//        };
//        Ok(SerializeArray { array })
unimplemented!()
    }

    fn serialize_tuple(self, len: usize) -> Result<SerializeArray> {
        self.serialize_seq(Some(len))
    }

    fn serialize_tuple_struct(self, _name: &'static str, len: usize) -> Result<SerializeArray> {
        self.serialize_seq(Some(len))
    }

    fn serialize_tuple_variant(
        self,
        _enum: &'static str,
        _idx: u32,
        variant: &'static str,
        len: usize,
    ) -> Result<SerializeTupleVariant> {
//        Ok(SerializeTupleVariant {
//            name: variant,
//            array: Vec::with_capacity(len),
//        })
unimplemented!()
    }

    fn serialize_map(self, _len: Option<usize>) -> Result<SerializeMap> {
unimplemented!()
//        Ok(SerializeMap {
//            hash: IndexMap::new(),
//            next_key: None,
//        })
    }

    fn serialize_struct(self, _name: &'static str, _len: usize) -> Result<SerializeStruct> {
//        Ok(SerializeStruct {
//            hash: IndexMap::new(),
//        })
unimplemented!()
    }

    fn serialize_struct_variant(
        self,
        _enum: &'static str,
        _idx: u32,
        variant: &'static str,
        _len: usize,
    ) -> Result<SerializeStructVariant> {
//        Ok(SerializeStructVariant {
//            name: variant,
//            hash: IndexMap::new(),
//        })
unimplemented!()
    }
}

pub struct SerializeArray {}
pub struct SerializeTupleVariant {}
pub struct SerializeStruct {}
pub struct SerializeStructVariant {}
pub struct SerializeMap {}

impl ser::SerializeSeq for SerializeArray {
    type Ok = GuraType;
    type Error = Error;

    fn serialize_element<T: ?Sized>(&mut self, elem: &T) -> Result<()>
    where
        T: ser::Serialize,
    {
        unimplemented!()
    }

    fn end(self) -> Result<GuraType> {
        unimplemented!()
    }
}

impl ser::SerializeTuple for SerializeArray {
    type Ok = GuraType;
    type Error = Error;

    fn serialize_element<T: ?Sized>(&mut self, elem: &T) -> Result<()>
    where
        T: ser::Serialize,
    {
    unimplemented!()
    }

    fn end(self) -> Result<GuraType> {
    unimplemented!()
    }
}

impl ser::SerializeTupleStruct for SerializeArray {
    type Ok = GuraType;
    type Error = Error;

    fn serialize_field<V: ?Sized>(&mut self, value: &V) -> Result<()>
    where
        V: ser::Serialize,
    {
unimplemented!()
    }

    fn end(self) -> Result<GuraType> {
unimplemented!()
    }
}

impl ser::SerializeTupleVariant for SerializeTupleVariant {
    type Ok = GuraType;
    type Error = Error;

    fn serialize_field<V: ?Sized>(&mut self, v: &V) -> Result<()>
    where
        V: ser::Serialize,
    {
unimplemented!()
    }

    fn end(self) -> Result<GuraType> {
unimplemented!()
    }
}

impl ser::SerializeMap for SerializeMap {
    type Ok = GuraType;
    type Error = Error;

    fn serialize_key<T: ?Sized>(&mut self, key: &T) -> Result<()>
    where
        T: ser::Serialize,
    {
unimplemented!()
    }

    fn serialize_value<T: ?Sized>(&mut self, value: &T) -> Result<()>
    where
        T: ser::Serialize,
    {
unimplemented!()
    }

    fn serialize_entry<K: ?Sized, V: ?Sized>(&mut self, key: &K, value: &V) -> Result<()>
    where
        K: ser::Serialize,
        V: ser::Serialize,
    {
unimplemented!()
    }

    fn end(self) -> Result<GuraType> {
unimplemented!()
    }
}

impl ser::SerializeStruct for SerializeStruct {
    type Ok = GuraType;
    type Error = Error;

    fn serialize_field<V: ?Sized>(&mut self, key: &'static str, value: &V) -> Result<()>
    where
        V: ser::Serialize,
    {
unimplemented!()
    }

    fn end(self) -> Result<GuraType> {
unimplemented!()
    }
}

impl ser::SerializeStructVariant for SerializeStructVariant {
    type Ok = GuraType;
    type Error = Error;

    fn serialize_field<V: ?Sized>(&mut self, field: &'static str, v: &V) -> Result<()>
    where
        V: ser::Serialize,
    {
unimplemented!()
    }

    fn end(self) -> Result<GuraType> {
unimplemented!()
    }
}

pub fn to_string<T>(value: &T) -> Result<String>
where
    T: ser::Serialize,
{
    let serializer = Serializer {};
    let result = value.serialize(serializer)?;
    unimplemented!()
//    Ok(dump(&result))
}

// TODO: implement complete serde serialiser

use crate::types::*;

pub fn to_bytes(value: EOFContainer) -> Result<Vec<u8>>
{
//  unimplemented!()
    let mut ret = vec![value.version];
//    let mut encoded_sections: Vec<u8> = value.sections.into_iter().map(|section| vec![1u8]).collect();
//    let encoded_sections: Vec<Vec<u8>> = value.sections.into_iter().fold(vec![], |buf, section| buf.push(1u8));
//    let encoded_sections = value.sections.into_iter().map(|section| vec![1u8]);
//    let mut encoded_sections = encoded_sections.flatten().collect();
    let mut encoded_sections = value.sections.into_iter().map(|section| vec![1u8]).flatten().collect();
    ret.append(&mut encoded_sections);
//    ret.extend_from_slice(value.sections.);
    Ok(ret)
}

#[cfg(test)]
mod tests {
    use crate::*;

    #[test]
    fn encode_eof() {
        let container = EOFContainer {
            version: 1,
            sections: vec![EOFSection::Code(vec![00])],
        };

        let serialized = to_string(&container).unwrap();
        println!("{}", serialized);
        assert_eq!(serialized, "{\"version\":1,\"sections\":[{\"Code\":[0]}]}");
    }

    #[test]
    fn encode_eof_bytes() {
        let container = EOFContainer {
            version: 1,
            sections: vec![EOFSection::Code(vec![0xfe]), EOFSection::Data(vec![0,1,2,3,4])],
        };

        let serialized = to_bytes(container).unwrap();
        println!("{:?}", serialized);
        assert_eq!(hex::encode(serialized), hex::encode("00")); //"{\"version\":1,\"sections\":[{\"Code\":[0]}]}");
    }
}
