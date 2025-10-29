import numpy as np
import json

# Mock EchoOS logs (replace with real from propensity_logs.jsonl or DB)
echo_logs = [
    {"request_id": "req1", "reward": 0.85, "return_rate_proxy": -0.1, "latency_ms": 900},
    {"request_id": "req2", "reward": 0.75, "return_rate_proxy": -0.2, "latency_ms": 1500},
]

# Baseline reward (fixed policy)
baseline_reward = 0.7

def estimate_uplift(new_weights, logs):
    uplifts = []
    for log in logs:
        uplift = log["reward"] - baseline_reward
        uplifts.append({"request_id": log["request_id"], "uplift": uplift, "weights": new_weights})
    return uplifts

def check_guardrails(uplifts, logs):
    p95_latency = np.percentile([log["latency_ms"] for log in logs], 95)
    return_rate_uplift = np.mean([log["return_rate_proxy"] for log in logs])
    if p95_latency > 800 or return_rate_uplift > 0.02:  # Guardrails
        return False
    return True

# New weights (α)
new_alpha = 0.4  # Example alpha

uplifts = estimate_uplift(new_alpha, echo_logs)
guardrail_pass = check_guardrails(uplifts, echo_logs)
print(f"Uplift: {uplifts}, Guardrail Pass: {guardrail_pass}")