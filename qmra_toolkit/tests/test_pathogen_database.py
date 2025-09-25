#!/usr/bin/env python3
"""
Unit tests for pathogen database module.
"""

import unittest
import json
import tempfile
from pathlib import Path
import sys

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from pathogen_database import PathogenDatabase, get_norovirus_parameters


class TestPathogenDatabase(unittest.TestCase):
    """Test cases for PathogenDatabase class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create temporary test data
        self.test_data = {
            "test_pathogen": {
                "name": "Test Pathogen",
                "pathogen_type": "virus",
                "dose_response_models": {
                    "beta_poisson": {
                        "alpha": 0.1,
                        "beta": 0.2,
                        "source": "Test source"
                    },
                    "exponential": {
                        "r": 0.01,
                        "source": "Test exponential"
                    }
                },
                "illness_to_infection_ratio": 0.5,
                "dalys_per_case": 0.001,
                "exposure_routes": ["test_route"],
                "environmental_data": {
                    "survival_time_days": 30,
                    "typical_concentrations": {
                        "test_matrix": 1000
                    }
                }
            }
        }

        # Create temporary file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(self.test_data, self.temp_file)
        self.temp_file.close()

        # Initialize database with test data
        self.db = PathogenDatabase(self.temp_file.name)

    def tearDown(self):
        """Clean up test fixtures."""
        Path(self.temp_file.name).unlink()

    def test_load_pathogen_data(self):
        """Test loading pathogen data from file."""
        pathogens = self.db.get_available_pathogens()
        self.assertIn('test_pathogen', pathogens)

    def test_get_available_pathogens(self):
        """Test getting list of available pathogens."""
        pathogens = self.db.get_available_pathogens()
        self.assertIsInstance(pathogens, list)
        self.assertGreater(len(pathogens), 0)

    def test_get_pathogen_info(self):
        """Test getting pathogen information."""
        info = self.db.get_pathogen_info('test_pathogen')
        self.assertEqual(info['name'], 'Test Pathogen')
        self.assertEqual(info['pathogen_type'], 'virus')

    def test_get_pathogen_info_invalid(self):
        """Test getting info for invalid pathogen."""
        with self.assertRaises(ValueError):
            self.db.get_pathogen_info('invalid_pathogen')

    def test_get_dose_response_parameters(self):
        """Test getting dose-response parameters."""
        params = self.db.get_dose_response_parameters('test_pathogen', 'beta_poisson')
        self.assertEqual(params['alpha'], 0.1)
        self.assertEqual(params['beta'], 0.2)

    def test_get_dose_response_parameters_invalid_model(self):
        """Test getting parameters for invalid model."""
        with self.assertRaises(ValueError):
            self.db.get_dose_response_parameters('test_pathogen', 'invalid_model')

    def test_get_environmental_data(self):
        """Test getting environmental data."""
        env_data = self.db.get_environmental_data('test_pathogen')
        self.assertEqual(env_data['survival_time_days'], 30)

    def test_get_health_impact_data(self):
        """Test getting health impact data."""
        health_data = self.db.get_health_impact_data('test_pathogen')
        self.assertEqual(health_data['illness_to_infection_ratio'], 0.5)
        self.assertEqual(health_data['dalys_per_case'], 0.001)

    def test_validate_exposure_route(self):
        """Test validating exposure routes."""
        self.assertTrue(self.db.validate_exposure_route('test_pathogen', 'test_route'))
        self.assertFalse(self.db.validate_exposure_route('test_pathogen', 'invalid_route'))

    def test_get_typical_concentration(self):
        """Test getting typical concentrations."""
        conc = self.db.get_typical_concentration('test_pathogen', 'test_matrix')
        self.assertEqual(conc, 1000)

        # Test invalid matrix
        conc = self.db.get_typical_concentration('test_pathogen', 'invalid_matrix')
        self.assertIsNone(conc)

    def test_add_custom_pathogen(self):
        """Test adding custom pathogen."""
        custom_data = {
            "name": "Custom Pathogen",
            "pathogen_type": "bacteria",
            "dose_response_models": {
                "exponential": {"r": 0.05}
            }
        }

        self.db.add_custom_pathogen('custom_pathogen', custom_data)
        self.assertIn('custom_pathogen', self.db.get_available_pathogens())

    def test_add_custom_pathogen_missing_fields(self):
        """Test adding custom pathogen with missing required fields."""
        incomplete_data = {"name": "Incomplete"}

        with self.assertRaises(ValueError):
            self.db.add_custom_pathogen('incomplete', incomplete_data)

    def test_get_model_citation(self):
        """Test getting model citation."""
        citation = self.db.get_model_citation('test_pathogen', 'beta_poisson')
        self.assertEqual(citation, 'Test source')


class TestNorovirusConvenience(unittest.TestCase):
    """Test convenience functions."""

    def test_get_norovirus_parameters(self):
        """Test getting norovirus parameters."""
        try:
            params = get_norovirus_parameters()
            self.assertIn('alpha', params)
            self.assertIn('beta', params)
        except FileNotFoundError:
            # Skip if default data file not found
            self.skipTest("Default pathogen data file not found")


if __name__ == '__main__':
    unittest.main()