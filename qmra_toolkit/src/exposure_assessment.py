"""
Exposure Assessment Module for QMRA Toolkit

This module provides exposure assessment capabilities for different pathways
including primary contact (recreational water) and shellfish consumption.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
import warnings


class ExposureRoute(Enum):
    """Supported exposure routes."""
    PRIMARY_CONTACT = "primary_contact"
    SHELLFISH_CONSUMPTION = "shellfish_consumption"
    DRINKING_WATER = "drinking_water"
    AEROSOL_INHALATION = "aerosol_inhalation"


@dataclass
class ExposureParameters:
    """Container for exposure scenario parameters."""
    route: ExposureRoute
    parameters: Dict[str, Union[float, int]]
    pathogen_concentration: Optional[Union[float, np.ndarray]] = None
    description: Optional[str] = None

    def validate(self) -> None:
        """Validate exposure parameters."""
        required_params = {
            ExposureRoute.PRIMARY_CONTACT: ["water_ingestion_volume", "exposure_frequency"],
            ExposureRoute.SHELLFISH_CONSUMPTION: ["shellfish_consumption", "consumption_frequency"],
            ExposureRoute.DRINKING_WATER: ["daily_consumption_volume"],
            ExposureRoute.AEROSOL_INHALATION: ["inhalation_rate", "exposure_duration"]
        }

        required = required_params.get(self.route, [])
        missing = [param for param in required if param not in self.parameters]

        if missing:
            raise ValueError(f"Missing required parameters for {self.route.value}: {missing}")

        if self.pathogen_concentration is None:
            warnings.warn("Pathogen concentration not specified - must be set before dose calculation")


@dataclass
class ExposureResult:
    """Container for exposure assessment results."""
    route: ExposureRoute
    doses: np.ndarray
    annual_doses: np.ndarray
    statistics: Dict[str, float]
    parameters_used: Dict[str, Union[float, int]]
    pathogen_concentration: Union[float, np.ndarray]


class ExposureAssessment(ABC):
    """Abstract base class for exposure assessment models."""

    def __init__(self, parameters: ExposureParameters):
        """Initialize exposure assessment model."""
        self.parameters = parameters
        self.parameters.validate()

    @abstractmethod
    def calculate_dose(self, n_samples: int = 1) -> np.ndarray:
        """Calculate exposure dose(s)."""
        pass

    @abstractmethod
    def calculate_annual_dose(self, n_samples: int = 1) -> np.ndarray:
        """Calculate annual exposure dose(s)."""
        pass

    def get_route(self) -> ExposureRoute:
        """Get exposure route."""
        return self.parameters.route

    def set_pathogen_concentration(self, concentration: Union[float, np.ndarray]) -> None:
        """Set pathogen concentration for dose calculations."""
        self.parameters.pathogen_concentration = concentration

    def _calculate_statistics(self, doses: np.ndarray) -> Dict[str, float]:
        """Calculate statistics for dose array."""
        clean_doses = doses[np.isfinite(doses)]

        if len(clean_doses) == 0:
            return {}

        return {
            "mean": float(np.mean(clean_doses)),
            "median": float(np.median(clean_doses)),
            "std": float(np.std(clean_doses)),
            "min": float(np.min(clean_doses)),
            "max": float(np.max(clean_doses)),
            "p95": float(np.percentile(clean_doses, 95)),
            "p99": float(np.percentile(clean_doses, 99))
        }


class PrimaryContactExposure(ExposureAssessment):
    """
    Primary contact exposure assessment (recreational water activities).

    Models exposure through inadvertent water ingestion during swimming,
    surfing, or other recreational water activities.
    """

    def calculate_dose(self, n_samples: int = 1) -> np.ndarray:
        """
        Calculate exposure dose per contact event.

        Args:
            n_samples: Number of samples to generate

        Returns:
            Array of doses (organisms per event)
        """
        if self.parameters.pathogen_concentration is None:
            raise ValueError("Pathogen concentration must be set before dose calculation")

        water_volume = self.parameters.parameters["water_ingestion_volume"]  # mL per event
        concentration = self.parameters.pathogen_concentration  # organisms per 100mL or per L

        # Convert to consistent units (organisms per mL)
        if isinstance(concentration, (int, float)):
            # Assume concentration is per 100mL (common for recreational water standards)
            conc_per_ml = concentration / 100.0
        else:
            # If array, assume same unit conversion needed
            conc_per_ml = np.array(concentration) / 100.0

        # Calculate dose = concentration × volume ingested
        if n_samples == 1:
            if isinstance(conc_per_ml, np.ndarray) and len(conc_per_ml) > 1:
                # Use first element if concentration is array but only one sample requested
                dose = conc_per_ml[0] * water_volume
            else:
                dose = conc_per_ml * water_volume
            return np.array([dose])
        else:
            if isinstance(conc_per_ml, np.ndarray):
                if len(conc_per_ml) == n_samples:
                    doses = conc_per_ml * water_volume
                else:
                    # Repeat concentration if not enough samples
                    conc_repeated = np.tile(conc_per_ml, (n_samples // len(conc_per_ml)) + 1)[:n_samples]
                    doses = conc_repeated * water_volume
            else:
                doses = np.full(n_samples, conc_per_ml * water_volume)

            return doses

    def calculate_annual_dose(self, n_samples: int = 1) -> np.ndarray:
        """
        Calculate annual exposure dose.

        Args:
            n_samples: Number of samples to generate

        Returns:
            Array of annual doses (organisms per year)
        """
        single_event_doses = self.calculate_dose(n_samples)
        exposure_frequency = self.parameters.parameters["exposure_frequency"]  # events per year

        return single_event_doses * exposure_frequency


class ShellfishConsumptionExposure(ExposureAssessment):
    """
    Shellfish consumption exposure assessment.

    Models exposure through consumption of shellfish (oysters, mussels, clams)
    that may have bioaccumulated pathogens from contaminated water.
    """

    def __init__(self, parameters: ExposureParameters, bioaccumulation_factor: float = 1.0):
        """
        Initialize shellfish consumption exposure model.

        Args:
            parameters: Exposure parameters
            bioaccumulation_factor: Factor accounting for pathogen concentration in shellfish
                                  relative to surrounding water
        """
        super().__init__(parameters)
        self.bioaccumulation_factor = bioaccumulation_factor

    def calculate_dose(self, n_samples: int = 1) -> np.ndarray:
        """
        Calculate exposure dose per consumption event.

        Args:
            n_samples: Number of samples to generate

        Returns:
            Array of doses (organisms per serving)
        """
        if self.parameters.pathogen_concentration is None:
            raise ValueError("Pathogen concentration must be set before dose calculation")

        shellfish_mass = self.parameters.parameters["shellfish_consumption"]  # grams per serving
        concentration = self.parameters.pathogen_concentration  # organisms per gram or per 100g

        # Apply bioaccumulation factor
        effective_concentration = concentration * self.bioaccumulation_factor

        # Calculate dose = concentration × mass consumed
        if n_samples == 1:
            if isinstance(effective_concentration, np.ndarray) and len(effective_concentration) > 1:
                dose = effective_concentration[0] * shellfish_mass / 100.0  # Assuming per 100g
            else:
                dose = effective_concentration * shellfish_mass / 100.0
            return np.array([dose])
        else:
            if isinstance(effective_concentration, np.ndarray):
                if len(effective_concentration) == n_samples:
                    doses = effective_concentration * shellfish_mass / 100.0
                else:
                    conc_repeated = np.tile(effective_concentration, (n_samples // len(effective_concentration)) + 1)[:n_samples]
                    doses = conc_repeated * shellfish_mass / 100.0
            else:
                doses = np.full(n_samples, effective_concentration * shellfish_mass / 100.0)

            return doses

    def calculate_annual_dose(self, n_samples: int = 1) -> np.ndarray:
        """
        Calculate annual exposure dose.

        Args:
            n_samples: Number of samples to generate

        Returns:
            Array of annual doses (organisms per year)
        """
        single_serving_doses = self.calculate_dose(n_samples)
        consumption_frequency = self.parameters.parameters["consumption_frequency"]  # servings per year

        return single_serving_doses * consumption_frequency

    def set_bioaccumulation_factor(self, factor: float) -> None:
        """Set bioaccumulation factor."""
        if factor <= 0:
            raise ValueError("Bioaccumulation factor must be positive")
        self.bioaccumulation_factor = factor


class DrinkingWaterExposure(ExposureAssessment):
    """
    Drinking water exposure assessment.

    Models exposure through consumption of treated or untreated drinking water.
    """

    def calculate_dose(self, n_samples: int = 1) -> np.ndarray:
        """
        Calculate daily exposure dose.

        Args:
            n_samples: Number of samples to generate

        Returns:
            Array of daily doses (organisms per day)
        """
        if self.parameters.pathogen_concentration is None:
            raise ValueError("Pathogen concentration must be set before dose calculation")

        daily_volume = self.parameters.parameters["daily_consumption_volume"]  # L per day
        concentration = self.parameters.pathogen_concentration  # organisms per L

        # Calculate dose = concentration × volume consumed
        if n_samples == 1:
            if isinstance(concentration, np.ndarray) and len(concentration) > 1:
                dose = concentration[0] * daily_volume
            else:
                dose = concentration * daily_volume
            return np.array([dose])
        else:
            if isinstance(concentration, np.ndarray):
                if len(concentration) == n_samples:
                    doses = concentration * daily_volume
                else:
                    conc_repeated = np.tile(concentration, (n_samples // len(concentration)) + 1)[:n_samples]
                    doses = conc_repeated * daily_volume
            else:
                doses = np.full(n_samples, concentration * daily_volume)

            return doses

    def calculate_annual_dose(self, n_samples: int = 1) -> np.ndarray:
        """
        Calculate annual exposure dose.

        Args:
            n_samples: Number of samples to generate

        Returns:
            Array of annual doses (organisms per year)
        """
        daily_doses = self.calculate_dose(n_samples)
        return daily_doses * 365


class AerosolInhalationExposure(ExposureAssessment):
    """
    Aerosol inhalation exposure assessment.

    Models exposure through inhalation of contaminated aerosols
    (e.g., from wastewater treatment plants, spray irrigation).
    """

    def calculate_dose(self, n_samples: int = 1) -> np.ndarray:
        """
        Calculate exposure dose per inhalation event.

        Args:
            n_samples: Number of samples to generate

        Returns:
            Array of doses (organisms per exposure)
        """
        if self.parameters.pathogen_concentration is None:
            raise ValueError("Pathogen concentration must be set before dose calculation")

        inhalation_rate = self.parameters.parameters["inhalation_rate"]  # m³/hr
        exposure_duration = self.parameters.parameters["exposure_duration"]  # hours
        concentration = self.parameters.pathogen_concentration  # organisms per m³

        total_volume = inhalation_rate * exposure_duration

        # Calculate dose = concentration × volume inhaled
        if n_samples == 1:
            if isinstance(concentration, np.ndarray) and len(concentration) > 1:
                dose = concentration[0] * total_volume
            else:
                dose = concentration * total_volume
            return np.array([dose])
        else:
            if isinstance(concentration, np.ndarray):
                if len(concentration) == n_samples:
                    doses = concentration * total_volume
                else:
                    conc_repeated = np.tile(concentration, (n_samples // len(concentration)) + 1)[:n_samples]
                    doses = conc_repeated * total_volume
            else:
                doses = np.full(n_samples, concentration * total_volume)

            return doses

    def calculate_annual_dose(self, n_samples: int = 1) -> np.ndarray:
        """
        Calculate annual exposure dose.

        Args:
            n_samples: Number of samples to generate

        Returns:
            Array of annual doses (organisms per year)
        """
        single_event_doses = self.calculate_dose(n_samples)
        exposure_frequency = self.parameters.parameters.get("exposure_frequency", 1)  # events per year

        return single_event_doses * exposure_frequency


def create_exposure_assessment(route: ExposureRoute,
                              parameters: Dict[str, Union[float, int]],
                              **kwargs) -> ExposureAssessment:
    """
    Factory function to create exposure assessment objects.

    Args:
        route: Exposure route
        parameters: Exposure parameters
        **kwargs: Additional route-specific parameters

    Returns:
        Appropriate exposure assessment object

    Raises:
        ValueError: If exposure route is not supported
    """
    exposure_params = ExposureParameters(route=route, parameters=parameters)

    if route == ExposureRoute.PRIMARY_CONTACT:
        return PrimaryContactExposure(exposure_params)
    elif route == ExposureRoute.SHELLFISH_CONSUMPTION:
        bioaccumulation_factor = kwargs.get("bioaccumulation_factor", 1.0)
        return ShellfishConsumptionExposure(exposure_params, bioaccumulation_factor)
    elif route == ExposureRoute.DRINKING_WATER:
        return DrinkingWaterExposure(exposure_params)
    elif route == ExposureRoute.AEROSOL_INHALATION:
        return AerosolInhalationExposure(exposure_params)
    else:
        available_routes = [route.value for route in ExposureRoute]
        raise ValueError(f"Unsupported exposure route: {route}. Available: {available_routes}")


def run_exposure_assessment(exposure_model: ExposureAssessment,
                           n_samples: int = 1000) -> ExposureResult:
    """
    Run complete exposure assessment with statistics.

    Args:
        exposure_model: Configured exposure assessment model
        n_samples: Number of samples for uncertainty analysis

    Returns:
        ExposureResult with doses and statistics
    """
    # Calculate doses
    single_event_doses = exposure_model.calculate_dose(n_samples)
    annual_doses = exposure_model.calculate_annual_dose(n_samples)

    # Calculate statistics
    single_stats = exposure_model._calculate_statistics(single_event_doses)
    annual_stats = exposure_model._calculate_statistics(annual_doses)

    # Combine statistics
    combined_stats = {
        "single_event_" + k: v for k, v in single_stats.items()
    }
    combined_stats.update({
        "annual_" + k: v for k, v in annual_stats.items()
    })

    return ExposureResult(
        route=exposure_model.get_route(),
        doses=single_event_doses,
        annual_doses=annual_doses,
        statistics=combined_stats,
        parameters_used=exposure_model.parameters.parameters,
        pathogen_concentration=exposure_model.parameters.pathogen_concentration
    )


if __name__ == "__main__":
    # Example usage and testing
    print("Testing Exposure Assessment Module")
    print("=" * 40)

    # Test primary contact exposure
    primary_params = {
        "water_ingestion_volume": 50.0,  # mL per swimming event
        "exposure_frequency": 10  # events per year
    }

    primary_exposure = create_exposure_assessment(
        ExposureRoute.PRIMARY_CONTACT,
        primary_params
    )

    # Set pathogen concentration (organisms per 100mL)
    primary_exposure.set_pathogen_concentration(10.0)

    print("Primary Contact Exposure:")
    single_dose = primary_exposure.calculate_dose(1)[0]
    annual_dose = primary_exposure.calculate_annual_dose(1)[0]
    print(f"  Single event dose: {single_dose:.2f} organisms")
    print(f"  Annual dose: {annual_dose:.2f} organisms")

    # Test shellfish consumption exposure
    shellfish_params = {
        "shellfish_consumption": 150.0,  # grams per serving
        "consumption_frequency": 12  # servings per year
    }

    shellfish_exposure = create_exposure_assessment(
        ExposureRoute.SHELLFISH_CONSUMPTION,
        shellfish_params,
        bioaccumulation_factor=2.0
    )

    # Set pathogen concentration (organisms per 100g)
    shellfish_exposure.set_pathogen_concentration(100.0)

    print("\nShellfish Consumption Exposure:")
    single_dose = shellfish_exposure.calculate_dose(1)[0]
    annual_dose = shellfish_exposure.calculate_annual_dose(1)[0]
    print(f"  Single serving dose: {single_dose:.2f} organisms")
    print(f"  Annual dose: {annual_dose:.2f} organisms")

    # Run complete assessment with uncertainty
    print("\nComplete Assessment with Uncertainty:")
    result = run_exposure_assessment(primary_exposure, n_samples=1000)
    print(f"  Annual dose mean: {result.statistics['annual_mean']:.2f} organisms")
    print(f"  Annual dose 95th percentile: {result.statistics['annual_p95']:.2f} organisms")

    print("\nExposure assessment completed successfully!")