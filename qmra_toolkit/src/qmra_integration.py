"""
QMRA Integration Module
Brings together dose-response, Monte Carlo, and pathogen database
Provides high-level interface for QMRA assessments matching NIWA standards
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
import logging

from .dose_response_advanced import DoseResponseSelector, calculate_n50
from .monte_carlo_advanced import MonteCarloQMRA, HydrodynamicDilution, SimulationResults
from .pathogen_database_advanced import PathogenDatabase, MORBIDITY_RATIOS, BIOACCUMULATION_FACTORS

logger = logging.getLogger(__name__)


@dataclass
class QMRAScenario:
    """Configuration for a QMRA scenario"""
    name: str
    pathogen: str
    exposure_route: str  # 'swimming', 'shellfish', 'drinking'
    treatment_efficacy: Union[Dict[str, float], float]  # log reduction
    influent_concentration: Dict[str, Union[str, Dict]]  # distribution params
    dilution_data: Optional[np.ndarray] = None  # hydrodynamic dilution
    exposure_duration: Optional[Dict] = None  # minutes
    ingestion_rate: Optional[Dict] = None  # L/min or g per serving
    events_per_year: int = 1
    population_size: Optional[int] = None


@dataclass
class QMRAResults:
    """Results from QMRA assessment"""
    scenario: QMRAScenario
    monte_carlo_results: SimulationResults
    infection_risks: np.ndarray
    illness_risks: np.ndarray
    annual_risks: np.ndarray
    statistics: pd.DataFrame
    risk_percentiles: Dict[str, float]


class QMRAAssessment:
    """
    High-level QMRA assessment class matching NIWA professional standards
    """

    def __init__(self):
        self.pathogen_db = PathogenDatabase()
        self.dr_selector = DoseResponseSelector()
        self.mc_simulator = MonteCarloQMRA()
        self.hydro_processor = HydrodynamicDilution()

    def setup_exposure_parameters(self, exposure_route: str) -> Tuple[Dict, Dict]:
        """
        Get default exposure parameters for different routes

        Args:
            exposure_route: Type of exposure ('swimming', 'shellfish', 'drinking')

        Returns:
            Tuple of (duration_params, ingestion_rate_params)
        """
        if exposure_route == 'swimming':
            duration = {
                'distribution': 'triangular',
                'params': {'min': 15, 'mode': 30, 'max': 60}  # minutes
            }
            ingestion_rate = {
                'distribution': 'triangular',
                'params': {'min': 0.001, 'mode': 0.003, 'max': 0.01}  # L/min
            }
        elif exposure_route == 'shellfish':
            duration = {
                'distribution': 'fixed',
                'params': {'value': 1}  # single serving
            }
            ingestion_rate = {
                'distribution': 'triangular',
                'params': {'min': 50, 'mode': 100, 'max': 150}  # grams per serving
            }
        elif exposure_route == 'drinking':
            duration = {
                'distribution': 'fixed',
                'params': {'value': 1}  # per day
            }
            ingestion_rate = {
                'distribution': 'triangular',
                'params': {'min': 1.5, 'mode': 2.0, 'max': 3.0}  # L/day
            }
        else:
            raise ValueError(f"Unknown exposure route: {exposure_route}")

        return duration, ingestion_rate

    def run_assessment(self, scenario: QMRAScenario, nsim: int = 10000) -> QMRAResults:
        """
        Run complete QMRA assessment

        Args:
            scenario: QMRAScenario configuration
            nsim: Number of Monte Carlo simulations

        Returns:
            QMRAResults object
        """
        logger.info(f"Running QMRA assessment: {scenario.name}")

        # Get pathogen parameters
        pathogen_params = self.pathogen_db.get_best_fit_model(scenario.pathogen)
        logger.info(f"Using {pathogen_params.model} model for {scenario.pathogen}")

        # Setup exposure parameters if not provided
        if scenario.exposure_duration is None or scenario.ingestion_rate is None:
            duration, ingestion_rate = self.setup_exposure_parameters(scenario.exposure_route)
            scenario.exposure_duration = scenario.exposure_duration or duration
            scenario.ingestion_rate = scenario.ingestion_rate or ingestion_rate

        # Process dilution data
        if scenario.dilution_data is not None:
            dilution_distribution = self.hydro_processor.prepare_dilution_distribution(
                scenario.dilution_data
            )
        else:
            # Default dilution if not provided
            dilution_distribution = {
                'x': np.array([0.001, 0.01, 0.1, 1.0]),
                'p': np.array([0.25, 0.5, 0.75, 1.0]),
                'min': 0.001,
                'max': 1.0
            }

        # Run Monte Carlo simulation
        mc_config = {
            'nsim': nsim,
            'efficacy': scenario.treatment_efficacy,
            'microbe_influent': scenario.influent_concentration,
            'dilution_exposure': dilution_distribution,
            'duration': scenario.exposure_duration,
            'vol_rate': scenario.ingestion_rate
        }

        mc_results = self.mc_simulator.simulate(**mc_config)

        # Apply bioaccumulation factor for shellfish
        doses = mc_results.doses.flatten()
        if scenario.exposure_route == 'shellfish':
            bio_factor = BIOACCUMULATION_FACTORS.get(
                scenario.pathogen.lower(),
                BIOACCUMULATION_FACTORS['default']
            )['default']
            doses = doses * bio_factor
            logger.info(f"Applied bioaccumulation factor of {bio_factor}")

        # Calculate infection risks
        infection_risks = self.dr_selector.calculate_risk(
            pathogen_params.model,
            doses,
            pathogen_params.parameters
        )

        # Calculate illness risks (morbidity)
        morbidity_ratio = MORBIDITY_RATIOS.get(scenario.pathogen.lower(), 0.5)
        illness_risks = infection_risks * morbidity_ratio

        # Calculate annual risks
        if scenario.events_per_year > 1:
            # P_annual = 1 - (1 - P_single)^n
            annual_infection_risks = 1 - (1 - infection_risks) ** scenario.events_per_year
            annual_illness_risks = 1 - (1 - illness_risks) ** scenario.events_per_year
        else:
            annual_infection_risks = infection_risks
            annual_illness_risks = illness_risks

        # Calculate statistics
        statistics = self._calculate_statistics(
            doses, infection_risks, illness_risks,
            annual_infection_risks, annual_illness_risks
        )

        # Calculate risk percentiles
        risk_percentiles = {
            'infection_median': np.median(infection_risks),
            'infection_95': np.percentile(infection_risks, 95),
            'illness_median': np.median(illness_risks),
            'illness_95': np.percentile(illness_risks, 95),
            'annual_infection_median': np.median(annual_infection_risks),
            'annual_infection_95': np.percentile(annual_infection_risks, 95),
            'annual_illness_median': np.median(annual_illness_risks),
            'annual_illness_95': np.percentile(annual_illness_risks, 95)
        }

        # Create results object
        results = QMRAResults(
            scenario=scenario,
            monte_carlo_results=mc_results,
            infection_risks=infection_risks,
            illness_risks=illness_risks,
            annual_risks=annual_infection_risks,
            statistics=statistics,
            risk_percentiles=risk_percentiles
        )

        return results

    def _calculate_statistics(self, doses: np.ndarray,
                            infection_risks: np.ndarray,
                            illness_risks: np.ndarray,
                            annual_infection_risks: np.ndarray,
                            annual_illness_risks: np.ndarray) -> pd.DataFrame:
        """Calculate comprehensive statistics"""

        def get_stats(arr, name):
            return {
                f'{name}_mean': np.mean(arr),
                f'{name}_median': np.median(arr),
                f'{name}_std': np.std(arr),
                f'{name}_min': np.min(arr),
                f'{name}_max': np.max(arr),
                f'{name}_p5': np.percentile(arr, 5),
                f'{name}_p25': np.percentile(arr, 25),
                f'{name}_p75': np.percentile(arr, 75),
                f'{name}_p95': np.percentile(arr, 95)
            }

        stats = {}
        stats.update(get_stats(doses, 'dose'))
        stats.update(get_stats(infection_risks, 'infection_risk'))
        stats.update(get_stats(illness_risks, 'illness_risk'))
        stats.update(get_stats(annual_infection_risks, 'annual_infection_risk'))
        stats.update(get_stats(annual_illness_risks, 'annual_illness_risk'))

        return pd.DataFrame([stats]).T.rename(columns={0: 'Value'})

    def run_multiple_sites(self, base_scenario: QMRAScenario,
                          site_dilutions: Dict[str, np.ndarray],
                          nsim: int = 10000) -> Dict[str, QMRAResults]:
        """
        Run QMRA for multiple sites with different dilution data

        Args:
            base_scenario: Base scenario configuration
            site_dilutions: Dict mapping site names to dilution arrays
            nsim: Number of simulations

        Returns:
            Dict mapping site names to results
        """
        results = {}

        for site_name, dilution_data in site_dilutions.items():
            # Create site-specific scenario
            site_scenario = QMRAScenario(
                name=f"{base_scenario.name} - {site_name}",
                pathogen=base_scenario.pathogen,
                exposure_route=base_scenario.exposure_route,
                treatment_efficacy=base_scenario.treatment_efficacy,
                influent_concentration=base_scenario.influent_concentration,
                dilution_data=dilution_data,
                exposure_duration=base_scenario.exposure_duration,
                ingestion_rate=base_scenario.ingestion_rate,
                events_per_year=base_scenario.events_per_year,
                population_size=base_scenario.population_size
            )

            # Run assessment
            results[site_name] = self.run_assessment(site_scenario, nsim)

        return results

    def compare_treatment_scenarios(self, base_scenario: QMRAScenario,
                                   treatment_scenarios: Dict[str, Union[Dict, float]],
                                   nsim: int = 10000) -> pd.DataFrame:
        """
        Compare different treatment scenarios

        Args:
            base_scenario: Base scenario configuration
            treatment_scenarios: Dict mapping scenario names to efficacy values
            nsim: Number of simulations

        Returns:
            DataFrame with comparison results
        """
        comparison_results = []

        for scenario_name, efficacy in treatment_scenarios.items():
            # Create modified scenario
            modified_scenario = QMRAScenario(
                name=f"{base_scenario.name} - {scenario_name}",
                pathogen=base_scenario.pathogen,
                exposure_route=base_scenario.exposure_route,
                treatment_efficacy=efficacy,
                influent_concentration=base_scenario.influent_concentration,
                dilution_data=base_scenario.dilution_data,
                exposure_duration=base_scenario.exposure_duration,
                ingestion_rate=base_scenario.ingestion_rate,
                events_per_year=base_scenario.events_per_year,
                population_size=base_scenario.population_size
            )

            # Run assessment
            results = self.run_assessment(modified_scenario, nsim)

            # Extract key metrics
            comparison_results.append({
                'Scenario': scenario_name,
                'Treatment': str(efficacy),
                'Median IIR': results.risk_percentiles['illness_median'],
                '95th IIR': results.risk_percentiles['illness_95'],
                'Median Annual IIR': results.risk_percentiles['annual_illness_median'],
                '95th Annual IIR': results.risk_percentiles['annual_illness_95'],
                'Mean Dose': np.mean(results.monte_carlo_results.doses),
                'Max Dose': np.max(results.monte_carlo_results.doses)
            })

        return pd.DataFrame(comparison_results)


def create_niwa_standard_assessment(
    pathogen: str = 'norovirus',
    treatment_level: str = 'secondary',
    sites: Optional[List[str]] = None,
    dilution_data: Optional[Dict[str, np.ndarray]] = None
) -> Dict[str, QMRAResults]:
    """
    Create QMRA assessment matching NIWA report standards

    Args:
        pathogen: Pathogen name
        treatment_level: 'bypass', 'primary', 'secondary', 'tertiary', 'UV'
        sites: List of site names
        dilution_data: Dilution data for each site

    Returns:
        Assessment results
    """
    # Treatment efficacy (log reduction)
    treatment_efficacies = {
        'bypass': 0,
        'primary': {'min': 0.5, 'max': 1.0},
        'secondary': {'min': 1.5, 'max': 2.5},
        'tertiary': {'min': 2.5, 'max': 3.5},
        'UV': {'min': 3.0, 'max': 4.0}
    }

    # Default influent concentration (log-normal)
    influent_config = {
        'distribution': 'lognormal',
        'params': {
            'meanlog': 5.0,  # log10 copies/L
            'sdlog': 1.0
        }
    }

    # Create base scenario
    base_scenario = QMRAScenario(
        name=f"NIWA QMRA - {pathogen} - {treatment_level}",
        pathogen=pathogen,
        exposure_route='swimming',
        treatment_efficacy=treatment_efficacies.get(treatment_level, 2.0),
        influent_concentration=influent_config,
        events_per_year=20  # typical swimming events
    )

    # Run assessment
    qmra = QMRAAssessment()

    if sites and dilution_data:
        results = qmra.run_multiple_sites(base_scenario, dilution_data)
    else:
        results = {'Single Site': qmra.run_assessment(base_scenario)}

    return results