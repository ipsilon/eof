use serde::{de, ser};
use std::fmt::{self, Display};

pub type Result<T> = std::result::Result<T, Error>;

#[derive(Clone, Debug, PartialEq)]
pub enum Error {
    Message(String),
    InvalidMagic,
    UnsupportedVersion,
    UnsupportedSectionKind,
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
        }
    }
}

impl std::error::Error for Error {}

impl From<std::io::Error> for Error {
    fn from(error: std::io::Error) -> Self {
        Error::Message(error.to_string())
    }
}
