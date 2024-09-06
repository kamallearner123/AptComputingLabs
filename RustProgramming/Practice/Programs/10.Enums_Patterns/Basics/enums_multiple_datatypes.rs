use std::env;
#[derive(Debug)]
enum SeverityLevel {
    Low(i64),
    Medium(i64),
    High(i64),
    Critical(i64),
    //ErrorMsg(String),
}

use self::SeverityLevel::*;

fn find_severity(identiy: i64) -> SeverityLevel {
    match identiy {
        1..=10 => Low,
        11..=20 => Medium,
        21..=30 => High,
        _ => Critical,
        //_ => ErrorMsg("Invalid range".to_string())
    }
}

fn main() {
    println!("Severity Level = {:?}", find_severity(10));
    println!("Severity Level = {:?}", find_severity(41));

    let LowSev = Low;
    let typeCast: i64;
    typeCast = LowSev as i64;
    println!("typeCast = {:?}", typeCast);
}

