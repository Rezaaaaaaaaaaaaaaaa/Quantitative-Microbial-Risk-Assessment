# Validation Module

Validation utilities for QMRA Toolkit

This module provides comprehensive validation functions for input parameters,
configuration files, and data integrity checks.

## Classes

### DataValidator

Validates data integrity and consistency.

### FileValidator

Validates configuration and data files.

### ParameterType

Supported parameter types for validation.

### ParameterValidator

Validates input parameters for QMRA assessments.

### ValidationError

Custom exception for validation errors.

### ValidationRule

Validation rule definition.

## Functions

### create_validation_summary(validation_results: Dict[str, Any]) -> str

Create human-readable validation summary.

Args:
    validation_results: Results from validation functions

Returns:
    Formatted validation summary

### validate_assessment_inputs(pathogen: str, concentration: float, volume: Optional[float] = None, frequency: Optional[float] = None, population: Optional[int] = None, iterations: int = 10000) -> Dict[str, Any]

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

