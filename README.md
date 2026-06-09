# market-latency-budget-simulator

[![ci](https://github.com/mizcausevic-dev/market-latency-budget-simulator/actions/workflows/ci.yml/badge.svg)](https://github.com/mizcausevic-dev/market-latency-budget-simulator/actions/workflows/ci.yml)
[![pages](https://github.com/mizcausevic-dev/market-latency-budget-simulator/actions/workflows/pages.yml/badge.svg)](https://github.com/mizcausevic-dev/market-latency-budget-simulator/actions/workflows/pages.yml)

Rust and Python simulator for market-data and order-path latency budget risk.

## What this product does

This product gives trading, market-data, platform, product, and finance leaders a shared simulation surface for latency-budget exposure. Instead of treating p50, p95, p99, jitter, packet loss, retry pressure, and path exposure as separate engineering metrics, it turns them into one board-readable view of which route can fail before market open.

The SaaS go-to-market analyst view is that latency proof is a buyer-confidence signal. If a fintech, trading infrastructure, or market-data product cannot explain route exposure clearly, every reliability, execution-quality, and enterprise-readiness claim becomes weaker. This simulator frames latency as customer trust, revenue protection, and launch readiness.

The SaaS value architect view is focused on avoidable loss. The repo compares market lanes by venue, budget pressure, risk score, and modeled revenue exposure so teams can prioritize route remediation, retry policy changes, or packet-loss investigation before the issue becomes an executive incident.

Technically, the repo demonstrates a Rust + Python signal without production market data, trading logs, credentials, or account identifiers. Rust handles the core scoring path, Python adds scenario analysis, and the generated static surface is backed by synthetic fixtures, cargo tests, CLI output, and smoke checks. The shared Kinetic Gain pattern is to translate specialist system pressure into an executive decision surface that still remains technically traceable.

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
