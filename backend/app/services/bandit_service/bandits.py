import numpy as np

class BanditBase:
    def __init__(self, n_arms):
        self.n_arms = n_arms  # Arms is the number of options
        self.counts = np.zeros(n_arms)  # Times each arm will be chosen
        self.rewards = np.zeros(n_arms)  # Total rewards per arm

    def select_arm(self):   # Deciding which option to recommend to users
        raise NotImplementedError("Subclasses must implement select_arm")

    def update(self, chosen_arm, reward):   # Updating the bandit's data after a choice
        self.counts[chosen_arm] += 1
        self.rewards[chosen_arm] += reward

class ThompsonSampling(BanditBase):
    def __init__(self, n_arms):
        super().__init__(n_arms)
        self.successes = np.zeros(n_arms)  # Number of successes
        self.failures = np.zeros(n_arms)  # Number of failures

    def select_arm(self):
        samples = np.random.beta(self.successes + 1, self.failures + 1)
        return np.argmax(samples)

    def update(self, chosen_arm, reward):
        super().update(chosen_arm, reward)
        self.successes[chosen_arm] += reward
        self.failures[chosen_arm] += 1 - reward

class LinUCB(BanditBase):
    def __init__(self, n_arms, dim, alpha=1.0):
        super().__init__(n_arms)
        self.dim = dim  # Feature dimension
        self.alpha = alpha  # Exploration parameter
        self.A = np.array([np.identity(dim) for _ in range(n_arms)])  # Covariance matrices
        self.b = np.zeros((n_arms, dim))  # Reward vectors
        self.theta = np.zeros((n_arms, dim))  # Estimated coefficients

    def select_arm(self, context):
        p = np.array([self.theta[i] @ context + self.alpha * np.sqrt(context @ np.linalg.inv(self.A[i]) @ context)
                     for i in range(self.n_arms)])
        return np.argmax(p)

    def update(self, chosen_arm, reward, context):
        super().update(chosen_arm, reward)
        x = context.reshape(-1, 1)
        self.A[chosen_arm] += x @ x.T
        self.b[chosen_arm] += reward * x.flatten()
        self.theta[chosen_arm] = np.linalg.inv(self.A[chosen_arm]) @ self.b[chosen_arm]

# Placeholder for Logistic-UCB 
class LogisticUCB(BanditBase):
    def __init__(self, n_arms, dim):
        super().__init__(n_arms)
        self.dim = dim
        self.A = np.array([np.identity(dim) for _ in range(n_arms)])
        self.b = np.zeros((n_arms, dim))

    def select_arm(self, context):
        # Using a simplified LinUCB-like approach for now
        p = np.array([np.random.random() for _ in range(self.n_arms)])  # Placeholder
        return np.argmax(p)

    def update(self, chosen_arm, reward, context):
        super().update(chosen_arm, reward)
        # Placeholder update