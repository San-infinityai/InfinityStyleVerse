import json

# Mock constraints from ai_requests
constraints = [
    {"latency_max_ms": 1000, "cost_max_cents": 5},  # Fast
    {"latency_max_ms": 2000, "cost_max_cents": 10}, # Accurate
]

def propose_routes(constraints):
    policies = []
    for const in constraints:
        if const["latency_max_ms"] < 1500:  # Fast threshold
            dag = ["eco", "style"]  # Simplified DAG
            alpha = 0.2  # Low α for speed
            route = "fast"
        else:
            dag = ["style", "eco", "trend"]  # Full DAG
            alpha = 0.5  # Higher α for accuracy
            route = "accurate"
        policies.append({"constraints": const, "route": route, "dag": dag, "alpha": alpha})
    return policies

# Generate and save policy JSON
policies = propose_routes(constraints)
with open("planner_policies.json", "w") as f:
    json.dump(policies, f)
print("planner_policies.json generated")