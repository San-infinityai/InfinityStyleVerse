import numpy as np
import json
import datetime
from bandits import ThompsonSampling, LinUCB  # Import bandits

def ips_uplift(logs_path, fixed_policy_arm=0):
    with open(logs_path, "r") as f:
        logs = [json.loads(line) for line in f if line.strip()]
    corrected_rewards = []
    control_rewards = []
    for log in logs:
        if log['reward'] is not None:
            if log.get('variant') == 'control':
                control_rewards.append(log['reward'])
            else:
                prop = log['propensities'][log['arm']]
                if prop > 0:
                    corrected_rewards.append(log['reward'] / prop)

    if len(corrected_rewards) == 0 or len(control_rewards) == 0:
        return 0.0
    mean_corrected = np.mean(corrected_rewards)
    mean_control = np.mean(control_rewards)
    uplift = mean_corrected - mean_control
    return uplift

def dr_uplift(logs_path, reward_model=None):  # Simple DR, reward_model estimates reward(context, arm)
    # Extension of IPS with bias correction; implement reward_model as needed
    with open(logs_path, "r") as f:
        logs = [json.loads(line) for line in f if line.strip()]
    corrected_rewards = []
    for log in logs:
        if log['reward'] is not None and log.get('variant') != 'control':
            prop = log['propensities'][log['arm']]
            if prop > 0:
                estimated = reward_model(log['context'], log['arm']) if reward_model else 0
                corrected_rewards.append(estimated + (log['reward'] - estimated) / prop)
    if not corrected_rewards:
        return 0.0
    return np.mean(corrected_rewards) - 0.5  # Assume fixed mean 0.5

def simulate_bandit(bandit, n_steps, task, logs_path, use_rollout=False, dim=5):
    # True reward probabilities for arms
    true_probs = [0.5, 0.6, 0.7]  # arm0 fixed-like, better arms
    true_theta = np.random.normal(0, 1, (3, dim))  # For contextual

    with open(logs_path, 'w') as f:  # Clear log
        pass

    for step in range(n_steps):
        request_id = f"sim_{step}"
        user_id = f"user_{step % 10}"  # Simulate users
        context = np.random.normal(0, 1, dim) if hasattr(bandit, 'dim') else None
        
        # Simulate variant: 50% control, 50% bandit for comparison
        variant = 'control' if np.random.random() < 0.5 else 'bandit'
        
        if variant == 'control':
            arm = 0
            propensities = [1.0, 0.0, 0.0]
        else:
            response = bandit.select_arm(context)
            arm = response['arm']
            propensities = response['propensities']
        
        # Simulate reward
        if context is not None:
            mean = true_theta[arm] @ context
            reward = np.random.binomial(1, 1 / (1 + np.exp(-mean)))
        else:
            reward = np.random.binomial(1, true_probs[arm])
        
        # Update if bandit
        if variant == 'bandit':
            bandit.update(arm, reward, context)
        
        # Log
        log_entry = {
            "task": task,
            "request_id": request_id,
            "context": context.tolist() if context is not None else None,
            "arm": arm,
            "propensities": propensities,
            "reward": float(reward),
            "timestamp": str(datetime.datetime.now()),
            "variant": variant
        }
        with open(logs_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

# Sandbox to verify uplift 
if __name__ == "__main__":
    #Simulate Thompson
    thompson = ThompsonSampling(n_arms=3)
    simulate_bandit(thompson, n_steps=4000, task='outfit_ranking', logs_path='thompson_logs.jsonl')
    print("Thompson IPS Uplift:", ips_uplift('thompson_logs.jsonl'))

    # Simulate LinUCB
    linucb = LinUCB(n_arms=3, dim=5, alpha=1.0)
    simulate_bandit(linucb, n_steps=4000, task='price_nudge', logs_path='linucb_logs.jsonl')
    print("LinUCB IPS Uplift:", ips_uplift('linucb_logs.jsonl'))