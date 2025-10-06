"""
Test suite for advanced dose-response models
"""

import unittest
import numpy as np
from src.dose_response_advanced import DoseResponseModels, DoseResponseSelector, calculate_n50


class TestDoseResponseModels(unittest.TestCase):
    """Test individual dose-response models"""

    def setUp(self):
        self.models = DoseResponseModels()
        self.selector = DoseResponseSelector()

    def test_exponential_model(self):
        """Test exponential dose-response model"""
        r = 0.01
        dose = np.array([10, 100, 1000])
        risk = self.models.exponential(r, dose)

        # Check shape
        self.assertEqual(risk.shape, dose.shape)

        # Check bounds
        self.assertTrue(np.all((risk >= 0) & (risk <= 1)))

        # Check monotonicity
        self.assertTrue(np.all(np.diff(risk) >= 0))

    def test_beta_poisson_model(self):
        """Test beta-poisson model"""
        alpha = 0.145
        beta = 7.59
        dose = np.array([10, 100, 1000])
        risk = self.models.beta_poisson(alpha, beta, dose)

        # Check shape
        self.assertEqual(risk.shape, dose.shape)

        # Check bounds
        self.assertTrue(np.all((risk >= 0) & (risk <= 1)))

    def test_fractional_poisson_model(self):
        """Test fractional poisson model"""
        p = 0.72
        mu = 1106
        dose = np.array([10, 100, 1000])
        risk = self.models.fractional_poisson(p, mu, dose)

        # Check shape
        self.assertEqual(risk.shape, dose.shape)

        # Check bounds
        self.assertTrue(np.all((risk >= 0) & (risk <= 1)))

    def test_weibull_model(self):
        """Test Weibull model"""
        q1 = 0.00752
        q2 = 0.131
        dose = np.array([10, 100, 1000])
        risk = self.models.weibull(q1, q2, dose)

        # Check shape
        self.assertEqual(risk.shape, dose.shape)

        # Check bounds
        self.assertTrue(np.all((risk >= 0) & (risk <= 1)))

    def test_log_logistic_model(self):
        """Test log-logistic model"""
        q1 = 1.0
        q2 = 0.5
        dose = np.array([10, 100, 1000])
        risk = self.models.log_logistic(q1, q2, dose)

        # Check shape
        self.assertEqual(risk.shape, dose.shape)

        # Check bounds
        self.assertTrue(np.all((risk >= 0) & (risk <= 1)))

    def test_model_selector(self):
        """Test model selector functionality"""
        dose = 100
        params = {'r': 0.01}

        risk = self.selector.calculate_risk('exponential', dose, params)

        self.assertIsInstance(risk, (float, np.floating))
        self.assertTrue(0 <= risk <= 1)

    def test_compare_models(self):
        """Test model comparison"""
        dose = np.array([10, 100, 1000])
        models_params = {
            'exponential': {'r': 0.01},
            'beta_poisson': {'alpha': 0.145, 'beta': 7.59}
        }

        results = self.selector.compare_models(dose, models_params)

        self.assertEqual(len(results), 2)
        self.assertIn('exponential', results)
        self.assertIn('beta_poisson', results)

    def test_zero_dose(self):
        """Test models with zero dose"""
        dose = 0

        # Exponential
        risk = self.models.exponential(0.01, dose)
        self.assertEqual(risk, 0)

        # Beta-Poisson
        risk = self.models.beta_poisson(0.145, 7.59, dose)
        self.assertEqual(risk, 0)

    def test_invalid_parameters(self):
        """Test model validation"""
        dose = 100

        # Invalid r for exponential
        with self.assertRaises(ValueError):
            self.models.exponential(1.5, dose)

        # Invalid alpha for beta-poisson
        with self.assertRaises(ValueError):
            self.models.beta_poisson(-0.5, 1.0, dose)

    def test_n50_calculation(self):
        """Test N50 calculation"""
        params = {'r': 0.0199}  # Known Cryptosporidium parameter
        n50 = calculate_n50('exponential', params)

        # N50 should be around 35 for these parameters
        self.assertTrue(30 < n50 < 40)


if __name__ == '__main__':
    unittest.main()