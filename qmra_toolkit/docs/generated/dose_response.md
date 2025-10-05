# Dose Response Module

Dose-Response Module for QMRA Toolkit

This module implements dose-response models for calculating infection probabilities
from pathogen exposure doses, including Beta-Poisson and exponential models.

## Classes

### BetaPoissonModel

Beta-Poisson dose-response model.

P(infection) = 1 - (1 + dose/beta)^(-alpha)

This is the most commonly used model for viral and bacterial pathogens.

### DoseResponseModel

Base class for dose-response models.

### ExponentialModel

Exponential dose-response model.

P(infection) = 1 - exp(-r * dose)

Often used for highly infectious pathogens or as a conservative approximation.

### HypergeometricModel

Hypergeometric dose-response model.

Used for some bacterial pathogens where exact microbial enumeration is important.

## Functions

### benchmark_model_performance(model: dose_response.DoseResponseModel, test_doses: numpy.ndarray) -> Dict

Benchmark model performance with test doses.

Args:
    model: Dose-response model to test
    test_doses: Array of test doses

Returns:
    Dictionary containing performance metrics

### calculate_illness_probability(infection_prob: Union[float, numpy.ndarray], illness_to_infection_ratio: float) -> Union[float, numpy.ndarray]

Calculate illness probability from infection probability.

Args:
    infection_prob: Probability of infection (0-1)
    illness_to_infection_ratio: Ratio of illness cases to infection cases

Returns:
    Probability of illness (0-1)

### create_dose_response_model(model_type: str, parameters: Dict) -> dose_response.DoseResponseModel

Factory function to create dose-response models.

Args:
    model_type: Type of model ("beta_poisson", "exponential", "hypergeometric")
    parameters: Model parameters

Returns:
    Appropriate dose-response model instance

Raises:
    ValueError: If model type is not recognized

