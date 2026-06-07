from __future__ import annotations

import json
from pathlib import Path


def load_lanes(path: str = "fixtures/market-latency-sample.json") -> list[dict]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return payload["lanes"]


def scenario_rows() -> list[dict]:
    rows = []
    for lane in load_lanes():
        p99_over_budget = max(0, lane["p99_micros"] - lane["budget_micros"])
        avoidable_loss = round(lane["revenue_at_risk_usd"] * min(0.45, p99_over_budget / lane["budget_micros"]))
        rows.append(
            {
                "lane": lane["name"],
                "venue": lane["venue"],
                "p99_over_budget_micros": p99_over_budget,
                "avoidable_loss_usd": avoidable_loss,
            }
        )
    return rows


if __name__ == "__main__":
    print(json.dumps(scenario_rows(), indent=2))
