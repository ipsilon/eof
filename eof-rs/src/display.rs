use super::types::*;
use std::fmt;

// TODO: implement this nicely
// TODO: use a markdown library

impl fmt::Display for EOFContainer {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            r#""EOF Version {}

| # | Kind | Size | Content |
|---|------|------|---------|
"#,
            self.version,
        )?;
        for i in 0..self.sections.len() {
            match self.sections[i] {
                EOFSection::Code(ref code) => writeln!(
                    f,
                    //"| {} | Code | {} | {} |",
                    "**Section #{}**\n(len: {})\n{}\n",
                    i,
                    code.len(),
                    hex::encode(code)
                )?,
                EOFSection::Data(ref data) => writeln!(
                    f,
                    "| {} | Data | {} | {} |",
                    i,
                    data.len(),
                    hex::encode(data)
                )?,
                EOFSection::Type(ref types) => {
                    //                    let type_str = types
                    //                        .iter()
                    //                        .flat_map(|type_entry| {
                    //                            format!("{}->{}", type_entry.inputs, type_entry.outputs)
                    //                        })
                    //                        .collect();
                    //let type_str: Vec<EOFTypeSectionEntry> = types.iter().collect();
                    let type_str = "";

                    writeln!(f, "| {} | Type | {} | {} |", i, types.len() * 2, type_str)?
                }
            }
        }

        write!(f, "")
    }
}

//impl fmt::Display for EOFSection {
//}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn complex_container() {
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
        println!("{}", container);
        let formatted = format!("{}", container);
        //        assert!(container.is_valid_eof().is_ok());
        println!("{}", termimad::inline(&formatted));
    }

    #[test]
    fn andreis_code() {
        let bin = "ef000103000601003b01001701001d0000000101010160043560003560e01c63c766526781145d001c63c6c2ea1781145d00065050600080fd50fb000260005260206000f350fb000160005260206000f3600181115d0004506001fc60018103fb000181029050fc600281115d0004506001fc60028103fb000260018203fb0002019050fc";
        let input = hex::decode(bin).unwrap();
        let deserialized = crate::de::from_slice(&input[..]).unwrap();
        let formatted = format!("{}", deserialized);
        println!("{}", termimad::inline(&formatted));
    }
}
