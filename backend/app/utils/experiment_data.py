import numpy as np
import pandas as pd

def fetch_experiment_data(experiment_id: str, num_samples: int = 1000) -> pd.DataFrame:
    """
    Mock function to simulate experiment data.
    In production, this will query Postgres for decisions + outcomes.
    """
    np.random.seed(42)

    # Random assignment to control (0) or treatment (1)
    treatment = np.random.binomial(1, 0.5, size=num_samples)

    # Pre-experiment covariate (e.g., prior engagement score)
    pre_metric = np.random.normal(loc=0.0, scale=1.0, size=num_samples)

    # True effect (seeded uplift for testing, can set =0 for A/A)
    true_effect = 0.05  

    # Outcome: baseline + treatment effect + noise
    outcome = 0.5 + 0.2 * pre_metric + true_effect * treatment + np.random.normal(0, 0.3, size=num_samples)

    return pd.DataFrame({
        "experiment_id": experiment_id,
        "treatment": treatment,
        "pre_metric": pre_metric,
        "outcome": outcome
    })
