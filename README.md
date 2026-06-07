# market-latency-budget-simulator

[![ci](https://github.com/mizcausevic-dev/market-latency-budget-simulator/actions/workflows/ci.yml/badge.svg)](https://github.com/mizcausevic-dev/market-latency-budget-simulator/actions/workflows/ci.yml)
[![pages](https://github.com/mizcausevic-dev/market-latency-budget-simulator/actions/workflows/pages.yml/badge.svg)](https://github.com/mizcausevic-dev/market-latency-budget-simulator/actions/workflows/pages.yml)

Rust and Python simulator for market-data and order-path latency budget risk.

## Why this exists

- FinTech and trading systems need p99 latency, jitter, retry pressure, and packet-loss risk to be visible before market-open exposure.
- Rust gives the repo a credible low-latency implementation signal.
- Python adds scenario analysis for avoidable loss and route prioritization.

## Local run

```bash
cargo test
cargo run -- fixtures/market-latency-sample.json
python scripts/scenario_analysis.py
python scripts/render_site.py
python scripts/smoke_check.py
```

## Data safety

This repo uses synthetic market-path metrics only. Do not commit production market data, trading logs, venue credentials, account identifiers, hostnames, or customer records.
