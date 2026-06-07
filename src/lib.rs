use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct LatencyLane {
    pub name: String,
    pub venue: String,
    pub owner: String,
    pub budget_micros: u32,
    pub p50_micros: u32,
    pub p95_micros: u32,
    pub p99_micros: u32,
    pub jitter_micros: u32,
    pub packet_loss_bps: u32,
    pub retry_rate_bps: u32,
    pub revenue_at_risk_usd: u64,
    pub next_action: String,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct LatencyInput {
    pub organization: String,
    pub generated_at: String,
    pub lanes: Vec<LatencyLane>,
}

#[derive(Debug, Clone, Serialize)]
pub struct ScoredLatencyLane {
    #[serde(flatten)]
    pub lane: LatencyLane,
    pub budget_pressure: i32,
    pub risk_score: u32,
    pub tier: String,
    pub routing_note: String,
}

#[derive(Debug, Clone, Serialize)]
pub struct LatencyConsole {
    pub organization: String,
    pub generated_at: String,
    pub primary_recommendation: String,
    pub lanes: Vec<ScoredLatencyLane>,
}

pub fn classify_tier(risk_score: u32) -> &'static str {
    match risk_score {
        0..=39 => "STABLE",
        40..=59 => "WATCH",
        60..=79 => "ROUTE",
        _ => "ESCALATE",
    }
}

pub fn score_lane(lane: LatencyLane) -> ScoredLatencyLane {
    let budget_pressure = lane.p99_micros as i32 - lane.budget_micros as i32;
    let pressure_points =
        ((budget_pressure.max(0) as f64 / lane.budget_micros as f64) * 55.0).round() as u32;
    let jitter_points = (lane.jitter_micros / 12).min(18);
    let loss_points = (lane.packet_loss_bps / 4).min(12);
    let retry_points = (lane.retry_rate_bps / 6).min(12);
    let tail_points = if lane.p95_micros > lane.budget_micros {
        10
    } else {
        0
    };
    let risk_score =
        (pressure_points + jitter_points + loss_points + retry_points + tail_points).min(100);
    let tier = classify_tier(risk_score).to_string();
    let routing_note = match tier.as_str() {
        "ESCALATE" => format!(
            "{} needs immediate latency-budget routing before tail latency becomes trading loss.",
            lane.name
        ),
        "ROUTE" => format!(
            "{} should be routed into a remediation packet with p99, jitter, and retry evidence.",
            lane.name
        ),
        "WATCH" => format!(
            "{} is inside the watch band; keep p95 and jitter evidence attached.",
            lane.name
        ),
        _ => format!(
            "{} is stable enough for standard market-path monitoring.",
            lane.name
        ),
    };
    ScoredLatencyLane {
        lane,
        budget_pressure,
        risk_score,
        tier,
        routing_note,
    }
}

pub fn build_console(input: LatencyInput) -> LatencyConsole {
    let mut lanes: Vec<ScoredLatencyLane> = input.lanes.into_iter().map(score_lane).collect();
    lanes.sort_by(|a, b| b.risk_score.cmp(&a.risk_score));
    let weakest = &lanes[0];
    LatencyConsole {
        organization: input.organization,
        generated_at: input.generated_at,
        primary_recommendation: format!(
            "Fix {} first; it has the highest market-path latency risk.",
            weakest.lane.name
        ),
        lanes,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn classifies_tiers() {
        assert_eq!(classify_tier(20), "STABLE");
        assert_eq!(classify_tier(45), "WATCH");
        assert_eq!(classify_tier(70), "ROUTE");
        assert_eq!(classify_tier(88), "ESCALATE");
    }

    #[test]
    fn scores_tail_latency_pressure() {
        let lane = LatencyLane {
            name: "Equities order gateway".into(),
            venue: "NYSE".into(),
            owner: "Low-latency trading".into(),
            budget_micros: 900,
            p50_micros: 410,
            p95_micros: 930,
            p99_micros: 1380,
            jitter_micros: 180,
            packet_loss_bps: 22,
            retry_rate_bps: 34,
            revenue_at_risk_usd: 2_800_000,
            next_action: "Pin gateway jitter and isolate retry storms.".into(),
        };
        let scored = score_lane(lane);
        assert_eq!(scored.tier, "ROUTE");
        assert!(scored.budget_pressure > 0);
        assert!(scored.routing_note.contains("remediation packet"));
    }
}
