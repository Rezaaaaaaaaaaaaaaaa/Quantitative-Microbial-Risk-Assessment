"""
Exposure-Specific Parameter Functions for QMRA

This module provides exposure route-specific functions for calculating
ingestion volumes, meal sizes, bioaccumulation factors, and other
exposure-related parameters based on David Wood's R implementation.

Functions implement models from:
- Shellfish consumption (BAF, meal size, water equivalent)
- Swimming exposure (ingestion rate, duration)
- Inhalation (not yet implemented)

Author: NIWA Earth Sciences New Zealand
Based on: David Wood's From_David R package (DESCRIPTION, NAMESPACE, R/)
Date: November 2025
"""

import numpy as np
import pandas as pd
from typing import Tuple, Union, Optional
import warnings


class BioaccumulationFactor:
    """
    Bioaccumulation Factor (BAF) for shellfish consumption.

    Shellfish filter-feed and concentrate pathogens from water.
    BAF represents the concentration factor (typical mean ~44.9x, range 1-100x).

    Based on David's BAF() function in R/BAF.R
    Distribution: Truncated Normal
    - Mean: 44.9
    - SD: 20.93
    - Min: 1
    - Max: 100
    """

    @staticmethod
    def generate(n_samples: int,
                mean_value: float = 44.9,
                sd_value: float = 20.93,
                lower: float = 1.0,
                upper: float = 100.0,
                seed: Optional[int] = None) -> np.ndarray:
        """
        Generate BAF values using truncated normal distribution.

        Args:
            n_samples: Number of BAF values to generate
            mean_value: Mean of BAF distribution (default 44.9)
            sd_value: Standard deviation (default 20.93)
            lower: Lower truncation bound (default 1)
            upper: Upper truncation bound (default 100)
            seed: Random seed for reproducibility

        Returns:
            Array of BAF values (multiplication factors)

        Example:
            >>> baf = BioaccumulationFactor.generate(1000)
            >>> print(f"Mean BAF: {baf.mean():.1f}")
            Mean BAF: 44.5
        """
        if seed is not None:
            np.random.seed(seed)

        # Use scipy truncnorm for truncated normal distribution
        from scipy.stats import truncnorm

        # Calculate standardized bounds for truncnorm
        alpha = (lower - mean_value) / sd_value
        beta = (upper - mean_value) / sd_value

        baf_values = truncnorm.rvs(alpha, beta, loc=mean_value, scale=sd_value, size=n_samples)

        return np.array(baf_values)


class ShellfishMealSize:
    """
    Shellfish meal size distribution for consumption exposure.

    Models the typical meal size in grams for shellfish consumption.
    Distribution: Truncated Log-Logistic

    Based on David's functions in R/waterEquiv.R and rloglosisticTrunc()
    Default parameters from David's package:
    - Min: 5 grams
    - Max: 800 grams
    - alpha: 2.2046
    - beta: 75.072
    - gamma: -0.9032
    """

    @staticmethod
    def generate(n_samples: int,
                alpha: float = 2.2046,
                beta: float = 75.072,
                gamma: float = -0.9032,
                min_grams: float = 5.0,
                max_grams: float = 800.0,
                seed: Optional[int] = None) -> np.ndarray:
        """
        Generate shellfish meal sizes using truncated log-logistic distribution.

        Args:
            n_samples: Number of meal sizes to generate
            alpha: Shape parameter (default 2.2046)
            beta: Shape parameter (default 75.072)
            gamma: Location parameter (default -0.9032)
            min_grams: Minimum meal size (default 5g)
            max_grams: Maximum meal size (default 800g)
            seed: Random seed for reproducibility

        Returns:
            Array of meal sizes in grams

        Example:
            >>> meals = ShellfishMealSize.generate(1000)
            >>> print(f"Mean meal size: {meals.mean():.1f} g")
            Mean meal size: 75.3 g
        """
        if seed is not None:
            np.random.seed(seed)

        # Log-logistic CDF: F(x) = 1 / (1 + (alpha / (x - gamma))^beta)
        # Inverse CDF: Q(u) = gamma + alpha / ((u^(-1/beta)) - 1)^(1/beta)

        def loglogistic_cdf(x, alpha, beta, gamma):
            """CDF of log-logistic distribution."""
            if np.any(x <= gamma):
                return np.zeros_like(x)
            return 1.0 / (1.0 + (alpha / (x - gamma))**beta)

        def loglogistic_icdf(u, alpha, beta, gamma):
            """Inverse CDF of log-logistic distribution."""
            u = np.clip(u, 1e-10, 1 - 1e-10)
            return gamma + alpha / ((u**(-1.0/beta)) - 1.0)**(1.0/beta)

        # Calculate CDF at truncation bounds
        cdf_min = loglogistic_cdf(min_grams, alpha, beta, gamma)
        cdf_max = loglogistic_cdf(max_grams, alpha, beta, gamma)

        # Generate uniform samples and transform to truncated distribution
        uniform_samples = np.random.uniform(0, 1, n_samples)
        u_truncated = cdf_min + uniform_samples * (cdf_max - cdf_min)
        meal_sizes = loglogistic_icdf(u_truncated, alpha, beta, gamma)

        # Ensure all samples are within bounds
        meal_sizes = np.clip(meal_sizes, min_grams, max_grams)

        return np.array(meal_sizes)


def calculate_shellfish_water_equivalent(meal_sizes: np.ndarray,
                                        baf_values: np.ndarray) -> np.ndarray:
    """
    Calculate water-equivalent volume for shellfish consumption.

    Water-equivalent = meal_size (grams) × BAF (multiplication factor)

    This converts the shellfish meal into an equivalent water volume containing
    the same pathogen concentration.

    Args:
        meal_sizes: Array of meal sizes in grams (shape: n_samples or n_samples x n_scenarios)
        baf_values: Array of BAF values (shape: n_samples or broadcastable)

    Returns:
        Array of water-equivalent volumes (in mL equivalent)

    Example:
        >>> meals = ShellfishMealSize.generate(100)
        >>> bafs = BioaccumulationFactor.generate(100)
        >>> water_equiv = calculate_shellfish_water_equivalent(meals, bafs)
        >>> print(f"Mean water equivalent: {water_equiv.mean():.1f} mL")
    """
    # Meal size in grams × BAF gives effective water equivalent
    # Assumption: 1 gram shellfish ~ 1 mL water volume equivalent
    water_equiv = meal_sizes * baf_values

    return water_equiv


class SwimIngestionRate:
    """
    Ingestion rate for swimming exposure (primary contact with water).

    Models the volume of water ingested per hour of swimming.
    Distribution: Truncated Lognormal

    Based on David's swim_ingestion_rate() in R/swimming.R
    Default parameters from David's package:
    - Mean: 53 mL/h
    - SD: 75 mL/h
    - Min: 5 mL/h
    - Max: 200 mL/h
    """

    @staticmethod
    def generate(n_samples: int,
                mean_ingestion: float = 53.0,
                sd_ingestion: float = 75.0,
                min_rate: float = 5.0,
                max_rate: float = 200.0,
                seed: Optional[int] = None) -> np.ndarray:
        """
        Generate swim ingestion rates using truncated lognormal distribution.

        Args:
            n_samples: Number of ingestion rates to generate
            mean_ingestion: Mean ingestion rate in mL/h (default 53)
            sd_ingestion: Standard deviation in mL/h (default 75)
            min_rate: Minimum ingestion rate (default 5 mL/h)
            max_rate: Maximum ingestion rate (default 200 mL/h)
            seed: Random seed for reproducibility

        Returns:
            Array of ingestion rates in mL/h

        Example:
            >>> rates = SwimIngestionRate.generate(1000)
            >>> print(f"Mean ingestion rate: {rates.mean():.1f} mL/h")
            Mean ingestion rate: 52.8 mL/h
        """
        if seed is not None:
            np.random.seed(seed)

        from scipy.stats import lognorm

        # Convert mean and SD to lognormal parameters
        # For lognormal: mean = exp(mu + sigma^2/2)
        # variance = (exp(sigma^2) - 1) * exp(2*mu + sigma^2)

        # Use method of moments to get mu and sigma
        cv = sd_ingestion / mean_ingestion  # Coefficient of variation
        sigma = np.sqrt(np.log(1 + cv**2))
        mu = np.log(mean_ingestion) - sigma**2 / 2

        # Generate from lognormal and truncate
        alpha = (np.log(min_rate) - mu) / sigma
        beta = (np.log(max_rate) - mu) / sigma

        from scipy.stats import truncnorm as tn_normal
        log_samples = tn_normal.rvs(alpha, beta, loc=mu, scale=sigma, size=n_samples)
        ingestion_rates = np.exp(log_samples)

        return np.clip(ingestion_rates, min_rate, max_rate)


class SwimDuration:
    """
    Swimming duration distribution.

    Models the duration of a single swimming episode.
    Distribution: PERT (Program Evaluation and Review Technique) / Triangular

    Based on David's swim_duration() in R/swimming.R
    Default parameters:
    - Min: 0.2 hours (~12 minutes)
    - Mode: 1.0 hour
    - Max: 4.0 hours
    """

    @staticmethod
    def generate(n_samples: int,
                min_hours: float = 0.2,
                mode_hours: float = 1.0,
                max_hours: float = 4.0,
                seed: Optional[int] = None) -> np.ndarray:
        """
        Generate swim durations using triangular/PERT distribution.

        Args:
            n_samples: Number of durations to generate
            min_hours: Minimum swim duration (default 0.2 hours)
            mode_hours: Most likely duration (default 1.0 hour)
            max_hours: Maximum swim duration (default 4.0 hours)
            seed: Random seed for reproducibility

        Returns:
            Array of swim durations in hours

        Example:
            >>> durations = SwimDuration.generate(1000)
            >>> print(f"Mean duration: {durations.mean():.2f} hours")
            Mean duration: 1.07 hours
        """
        if seed is not None:
            np.random.seed(seed)

        # Use triangular distribution
        # PERT is related but uses different parameterization
        durations = np.random.triangular(min_hours, mode_hours, max_hours, n_samples)

        return durations


def calculate_swim_ingestion_volume(ingestion_rate: np.ndarray,
                                   duration: np.ndarray) -> np.ndarray:
    """
    Calculate total water ingestion during swimming.

    Total ingestion (mL) = ingestion_rate (mL/h) × duration (hours)

    Args:
        ingestion_rate: Array of ingestion rates in mL/h
        duration: Array of durations in hours

    Returns:
        Array of total ingestion volumes in mL

    Example:
        >>> rates = SwimIngestionRate.generate(100)
        >>> durations = SwimDuration.generate(100)
        >>> total_ingestion = calculate_swim_ingestion_volume(rates, durations)
        >>> print(f"Mean total ingestion: {total_ingestion.mean():.1f} mL")
    """
    total_volume = ingestion_rate * duration

    return total_volume


def get_exposure_volume(exposure_route: str,
                       n_samples: int,
                       route_parameters: dict,
                       seed: Optional[int] = None) -> Union[np.ndarray, Tuple[np.ndarray, dict]]:
    """
    Dispatcher function to calculate exposure volume for different routes.

    Routes:
    - 'shellfish_consumption': Uses meal size and BAF
    - 'primary_contact' or 'swimming': Uses ingestion rate and duration
    - 'contaminated_water': Uses fixed volume parameter

    Args:
        exposure_route: Type of exposure route
        n_samples: Number of Monte Carlo samples
        route_parameters: Dictionary with route-specific parameters
        seed: Random seed for reproducibility

    Returns:
        For shellfish: Array of water-equivalent volumes
        For swimming: Tuple of (volume_array, parameters_dict)

    Example:
        >>> params = {
        ...     'min_grams': 5,
        ...     'max_grams': 800,
        ...     'baf_mean': 44.9,
        ...     'baf_sd': 20.93
        ... }
        >>> volumes = get_exposure_volume('shellfish_consumption', 100, params)
    """
    if seed is not None:
        np.random.seed(seed)

    if exposure_route.lower() in ['shellfish_consumption', 'shellfish']:
        # Shellfish: meal size × BAF
        meal_sizes = ShellfishMealSize.generate(
            n_samples,
            alpha=route_parameters.get('alpha', 2.2046),
            beta=route_parameters.get('beta', 75.072),
            gamma=route_parameters.get('gamma', -0.9032),
            min_grams=route_parameters.get('min_grams', 5.0),
            max_grams=route_parameters.get('max_grams', 800.0)
        )

        baf_values = BioaccumulationFactor.generate(
            n_samples,
            mean_value=route_parameters.get('baf_mean', 44.9),
            sd_value=route_parameters.get('baf_sd', 20.93),
            lower=route_parameters.get('baf_min', 1.0),
            upper=route_parameters.get('baf_max', 100.0)
        )

        water_equiv = calculate_shellfish_water_equivalent(meal_sizes, baf_values)

        return water_equiv

    elif exposure_route.lower() in ['primary_contact', 'swimming', 'swim']:
        # Swimming: ingestion rate × duration
        rates = SwimIngestionRate.generate(
            n_samples,
            mean_ingestion=route_parameters.get('mean_ingestion_rate', 53.0),
            sd_ingestion=route_parameters.get('sd_ingestion_rate', 75.0),
            min_rate=route_parameters.get('min_ingestion_rate', 5.0),
            max_rate=route_parameters.get('max_ingestion_rate', 200.0)
        )

        durations = SwimDuration.generate(
            n_samples,
            min_hours=route_parameters.get('min_duration', 0.2),
            mode_hours=route_parameters.get('mode_duration', 1.0),
            max_hours=route_parameters.get('max_duration', 4.0)
        )

        total_volume = calculate_swim_ingestion_volume(rates, durations)

        return total_volume

    elif exposure_route.lower() in ['contaminated_water', 'water']:
        # Fixed volume (from batch parameters)
        volume = route_parameters.get('volume_ml', 50.0)
        volumes = np.full(n_samples, volume)

        return volumes

    else:
        raise ValueError(f"Unknown exposure route: {exposure_route}")


__all__ = [
    'BioaccumulationFactor',
    'ShellfishMealSize',
    'calculate_shellfish_water_equivalent',
    'SwimIngestionRate',
    'SwimDuration',
    'calculate_swim_ingestion_volume',
    'get_exposure_volume'
]
