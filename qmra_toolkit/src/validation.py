"""
Validation utilities for QMRA Toolkit

This module provides comprehensive validation functions for input parameters,
configuration files, and data integrity checks.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Union, Any, Tuple
from pathlib import Path
import logging
from dataclasses import dataclass
from enum import Enum
import json
import yaml

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class ParameterType(Enum):
    """Supported parameter types for validation."""
    POSITIVE_FLOAT = "positive_float"
    POSITIVE_INT = "positive_int"
    PROBABILITY = "probability"
    CONCENTRATION = "concentration"
    VOLUME = "volume"
    FREQUENCY = "frequency"
    POPULATION = "population"
    ITERATIONS = "iterations"


@dataclass
class ValidationRule:
    """Validation rule definition."""
    param_name: str
    param_type: ParameterType
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    required: bool = True
    description: str = ""


class ParameterValidator:
    """Validates input parameters for QMRA assessments."""

    def __init__(self):
        """Initialize validator with standard rules."""
        self.rules = {
            "concentration": ValidationRule(
                "concentration", ParameterType.CONCENTRATION,
                min_value=0.0, max_value=1e12,
                description="Pathogen concentration (organisms per unit)"
            ),
            "volume": ValidationRule(
                "volume", ParameterType.VOLUME,
                min_value=0.1, max_value=10000.0,
                description="Exposure volume (mL for water, g for food)"
            ),
            "frequency": ValidationRule(
                "frequency", ParameterType.FREQUENCY,
                min_value=0.1, max_value=365.0,
                description="Exposure frequency (events per year)"
            ),
            "population": ValidationRule(
                "population", ParameterType.POPULATION,
                min_value=1, max_value=10000000,
                description="Population size"
            ),
            "iterations": ValidationRule(
                "iterations", ParameterType.ITERATIONS,
                min_value=100, max_value=1000000,
                description="Number of Monte Carlo iterations"
            ),
            "probability": ValidationRule(
                "probability", ParameterType.PROBABILITY,
                min_value=0.0, max_value=1.0,
                description="Probability value (0-1)"
            )
        }

    def validate_parameter(self, value: Any, rule: ValidationRule) -> Union[float, int]:
        """
        Validate a single parameter against its rule.

        Args:
            value: Parameter value to validate
            rule: Validation rule to apply

        Returns:
            Validated and converted parameter value

        Raises:
            ValidationError: If validation fails
        """
        if value is None and rule.required:
            raise ValidationError(f"Required parameter '{rule.param_name}' is missing")

        if value is None:
            return value

        # Type conversion and validation
        try:
            if rule.param_type in [ParameterType.POSITIVE_INT, ParameterType.POPULATION, ParameterType.ITERATIONS]:
                value = int(value)
                if value <= 0:
                    raise ValidationError(f"Parameter '{rule.param_name}' must be positive integer")
            else:
                value = float(value)
                if rule.param_type == ParameterType.POSITIVE_FLOAT and value <= 0:
                    raise ValidationError(f"Parameter '{rule.param_name}' must be positive")
        except (ValueError, TypeError) as e:
            raise ValidationError(f"Parameter '{rule.param_name}' must be numeric: {e}")

        # Range validation
        if rule.min_value is not None and value < rule.min_value:
            raise ValidationError(
                f"Parameter '{rule.param_name}' ({value}) is below minimum ({rule.min_value})"
            )

        if rule.max_value is not None and value > rule.max_value:
            raise ValidationError(
                f"Parameter '{rule.param_name}' ({value}) exceeds maximum ({rule.max_value})"
            )

        # Special validations
        if rule.param_type == ParameterType.PROBABILITY and not (0.0 <= value <= 1.0):
            raise ValidationError(f"Probability '{rule.param_name}' must be between 0 and 1")

        return value

    def validate_assessment_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate complete set of assessment parameters.

        Args:
            params: Dictionary of parameters to validate

        Returns:
            Dictionary of validated parameters

        Raises:
            ValidationError: If any validation fails
        """
        validated = {}
        errors = []

        for param_name, value in params.items():
            if param_name in self.rules:
                try:
                    validated[param_name] = self.validate_parameter(value, self.rules[param_name])
                except ValidationError as e:
                    errors.append(str(e))
            else:
                # Unknown parameter - log warning but don't fail
                logger.warning(f"Unknown parameter '{param_name}' - skipping validation")
                validated[param_name] = value

        if errors:
            raise ValidationError(f"Parameter validation failed:\n" + "\n".join(f"  - {e}" for e in errors))

        return validated

    def add_custom_rule(self, rule: ValidationRule) -> None:
        """Add a custom validation rule."""
        self.rules[rule.param_name] = rule


class DataValidator:
    """Validates data integrity and consistency."""

    @staticmethod
    def validate_pathogen_data(pathogen_data: Dict[str, Any]) -> bool:
        """
        Validate pathogen database structure and values.

        Args:
            pathogen_data: Pathogen data dictionary

        Returns:
            True if valid

        Raises:
            ValidationError: If validation fails
        """
        required_fields = ["name", "pathogen_type", "dose_response_models"]
        errors = []

        for field in required_fields:
            if field not in pathogen_data:
                errors.append(f"Missing required field: {field}")

        # Validate dose-response models
        if "dose_response_models" in pathogen_data:
            for model_name, model_data in pathogen_data["dose_response_models"].items():
                if not isinstance(model_data, dict):
                    errors.append(f"Dose-response model '{model_name}' must be a dictionary")
                    continue

                # Check for required model parameters
                if model_name == "beta_poisson":
                    required_params = ["alpha", "beta"]
                elif model_name == "exponential":
                    required_params = ["r"]
                else:
                    logger.warning(f"Unknown dose-response model: {model_name}")
                    continue

                for param in required_params:
                    if param not in model_data:
                        errors.append(f"Model '{model_name}' missing parameter: {param}")
                    elif not isinstance(model_data[param], (int, float)):
                        errors.append(f"Model '{model_name}' parameter '{param}' must be numeric")
                    elif model_data[param] <= 0:
                        errors.append(f"Model '{model_name}' parameter '{param}' must be positive")

        if errors:
            raise ValidationError(f"Pathogen data validation failed:\n" + "\n".join(f"  - {e}" for e in errors))

        return True

    @staticmethod
    def validate_concentration_array(concentrations: Union[float, np.ndarray, List[float]]) -> np.ndarray:
        """
        Validate and convert concentration data.

        Args:
            concentrations: Concentration values

        Returns:
            Validated numpy array of concentrations

        Raises:
            ValidationError: If validation fails
        """
        try:
            concentrations = np.asarray(concentrations, dtype=float)
        except (ValueError, TypeError) as e:
            raise ValidationError(f"Concentrations must be numeric: {e}")

        if concentrations.size == 0:
            raise ValidationError("Concentration array cannot be empty")

        if np.any(concentrations < 0):
            raise ValidationError("Concentrations cannot be negative")

        if np.any(np.isnan(concentrations)):
            raise ValidationError("Concentrations cannot contain NaN values")

        if np.any(np.isinf(concentrations)):
            raise ValidationError("Concentrations cannot contain infinite values")

        return concentrations

    @staticmethod
    def validate_results_structure(results: Dict[str, Any]) -> bool:
        """
        Validate QMRA results structure.

        Args:
            results: Results dictionary to validate

        Returns:
            True if valid

        Raises:
            ValidationError: If validation fails
        """
        required_fields = ["individual_risks", "population_risks", "assessment_parameters"]
        errors = []

        for field in required_fields:
            if field not in results:
                errors.append(f"Missing required results field: {field}")

        # Validate individual risks
        if "individual_risks" in results:
            risks = results["individual_risks"]
            if not isinstance(risks, (list, np.ndarray)):
                errors.append("Individual risks must be array-like")
            else:
                risks = np.asarray(risks)
                if risks.size == 0:
                    errors.append("Individual risks array cannot be empty")
                elif np.any(risks < 0) or np.any(risks > 1):
                    errors.append("Individual risks must be probabilities (0-1)")

        if errors:
            raise ValidationError(f"Results validation failed:\n" + "\n".join(f"  - {e}" for e in errors))

        return True


class FileValidator:
    """Validates configuration and data files."""

    @staticmethod
    def validate_json_file(file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Validate and load JSON file.

        Args:
            file_path: Path to JSON file

        Returns:
            Loaded JSON data

        Raises:
            ValidationError: If file is invalid
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise ValidationError(f"File not found: {file_path}")

        if not file_path.is_file():
            raise ValidationError(f"Path is not a file: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON in file {file_path}: {e}")
        except Exception as e:
            raise ValidationError(f"Error reading file {file_path}: {e}")

        return data

    @staticmethod
    def validate_yaml_file(file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Validate and load YAML file.

        Args:
            file_path: Path to YAML file

        Returns:
            Loaded YAML data

        Raises:
            ValidationError: If file is invalid
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise ValidationError(f"File not found: {file_path}")

        if not file_path.is_file():
            raise ValidationError(f"Path is not a file: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValidationError(f"Invalid YAML in file {file_path}: {e}")
        except Exception as e:
            raise ValidationError(f"Error reading file {file_path}: {e}")

        return data


def validate_assessment_inputs(
    pathogen: str,
    concentration: float,
    volume: Optional[float] = None,
    frequency: Optional[float] = None,
    population: Optional[int] = None,
    iterations: int = 10000
) -> Dict[str, Any]:
    """
    Comprehensive validation of QMRA assessment inputs.

    Args:
        pathogen: Pathogen name
        concentration: Pathogen concentration
        volume: Exposure volume
        frequency: Exposure frequency
        population: Population size
        iterations: Monte Carlo iterations

    Returns:
        Dictionary of validated parameters

    Raises:
        ValidationError: If any validation fails
    """
    validator = ParameterValidator()

    # Build parameter dictionary
    params = {
        "concentration": concentration,
        "iterations": iterations
    }

    if volume is not None:
        params["volume"] = volume
    if frequency is not None:
        params["frequency"] = frequency
    if population is not None:
        params["population"] = population

    # Validate pathogen name
    if not isinstance(pathogen, str) or not pathogen.strip():
        raise ValidationError("Pathogen name must be a non-empty string")

    # Validate parameters
    validated_params = validator.validate_assessment_parameters(params)
    validated_params["pathogen"] = pathogen.strip().lower()

    return validated_params


def create_validation_summary(validation_results: Dict[str, Any]) -> str:
    """
    Create human-readable validation summary.

    Args:
        validation_results: Results from validation functions

    Returns:
        Formatted validation summary
    """
    summary = ["QMRA Parameter Validation Summary"]
    summary.append("=" * 40)

    for param, value in validation_results.items():
        if isinstance(value, (int, float)):
            summary.append(f"  {param}: {value:g}")
        else:
            summary.append(f"  {param}: {value}")

    summary.append("")
    summary.append("✓ All parameters validated successfully")

    return "\n".join(summary)