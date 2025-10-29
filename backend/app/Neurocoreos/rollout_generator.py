import json

rollout_plan = {
    "stages": [
        {"stage": "shadow", "percent": 0, "duration": "2 days", "guardrails": {"latency_p95": 800, "return_rate_uplift": 0.02}},
        {"stage": "canary", "percent": 5, "duration": "3 days", "guardrails": {"latency_p95": 800, "return_rate_uplift": 0.02}},
        {"stage": "full", "percent": 100, "duration": "ongoing", "guardrails": {"latency_p95": 800, "return_rate_uplift": 0.02}}
    ],
    "uplift_target": 0.05,  # ≥ +5%
    "notes": "Rollout new weights if uplift ≥5% and no latency regression"
}

with open("rollout_plan.json", "w") as f:
    json.dump(rollout_plan, f)
print("rollout_plan.json generated")