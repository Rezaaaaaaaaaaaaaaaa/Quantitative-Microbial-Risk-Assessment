"""
QMRA Core Modules
=================

Core QMRA toolkit modules for standalone batch processing application.

This package contains the essential QMRA modules needed for batch processing:
- pathogen_database: Pathogen parameters and dose-response data
- dose_response: Dose-response models (Beta-Poisson, Exponential)
- monte_carlo: Monte Carlo simulation engine

Author: NIWA Earth Sciences New Zealand
Date: October 2025
"""

from .pathogen_database import PathogenDatabase, get_norovirus_parameters
from .dose_response import create_dose_response_model
from .monte_carlo import (
    MonteCarloSimulator,
    create_lognormal_distribution,
    create_uniform_distribution,
    create_triangular_distribution,
    create_empirical_cdf_from_data,
    create_empirical_cdf_distribution,
    create_hockey_stick_distribution,
    calculate_empirical_cdf
)

__version__ = "1.1.0"
__all__ = [
    "PathogenDatabase",
    "get_norovirus_parameters",
    "create_dose_response_model",
    "MonteCarloSimulator",
    "create_lognormal_distribution",
    "create_uniform_distribution",
    "create_triangular_distribution",
    "create_empirical_cdf_from_data",
    "create_empirical_cdf_distribution",
    "create_hockey_stick_distribution",
    "calculate_empirical_cdf"
]
