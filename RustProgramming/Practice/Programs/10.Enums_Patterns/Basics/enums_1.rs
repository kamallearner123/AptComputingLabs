use std::env;
#[derive(Debug)]
enum SeverityLevel {
    Low,
    Medium,
    High,
    Critical,
}

fn find_severity(identiy: i32) -> SeverityLevel {
    match identiy {
        1..=10 => SeverityLevel::Low,
        11..=20 => SeverityLevel::Medium,
        21..=30 => SeverityLevel::High,
        _ => SeverityLevel::Critical,
    }
}

fn main() {
    println!("Severity Level = {:?}", find_severity(10));
}