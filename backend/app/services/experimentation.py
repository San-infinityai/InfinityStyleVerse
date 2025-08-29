import numpy as np
import pandas as pd

def calculate_cuped_adjusted_metric(control_metric: np.ndarray,
                                    control_covariate: np.ndarray,
                                    treatment_metric: np.ndarray,
                                    treatment_covariate: np.ndarray) -> dict:
    """
    Apply CUPED adjustment.
    control_metric / treatment_metric: arrays of observed outcomes.
    control_covariate / treatment_covariate: pre-experiment covariates.
    Returns adjusted means and theta.
    """

    # Stack covariates
    X = np.concatenate([control_covariate, treatment_covariate])
    Y = np.concatenate([control_metric, treatment_metric])

    # Estimate theta (cov(X,Y)/var(X))
    theta = np.cov(X, Y, ddof=1)[0,1] / np.var(X, ddof=1)

    # Apply CUPED
    control_adj = control_metric - theta * (control_covariate - np.mean(X))
    treatment_adj = treatment_metric - theta * (treatment_covariate - np.mean(X))

    return {
        "theta": theta,
        "control_mean_raw": np.mean(control_metric),
        "treatment_mean_raw": np.mean(treatment_metric),
        "control_mean_cuped": np.mean(control_adj),
        "treatment_mean_cuped": np.mean(treatment_adj),
        "uplift_raw": np.mean(treatment_metric) - np.mean(control_metric),
        "uplift_cuped": np.mean(treatment_adj) - np.mean(control_adj),
        "var_reduction": (np.var(Y, ddof=1) - np.var(np.concatenate([control_adj, treatment_adj]), ddof=1)) / np.var(Y, ddof=1)
    }