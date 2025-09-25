"""
Risk Characterization Module for QMRA Toolkit

This module integrates exposure assessment and dose-response models to calculate
health risks including infection probability, illness probability, and DALYs.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum

from pathogen_database import PathogenDatabase
from dose_response import create_dose_response_model, DoseResponseModel
from exposure_assessment import ExposureAssessment, ExposureResult
from dilution_model import DilutionModel


class RiskMetric(Enum):
    """Types of risk metrics that can be calculated."""
    INFECTION_PROBABILITY = "infection_probability"
    ILLNESS_PROBABILITY = "illness_probability"
    ANNUAL_RISK = "annual_risk"
    DALYS = "dalys"
    EXCESS_CASES = "excess_cases"


@dataclass
class RiskCalculationInputs:
    """Container for risk calculation inputs."""
    pathogen_name: str
    doses: np.ndarray
    population_size: Optional[int] = None
    exposure_frequency: Optional[float] = None
    illness_to_infection_ratio: Optional[float] = None
    dalys_per_case: Optional[float] = None


@dataclass
class RiskResult:
    """Container for risk calculation results."""
    pathogen_name: str
    risk_metric: RiskMetric
    individual_risks: np.ndarray
    statistics: Dict[str, float]
    population_risks: Optional[Dict[str, float]] = None
    inputs_used: Optional[RiskCalculationInputs] = None

    def get_summary(self) -> str:
        """Get a formatted summary of risk results."""
        summary = f"Risk Assessment Results: {self.pathogen_name}\n"
        summary += f"Risk Metric: {self.risk_metric.value}\n"
        summary += "=" * 50 + "\n"

        summary += "Individual Risk Statistics:\n"
        for stat, value in self.statistics.items():
            if "probability" in self.risk_metric.value:
                summary += f"  {stat}: {value:.2e}\n"
            elif self.risk_metric == RiskMetric.DALYS:
                summary += f"  {stat}: {value:.6f}\n"
            else:
                summary += f"  {stat}: {value:.3f}\n"

        if self.population_risks:
            summary += "\nPopulation Risk:\n"
            for metric, value in self.population_risks.items():
                summary += f"  {metric}: {value:.1f}\n"

        return summary


class RiskCharacterization:
    """
    Risk characterization engine that integrates all QMRA components.

    This class combines pathogen data, dose-response models, exposure assessment,
    and dilution modelling to calculate comprehensive health risks.
    """

    def __init__(self, pathogen_database: Optional[PathogenDatabase] = None):
        """
        Initialize risk characterization engine.

        Args:
            pathogen_database: PathogenDatabase instance. If None, creates default.
        """
        self.pathogen_db = pathogen_database or PathogenDatabase()
        self.regulatory_thresholds = {
            "acceptable_annual_risk": 1e-6,
            "recreational_water_risk": 1e-3,
            "drinking_water_annual_risk": 1e-4
        }

    def calculate_infection_probability(self,
                                      pathogen_name: str,
                                      doses: Union[float, np.ndarray],
                                      model_type: Optional[str] = None) -> RiskResult:
        """
        Calculate infection probability from pathogen doses.

        Args:
            pathogen_name: Name of the pathogen
            doses: Pathogen doses (organisms)
            model_type: Type of dose-response model

        Returns:
            RiskResult with infection probabilities
        """
        # Auto-select model type if not specified
        if model_type is None:
            model_type = self.pathogen_db.get_default_model_type(pathogen_name)

        # Get dose-response parameters
        dr_params = self.pathogen_db.get_dose_response_parameters(pathogen_name, model_type)

        # Create dose-response model
        dr_model = create_dose_response_model(model_type, dr_params)

        # Calculate infection probabilities
        doses_array = np.asarray(doses)
        infection_probs = dr_model.calculate_infection_probability(doses_array)

        # Calculate statistics
        statistics = self._calculate_statistics(infection_probs)

        inputs = RiskCalculationInputs(
            pathogen_name=pathogen_name,
            doses=doses_array
        )

        return RiskResult(
            pathogen_name=pathogen_name,
            risk_metric=RiskMetric.INFECTION_PROBABILITY,
            individual_risks=infection_probs,
            statistics=statistics,
            inputs_used=inputs
        )

    def calculate_illness_probability(self,
                                    pathogen_name: str,
                                    doses: Union[float, np.ndarray],
                                    model_type: Optional[str] = None) -> RiskResult:
        """
        Calculate illness probability from pathogen doses.

        Args:
            pathogen_name: Name of the pathogen
            doses: Pathogen doses (organisms)
            model_type: Type of dose-response model

        Returns:
            RiskResult with illness probabilities
        """
        # First calculate infection probability
        infection_result = self.calculate_infection_probability(pathogen_name, doses, model_type)

        # Get illness-to-infection ratio
        health_data = self.pathogen_db.get_health_impact_data(pathogen_name)
        illness_ratio = health_data["illness_to_infection_ratio"]

        # Calculate illness probabilities
        illness_probs = infection_result.individual_risks * illness_ratio

        # Calculate statistics
        statistics = self._calculate_statistics(illness_probs)

        inputs = RiskCalculationInputs(
            pathogen_name=pathogen_name,
            doses=np.asarray(doses),
            illness_to_infection_ratio=illness_ratio
        )

        return RiskResult(
            pathogen_name=pathogen_name,
            risk_metric=RiskMetric.ILLNESS_PROBABILITY,
            individual_risks=illness_probs,
            statistics=statistics,
            inputs_used=inputs
        )

    def calculate_annual_risk(self,
                            pathogen_name: str,
                            single_event_doses: Union[float, np.ndarray],
                            exposure_frequency: float,
                            model_type: Optional[str] = None) -> RiskResult:
        """
        Calculate annual infection risk.

        Args:
            pathogen_name: Name of the pathogen
            single_event_doses: Doses per single exposure event (organisms)
            exposure_frequency: Number of exposure events per year
            model_type: Type of dose-response model

        Returns:
            RiskResult with annual infection risks
        """
        # Calculate single event infection probability
        single_event_result = self.calculate_infection_probability(
            pathogen_name, single_event_doses, model_type
        )

        # Calculate annual risk: 1 - (1 - P_single)^frequency
        single_probs = single_event_result.individual_risks
        annual_risks = 1 - np.power(1 - single_probs, exposure_frequency)

        # Calculate statistics
        statistics = self._calculate_statistics(annual_risks)

        inputs = RiskCalculationInputs(
            pathogen_name=pathogen_name,
            doses=np.asarray(single_event_doses),
            exposure_frequency=exposure_frequency
        )

        return RiskResult(
            pathogen_name=pathogen_name,
            risk_metric=RiskMetric.ANNUAL_RISK,
            individual_risks=annual_risks,
            statistics=statistics,
            inputs_used=inputs
        )

    def calculate_dalys(self,
                       pathogen_name: str,
                       doses: Union[float, np.ndarray],
                       model_type: Optional[str] = None) -> RiskResult:
        """
        Calculate Disability Adjusted Life Years (DALYs).

        Args:
            pathogen_name: Name of the pathogen
            doses: Pathogen doses (organisms)
            model_type: Type of dose-response model

        Returns:
            RiskResult with DALY values
        """
        # Calculate illness probability
        illness_result = self.calculate_illness_probability(pathogen_name, doses, model_type)

        # Get DALYs per case
        health_data = self.pathogen_db.get_health_impact_data(pathogen_name)
        dalys_per_case = health_data["dalys_per_case"]

        # Calculate DALYs
        dalys = illness_result.individual_risks * dalys_per_case

        # Calculate statistics
        statistics = self._calculate_statistics(dalys)

        inputs = RiskCalculationInputs(
            pathogen_name=pathogen_name,
            doses=np.asarray(doses),
            illness_to_infection_ratio=illness_result.inputs_used.illness_to_infection_ratio,
            dalys_per_case=dalys_per_case
        )

        return RiskResult(
            pathogen_name=pathogen_name,
            risk_metric=RiskMetric.DALYS,
            individual_risks=dalys,
            statistics=statistics,
            inputs_used=inputs
        )

    def calculate_population_risk(self,
                                 individual_risk_result: RiskResult,
                                 population_size: int) -> RiskResult:
        """
        Calculate population-level risk metrics.

        Args:
            individual_risk_result: RiskResult from individual risk calculation
            population_size: Size of exposed population

        Returns:
            Updated RiskResult with population risk metrics
        """
        mean_individual_risk = individual_risk_result.statistics["mean"]

        population_risks = {
            "expected_cases_per_year": mean_individual_risk * population_size,
            "population_size": population_size
        }

        # Add confidence intervals for expected cases
        percentiles = [5, 25, 50, 75, 95]
        for p in percentiles:
            p_key = f"p{p}"
            if p_key in individual_risk_result.statistics:
                population_risks[f"cases_{p}th_percentile"] = (
                    individual_risk_result.statistics[p_key] * population_size
                )

        # Create new result with population data
        updated_result = RiskResult(
            pathogen_name=individual_risk_result.pathogen_name,
            risk_metric=individual_risk_result.risk_metric,
            individual_risks=individual_risk_result.individual_risks,
            statistics=individual_risk_result.statistics,
            population_risks=population_risks,
            inputs_used=individual_risk_result.inputs_used
        )

        return updated_result

    def evaluate_regulatory_compliance(self, risk_result: RiskResult) -> Dict[str, bool]:
        """
        Evaluate compliance with regulatory risk thresholds.

        Args:
            risk_result: RiskResult to evaluate

        Returns:
            Dictionary mapping threshold names to compliance status
        """
        mean_risk = risk_result.statistics["mean"]
        p95_risk = risk_result.statistics.get("p95", mean_risk)

        compliance = {}

        # Check annual risk thresholds
        if risk_result.risk_metric == RiskMetric.ANNUAL_RISK:
            compliance["acceptable_annual_risk"] = mean_risk <= self.regulatory_thresholds["acceptable_annual_risk"]
            compliance["drinking_water_annual_risk"] = mean_risk <= self.regulatory_thresholds["drinking_water_annual_risk"]

        # Check single event thresholds
        elif risk_result.risk_metric in [RiskMetric.INFECTION_PROBABILITY, RiskMetric.ILLNESS_PROBABILITY]:
            compliance["recreational_water_risk"] = mean_risk <= self.regulatory_thresholds["recreational_water_risk"]

        # Conservative check using 95th percentile
        for threshold_name, threshold_value in self.regulatory_thresholds.items():
            compliance[f"{threshold_name}_p95"] = p95_risk <= threshold_value

        return compliance

    def run_comprehensive_assessment(self,
                                   pathogen_name: str,
                                   exposure_assessment: ExposureAssessment,
                                   dilution_model: Optional[DilutionModel] = None,
                                   population_size: Optional[int] = None,
                                   n_samples: int = 10000) -> Dict[str, RiskResult]:
        """
        Run comprehensive QMRA including all risk metrics.

        Args:
            pathogen_name: Name of the pathogen
            exposure_assessment: Configured exposure assessment model
            dilution_model: Optional dilution model for concentration reduction
            population_size: Optional population size for population risk
            n_samples: Number of Monte Carlo samples

        Returns:
            Dictionary mapping risk metrics to RiskResult objects
        """
        results = {}

        # Get exposure doses
        single_doses = exposure_assessment.calculate_dose(n_samples)
        annual_doses = exposure_assessment.calculate_annual_dose(n_samples)

        # Apply dilution/treatment if provided
        if dilution_model:
            # Note: This is a simplified integration - in practice, dilution would be applied
            # to the pathogen concentration before exposure assessment
            pass

        # Calculate all risk metrics
        results["infection_probability"] = self.calculate_infection_probability(
            pathogen_name, single_doses
        )

        results["illness_probability"] = self.calculate_illness_probability(
            pathogen_name, single_doses
        )

        results["annual_risk"] = self.calculate_annual_risk(
            pathogen_name, single_doses,
            exposure_assessment.parameters.parameters.get("exposure_frequency", 1)
        )

        results["dalys"] = self.calculate_dalys(pathogen_name, single_doses)

        # Add population risks if population size provided
        if population_size:
            for metric_name, result in results.items():
                results[metric_name] = self.calculate_population_risk(result, population_size)

        return results

    def _calculate_statistics(self, values: np.ndarray) -> Dict[str, float]:
        """Calculate statistical summary of risk values."""
        clean_values = values[np.isfinite(values)]

        if len(clean_values) == 0:
            return {}

        statistics = {
            "mean": float(np.mean(clean_values)),
            "median": float(np.median(clean_values)),
            "std": float(np.std(clean_values)),
            "min": float(np.min(clean_values)),
            "max": float(np.max(clean_values))
        }

        # Add percentiles
        percentiles = [1, 5, 10, 25, 75, 90, 95, 99]
        for p in percentiles:
            statistics[f"p{p}"] = float(np.percentile(clean_values, p))

        return statistics

    def create_risk_summary_table(self, results: Dict[str, RiskResult]) -> pd.DataFrame:
        """
        Create summary table of risk results.

        Args:
            results: Dictionary of risk results

        Returns:
            Pandas DataFrame with summary statistics
        """
        summary_data = []

        for metric_name, result in results.items():
            row = {
                "Risk_Metric": metric_name,
                "Pathogen": result.pathogen_name,
                "Mean": result.statistics.get("mean", np.nan),
                "Median": result.statistics.get("median", np.nan),
                "P95": result.statistics.get("p95", np.nan),
                "P99": result.statistics.get("p99", np.nan)
            }

            # Add population data if available
            if result.population_risks:
                row["Expected_Cases_Per_Year"] = result.population_risks.get("expected_cases_per_year", np.nan)

            summary_data.append(row)

        return pd.DataFrame(summary_data)


if __name__ == "__main__":
    # Example usage and testing
    print("Testing Risk Characterization Module")
    print("=" * 40)

    # Initialize risk characterization
    risk_calc = RiskCharacterization()

    # Test with norovirus and various dose levels
    pathogen_name = "norovirus"
    test_doses = np.array([1, 10, 100, 1000, 10000])

    print(f"Testing with {pathogen_name} at doses: {test_doses}")
    print()

    # Calculate infection probability
    infection_result = risk_calc.calculate_infection_probability(pathogen_name, test_doses)
    print("Infection Probabilities:")
    for dose, prob in zip(test_doses, infection_result.individual_risks):
        print(f"  Dose {dose}: {prob:.4f}")

    # Calculate illness probability
    illness_result = risk_calc.calculate_illness_probability(pathogen_name, test_doses)
    print("\nIllness Probabilities:")
    for dose, prob in zip(test_doses, illness_result.individual_risks):
        print(f"  Dose {dose}: {prob:.4f}")

    # Calculate DALYs
    dalys_result = risk_calc.calculate_dalys(pathogen_name, test_doses)
    print("\nDALYs per exposure:")
    for dose, dalys in zip(test_doses, dalys_result.individual_risks):
        print(f"  Dose {dose}: {dalys:.6f}")

    # Calculate annual risk
    annual_result = risk_calc.calculate_annual_risk(pathogen_name, test_doses, exposure_frequency=10)
    print("\nAnnual Infection Risk (10 exposures/year):")
    for dose, risk in zip(test_doses, annual_result.individual_risks):
        print(f"  Dose {dose}: {risk:.4f}")

    # Test population risk
    pop_result = risk_calc.calculate_population_risk(annual_result, population_size=100000)
    print(f"\nExpected cases per year (population 100,000): {pop_result.population_risks['expected_cases_per_year']:.1f}")

    # Test regulatory compliance
    compliance = risk_calc.evaluate_regulatory_compliance(annual_result)
    print("\nRegulatory Compliance:")
    for threshold, compliant in compliance.items():
        status = "PASS" if compliant else "FAIL"
        print(f"  {threshold}: {status}")

    print("\nRisk characterization completed successfully!")