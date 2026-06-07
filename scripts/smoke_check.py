from pathlib import Path

html = Path("site/index.html").read_text(encoding="utf-8")
for marker in [
    "Market Latency Budget Simulator",
    "Latency budgets should fail in simulation",
    "Equities order gateway",
    "Primary recommendation",
]:
    if marker not in html:
        raise SystemExit(f"Missing marker: {marker}")
print("smoke ok")
