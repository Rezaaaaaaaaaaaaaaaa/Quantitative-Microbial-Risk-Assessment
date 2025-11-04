"""
QMRA Core Modules
=================

Core QMRA toolkit modules for standalone batch processing application.

This package contains the essential QMRA modules needed for batch processing:
- pathogen_database: Pathogen parameters and dose-response data
- dose_response: Dose-response models (Beta-Poisson, Exponential)
- monte_carlo: Monte Carlo simulation engine (includes truncated log-logistic)
- exposure_parameters: Exposure route-specific functions (shellfish, swimming)
- illness_model: Infection to illness conversion and risk classification

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
from .exposure_parameters import (
    BioaccumulationFactor,
    ShellfishMealSize,
    calculate_shellfish_water_equivalent,
    SwimIngestionRate,
    SwimDuration,
    calculate_swim_ingestion_volume,
    get_exposure_volume
)
from .illness_model import (
    infection_to_illness,
    calculate_illness_risk_metrics,
    calculate_population_illness_cases,
    classify_illness_risk,
    get_who_compliance_status,
    apply_illness_model_to_dataframe
)

__version__ = "1.2.0"
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
    "calculate_empirical_cdf",
    "BioaccumulationFactor",
    "ShellfishMealSize",
    "calculate_shellfish_water_equivalent",
    "SwimIngestionRate",
    "SwimDuration",
    "calculate_swim_ingestion_volume",
    "get_exposure_volume",
    "infection_to_illness",
    "calculate_illness_risk_metrics",
    "calculate_population_illness_cases",
    "classify_illness_risk",
    "get_who_compliance_status",
    "apply_illness_model_to_dataframe"
]
