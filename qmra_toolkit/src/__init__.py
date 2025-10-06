"""
Enhanced QMRA Toolkit
Based on Charlotte Jones-Todd's R QMRA Package
"""

from .dose_response_advanced import DoseResponseModels, DoseResponseSelector, calculate_n50, calculate_id50
from .monte_carlo_advanced import (
    MonteCarloQMRA, ConcentrationQMRA, IngestedQMRA,
    HydrodynamicDilution, SimulationResults, DistributionSampler
)
from .pathogen_database_advanced import (
    PathogenDatabase, PathogenParameters,
    BIOACCUMULATION_FACTORS, MORBIDITY_RATIOS
)
from .qmra_integration import QMRAAssessment, QMRAScenario, QMRAResults

__all__ = [
    # Dose-response
    'DoseResponseModels', 'DoseResponseSelector', 'calculate_n50', 'calculate_id50',
    # Monte Carlo
    'MonteCarloQMRA', 'ConcentrationQMRA', 'IngestedQMRA',
    'HydrodynamicDilution', 'SimulationResults', 'DistributionSampler',
    # Pathogen database
    'PathogenDatabase', 'PathogenParameters',
    'BIOACCUMULATION_FACTORS', 'MORBIDITY_RATIOS',
    # Integration
    'QMRAAssessment', 'QMRAScenario', 'QMRAResults'
]

__version__ = '2.0.0'  # Enhanced version with R package features