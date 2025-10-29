import json
import numpy as np

# Mock data (replace with real from logs/DB)
ai_requests = [
    {"request_id": "req1", "task": "design", "constraints": {"latency_max_ms": 1000, "cost_max_cents": 5}},
    {"request_id": "req2", "task": "price", "constraints": {"latency_max_ms": 2000, "cost_max_cents": 10}},
]
ai_results = [
    {"request_id": "req1", "scores": {"trend": 0.8, "eco": 0.7, "style": 0.9}},
    {"request_id": "req2", "scores": {"trend": 0.6, "eco": 0.8, "style": 0.7}},
]
model_trace = [
    {"request_id": "req1", "dag": ["style", "eco", "trend"], "latency_ms": 900, "cost_cents": 4},
    {"request_id": "req2", "dag": ["trend", "style", "eco"], "latency_ms": 1500, "cost_cents": 8},
]

# Alternative DAGs to evaluate
alternative_dags = [
    ["eco", "trend", "style"],  # Alternative order 1
    ["style", "trend", "eco"],  # Alternative order 2
]

# Weight grids (α=trend, β=eco, γ=style; sum=1)
weight_grids = [
    {"alpha": 0.3, "beta": 0.4, "gamma": 0.3},
    {"alpha": 0.2, "beta": 0.5, "gamma": 0.3},
]

def evaluate_dag_weights(dag, weights, requests, results, trace):
    scores = []
    for req, res, tr in zip(requests, results, trace):
        score = weights["alpha"] * res["scores"]["trend"] + weights["beta"] * res["scores"]["eco"] + weights["gamma"] * res["scores"]["style"]
        scores.append({"dag": dag, "request_id": req["request_id"], "score": score, "latency_ms": tr["latency_ms"]})
    return scores

# Run evaluation
for dag in alternative_dags:
    for weights in weight_grids:
        eval_results = evaluate_dag_weights(dag, weights, ai_requests, ai_results, model_trace)
        print(f"DAG: {dag}, Weights: {weights}, Eval: {eval_results}")

# Save to JSON for reference
with open("eval_results.json", "w") as f:
    json.dump(eval_results, f)