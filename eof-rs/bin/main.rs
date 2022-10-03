use std::io;

use std::fs::File;
use std::io::BufReader;
use std::path::PathBuf;

use eof_rs::*;
//use eof_rs::error

//use clap::{crate_authors, crate_description, crate_name, crate_version, Arg, ArgMatches, Command};
use clap::{arg, command, value_parser, ArgAction, Command};

fn validate(input: Option<&String>) -> Result<()> {
    let reader: std::result::Result<EOFContainer, serde_json::Error> = if let Some(path) = input {
        serde_json::from_reader(BufReader::new(File::open(path)?))
    } else {
        serde_json::from_reader(io::stdin())
    };
    reader?.is_valid_eof()
}

fn convert(input: Option<&String>, fmt: &str) -> Result<()> {
    println!("fmt: {}", fmt);
    let a = Vec::new();
    let container = eof_rs::from_slice(&a).unwrap(); // FIXME: translate error
    unimplemented!()
}

fn main() -> Result<()> {
    let matches = command!()
        .subcommand_required(true)
        .subcommand(
        Command::new("validate").about("validates a given EOF structure")
        .arg(arg!([input] "Input file to operate on (stdin if omitted)"))
        )
        .subcommand(
            Command::new("convert")
                .about("converts between various representations")
        .arg(arg!([input] "Input file to operate on (stdin if omitted)"))
                .arg(
                    arg!(--fmt <FMT> "target format (bin, json, yaml)").required(true), //.value_parser(value_parser!(PathBuf)),
                ),
        )
        .get_matches();

    if let Some(_) = matches.subcommand_matches("validate") {
        validate(matches.get_one::<String>("input"))?
    } else if let Some(matches) = matches.subcommand_matches("convert") {
        let fmt = matches.get_one::<String>("fmt").expect("ensurde by clap");
        convert(matches.get_one::<String>("input"), fmt)?
    }

    Ok(())
}
