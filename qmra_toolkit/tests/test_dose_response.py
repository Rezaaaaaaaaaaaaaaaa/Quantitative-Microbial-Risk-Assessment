#!/usr/bin/env python3
"""
Unit tests for dose-response module.
"""

import unittest
import numpy as np
import warnings
from pathlib import Path
import sys

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from dose_response import (
    BetaPoissonModel, ExponentialModel, HypergeometricModel,
    create_dose_response_model, calculate_illness_probability,
    benchmark_model_performance
)


class TestBetaPoissonModel(unittest.TestCase):
    """Test cases for Beta-Poisson dose-response model."""

    def setUp(self):
        """Set up test fixtures."""
        self.params = {"alpha": 0.1, "beta": 50.0, "source": "Test"}
        self.model = BetaPoissonModel(self.params)

    def test_initialization(self):
        """Test model initialization."""
        self.assertEqual(self.model.parameters['alpha'], 0.1)
        self.assertEqual(self.model.parameters['beta'], 50.0)

    def test_invalid_parameters(self):
        """Test validation of invalid parameters."""
        # Missing parameters
        with self.assertRaises(ValueError):
            BetaPoissonModel({"alpha": 0.1})

        # Negative parameters
        with self.assertRaises(ValueError):
            BetaPoissonModel({"alpha": -0.1, "beta": 50.0})

        with self.assertRaises(ValueError):
            BetaPoissonModel({"alpha": 0.1, "beta": -50.0})

    def test_single_dose(self):
        """Test calculation with single dose."""
        prob = self.model.calculate_infection_probability(10.0)
        self.assertIsInstance(prob, float)
        self.assertGreaterEqual(prob, 0.0)
        self.assertLessEqual(prob, 1.0)

    def test_array_doses(self):
        """Test calculation with array of doses."""
        doses = np.array([1, 10, 100, 1000])
        probs = self.model.calculate_infection_probability(doses)

        self.assertIsInstance(probs, np.ndarray)
        self.assertEqual(len(probs), len(doses))
        self.assertTrue(np.all(probs >= 0))
        self.assertTrue(np.all(probs <= 1))

        # Check monotonicity (higher doses should give higher probabilities)
        self.assertTrue(np.all(np.diff(probs) >= 0))

    def test_zero_dose(self):
        """Test calculation with zero dose."""
        prob = self.model.calculate_infection_probability(0.0)
        self.assertEqual(prob, 0.0)

    def test_negative_dose(self):
        """Test calculation with negative dose."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            prob = self.model.calculate_infection_probability(-10.0)
            self.assertEqual(prob, 0.0)
            self.assertEqual(len(w), 1)

    def test_very_high_dose(self):
        """Test calculation with very high dose."""
        prob = self.model.calculate_infection_probability(1e10)
        self.assertLessEqual(prob, 1.0)

    def test_calculate_dose_for_risk(self):
        """Test calculating dose for target risk."""
        target_risk = 0.01  # 1%
        dose = self.model.calculate_dose_for_risk(target_risk)

        # Verify the calculated dose gives approximately the target risk
        actual_risk = self.model.calculate_infection_probability(dose)
        self.assertAlmostEqual(actual_risk, target_risk, places=3)

    def test_calculate_dose_for_risk_invalid(self):
        """Test calculating dose for invalid target risk."""
        with self.assertRaises(ValueError):
            self.model.calculate_dose_for_risk(0.0)

        with self.assertRaises(ValueError):
            self.model.calculate_dose_for_risk(1.0)

        with self.assertRaises(ValueError):
            self.model.calculate_dose_for_risk(-0.1)

    def test_get_model_info(self):
        """Test getting model information."""
        info = self.model.get_model_info()
        self.assertIn('model_type', info)
        self.assertIn('parameters', info)
        self.assertIn('citation', info)


class TestExponentialModel(unittest.TestCase):
    """Test cases for Exponential dose-response model."""

    def setUp(self):
        """Set up test fixtures."""
        self.params = {"r": 0.01, "source": "Test"}
        self.model = ExponentialModel(self.params)

    def test_initialization(self):
        """Test model initialization."""
        self.assertEqual(self.model.parameters['r'], 0.01)

    def test_invalid_parameters(self):
        """Test validation of invalid parameters."""
        with self.assertRaises(ValueError):
            ExponentialModel({})

        with self.assertRaises(ValueError):
            ExponentialModel({"r": -0.01})

    def test_single_dose(self):
        """Test calculation with single dose."""
        prob = self.model.calculate_infection_probability(100.0)
        expected = 1 - np.exp(-0.01 * 100.0)
        self.assertAlmostEqual(prob, expected, places=6)

    def test_array_doses(self):
        """Test calculation with array of doses."""
        doses = np.array([0, 50, 100, 200])
        probs = self.model.calculate_infection_probability(doses)

        # Check first element (should be 0)
        self.assertEqual(probs[0], 0.0)

        # Check monotonicity
        self.assertTrue(np.all(np.diff(probs) >= 0))

    def test_calculate_dose_for_risk(self):
        """Test calculating dose for target risk."""
        target_risk = 0.1  # 10%
        dose = self.model.calculate_dose_for_risk(target_risk)

        # Verify using analytical solution: dose = -ln(1 - target_risk) / r
        expected_dose = -np.log(1 - target_risk) / 0.01
        self.assertAlmostEqual(dose, expected_dose, places=6)


class TestHypergeometricModel(unittest.TestCase):
    """Test cases for Hypergeometric dose-response model."""

    def setUp(self):
        """Set up test fixtures."""
        self.params = {"alpha": 0.2, "beta": 100.0, "source": "Test"}
        self.model = HypergeometricModel(self.params)

    def test_initialization(self):
        """Test model initialization."""
        self.assertEqual(self.model.parameters['alpha'], 0.2)
        self.assertEqual(self.model.parameters['beta'], 100.0)

    def test_calculation(self):
        """Test probability calculation."""
        prob = self.model.calculate_infection_probability(10.0)
        self.assertGreaterEqual(prob, 0.0)
        self.assertLessEqual(prob, 1.0)


class TestFactoryFunction(unittest.TestCase):
    """Test cases for model factory function."""

    def test_create_beta_poisson(self):
        """Test creating Beta-Poisson model."""
        params = {"alpha": 0.1, "beta": 50.0}
        model = create_dose_response_model("beta_poisson", params)
        self.assertIsInstance(model, BetaPoissonModel)

    def test_create_exponential(self):
        """Test creating exponential model."""
        params = {"r": 0.01}
        model = create_dose_response_model("exponential", params)
        self.assertIsInstance(model, ExponentialModel)

    def test_create_hypergeometric(self):
        """Test creating hypergeometric model."""
        params = {"alpha": 0.2, "beta": 100.0}
        model = create_dose_response_model("hypergeometric", params)
        self.assertIsInstance(model, HypergeometricModel)

    def test_invalid_model_type(self):
        """Test creating model with invalid type."""
        with self.assertRaises(ValueError):
            create_dose_response_model("invalid_model", {})


class TestUtilityFunctions(unittest.TestCase):
    """Test cases for utility functions."""

    def test_calculate_illness_probability(self):
        """Test calculating illness probability."""
        infection_prob = 0.1
        illness_ratio = 0.7
        illness_prob = calculate_illness_probability(infection_prob, illness_ratio)

        expected = infection_prob * illness_ratio
        self.assertAlmostEqual(illness_prob, expected, places=6)

    def test_calculate_illness_probability_array(self):
        """Test calculating illness probability with arrays."""
        infection_probs = np.array([0.1, 0.2, 0.3])
        illness_ratio = 0.5
        illness_probs = calculate_illness_probability(infection_probs, illness_ratio)

        expected = infection_probs * illness_ratio
        np.testing.assert_array_almost_equal(illness_probs, expected)

    def test_calculate_illness_probability_invalid_ratio(self):
        """Test illness probability with invalid ratio."""
        with self.assertRaises(ValueError):
            calculate_illness_probability(0.1, -0.1)

        with self.assertRaises(ValueError):
            calculate_illness_probability(0.1, 1.5)

    def test_benchmark_model_performance(self):
        """Test benchmarking model performance."""
        params = {"alpha": 0.1, "beta": 50.0}
        model = BetaPoissonModel(params)
        test_doses = np.logspace(0, 3, 100)

        results = benchmark_model_performance(model, test_doses)

        self.assertIn('execution_time_seconds', results)
        self.assertIn('test_doses_count', results)
        self.assertIn('mean_probability', results)
        self.assertIn('model_info', results)

        self.assertEqual(results['test_doses_count'], 100)
        self.assertGreaterEqual(results['execution_time_seconds'], 0)  # May be 0 for very fast operations


class TestModelValidation(unittest.TestCase):
    """Test cases for model validation against literature."""

    def test_norovirus_beta_poisson(self):
        """Test norovirus Beta-Poisson model against literature values."""
        # Parameters from Teunis et al. (2008)
        params = {"alpha": 0.04, "beta": 0.055}
        model = BetaPoissonModel(params)

        # Test some expected values (approximate)
        prob_1 = model.calculate_infection_probability(1.0)
        prob_10 = model.calculate_infection_probability(10.0)
        prob_100 = model.calculate_infection_probability(100.0)

        # Probabilities should increase with dose
        self.assertLess(prob_1, prob_10)
        self.assertLess(prob_10, prob_100)

        # Check reasonable ranges (these are approximations)
        # With alpha=0.04, beta=0.055:
        # - dose=1: P ≈ 0.111 (11.1%)
        # - dose=100: P ≈ 0.26 (26%)
        self.assertGreater(prob_1, 0.01)    # Should be > 1%
        self.assertLess(prob_1, 0.15)       # Should be < 15%
        self.assertGreater(prob_100, 0.2)   # Should be > 20%
        self.assertLess(prob_100, 0.4)      # Should be < 40%

    def test_cryptosporidium_exponential(self):
        """Test Cryptosporidium exponential model."""
        # Parameters from literature
        params = {"r": 0.0042}
        model = ExponentialModel(params)

        # Test ID50 (dose for 50% infection probability)
        dose_50 = model.calculate_dose_for_risk(0.5)
        expected_id50 = np.log(2) / 0.0042  # Analytical solution
        self.assertAlmostEqual(dose_50, expected_id50, places=1)


if __name__ == '__main__':
    unittest.main()