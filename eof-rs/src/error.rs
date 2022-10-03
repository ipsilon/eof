use serde::{de, ser};
use std::fmt::{self, Display};

pub type Result<T> = std::result::Result<T, Error>;

#[derive(Clone, Debug, PartialEq)]
pub enum Error {
    Message(String),
    InvalidMagic,
    UnsupportedVersion,
    UnsupportedSectionKind,
    NoSections,
    InvalidSectionOrder,
    MissingCodeSection,
    MismatchingCodeAndTypeSections,
    DuplicateTypeSection,
}

impl ser::Error for Error {
    fn custom<T: Display>(msg: T) -> Self {
        Error::Message(msg.to_string())
    }
}

impl de::Error for Error {
    fn custom<T: Display>(msg: T) -> Self {
        Error::Message(msg.to_string())
    }
}

impl Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        use Error::*;

        match self {
            Message(msg) => write!(f, "{}", msg),
            InvalidMagic => write!(f, "Invalid magic"),
            UnsupportedVersion => write!(f, "Unsupporetd version"),
            UnsupportedSectionKind => write!(f, "Unsupported section kind"),
            NoSections => write!(f, "No sections"),
            InvalidSectionOrder => write!(f, "Invalid section order"),
            MissingCodeSection => write!(f, "Missing Code section"),
            MismatchingCodeAndTypeSections => {
                write!(f, "Mismatching number of Code and Type sections")
            }
            DuplicateTypeSection => write!(f, "Duplicate Type section"),
        }
    }
}

impl std::error::Error for Error {}

impl From<std::io::Error> for Error {
    fn from(error: std::io::Error) -> Self {
        Error::Message(error.to_string())
    }
}

impl From<serde_json::Error> for Error {
    fn from(error: serde_json::Error) -> Self {
        Error::Message(error.to_string())
    }
}
