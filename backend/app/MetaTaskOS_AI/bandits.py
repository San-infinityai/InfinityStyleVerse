import numpy as np
from scipy.stats import beta
from scipy.optimize import minimize

class BanditBase:
    def __init__(self, n_arms):
        self.n_arms = n_arms  # Number of options
        self.counts = np.zeros(n_arms)  # Times each arm chosen
        self.rewards = np.zeros(n_arms)  # Total rewards per arm

    def select_arm(self, context=None):
        raise NotImplementedError("Subclasses must implement select_arm")

    def update(self, chosen_arm, reward, context=None):
        self.counts[chosen_arm] += 1
        self.rewards[chosen_arm] += reward


class ThompsonSampling(BanditBase):
    def __init__(self, n_arms, exploration_floor=0.05):
        super().__init__(n_arms)
        self.successes = np.zeros(n_arms)
        self.failures = np.zeros(n_arms)
        self.exploration_floor = exploration_floor

    def select_arm(self, context=None):
        if np.random.random() < self.exploration_floor:
            arm = np.random.randint(self.n_arms)
            propensities = np.ones(self.n_arms) / self.n_arms
        else:
            samples = np.random.beta(self.successes + 1, self.failures + 1)
            arm = int(np.argmax(samples))
            exp_samples = np.exp(samples)
            propensities = exp_samples / np.sum(exp_samples)

        variances = beta.var(self.successes + 1, self.failures + 1)
        confidence_bounds = beta.interval(0.95, self.successes + 1, self.failures + 1)

        response = {
            "arm": int(arm),
            "propensities": propensities.tolist(),
            "confidence_bounds": [(float(low), float(high)) for low, high in zip(*confidence_bounds)],
            "variances": variances.tolist() if isinstance(variances, np.ndarray) else float(variances)
        }

        return response

    def update(self, chosen_arm, reward, context=None):
        super().update(chosen_arm, reward)
        self.successes[chosen_arm] += reward
        self.failures[chosen_arm] += 1 - reward


class LinUCB(BanditBase):
    def __init__(self, n_arms, dim, alpha=1.0, exploration_floor=0.05):
        super().__init__(n_arms)
        self.dim = dim
        self.alpha = alpha
        self.exploration_floor = exploration_floor
        self.A = np.array([np.identity(dim) for _ in range(n_arms)])
        self.b = np.zeros((n_arms, dim))
        self.theta = np.zeros((n_arms, dim))

    def select_arm(self, context):
        if np.random.random() < self.exploration_floor:
            arm = np.random.randint(self.n_arms)
            propensities = np.ones(self.n_arms) / self.n_arms
        else:
            p = np.array([
                self.theta[i] @ context + self.alpha * np.sqrt(context @ np.linalg.pinv(self.A[i]) @ context)
                for i in range(self.n_arms)
            ])
            arm = int(np.argmax(p))
            exp_scores = np.exp(p / self.alpha)
            propensities = exp_scores / np.sum(exp_scores)

        uncertainties = np.array([
            self.alpha * np.sqrt(context @ np.linalg.pinv(self.A[i]) @ context)
            for i in range(self.n_arms)
        ])
        means = np.array([self.theta[i] @ context for i in range(self.n_arms)])
        confidence_bounds = [(float(means[i] - uncertainties[i]), float(means[i] + uncertainties[i])) 
                             for i in range(self.n_arms)]

        response = {
            "arm": arm,
            "propensities": propensities.tolist(),
            "confidence_bounds": confidence_bounds,
            "uncertainties": uncertainties.tolist()
        }

        return response

    def update(self, chosen_arm, reward, context):
        super().update(chosen_arm, reward)
        x = context.reshape(-1, 1)
        self.A[chosen_arm] += x @ x.T
        self.b[chosen_arm] += reward * x.flatten()
        self.theta[chosen_arm] = np.linalg.pinv(self.A[chosen_arm]) @ self.b[chosen_arm]
        
class LogisticUCB(BanditBase):
    def __init__(self, n_arms, dim, lambda_reg=1.0, exploration_floor=0.05):
        super().__init__(n_arms)
        self.dim = dim
        self.lambda_reg = lambda_reg
        self.exploration_floor = exploration_floor
        self.theta = np.zeros((n_arms, dim))  # Parameters for logistic regression
        self.H = np.array([self.lambda_reg * np.identity(dim) for _ in range(n_arms)])  # Hessian approx

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def select_arm(self, context):
        if np.random.random() < self.exploration_floor:
            arm = np.random.randint(self.n_arms)
            propensities = np.ones(self.n_arms) / self.n_arms
        else:
            means = np.array([self.theta[i] @ context for i in range(self.n_arms)])
            uncertainties = np.array([np.sqrt(context @ np.linalg.pinv(self.H[i]) @ context) for i in range(self.n_arms)])
            ucb_scores = means + uncertainties  # UCB on logistic mean
            arm = int(np.argmax(ucb_scores))
            exp_scores = np.exp(ucb_scores)
            propensities = exp_scores / np.sum(exp_scores)

        confidence_bounds = [(float(means[i] - uncertainties[i]), float(means[i] + uncertainties[i])) 
                             for i in range(self.n_arms)]

        response = {
            "arm": arm,
            "propensities": propensities.tolist(),
            "confidence_bounds": confidence_bounds,
            "uncertainties": uncertainties.tolist()
        }
        return response

    def update(self, chosen_arm, reward, context):
        super().update(chosen_arm, reward)
        x = context.reshape(-1, 1)
        pred = self._sigmoid(self.theta[chosen_arm] @ context)
        grad = (reward - pred) * context
        self.H[chosen_arm] += np.outer(context, context) * pred * (1 - pred)  
        self.theta[chosen_arm] += np.linalg.pinv(self.H[chosen_arm]) @ grad        