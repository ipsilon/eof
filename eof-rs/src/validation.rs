use super::error::{Error, Result};
use super::types::*;

pub trait EOFValidator {
    fn is_valid_eof(&self) -> Result<()>;
}

impl EOFValidator for EOFContainer {
    fn is_valid_eof(&self) -> Result<()> {
        if self.version != 1 {
            return Err(Error::UnsupportedVersion);
        }

        let mut code_found = false;
        let mut type_found = false;

        let mut last_section_priority = 0u8;
        for i in 0..self.sections.len() {
            let current_priority = self.sections[i].priority();
            if last_section_priority > current_priority {
                return Err(Error::InvalidSectionOrder);
            } else if last_section_priority == current_priority {
                return Err(Error::DuplicateSection);
            }
            last_section_priority = self.sections[i].kind();

            if let EOFSection::Code(_) = self.sections[i] {
                code_found = true;
                //            } else if EOFSection::Type(_) = self.sections[i] {
                //                type_found = true;
            }
        }

        if !code_found {
            return Err(Error::MissingCodeSection);
        }

        /*
                if self
                    .sections
                    .iter()
                    .filter(|section| section.kind() == 1)
                    .collect()
                    .len()
                    != self
                        .sections
                        .iter()
                        .filter(|section| section.kind() == 3)
                        .collect::<EOFSection>()
                        .len()
                {
                    return Err(Error::MismatchingCodeAndTypeSections);
                }
        */

        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

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
        assert_eq!(
            container.is_valid_eof().err(),
            Some(Error::UnsupportedVersion)
        );
    }

    #[test]
    fn no_sections() {
        let container = EOFContainer {
            version: 1,
            sections: vec![],
        };
        assert_eq!(container.is_valid_eof().err(), Some(Error::NoSections));
    }

    #[test]
    fn no_code() {
        let container = EOFContainer {
            version: 1,
            sections: vec![EOFSection::Data(vec![0xfe])],
        };
        assert_eq!(
            container.is_valid_eof().err(),
            Some(Error::MissingCodeSection)
        );
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
        assert_eq!(
            container.is_valid_eof().err(),
            Some(Error::InvalidSectionOrder)
        );
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
        assert_eq!(
            container.is_valid_eof().err(),
            Some(Error::InvalidSectionOrder)
        );
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
        assert_eq!(
            container.is_valid_eof().err(),
            Some(Error::MismatchingCodeAndTypeSections)
        );
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
        assert_eq!(
            container.is_valid_eof().err(),
            Some(Error::MismatchingCodeAndTypeSections)
        );
    }
}
