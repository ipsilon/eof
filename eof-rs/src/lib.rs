mod de;
mod display;
mod error;
mod ser;
mod types;
mod validation;

pub use error::{Result, Error};
pub use de::from_slice;
pub use ser::to_bytes;
pub use types::*;
pub use validation::EOFValidator;
