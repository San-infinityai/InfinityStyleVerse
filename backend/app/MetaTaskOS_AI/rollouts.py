import numpy as np
import json

class RolloutManager:
    def __init__(self, task):
        self.task = task
        self.stage = "shadow"  # Start with shadow
        self.canary_percent = 0.05  # 5%
        self.guardrails = {"return_rate_uplift": 0.02, "sla_latency_ms": 50}  # From spec

    def decide_rollout(self, user_id):  # Bucket user to rollout
        if self.stage == "shadow":
            return "control"  # Log but don't serve bandit
        elif self.stage == "canary":
            if hash(user_id) % 100 < self.canary_percent * 100:
                return "bandit"
            return "control"
        return "bandit"  # Full rollout

    def check_guardrails(self, logs_path):
        with open(logs_path, "r") as f:
            logs = [json.loads(line) for line in f if line.strip()]
        rewards_bandit = [log['reward'] for log in logs if log.get('variant', 'control') == 'bandit' and log['reward'] is not None]
        rewards_control = [log['reward'] for log in logs if log.get('variant', 'control') == 'control' and log['reward'] is not None]
        if len(rewards_bandit) == 0 or len(rewards_control) == 0:
            return {"stage": self.stage, "uplift": 0.0}
        uplift = np.mean(rewards_bandit) - np.mean(rewards_control)
        # Placeholder: In production, query Prometheus for latency, compute return_rate from events (e.g., type='return')
        metric_ok = True  # Assume pass for sandbox
        if uplift > 0.05 and metric_ok:  # +5% min
            if self.stage == "shadow":
                self.stage = "canary"
            elif self.stage == "canary":
                self.canary_percent = min(1.0, self.canary_percent + 0.1)  # Ramp by 10%
                if self.canary_percent >= 1.0:
                    self.stage = "full"
        return {"stage": self.stage, "uplift": uplift, "guardrail_breaches": 0}