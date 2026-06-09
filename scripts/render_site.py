from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def main() -> None:
    result = subprocess.run(
        ["cargo", "run", "--quiet", "--", "fixtures/market-latency-sample.json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    console = json.loads(result.stdout)
    exposure = sum(lane["revenue_at_risk_usd"] for lane in console["lanes"])
    cards = "\n".join(
        f"""
        <article class="card">
          <span>{lane["tier"]}</span>
          <h3>{lane["name"]}</h3>
          <p>{lane["routing_note"]}</p>
          <dl>
            <div><dt>Venue</dt><dd>{lane["venue"]}</dd></div>
            <div><dt>Budget pressure</dt><dd>{lane["budget_pressure"]} micros</dd></div>
            <div><dt>Risk</dt><dd>{lane["risk_score"]}</dd></div>
            <div><dt>Exposure</dt><dd>${lane["revenue_at_risk_usd"]:,}</dd></div>
          </dl>
        </article>
        """
        for lane in console["lanes"]
    )
    depth_cards = """
        <article class="depth-card story">
          <span>SaaS go-to-market analyst lens</span>
          <h3>Turns low-latency engineering into a revenue-protection story.</h3>
          <p>Market latency is not only an engineering metric. P99 drift, jitter, retry pressure, and packet loss can become missed execution windows, customer trust issues, venue-risk narratives, and investor questions when leadership cannot see exposure before market open.</p>
        </article>
        <article class="depth-card">
          <span>SaaS value architect lens</span>
          <h3>Connects path latency to avoidable loss and route priority.</h3>
          <p>The simulator makes each market lane comparable by venue, budget pressure, risk score, and modeled revenue exposure. It helps product, trading operations, platform, and finance decide which route needs remediation before the next launch or trading window.</p>
        </article>
        <article class="depth-card">
          <span>Technical proof</span>
          <h3>The repo keeps the latency model reproducible.</h3>
          <p>Rust handles the core scoring path, Python provides scenario analysis, synthetic fixtures avoid production trading data, and the generated static page is backed by cargo tests, CLI output, and smoke checks.</p>
        </article>
        <article class="depth-card">
          <span>What these repos have in common</span>
          <h3>They translate specialist system pressure into board-ready decisions.</h3>
          <p>The shared Kinetic Gain pattern is to model the exposed lane, quantify impact, preserve technical traceability, and publish a buyer-readable surface that explains where to intervene first.</p>
        </article>
    """
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Market Latency Budget Simulator</title>
  <meta name="description" content="Rust and Python simulator for market-data and order-path latency budget risk." />
  <style>
    :root {{ --bg:#050912; --panel:#0c1523; --line:rgba(116,241,219,.24); --text:#f6f3ea; --muted:#aeb7c7; --cyan:#30d5ff; --mint:#65f0c4; --violet:#a78bfa; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:radial-gradient(circle at top left, rgba(48,213,255,.15), transparent 34rem), radial-gradient(circle at top right, rgba(167,139,250,.14), transparent 30rem), var(--bg); color:var(--text); font-family:ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    main {{ width:min(1180px, calc(100% - 32px)); margin:0 auto; padding:48px 0 56px; }}
    .hero {{ border:1px solid var(--line); border-radius:28px; padding:clamp(28px,6vw,64px); background:linear-gradient(135deg, rgba(16,28,45,.96), rgba(8,13,24,.9)); box-shadow:0 30px 90px rgba(0,0,0,.35); }}
    .eyebrow {{ color:var(--mint); font-family:ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size:12px; letter-spacing:.22em; text-transform:uppercase; }}
    h1 {{ margin:18px 0; max-width:900px; font-size:clamp(46px,8vw,100px); line-height:.92; letter-spacing:-.065em; }}
    .lede {{ max-width:740px; color:var(--muted); font-size:clamp(18px,2.4vw,24px); line-height:1.55; }}
    .metrics,.depth-grid {{ display:grid; gap:14px; margin-top:34px; }}
    .metrics {{ grid-template-columns:repeat(4,1fr); }}
    .metric,.card,.recommendation,.depth {{ border:1px solid rgba(255,255,255,.1); background:rgba(16,28,45,.72); border-radius:20px; }}
    .metric {{ padding:20px; }}
    .metric strong {{ display:block; font-size:34px; letter-spacing:-.04em; }}
    .metric span {{ color:var(--muted); font-size:13px; text-transform:uppercase; letter-spacing:.12em; }}
    h2 {{ font-size:clamp(34px,5vw,62px); letter-spacing:-.05em; margin:46px 0 16px; }}
    .depth {{ margin-top:28px; padding:28px; }}
    .section-head {{ display:flex; align-items:end; justify-content:space-between; gap:18px; border-bottom:1px solid rgba(255,255,255,.08); padding-bottom:16px; }}
    .section-head h2 {{ margin:0; }}
    .section-note {{ color:var(--muted); font-family:ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size:12px; letter-spacing:.16em; text-transform:uppercase; }}
    .depth-grid {{ grid-template-columns:repeat(4,1fr); }}
    .grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:18px; }}
    .card,.depth-card {{ padding:24px; min-height:250px; }}
    .depth-card {{ border:1px solid rgba(255,255,255,.08); border-radius:18px; background:rgba(5,9,18,.48); }}
    .depth-card.story {{ border-left:4px solid var(--cyan); }}
    .card span,.depth-card span {{ color:var(--cyan); font-family:ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size:12px; letter-spacing:.16em; text-transform:uppercase; }}
    .card h3 {{ margin:14px 0; font-size:26px; letter-spacing:-.035em; }}
    .card p {{ color:var(--muted); line-height:1.55; }}
    dl {{ display:grid; grid-template-columns:repeat(2,1fr); gap:12px; margin:22px 0 0; }}
    dt {{ color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.12em; }}
    dd {{ margin:4px 0 0; font-weight:700; }}
    .recommendation {{ margin-top:18px; padding:26px; border-left:4px solid var(--mint); }}
    .recommendation strong {{ color:var(--mint); }}
    footer {{ color:var(--muted); margin-top:32px; font-size:14px; }}
    @media (max-width:1100px) {{ .depth-grid {{ grid-template-columns:repeat(2,1fr); }} }}
    @media (max-width:820px) {{ .metrics,.grid,.depth-grid {{ grid-template-columns:1fr; }} dl {{ grid-template-columns:1fr; }} .section-head {{ align-items:flex-start; flex-direction:column; }} }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <div class="eyebrow">Rust + Python FinTech simulator</div>
      <h1>Latency budgets should fail in simulation before they fail at market open.</h1>
      <p class="lede">Market Latency Budget Simulator turns p50, p95, p99, jitter, packet loss, retry pressure, and revenue exposure into one board-readable market-path risk surface.</p>
      <div class="metrics">
        <div class="metric"><strong>{len(console["lanes"])}</strong><span>Market lanes</span></div>
        <div class="metric"><strong>${round(exposure / 1_000_000, 1)}M</strong><span>Exposure modeled</span></div>
        <div class="metric"><strong>{console["lanes"][0]["risk_score"]}</strong><span>Highest risk</span></div>
        <div class="metric"><strong>Rust</strong><span>Core scoring</span></div>
      </div>
    </section>
    <section class="depth">
      <div class="section-head">
        <h2>What this product does</h2>
        <div class="section-note">market risk / route priority / execution trust</div>
      </div>
      <div class="depth-grid">{depth_cards}</div>
    </section>
    <h2>Latency lanes</h2>
    <section class="grid">{cards}</section>
    <section class="recommendation"><strong>Primary recommendation</strong><p>{console["primary_recommendation"]}</p></section>
    <footer>Kinetic Gain synthetic proof surface. No production market data, venues credentials, or trading records included.</footer>
  </main>
</body>
</html>"""
    SITE.mkdir(exist_ok=True)
    (SITE / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
