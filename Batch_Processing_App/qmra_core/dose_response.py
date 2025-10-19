"""
Dose-Response Module for QMRA Toolkit

This module implements dose-response models for calculating infection probabilities
from pathogen exposure doses, including Beta-Poisson and exponential models.
"""

import numpy as np
from typing import Union, Dict, Optional
from scipy.special import gamma, gammaln, hyp2f1
import warnings


class DoseResponseModel:
    """Base class for dose-response models."""

    def __init__(self, parameters: Dict):
        """
        Initialize dose-response model.

        Args:
            parameters: Dictionary containing model parameters
        """
        self.parameters = parameters
        self.validate_parameters()

    def validate_parameters(self) -> None:
        """Validate model parameters. Should be implemented by subclasses."""
        pass

    def calculate_infection_probability(self, dose: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Calculate infection probability from dose.

        Args:
            dose: Pathogen dose (organisms)

        Returns:
            Probability of infection (0-1)
        """
        raise NotImplementedError("Subclasses must implement this method")

    def get_model_info(self) -> Dict:
        """Get model information including parameters and citation."""
        return {
            "model_type": self.__class__.__name__,
            "parameters": self.parameters,
            "citation": self.parameters.get("source", "No citation available")
        }


class BetaPoissonModel(DoseResponseModel):
    """
    Beta-Poisson dose-response model.

    P(infection) = 1 - (1 + dose/beta)^(-alpha)

    This is the most commonly used model for viral and bacterial pathogens.
    """

    def validate_parameters(self) -> None:
        """Validate Beta-Poisson parameters."""
        required_params = ["alpha", "beta"]
        for param in required_params:
            if param not in self.parameters:
                raise ValueError(f"Missing required parameter: {param}")

        if self.parameters["alpha"] <= 0:
            raise ValueError("Alpha parameter must be positive")
        if self.parameters["beta"] <= 0:
            raise ValueError("Beta parameter must be positive")

    def calculate_infection_probability(self, dose: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Calculate infection probability using Beta-Poisson model.

        Args:
            dose: Pathogen dose (organisms)

        Returns:
            Probability of infection (0-1)
        """
        dose = np.asarray(dose)
        alpha = self.parameters["alpha"]
        beta = self.parameters["beta"]

        # Handle zero and negative doses
        if np.any(dose < 0):
            warnings.warn("Negative doses encountered, setting to zero")
            dose = np.maximum(dose, 0)

        # Beta-Poisson formula: P = 1 - (1 + dose/beta)^(-alpha)
        with np.errstate(over='warn', divide='warn'):
            prob = 1 - np.power(1 + dose / beta, -alpha)

        # Ensure probabilities are in valid range [0, 1]
        prob = np.clip(prob, 0, 1)

        return prob if prob.shape else float(prob)

    def calculate_dose_for_risk(self, target_risk: float) -> float:
        """
        Calculate dose required to achieve target infection risk.

        Args:
            target_risk: Target infection probability (0-1)

        Returns:
            Required dose (organisms)
        """
        if not 0 < target_risk < 1:
            raise ValueError("Target risk must be between 0 and 1")

        alpha = self.parameters["alpha"]
        beta = self.parameters["beta"]

        # Solve: target_risk = 1 - (1 + dose/beta)^(-alpha)
        # Rearranged: dose = beta * ((1 - target_risk)^(-1/alpha) - 1)
        dose = beta * (np.power(1 - target_risk, -1/alpha) - 1)
        return float(dose)


class ExponentialModel(DoseResponseModel):
    """
    Exponential dose-response model.

    P(infection) = 1 - exp(-r * dose)

    Often used for highly infectious pathogens or as a conservative approximation.
    """

    def validate_parameters(self) -> None:
        """Validate exponential model parameters."""
        if "r" not in self.parameters:
            raise ValueError("Missing required parameter: r")

        if self.parameters["r"] <= 0:
            raise ValueError("r parameter must be positive")

    def calculate_infection_probability(self, dose: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Calculate infection probability using exponential model.

        Args:
            dose: Pathogen dose (organisms)

        Returns:
            Probability of infection (0-1)
        """
        dose = np.asarray(dose)
        r = self.parameters["r"]

        # Handle zero and negative doses
        if np.any(dose < 0):
            warnings.warn("Negative doses encountered, setting to zero")
            dose = np.maximum(dose, 0)

        # Exponential formula: P = 1 - exp(-r * dose)
        prob = 1 - np.exp(-r * dose)

        # Ensure probabilities are in valid range [0, 1]
        prob = np.clip(prob, 0, 1)

        return prob if prob.shape else float(prob)

    def calculate_dose_for_risk(self, target_risk: float) -> float:
        """
        Calculate dose required to achieve target infection risk.

        Args:
            target_risk: Target infection probability (0-1)

        Returns:
            Required dose (organisms)
        """
        if not 0 < target_risk < 1:
            raise ValueError("Target risk must be between 0 and 1")

        r = self.parameters["r"]

        # Solve: target_risk = 1 - exp(-r * dose)
        # Rearranged: dose = -ln(1 - target_risk) / r
        dose = -np.log(1 - target_risk) / r
        return float(dose)


class HypergeometricModel(DoseResponseModel):
    """
    Hypergeometric dose-response model.

    Used for some bacterial pathogens where exact microbial enumeration is important.
    """

    def validate_parameters(self) -> None:
        """Validate hypergeometric model parameters."""
        required_params = ["alpha", "beta"]
        for param in required_params:
            if param not in self.parameters:
                raise ValueError(f"Missing required parameter: {param}")

    def calculate_infection_probability(self, dose: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Calculate infection probability using hypergeometric model.

        Args:
            dose: Pathogen dose (organisms)

        Returns:
            Probability of infection (0-1)
        """
        # This is a simplified implementation - more complex versions exist
        # For now, use Beta-Poisson approximation
        alpha = self.parameters["alpha"]
        beta = self.parameters["beta"]

        dose = np.asarray(dose)
        dose = np.maximum(dose, 0)

        prob = 1 - np.power(1 + dose / beta, -alpha)
        prob = np.clip(prob, 0, 1)

        return prob if prob.shape else float(prob)

    def calculate_dose_for_risk(self, target_risk: float) -> float:
        """Calculate dose for target risk using Beta-Poisson approximation."""
        alpha = self.parameters["alpha"]
        beta = self.parameters["beta"]

        if not 0 < target_risk < 1:
            raise ValueError("Target risk must be between 0 and 1")

        dose = beta * (np.power(1 - target_risk, -1/alpha) - 1)
        return float(dose)


def create_dose_response_model(model_type: str, parameters: Dict) -> DoseResponseModel:
    """
    Factory function to create dose-response models.

    Args:
        model_type: Type of model ("beta_poisson", "exponential", "hypergeometric")
        parameters: Model parameters

    Returns:
        Appropriate dose-response model instance

    Raises:
        ValueError: If model type is not recognized
    """
    model_types = {
        "beta_poisson": BetaPoissonModel,
        "exponential": ExponentialModel,
        "hypergeometric": HypergeometricModel
    }

    if model_type.lower() not in model_types:
        available = ", ".join(model_types.keys())
        raise ValueError(f"Unknown model type: {model_type}. Available: {available}")

    model_class = model_types[model_type.lower()]
    return model_class(parameters)


def calculate_illness_probability(infection_prob: Union[float, np.ndarray],
                                illness_to_infection_ratio: float) -> Union[float, np.ndarray]:
    """
    Calculate illness probability from infection probability.

    Args:
        infection_prob: Probability of infection (0-1)
        illness_to_infection_ratio: Ratio of illness cases to infection cases

    Returns:
        Probability of illness (0-1)
    """
    if not 0 <= illness_to_infection_ratio <= 1:
        raise ValueError("Illness to infection ratio must be between 0 and 1")

    illness_prob = np.asarray(infection_prob) * illness_to_infection_ratio
    return illness_prob if illness_prob.shape else float(illness_prob)


def benchmark_model_performance(model: DoseResponseModel, test_doses: np.ndarray) -> Dict:
    """
    Benchmark model performance with test doses.

    Args:
        model: Dose-response model to test
        test_doses: Array of test doses

    Returns:
        Dictionary containing performance metrics
    """
    import time

    start_time = time.perf_counter()
    probabilities = model.calculate_infection_probability(test_doses)
    end_time = time.perf_counter()

    return {
        "execution_time_seconds": end_time - start_time,
        "test_doses_count": len(test_doses),
        "mean_probability": float(np.mean(probabilities)),
        "min_probability": float(np.min(probabilities)),
        "max_probability": float(np.max(probabilities)),
        "model_info": model.get_model_info()
    }


if __name__ == "__main__":
    # Example usage and testing
    print("Testing QMRA Dose-Response Models")
    print("=" * 40)

    # Test Beta-Poisson model with norovirus parameters
    norovirus_params = {"alpha": 0.04, "beta": 0.055, "source": "Teunis et al. (2008)"}
    bp_model = BetaPoissonModel(norovirus_params)

    test_doses = np.array([1, 10, 100, 1000])
    probabilities = bp_model.calculate_infection_probability(test_doses)

    print("Beta-Poisson Model (Norovirus):")
    for dose, prob in zip(test_doses, probabilities):
        print(f"  Dose {dose}: {prob:.4f} infection probability")

    # Test exponential model
    exp_params = {"r": 0.5, "source": "Conservative approximation"}
    exp_model = ExponentialModel(exp_params)

    print("\nExponential Model:")
    exp_probs = exp_model.calculate_infection_probability(test_doses)
    for dose, prob in zip(test_doses, exp_probs):
        print(f"  Dose {dose}: {prob:.4f} infection probability")

    # Test dose for target risk
    target_risk = 1e-4  # 1 in 10,000
    required_dose = bp_model.calculate_dose_for_risk(target_risk)
    print(f"\nDose for {target_risk} risk: {required_dose:.2f} organisms")

    # Benchmark performance
    large_dose_array = np.logspace(0, 5, 10000)  # 1 to 100,000 organisms
    benchmark_results = benchmark_model_performance(bp_model, large_dose_array)
    print(f"\nBenchmark Results:")
    print(f"  Execution time: {benchmark_results['execution_time_seconds']:.4f} seconds")
    print(f"  Mean probability: {benchmark_results['mean_probability']:.4f}")