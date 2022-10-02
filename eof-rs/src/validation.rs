use super::error::{Error, Result};
use super::types::*;

pub trait EOFValidator {
    fn is_valid_eof(&self) -> Result<()>;
}

impl EOFValidator for EOFContainer {
    fn is_valid_eof(&self) -> Result<()> {
        //        if self.version != 1 {
        //          return Err(Error::UnsupportedVersion);
        //        }

        //        for i in 0..self.sections.len() {
        //        }
        unimplemented!()
    }
}

#[cfg(test)]
mod tests {
    use crate::*;

    #[test]
    fn valid_container() {
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
        assert!(container.is_valid_eof().is_ok());
    }

    #[test]
    fn valid_simple_container() {
        let container = EOFContainer {
            version: 1,
            sections: vec![EOFSection::Code(vec![0xfe])],
        };
        assert!(container.is_valid_eof().is_ok());
    }

    #[test]
    fn unsupported_version() {
        let container = EOFContainer {
            version: 2,
            sections: vec![
                EOFSection::Code(vec![0xfe]),
                EOFSection::Data(vec![0, 1, 2, 3, 4]),
            ],
        };
        assert!(container.is_valid_eof().is_err());
    }

    #[test]
    fn no_sections() {
        let container = EOFContainer {
            version: 1,
            sections: vec![],
        };
        assert!(container.is_valid_eof().is_err());
    }

    #[test]
    fn no_code() {
        let container = EOFContainer {
            version: 1,
            sections: vec![EOFSection::Code(vec![0xfe])],
        };
        assert!(container.is_valid_eof().is_err());
    }

    #[test]
    fn data_before_code() {
        let container = EOFContainer {
            version: 1,
            sections: vec![
                EOFSection::Data(vec![0, 1, 2, 3, 4]),
                EOFSection::Code(vec![0xfe]),
            ],
        };
        assert!(container.is_valid_eof().is_err());
    }

    #[test]
    fn type_after_code() {
        let container = EOFContainer {
            version: 1,
            sections: vec![
                EOFSection::Code(vec![0xfe]),
                EOFSection::Type(vec![EOFTypeSectionEntry {
                    inputs: 0,
                    outputs: 0,
                }]),
            ],
        };
        assert!(container.is_valid_eof().is_err());
    }

    #[test]
    fn more_type_than_code() {
        let container = EOFContainer {
            version: 1,
            sections: vec![
                EOFSection::Type(vec![EOFTypeSectionEntry {
                    inputs: 0,
                    outputs: 0,
                }]),
                EOFSection::Type(vec![EOFTypeSectionEntry {
                    inputs: 1,
                    outputs: 1,
                }]),
                EOFSection::Code(vec![0xfe]),
            ],
        };
        assert!(container.is_valid_eof().is_err());
    }

    #[test]
    fn more_code_than_type() {
        let container = EOFContainer {
            version: 1,
            sections: vec![
                EOFSection::Type(vec![EOFTypeSectionEntry {
                    inputs: 0,
                    outputs: 0,
                }]),
                EOFSection::Code(vec![0xfe]),
                EOFSection::Code(vec![0xfe]),
            ],
        };
        assert!(container.is_valid_eof().is_err());
    }
}
