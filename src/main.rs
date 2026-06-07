use std::{env, fs, process};

use market_latency_budget_simulator::{LatencyInput, build_console};

fn main() {
    let Some(path) = env::args().nth(1) else {
        eprintln!("Usage: market-latency-budget-simulator <input.json>");
        process::exit(1);
    };
    let raw = fs::read_to_string(&path).unwrap_or_else(|err| {
        eprintln!("Could not read {path}: {err}");
        process::exit(1);
    });
    let input: LatencyInput = serde_json::from_str(&raw).unwrap_or_else(|err| {
        eprintln!("Invalid latency input: {err}");
        process::exit(1);
    });
    let console = build_console(input);
    println!(
        "{}",
        serde_json::to_string_pretty(&console).expect("console should serialize")
    );
}
