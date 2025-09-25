"""
Dilution Modelling Integration Module for QMRA Toolkit

This module provides dilution modelling capabilities and integration with
engineer-provided log reduction values (LRVs), which is NIWA's key differentiator.
"""

import numpy as np
from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum
import warnings


class TreatmentType(Enum):
    """Types of treatment processes."""
    PHYSICAL = "physical"
    CHEMICAL = "chemical"
    BIOLOGICAL = "biological"
    UV = "uv_disinfection"
    CHLORINATION = "chlorination"
    OZONATION = "ozonation"
    MEMBRANE_FILTRATION = "membrane_filtration"
    NATURAL_DIE_OFF = "natural_die_off"
    DILUTION = "dilution"


@dataclass
class TreatmentBarrier:
    """Container for treatment barrier information."""
    name: str
    treatment_type: TreatmentType
    log_reduction_value: float
    variability: Optional[float] = None  # Standard deviation for uncertainty
    pathogen_specific: Optional[Dict[str, float]] = None
    description: Optional[str] = None

    def validate(self) -> None:
        """Validate treatment barrier parameters."""
        if self.log_reduction_value < 0:
            raise ValueError(f"Log reduction value must be non-negative, got {self.log_reduction_value}")

        if self.log_reduction_value > 10:
            warnings.warn(f"Very high LRV ({self.log_reduction_value}) - verify this is realistic")

        if self.variability is not None and self.variability < 0:
            raise ValueError("Variability must be non-negative")


@dataclass
class DilutionScenario:
    """Container for dilution scenario parameters."""
    initial_flow: float  # m³/s
    receiving_flow: float  # m³/s
    distance: Optional[float] = None  # km downstream
    decay_rate: Optional[float] = None  # per day
    travel_time: Optional[float] = None  # days
    mixing_efficiency: float = 1.0  # 0-1, default complete mixing


class DilutionModel:
    """
    Dilution modelling for QMRA - NIWA's key differentiator.

    This class handles dilution calculations for various scenarios including:
    - Point source discharge dilution
    - Far-field dilution
    - Natural die-off during transport
    - Multiple treatment barriers
    """

    def __init__(self):
        """Initialize dilution model."""
        self.treatment_barriers: List[TreatmentBarrier] = []
        self.dilution_scenario: Optional[DilutionScenario] = None

    def add_treatment_barrier(self, barrier: TreatmentBarrier) -> None:
        """
        Add a treatment barrier to the treatment train.

        Args:
            barrier: TreatmentBarrier object with LRV information
        """
        barrier.validate()
        self.treatment_barriers.append(barrier)

    def set_dilution_scenario(self, scenario: DilutionScenario) -> None:
        """
        Set the dilution scenario parameters.

        Args:
            scenario: DilutionScenario object with flow and mixing parameters
        """
        if scenario.initial_flow <= 0 or scenario.receiving_flow <= 0:
            raise ValueError("Flow rates must be positive")

        if scenario.mixing_efficiency < 0 or scenario.mixing_efficiency > 1:
            raise ValueError("Mixing efficiency must be between 0 and 1")

        self.dilution_scenario = scenario

    def calculate_simple_dilution(self,
                                 initial_concentration: Union[float, np.ndarray],
                                 initial_flow: float,
                                 receiving_flow: float) -> Union[float, np.ndarray]:
        """
        Calculate simple dilution based on flow rates.

        Args:
            initial_concentration: Pathogen concentration in discharge (organisms/L)
            initial_flow: Discharge flow rate (m³/s)
            receiving_flow: Receiving water flow rate (m³/s)

        Returns:
            Diluted concentration (organisms/L)
        """
        dilution_factor = initial_flow / (initial_flow + receiving_flow)
        return initial_concentration * dilution_factor

    def calculate_far_field_dilution(self,
                                    initial_concentration: Union[float, np.ndarray],
                                    distance: float,
                                    dispersion_coefficient: float = 0.1) -> Union[float, np.ndarray]:
        """
        Calculate far-field dilution using simplified dispersion model.

        Args:
            initial_concentration: Initial pathogen concentration (organisms/L)
            distance: Distance downstream (km)
            dispersion_coefficient: Dispersion coefficient

        Returns:
            Concentration at distance (organisms/L)
        """
        if distance <= 0:
            return initial_concentration

        # Simplified exponential decay with distance
        dilution_factor = np.exp(-dispersion_coefficient * distance)
        return initial_concentration * dilution_factor

    def apply_log_reduction(self,
                          concentration: Union[float, np.ndarray],
                          log_reduction: float,
                          variability: Optional[float] = None) -> Union[float, np.ndarray]:
        """
        Apply log reduction value to concentration.

        Args:
            concentration: Initial concentration (organisms/L)
            log_reduction: Log reduction value (log10 units)
            variability: Standard deviation for LRV uncertainty

        Returns:
            Reduced concentration (organisms/L)
        """
        if variability is not None and variability > 0:
            # Add uncertainty to LRV
            if isinstance(concentration, np.ndarray):
                n_samples = len(concentration)
                actual_lrv = np.random.normal(log_reduction, variability, n_samples)
                actual_lrv = np.maximum(actual_lrv, 0)  # Ensure non-negative
            else:
                actual_lrv = max(0, np.random.normal(log_reduction, variability))
        else:
            actual_lrv = log_reduction

        reduction_factor = 10 ** (-actual_lrv)
        return concentration * reduction_factor

    def apply_natural_die_off(self,
                            concentration: Union[float, np.ndarray],
                            decay_rate: float,
                            time: float) -> Union[float, np.ndarray]:
        """
        Apply natural die-off during transport.

        Args:
            concentration: Initial concentration (organisms/L)
            decay_rate: First-order decay rate (per day)
            time: Travel time (days)

        Returns:
            Concentration after die-off (organisms/L)
        """
        if decay_rate < 0:
            raise ValueError("Decay rate must be non-negative")

        if time < 0:
            raise ValueError("Time must be non-negative")

        return concentration * np.exp(-decay_rate * time)

    def calculate_cumulative_log_reduction(self, pathogen_name: Optional[str] = None) -> Tuple[float, float]:
        """
        Calculate cumulative log reduction across all treatment barriers.

        Args:
            pathogen_name: Optional pathogen name for specific LRVs

        Returns:
            Tuple of (mean_lrv, std_lrv)
        """
        if not self.treatment_barriers:
            return 0.0, 0.0

        total_lrv = 0.0
        total_variance = 0.0

        for barrier in self.treatment_barriers:
            # Use pathogen-specific LRV if available
            if pathogen_name and barrier.pathogen_specific and pathogen_name in barrier.pathogen_specific:
                lrv = barrier.pathogen_specific[pathogen_name]
            else:
                lrv = barrier.log_reduction_value

            total_lrv += lrv

            if barrier.variability is not None:
                total_variance += barrier.variability ** 2

        return total_lrv, np.sqrt(total_variance)

    def apply_treatment_train(self,
                             initial_concentration: Union[float, np.ndarray],
                             pathogen_name: Optional[str] = None,
                             include_uncertainty: bool = True) -> Union[float, np.ndarray]:
        """
        Apply complete treatment train to initial concentration.

        Args:
            initial_concentration: Initial pathogen concentration (organisms/L)
            pathogen_name: Optional pathogen name for specific LRVs
            include_uncertainty: Whether to include LRV uncertainty

        Returns:
            Final concentration after all treatment (organisms/L)
        """
        concentration = initial_concentration

        for barrier in self.treatment_barriers:
            # Use pathogen-specific LRV if available
            if pathogen_name and barrier.pathogen_specific and pathogen_name in barrier.pathogen_specific:
                lrv = barrier.pathogen_specific[pathogen_name]
            else:
                lrv = barrier.log_reduction_value

            variability = barrier.variability if include_uncertainty else None
            concentration = self.apply_log_reduction(concentration, lrv, variability)

        return concentration

    def apply_complete_scenario(self,
                              initial_concentration: Union[float, np.ndarray],
                              pathogen_name: Optional[str] = None) -> Dict[str, Union[float, np.ndarray]]:
        """
        Apply complete dilution and treatment scenario.

        Args:
            initial_concentration: Initial pathogen concentration (organisms/L)
            pathogen_name: Optional pathogen name for specific parameters

        Returns:
            Dictionary with concentrations at each stage
        """
        results = {
            "initial": initial_concentration,
            "after_treatment": initial_concentration,
            "after_dilution": initial_concentration,
            "after_die_off": initial_concentration,
            "final": initial_concentration
        }

        # Apply treatment train
        if self.treatment_barriers:
            results["after_treatment"] = self.apply_treatment_train(
                initial_concentration, pathogen_name
            )
        else:
            results["after_treatment"] = initial_concentration

        current_concentration = results["after_treatment"]

        # Apply dilution
        if self.dilution_scenario:
            results["after_dilution"] = self.calculate_simple_dilution(
                current_concentration,
                self.dilution_scenario.initial_flow,
                self.dilution_scenario.receiving_flow
            )
            current_concentration = results["after_dilution"]

            # Apply natural die-off if parameters provided
            if self.dilution_scenario.decay_rate and self.dilution_scenario.travel_time:
                results["after_die_off"] = self.apply_natural_die_off(
                    current_concentration,
                    self.dilution_scenario.decay_rate,
                    self.dilution_scenario.travel_time
                )
                current_concentration = results["after_die_off"]

        results["final"] = current_concentration

        return results

    def get_treatment_summary(self) -> str:
        """
        Get a summary of the treatment train.

        Returns:
            Formatted summary string
        """
        if not self.treatment_barriers:
            return "No treatment barriers configured"

        summary = "Treatment Train Summary\n"
        summary += "=" * 30 + "\n"

        cumulative_lrv = 0.0
        for i, barrier in enumerate(self.treatment_barriers, 1):
            summary += f"{i}. {barrier.name}\n"
            summary += f"   Type: {barrier.treatment_type.value}\n"
            summary += f"   LRV: {barrier.log_reduction_value:.1f} log₁₀\n"
            if barrier.variability:
                summary += f"   Variability: ±{barrier.variability:.2f} log₁₀\n"
            cumulative_lrv += barrier.log_reduction_value
            summary += "\n"

        summary += f"Total LRV: {cumulative_lrv:.1f} log₁₀\n"
        summary += f"Overall reduction: {10**cumulative_lrv:.1e} fold\n"

        return summary


# Convenience functions for common treatment processes
def create_uv_barrier(log_reduction: float, variability: float = 0.2) -> TreatmentBarrier:
    """Create UV disinfection barrier."""
    return TreatmentBarrier(
        name="UV Disinfection",
        treatment_type=TreatmentType.UV,
        log_reduction_value=log_reduction,
        variability=variability,
        description="Ultraviolet disinfection system"
    )


def create_chlorination_barrier(log_reduction: float, variability: float = 0.3) -> TreatmentBarrier:
    """Create chlorination barrier."""
    return TreatmentBarrier(
        name="Chlorination",
        treatment_type=TreatmentType.CHLORINATION,
        log_reduction_value=log_reduction,
        variability=variability,
        description="Chlorine disinfection"
    )


def create_membrane_barrier(log_reduction: float, variability: float = 0.1) -> TreatmentBarrier:
    """Create membrane filtration barrier."""
    return TreatmentBarrier(
        name="Membrane Filtration",
        treatment_type=TreatmentType.MEMBRANE_FILTRATION,
        log_reduction_value=log_reduction,
        variability=variability,
        description="Membrane filtration system"
    )


def create_wastewater_treatment_train() -> DilutionModel:
    """
    Create a typical wastewater treatment train.

    Returns:
        Configured DilutionModel with typical wastewater treatment barriers
    """
    model = DilutionModel()

    # Primary treatment (minimal pathogen removal)
    model.add_treatment_barrier(TreatmentBarrier(
        name="Primary Settling",
        treatment_type=TreatmentType.PHYSICAL,
        log_reduction_value=0.5,
        variability=0.2
    ))

    # Secondary treatment (biological)
    model.add_treatment_barrier(TreatmentBarrier(
        name="Activated Sludge",
        treatment_type=TreatmentType.BIOLOGICAL,
        log_reduction_value=2.0,
        variability=0.5
    ))

    # Tertiary treatment (disinfection)
    model.add_treatment_barrier(create_uv_barrier(3.0))

    return model


if __name__ == "__main__":
    # Example usage and testing
    print("Testing Dilution Modelling Integration")
    print("=" * 40)

    # Create dilution model
    model = DilutionModel()

    # Add treatment barriers (engineer-provided LRVs)
    model.add_treatment_barrier(TreatmentBarrier(
        name="Secondary Treatment",
        treatment_type=TreatmentType.BIOLOGICAL,
        log_reduction_value=2.5,
        variability=0.3
    ))

    model.add_treatment_barrier(create_uv_barrier(3.0))

    # Set dilution scenario
    scenario = DilutionScenario(
        initial_flow=0.5,  # m³/s discharge
        receiving_flow=10.0,  # m³/s river flow
        distance=5.0,  # km downstream
        decay_rate=0.1,  # per day
        travel_time=0.5  # days
    )
    model.set_dilution_scenario(scenario)

    # Test with initial concentration
    initial_conc = 1e6  # organisms/L

    print(f"Initial concentration: {initial_conc:.2e} organisms/L")
    print()

    # Apply complete scenario
    results = model.apply_complete_scenario(initial_conc)

    print("Concentration at each stage:")
    for stage, conc in results.items():
        print(f"  {stage}: {conc:.2e} organisms/L")

    print()
    print(model.get_treatment_summary())

    # Calculate overall reduction
    overall_reduction = initial_conc / results["final"]
    overall_lrv = np.log10(overall_reduction)
    print(f"\nOverall reduction: {overall_reduction:.1e} fold")
    print(f"Overall LRV: {overall_lrv:.1f} log₁₀")

    print("\nDilution modelling completed successfully!")