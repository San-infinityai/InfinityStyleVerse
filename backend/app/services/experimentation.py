import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, Tuple, Optional

def calculate_cuped_adjusted_metric(
    control_metric: np.ndarray,
    control_covariate: np.ndarray,
    treatment_metric: np.ndarray,
    treatment_covariate: np.ndarray,
    alpha: float = 0.05
) -> Dict:
    """
    Apply CUPED adjustment with proper statistical inference.
    
    Args:
        control_metric: Array of observed outcomes for control group
        control_covariate: Pre-experiment covariates for control group  
        treatment_metric: Array of observed outcomes for treatment group
        treatment_covariate: Pre-experiment covariates for treatment group
        alpha: Significance level for confidence intervals
        
    Returns:
        Dictionary with adjusted means, statistics, and confidence intervals
    """
    
    # Input validation
    if len(control_metric) != len(control_covariate):
        raise ValueError("Control metric and covariate arrays must have same length")
    if len(treatment_metric) != len(treatment_covariate):
        raise ValueError("Treatment metric and covariate arrays must have same length")
    
    # Combine data for theta estimation
    X = np.concatenate([control_covariate, treatment_covariate])
    Y = np.concatenate([control_metric, treatment_metric])
    
    # Estimate theta (using population estimates - ddof=0)
    cov_xy = np.cov(X, Y, ddof=0)[0, 1]
    var_x = np.var(X, ddof=0)
    
    if var_x == 0:
        # If no variance in covariate, CUPED provides no benefit
        theta = 0
        print("Warning: Zero variance in covariate. CUPED adjustment has no effect.")
    else:
        theta = cov_xy / var_x
    
    # Calculate pooled covariate mean
    x_mean = np.mean(X)
    
    # Apply CUPED adjustment
    control_adj = control_metric - theta * (control_covariate - x_mean)
    treatment_adj = treatment_metric - theta * (treatment_covariate - x_mean)
    
    # Calculate means
    control_mean_raw = np.mean(control_metric)
    treatment_mean_raw = np.mean(treatment_metric)
    control_mean_cuped = np.mean(control_adj)
    treatment_mean_cuped = np.mean(treatment_adj)
    
    # Calculate uplifts
    uplift_raw = treatment_mean_raw - control_mean_raw
    uplift_cuped = treatment_mean_cuped - control_mean_cuped
    
    # Calculate variances and standard errors
    var_control_raw = np.var(control_metric, ddof=1)
    var_treatment_raw = np.var(treatment_metric, ddof=1)
    var_control_cuped = np.var(control_adj, ddof=1)
    var_treatment_cuped = np.var(treatment_adj, ddof=1)
    
    # Standard errors for uplift
    se_raw = np.sqrt(var_control_raw / len(control_metric) + 
                     var_treatment_raw / len(treatment_metric))
    se_cuped = np.sqrt(var_control_cuped / len(control_adj) + 
                       var_treatment_cuped / len(treatment_adj))
    
    # T-test statistics
    if se_raw > 0:
        t_stat_raw = uplift_raw / se_raw
        df_raw = len(control_metric) + len(treatment_metric) - 2
        p_value_raw = 2 * (1 - stats.t.cdf(abs(t_stat_raw), df_raw))
        
        # Confidence intervals for raw uplift
        t_critical_raw = stats.t.ppf(1 - alpha/2, df_raw)
        ci_raw_lower = uplift_raw - t_critical_raw * se_raw
        ci_raw_upper = uplift_raw + t_critical_raw * se_raw
    else:
        t_stat_raw = p_value_raw = float('nan')
        ci_raw_lower = ci_raw_upper = uplift_raw
    
    if se_cuped > 0:
        t_stat_cuped = uplift_cuped / se_cuped
        df_cuped = len(control_adj) + len(treatment_adj) - 2
        p_value_cuped = 2 * (1 - stats.t.cdf(abs(t_stat_cuped), df_cuped))
        
        # Confidence intervals for CUPED uplift
        t_critical_cuped = stats.t.ppf(1 - alpha/2, df_cuped)
        ci_cuped_lower = uplift_cuped - t_critical_cuped * se_cuped
        ci_cuped_upper = uplift_cuped + t_critical_cuped * se_cuped
    else:
        t_stat_cuped = p_value_cuped = float('nan')
        ci_cuped_lower = ci_cuped_upper = uplift_cuped
    
    # Variance reduction calculation
    var_pooled_raw = np.var(Y, ddof=1)
    var_pooled_cuped = np.var(np.concatenate([control_adj, treatment_adj]), ddof=1)
    
    if var_pooled_raw > 0:
        var_reduction = (var_pooled_raw - var_pooled_cuped) / var_pooled_raw
    else:
        var_reduction = 0
    
    # Relative efficiency (how much smaller sample size needed with CUPED)
    if se_raw > 0:
        relative_efficiency = (se_raw / se_cuped) ** 2 if se_cuped > 0 else float('inf')
    else:
        relative_efficiency = 1.0
    
    return {
        # Theta and adjustment info
        "theta": theta,
        "covariate_mean": x_mean,
        "covariate_outcome_corr": np.corrcoef(X, Y)[0, 1],
        
        # Raw results
        "control_mean_raw": control_mean_raw,
        "treatment_mean_raw": treatment_mean_raw,
        "uplift_raw": uplift_raw,
        "se_raw": se_raw,
        "t_stat_raw": t_stat_raw,
        "p_value_raw": p_value_raw,
        "ci_raw": (ci_raw_lower, ci_raw_upper),
        
        # CUPED results  
        "control_mean_cuped": control_mean_cuped,
        "treatment_mean_cuped": treatment_mean_cuped,
        "uplift_cuped": uplift_cuped,
        "se_cuped": se_cuped,
        "t_stat_cuped": t_stat_cuped,
        "p_value_cuped": p_value_cuped,
        "ci_cuped": (ci_cuped_lower, ci_cuped_upper),
        
        # Efficiency metrics
        "var_reduction": var_reduction,
        "relative_efficiency": relative_efficiency,
        "se_reduction": (se_raw - se_cuped) / se_raw if se_raw > 0 else 0,
        
        # Sample sizes
        "n_control": len(control_metric),
        "n_treatment": len(treatment_metric),
        "n_total": len(control_metric) + len(treatment_metric)
    }


def validate_cuped_aa_test(
    n_simulations: int = 100,
    sample_size: int = 1000,
    alpha: float = 0.05,
    random_seed: Optional[int] = None
) -> Dict:
    """
    Validate CUPED implementation with A/A test simulation.
    Should show no false positives (Type I error rate ≈ alpha).
    
    Args:
        n_simulations: Number of A/A tests to simulate
        sample_size: Sample size per group  
        alpha: Significance level
        random_seed: Random seed for reproducibility
        
    Returns:
        Validation results with Type I error rates
    """
    if random_seed is not None:
        np.random.seed(random_seed)
    
    p_values_raw = []
    p_values_cuped = []
    var_reductions = []
    
    for i in range(n_simulations):
        # Generate A/A test data (no treatment effect)
        pre_metric = np.random.normal(0, 1, size=2*sample_size)
        
        # Random assignment
        treatment = np.random.binomial(1, 0.5, size=2*sample_size)
        
        # Outcome correlated with pre-metric but NO treatment effect
        outcome = 0.5 + 0.3 * pre_metric + np.random.normal(0, 0.4, size=2*sample_size)
        
        # Split by treatment
        control_mask = treatment == 0
        treatment_mask = treatment == 1
        
        try:
            results = calculate_cuped_adjusted_metric(
                control_metric=outcome[control_mask],
                control_covariate=pre_metric[control_mask],
                treatment_metric=outcome[treatment_mask], 
                treatment_covariate=pre_metric[treatment_mask],
                alpha=alpha
            )
            
            p_values_raw.append(results["p_value_raw"])
            p_values_cuped.append(results["p_value_cuped"])
            var_reductions.append(results["var_reduction"])
            
        except Exception as e:
            print(f"Error in simulation {i}: {e}")
            continue
    
    # Calculate Type I error rates
    type_i_error_raw = np.mean(np.array(p_values_raw) < alpha)
    type_i_error_cuped = np.mean(np.array(p_values_cuped) < alpha)
    
    return {
        "n_simulations": len(p_values_raw),
        "alpha": alpha,
        "type_i_error_raw": type_i_error_raw,
        "type_i_error_cuped": type_i_error_cuped,
        "expected_type_i_error": alpha,
        "raw_within_bounds": abs(type_i_error_raw - alpha) < 2 * np.sqrt(alpha * (1-alpha) / len(p_values_raw)),
        "cuped_within_bounds": abs(type_i_error_cuped - alpha) < 2 * np.sqrt(alpha * (1-alpha) / len(p_values_raw)),
        "mean_var_reduction": np.mean(var_reductions),
        "p_values_raw": p_values_raw[:10],  # First 10 for inspection
        "p_values_cuped": p_values_cuped[:10]
    }


# Example usage and testing
if __name__ == "__main__":
    # Run A/A validation test
    print("Running A/A validation test...")
    validation_results = validate_cuped_aa_test(n_simulations=100, random_seed=42)
    
    print(f"Type I Error Rate (Raw): {validation_results['type_i_error_raw']:.3f}")
    print(f"Type I Error Rate (CUPED): {validation_results['type_i_error_cuped']:.3f}")
    print(f"Expected: {validation_results['alpha']:.3f}")
    print(f"Mean Variance Reduction: {validation_results['mean_var_reduction']:.3f}")
    print(f"Raw within bounds: {validation_results['raw_within_bounds']}")
    print(f"CUPED within bounds: {validation_results['cuped_within_bounds']}")