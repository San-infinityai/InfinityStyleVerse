import pandas as pd
import json
import random
from datetime import datetime, timedelta

num_runs = 500
agents = ["StylistAgent", "TrendAgent", "EcoAgent", "CultureAgent", "Aggregator", "Verifier", "PersonaAgent", "ReturnRiskAgent", "ElasticityAgent", "DemandAgent"]
tasks = ["design_recommendation", "personalized_outfit", "dynamic_pricing"]
modes = ["fast", "thorough"]
tenants = ["tenant_a", "tenant_b", "tenant_c", "tenant_d"]  # Sample tenants

# Generating data for the runs table
runs_data = []
for i in range(num_runs):
    run_id = f"run_{i:03d}"
    task = random.choice(tasks)
    tenant = random.choice(tenants)
    status = random.choice(["succeeded", "failed"]) if random.random() < 0.8 else "succeeded"
    mode = random.choice(modes)
    budget = {"max_latency_ms": random.randint(1000, 3000), "max_cost_cents": random.randint(5, 15)}
    policy = {"eco_min_score": 0.7, "culture_check": True} if random.random() > 0.1 else {"eco_min_score": 0.4, "culture_check": False}
    started_at = datetime.now() - timedelta(days=random.randint(1, 30))
    ended_at = started_at + timedelta(seconds=random.randint(100, 2000))
    cost_cents = round(random.uniform(1.0, 10.0), 2)
    latency_ms = random.randint(500, 2500)
    reward = round(min(1.0, max(0.0, 0.5 + (random.random() - 0.3) + (cost_cents / -20) + (latency_ms / -5000))), 2)  # Synthetic reward, which is penalized by cost and latency
    runs_data.append([run_id, task, tenant, status, mode, json.dumps(budget), json.dumps(policy), started_at, ended_at, cost_cents, latency_ms, reward])

runs_df = pd.DataFrame(runs_data, columns=["id", "task", "tenant", "status", "mode", "budget_json", "policy_json", "started_at", "ended_at", "cost_cents", "latency_ms", "reward"])
runs_df.to_csv("synthetic_runs.csv", index=False)

# Generating data for the messages table
messages_data = []
for run_id in runs_df["id"]:
    num_turns = random.randint(2, 5)
    for turn in range(num_turns):
        msg_id = f"msg_{run_id}_{turn}"
        agent = random.choice(agents)
        role = "assistant"
        content = f"Sample output from {agent}..."
        tools = [{"name": f"{agent}Tool.search", "args": {"tags": [random.choice(["streetwear", "neon", "sustainable"])]}, "latency_ms": random.randint(100, 500)}]
        confidence = round(random.uniform(0.5, 0.95), 2)
        cost_cents = round(random.uniform(0.5, 2.0), 2)
        created_at = datetime.now() - timedelta(days=random.randint(1, 30))
        messages_data.append([msg_id, run_id, turn, agent, role, content, json.dumps(tools), confidence, cost_cents, created_at])

messages_df = pd.DataFrame(messages_data, columns=["id", "run_id", "turn", "agent", "role", "content", "tools_json", "confidence", "cost_cents", "created_at"])
messages_df.to_csv("synthetic_messages.csv", index=False)

print("Data generated and saved")