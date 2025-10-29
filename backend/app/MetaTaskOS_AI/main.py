from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional
from bandits import ThompsonSampling, LinUCB, LogisticUCB
from rollouts import RolloutManager
import numpy as np
import json
import datetime

app = FastAPI(title="Bandit Microservice")

# Initializing the bandits (3 arms and context dimension - 5)
thompson = ThompsonSampling(n_arms=3)
linucb = LinUCB(n_arms=3, dim=5, alpha=1.0)
logisticucb = LogisticUCB(n_arms=3, dim=5)

rollout_managers = {
    "outfit_ranking": RolloutManager("outfit_ranking"),
    "price_nudge": RolloutManager("price_nudge")
}

# Request Models 
class SelectArmRequest(BaseModel):
    task: str
    request_id: str
    user_id: str
    context: Optional[List[float]] = None

class UpdateRequest(BaseModel):
    chosen_arm: int = Field(ge=0)
    reward: float
    task: str
    request_id: str
    context: Optional[List[float]] = None
    
def log_propensity(task, request_id, context, arm, propensities, reward=None, variant='bandit'):
    log_entry = {
        "task": task,
        "request_id": request_id,
        "context": context.tolist() if context is not None else None,
        "arm": arm,
        "propensities": propensities,
        "reward": reward,
        "timestamp": str(datetime.datetime.now()),
        "variant": variant
    }
    with open("propensity_logs.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")    
    
@app.post("/select_arm")
async def select_arm(req: SelectArmRequest):
    task = req.task
    context = np.array(req.context) if req.context else np.zeros(5)
    manager = rollout_managers.get(task)
    variant = manager.decide_rollout(req.user_id) if manager else 'bandit'
    
    if variant == 'control':
        arm = 0  # Fixed policy
        propensities = [1.0 if i == 0 else 0.0 for i in range(3)]
        uncertainties = None
        confidence_bounds = None
        method = "fixed"
        context_used = None
    else:
        if task == "outfit_ranking":
            response = thompson.select_arm()
            method = "ThompsonSampling"
            context_used = None
        elif task == "price_nudge":
            response = linucb.select_arm(context)
            method = "LinUCB"
            context_used = req.context
        else:
            response = logisticucb.select_arm(context)
            method = "LogisticUCB"
            context_used = req.context
        arm = response["arm"]
        propensities = response["propensities"]
        uncertainties = response.get("uncertainties")
        confidence_bounds = response["confidence_bounds"]

    log_propensity(task, req.request_id, np.array(req.context), arm, propensities, variant=variant)
    
    return {
        "task": task,
        "selected_arm": arm,
        "method": method,
        "context_used": context_used,
        "propensities": propensities,
        "confidence_bounds": confidence_bounds,
        "uncertainties": uncertainties
    }

@app.post("/update")
async def update(req: UpdateRequest):
    chosen_arm = req.chosen_arm
    reward = req.reward
    task = req.task
    context = np.array(req.context) if req.context else np.zeros(5)

    if task == "outfit_ranking":
        thompson.update(chosen_arm, reward)
    elif task == "price_nudge":
        linucb.update(chosen_arm, reward, context)
    else:
        logisticucb.update(chosen_arm, reward, context)
        
    log_propensity(task, req.request_id, context, chosen_arm, None, reward=reward)
    return {"status": "updated", "task": task, "chosen_arm": chosen_arm, "reward": reward}

@app.get("/echo/policy/{task}")
async def get_policy(task: str):
    if task == "outfit_ranking":
        weights = {"successes": thompson.successes.tolist(), "failures": thompson.failures.tolist()}
    elif task == "price_nudge":
        weights = {"theta": linucb.theta.tolist()}
    else:
        weights = {"theta": logisticucb.theta.tolist()}
    manager = rollout_managers.get(task)
    rollout_config = {"stage": manager.stage, "canary_percent": manager.canary_percent} if manager else {}
    return {"weights": weights, "rollout_config": rollout_config}

@app.post("/check_rollout")
async def check_rollout(task: str):
    manager = rollout_managers.get(task)
    if not manager:
        return {"error": "No rollout manager for task"}
    return manager.check_guardrails("propensity_logs.jsonl")