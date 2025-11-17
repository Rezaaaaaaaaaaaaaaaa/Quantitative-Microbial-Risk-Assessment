"""
Illness Modeling for QMRA

This module provides functions to convert infection probabilities to illness probabilities,
accounting for the difference between pathogen infection and clinical illness.

Key Concept:
- Not all infected individuals become ill
- Different pathogens have different P(ill | infected) values
- Population susceptibility varies by pathogen and demographics

Based on David Wood's R implementation:
- isIllNoro() function in R/isIllNoro.R
- WHO (2016) guidance on QMRA

Author: NIWA Earth Sciences New Zealand
Date: November 2025
"""

import numpy as np
import pandas as pd
from typing import Union, Dict, Optional, Tuple
import warnings


def infection_to_illness(infection_status: Union[np.ndarray, pd.Series],
                        probability_illness_given_infection: float,
                        population_susceptibility: float = 1.0,
                        seed: Optional[int] = None) -> Union[np.ndarray, pd.Series]:
    """
    Convert infection status to illness status using conditional probabilities.

    Formula: P(illness) = P(infection) × P(ill | infected) × susceptibility

    Args:
        infection_status: Binary array/series (1=infected, 0=not infected) or probabilities (0-1)
        probability_illness_given_infection: Fraction of infected who develop symptoms (0-1)
        population_susceptibility: Fraction of population susceptible to pathogen (0-1)
        seed: Random seed for reproducibility

    Returns:
        Array/series of illness status (0 or 1) or illness probability (0-1)

    References:
        - WHO (2016): Quantitative Microbial Risk Assessment: Application for Water Safety Management
        - Teunis et al. (2008): Cryptosporidium and Giardia in ground and drinking water supplies

    Example:
        >>> # For Norovirus: P(ill|inf)=0.60, susceptibility=0.74
        >>> infections = np.array([1, 1, 0, 1, 0, 1])
        >>> illness = infection_to_illness(infections, 0.60, 0.74, seed=42)
        >>> print(f"Infection rate: {infections.mean():.2%}")
        >>> print(f"Illness rate: {illness.mean():.2%}")
    """
    if seed is not None:
        np.random.seed(seed)

    # Convert to numpy array if pandas Series
    is_series = isinstance(infection_status, pd.Series)
    if is_series:
        original_index = infection_status.index
        infection_status = infection_status.values

    infection_status = np.asarray(infection_status)

    # Validate parameters
    if not (0 <= probability_illness_given_infection <= 1):
        raise ValueError(f"P(ill|infected) must be in [0, 1], got {probability_illness_given_infection}")
    if not (0 <= population_susceptibility <= 1):
        raise ValueError(f"Population susceptibility must be in [0, 1], got {population_susceptibility}")

    # Calculate effective illness probability
    adjusted_prob_ill = probability_illness_given_infection * population_susceptibility

    # If infection_status is binary (0/1), convert to illness stochastically
    if np.all((infection_status == 0) | (infection_status == 1)):
        # Binary case: randomly assign illness status
        illness_status = np.zeros_like(infection_status, dtype=float)

        # For infected individuals, apply conditional probability
        infected_mask = infection_status == 1
        if np.any(infected_mask):
            random_values = np.random.uniform(0, 1, np.sum(infected_mask))
            illness_status[infected_mask] = (random_values < adjusted_prob_ill).astype(int)

        result = illness_status
    else:
        # Continuous case: probability interpretation
        # P(illness) = P(infection) × P(ill|infected) × susceptibility
        illness_probability = infection_status * adjusted_prob_ill
        result = illness_probability

    # Return in original format
    if is_series:
        return pd.Series(result, index=original_index)

    return result


def calculate_illness_risk_metrics(illness_array: np.ndarray) -> Dict[str, float]:
    """
    Calculate illness risk metrics from Monte Carlo simulation results.

    Args:
        illness_array: Array of illness probabilities or proportions from MC simulations

    Returns:
        Dictionary with metrics:
        - mean: Mean illness probability
        - median: Median illness probability
        - p5: 5th percentile
        - p95: 95th percentile
        - std: Standard deviation
        - min: Minimum value
        - max: Maximum value
    """
    return {
        "mean": np.mean(illness_array),
        "median": np.median(illness_array),
        "p5": np.percentile(illness_array, 5),
        "p95": np.percentile(illness_array, 95),
        "std": np.std(illness_array),
        "min": np.min(illness_array),
        "max": np.max(illness_array)
    }


def calculate_population_illness_cases(infection_risk: np.ndarray,
                                      probability_illness_given_infection: float,
                                      population_susceptibility: float,
                                      population_size: int,
                                      frequency_per_year: float) -> np.ndarray:
    """
    Calculate expected number of illness cases per year in a population.

    Formula: Expected cases = population × frequency × infection_risk × P(ill|inf) × susceptibility

    Args:
        infection_risk: Array of annual infection risks (0-1)
        probability_illness_given_infection: P(ill | infected) for the pathogen
        population_susceptibility: Fraction of population susceptible
        population_size: Number of people in exposed population
        frequency_per_year: Number of exposure events per person per year

    Returns:
        Array of expected annual illness cases

    Example:
        >>> infection_risk = np.array([0.01, 0.02, 0.015])  # 1-2% risk
        >>> cases = calculate_population_illness_cases(
        ...     infection_risk,
        ...     p_ill=0.60,
        ...     susceptibility=0.74,
        ...     population_size=10000,
        ...     frequency=20
        ... )
        >>> print(f"Expected cases per year: {cases.mean():.1f}")
    """
    adjusted_illness_prob = probability_illness_given_infection * population_susceptibility

    annual_illness_cases = (infection_risk * adjusted_illness_prob *
                           population_size * frequency_per_year)

    return annual_illness_cases


def classify_illness_risk(annual_illness_probability: float) -> str:
    """
    Classify illness risk level based on annual probability.

    Based on WHO guideline (annual risk < 1e-4 is acceptable):

    Classification thresholds:
    - < 1e-6: Negligible
    - 1e-6 to 1e-4: Very Low (WHO acceptable)
    - 1e-4 to 1e-3: Low
    - 1e-3 to 1e-2: Medium
    - >= 1e-2: High

    Args:
        annual_illness_probability: Annual probability of illness per person

    Returns:
        Risk classification string
    """
    if annual_illness_probability < 1e-6:
        return "Negligible"
    elif annual_illness_probability < 1e-4:
        return "Very Low"
    elif annual_illness_probability < 1e-3:
        return "Low"
    elif annual_illness_probability < 1e-2:
        return "Medium"
    else:
        return "High"


def get_who_compliance_status(annual_illness_probability: float,
                              guideline_threshold: float = 1e-4) -> Tuple[str, bool]:
    """
    Determine WHO compliance status for illness risk.

    WHO (2016) guideline: Annual risk of illness < 1e-4 is acceptable

    Args:
        annual_illness_probability: Annual probability of illness per person
        guideline_threshold: WHO threshold (default 1e-4)

    Returns:
        Tuple of (status_string, is_compliant_boolean)

    Example:
        >>> status, compliant = get_who_compliance_status(0.00005)
        >>> print(f"{status}: {compliant}")
        COMPLIANT: True
    """
    is_compliant = annual_illness_probability <= guideline_threshold

    if is_compliant:
        status = "COMPLIANT"
    else:
        status = "NON-COMPLIANT"

    return status, is_compliant


def apply_illness_model_to_dataframe(df: pd.DataFrame,
                                    probability_illness_given_infection: float,
                                    population_susceptibility: float = 1.0) -> pd.DataFrame:
    """
    Apply illness conversion to a DataFrame of infection risks.

    Adds new columns:
    - Mean_Illness_Risk: Mean annual illness probability
    - Median_Illness_Risk: Median annual illness probability
    - P95_Illness_Risk: 95th percentile illness risk
    - Illness_Classification: Risk level (Negligible/Very Low/Low/Medium/High)
    - WHO_Compliance: COMPLIANT or NON-COMPLIANT

    Args:
        df: DataFrame with 'Mean_Annual_Risk' and 'P95_Annual_Risk' columns
        probability_illness_given_infection: P(ill | infected)
        population_susceptibility: Population susceptibility factor

    Returns:
        DataFrame with new illness-related columns

    Example:
        >>> df = pd.DataFrame({
        ...     'Mean_Annual_Risk': [0.0001, 0.001, 0.01],
        ...     'Median_Annual_Risk': [0.00008, 0.0008, 0.008],
        ...     'P95_Annual_Risk': [0.0002, 0.002, 0.02]
        ... })
        >>> result = apply_illness_model_to_dataframe(df, 0.60, 0.74)
    """
    df = df.copy()

    adjustment_factor = probability_illness_given_infection * population_susceptibility

    # Convert infection risk to illness risk
    if 'Mean_Annual_Risk' in df.columns:
        df['Mean_Illness_Risk'] = df['Mean_Annual_Risk'] * adjustment_factor

    if 'Median_Annual_Risk' in df.columns:
        df['Median_Illness_Risk'] = df['Median_Annual_Risk'] * adjustment_factor

    if 'P95_Annual_Risk' in df.columns:
        df['P95_Illness_Risk'] = df['P95_Annual_Risk'] * adjustment_factor

    # Use Mean_Illness_Risk for classification if available
    if 'Mean_Illness_Risk' in df.columns:
        df['Illness_Classification'] = df['Mean_Illness_Risk'].apply(classify_illness_risk)
        df['WHO_Compliance'] = df['Mean_Illness_Risk'].apply(
            lambda x: get_who_compliance_status(x)[0]
        )

    return df


__all__ = [
    'infection_to_illness',
    'calculate_illness_risk_metrics',
    'calculate_population_illness_cases',
    'classify_illness_risk',
    'get_who_compliance_status',
    'apply_illness_model_to_dataframe'
]
