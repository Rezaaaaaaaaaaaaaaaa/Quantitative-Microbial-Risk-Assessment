#!/usr/bin/env python3
"""
Tests for validation module
"""

import unittest
import numpy as np
import tempfile
import json
import os
from pathlib import Path

# Add src directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from validation import (
    ParameterValidator, DataValidator, FileValidator, ValidationError,
    validate_assessment_inputs, ParameterType, ValidationRule
)


class TestParameterValidator(unittest.TestCase):
    """Test parameter validation functionality."""

    def setUp(self):
        self.validator = ParameterValidator()

    def test_positive_float_validation(self):
        """Test positive float parameter validation."""
        rule = ValidationRule("test_param", ParameterType.POSITIVE_FLOAT, min_value=0.1, max_value=100.0)

        # Valid values
        self.assertEqual(self.validator.validate_parameter(1.5, rule), 1.5)
        self.assertEqual(self.validator.validate_parameter(50.0, rule), 50.0)

        # Invalid values
        with self.assertRaises(ValidationError):
            self.validator.validate_parameter(-1.0, rule)  # Negative
        with self.assertRaises(ValidationError):
            self.validator.validate_parameter(0.0, rule)   # Zero
        with self.assertRaises(ValidationError):
            self.validator.validate_parameter(150.0, rule) # Too large

    def test_concentration_validation(self):
        """Test concentration parameter validation."""
        params = {
            "concentration": 100.0,
            "volume": 50.0,
            "frequency": 12.0,
            "population": 10000,
            "iterations": 1000
        }

        validated = self.validator.validate_assessment_parameters(params)
        self.assertEqual(validated["concentration"], 100.0)
        self.assertEqual(validated["population"], 10000)

    def test_invalid_concentration(self):
        """Test validation of invalid concentration values."""
        params = {"concentration": -10.0}

        with self.assertRaises(ValidationError):
            self.validator.validate_assessment_parameters(params)

    def test_missing_required_parameter(self):
        """Test handling of missing required parameters."""
        rule = ValidationRule("required_param", ParameterType.POSITIVE_FLOAT, required=True)

        with self.assertRaises(ValidationError):
            self.validator.validate_parameter(None, rule)

    def test_optional_parameter(self):
        """Test handling of optional parameters."""
        rule = ValidationRule("optional_param", ParameterType.POSITIVE_FLOAT, required=False)

        result = self.validator.validate_parameter(None, rule)
        self.assertIsNone(result)

    def test_probability_validation(self):
        """Test probability parameter validation."""
        rule = ValidationRule("prob", ParameterType.PROBABILITY)

        # Valid probabilities
        self.assertEqual(self.validator.validate_parameter(0.0, rule), 0.0)
        self.assertEqual(self.validator.validate_parameter(0.5, rule), 0.5)
        self.assertEqual(self.validator.validate_parameter(1.0, rule), 1.0)

        # Invalid probabilities
        with self.assertRaises(ValidationError):
            self.validator.validate_parameter(-0.1, rule)
        with self.assertRaises(ValidationError):
            self.validator.validate_parameter(1.1, rule)

    def test_integer_validation(self):
        """Test integer parameter validation."""
        rule = ValidationRule("int_param", ParameterType.POSITIVE_INT, min_value=1, max_value=1000)

        # Valid integers
        self.assertEqual(self.validator.validate_parameter(10, rule), 10)
        self.assertEqual(self.validator.validate_parameter("20", rule), 20)  # String conversion

        # Invalid values
        with self.assertRaises(ValidationError):
            self.validator.validate_parameter(0, rule)     # Zero
        with self.assertRaises(ValidationError):
            self.validator.validate_parameter(1500, rule) # Too large

    def test_custom_rule(self):
        """Test adding custom validation rules."""
        custom_rule = ValidationRule(
            "custom_param", ParameterType.POSITIVE_FLOAT,
            min_value=10.0, max_value=20.0,
            description="Custom parameter for testing"
        )

        self.validator.add_custom_rule(custom_rule)

        params = {"custom_param": 15.0}
        validated = self.validator.validate_assessment_parameters(params)
        self.assertEqual(validated["custom_param"], 15.0)


class TestDataValidator(unittest.TestCase):
    """Test data validation functionality."""

    def test_pathogen_data_validation(self):
        """Test pathogen data structure validation."""
        valid_pathogen_data = {
            "name": "Test Pathogen",
            "pathogen_type": "virus",
            "dose_response_models": {
                "beta_poisson": {
                    "alpha": 0.04,
                    "beta": 0.055,
                    "source": "Test source"
                },
                "exponential": {
                    "r": 0.5,
                    "source": "Test source"
                }
            }
        }

        # Should pass validation
        self.assertTrue(DataValidator.validate_pathogen_data(valid_pathogen_data))

    def test_invalid_pathogen_data(self):
        """Test validation of invalid pathogen data."""
        # Missing required fields
        invalid_data = {
            "name": "Test Pathogen"
            # Missing pathogen_type and dose_response_models
        }

        with self.assertRaises(ValidationError):
            DataValidator.validate_pathogen_data(invalid_data)

    def test_concentration_array_validation(self):
        """Test concentration array validation."""
        # Valid arrays
        valid_concentrations = [1.0, 10.0, 100.0]
        result = DataValidator.validate_concentration_array(valid_concentrations)
        np.testing.assert_array_equal(result, np.array([1.0, 10.0, 100.0]))

        # Single value
        single_value = 50.0
        result = DataValidator.validate_concentration_array(single_value)
        np.testing.assert_array_equal(result, np.array([50.0]))

    def test_invalid_concentration_array(self):
        """Test validation of invalid concentration arrays."""
        # Negative concentrations
        with self.assertRaises(ValidationError):
            DataValidator.validate_concentration_array([-1.0, 10.0])

        # NaN values
        with self.assertRaises(ValidationError):
            DataValidator.validate_concentration_array([1.0, np.nan])

        # Infinite values
        with self.assertRaises(ValidationError):
            DataValidator.validate_concentration_array([1.0, np.inf])

        # Empty array
        with self.assertRaises(ValidationError):
            DataValidator.validate_concentration_array([])

    def test_results_structure_validation(self):
        """Test QMRA results structure validation."""
        valid_results = {
            "individual_risks": [0.1, 0.2, 0.15],
            "population_risks": {"expected_cases": 100},
            "assessment_parameters": {"pathogen": "norovirus"}
        }

        self.assertTrue(DataValidator.validate_results_structure(valid_results))

    def test_invalid_results_structure(self):
        """Test validation of invalid results structure."""
        # Missing required fields
        invalid_results = {
            "individual_risks": [0.1, 0.2]
            # Missing population_risks and assessment_parameters
        }

        with self.assertRaises(ValidationError):
            DataValidator.validate_results_structure(invalid_results)

        # Invalid risk values
        invalid_risks = {
            "individual_risks": [-0.1, 1.5],  # Invalid probabilities
            "population_risks": {},
            "assessment_parameters": {}
        }

        with self.assertRaises(ValidationError):
            DataValidator.validate_results_structure(invalid_risks)


class TestFileValidator(unittest.TestCase):
    """Test file validation functionality."""

    def setUp(self):
        # Create temporary files for testing
        self.temp_dir = tempfile.mkdtemp()

        # Valid JSON file
        self.json_file = Path(self.temp_dir) / "test.json"
        with open(self.json_file, 'w') as f:
            json.dump({"test": "data"}, f)

        # Invalid JSON file
        self.invalid_json_file = Path(self.temp_dir) / "invalid.json"
        with open(self.invalid_json_file, 'w') as f:
            f.write("{ invalid json }")

    def tearDown(self):
        # Clean up temporary files
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_valid_json_file(self):
        """Test validation of valid JSON file."""
        data = FileValidator.validate_json_file(self.json_file)
        self.assertEqual(data, {"test": "data"})

    def test_invalid_json_file(self):
        """Test validation of invalid JSON file."""
        with self.assertRaises(ValidationError):
            FileValidator.validate_json_file(self.invalid_json_file)

    def test_nonexistent_file(self):
        """Test validation of nonexistent file."""
        nonexistent_file = Path(self.temp_dir) / "nonexistent.json"

        with self.assertRaises(ValidationError):
            FileValidator.validate_json_file(nonexistent_file)


class TestAssessmentInputValidation(unittest.TestCase):
    """Test comprehensive assessment input validation."""

    def test_valid_assessment_inputs(self):
        """Test validation of valid assessment inputs."""
        validated = validate_assessment_inputs(
            pathogen="norovirus",
            concentration=100.0,
            volume=50.0,
            frequency=12.0,
            population=10000,
            iterations=1000
        )

        self.assertEqual(validated["pathogen"], "norovirus")
        self.assertEqual(validated["concentration"], 100.0)
        self.assertEqual(validated["volume"], 50.0)
        self.assertEqual(validated["frequency"], 12.0)
        self.assertEqual(validated["population"], 10000)
        self.assertEqual(validated["iterations"], 1000)

    def test_invalid_pathogen_name(self):
        """Test validation with invalid pathogen name."""
        with self.assertRaises(ValidationError):
            validate_assessment_inputs(
                pathogen="",  # Empty pathogen name
                concentration=100.0,
                iterations=1000
            )

    def test_invalid_concentration(self):
        """Test validation with invalid concentration."""
        with self.assertRaises(ValidationError):
            validate_assessment_inputs(
                pathogen="norovirus",
                concentration=-10.0,  # Negative concentration
                iterations=1000
            )

    def test_optional_parameters(self):
        """Test validation with optional parameters."""
        validated = validate_assessment_inputs(
            pathogen="norovirus",
            concentration=100.0,
            iterations=1000
            # volume, frequency, and population are optional
        )

        self.assertEqual(validated["pathogen"], "norovirus")
        self.assertEqual(validated["concentration"], 100.0)
        self.assertEqual(validated["iterations"], 1000)
        self.assertNotIn("volume", validated)
        self.assertNotIn("frequency", validated)
        self.assertNotIn("population", validated)

    def test_parameter_type_conversion(self):
        """Test automatic parameter type conversion."""
        validated = validate_assessment_inputs(
            pathogen="  Norovirus  ",  # Whitespace should be stripped
            concentration="100.5",      # String should be converted to float
            population="10000",         # String should be converted to int
            iterations=1000
        )

        self.assertEqual(validated["pathogen"], "norovirus")  # Lowercased and stripped
        self.assertEqual(validated["concentration"], 100.5)
        self.assertEqual(validated["population"], 10000)


if __name__ == '__main__':
    unittest.main()