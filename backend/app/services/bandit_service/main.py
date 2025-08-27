from fastapi import FastAPI
from bandits import ThompsonThompsonSampling, LinUCB, LogisticUCB
import numpy as np

app = FastAPI(title="Bandit Microservice")

# Initializing the bandits (3 arms and context dimension - 5)
thompson = ThompsonSampling(n_arms=3)
linucb = LinUCB(n_arms=3, dim=5, alpha=1.0)
logisticucb = LogisticUCB(n_arms=3, dim=5)

@app.post("/select_arm")
async def select_arm(task: str, context: list[float] = None):
    """
    Select an option (arm) based on the task and optional context.
    Task - 'outfit_ranking' or 'price_nudge'
    Context - List of features, Eg: (age, region, event) if provided
    """
    if context is None:
        context = np.zeros(5)  # Default context of zeroes if it is not provided

    if task == "outfit_ranking":
        arm = thompson.select_arm()
        return {"task": task, "selected_arm": int(arm), "method": "ThompsonSampling"}
    elif task == "price_nudge":
        arm = linucb.select_arm(np.array(context))
        return {"task": task, "selected_arm": int(arm), "method": "LinUCB", "context_used": context}
    else:
        arm = logisticucb.select_arm(np.array(context))
        return {"task": task, "selected_arm": int(arm), "method": "LogisticUCB", "context_used": context}

@app.post("/update")
async def update(chosen_arm: int, reward: float, task: str, context: list[float] = None):
    """
    Updating the bandit model with the chosen arm, reward, and optional context.
    - chosen_arm is the index of the selected arm
    - reward is the reward value (Eg: 1.0 point for success)
    - task is 'outfit_ranking' or 'price_nudge'
    - context is a list of features if given
    """
    if context is None:
        context = np.zeros(5) 

    if task == "outfit_ranking":
        thompson.update(chosen_arm, reward)
    elif task == "price_nudge":
        linucb.update(chosen_arm, reward, np.array(context))
    else:
        logisticucb.update(chosen_arm, reward, np.array(context))
    return {"status": "updated", "task": task, "chosen_arm": chosen_arm, "reward": reward}