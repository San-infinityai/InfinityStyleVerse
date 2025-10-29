import numpy as np
from typing import Callable, Dict, Any


class RewardFunctions:
    @staticmethod
    def clicks(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        return np.sum(y_true)

    @staticmethod
    def conversions(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        return np.sum(y_true)

    @staticmethod
    def revenue(y_true: np.ndarray, y_pred: np.ndarray, values: np.ndarray) -> float:
        return np.sum(y_true * values)

    @staticmethod
    def engagement(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        return float(np.mean(y_true))


def get_reward_function(task: str, tenant: str, config: Dict[str, Any]) -> Callable:
    fn_name = config.get(tenant, {}).get(task, "clicks")

    if not hasattr(RewardFunctions, fn_name):
        raise ValueError(f"Reward function '{fn_name}' not defined.")

    return getattr(RewardFunctions, fn_name)