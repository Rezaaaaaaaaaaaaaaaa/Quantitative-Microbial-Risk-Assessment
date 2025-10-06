"""
Test suite for advanced pathogen database
"""

import unittest
import json
import tempfile
import os
from src.pathogen_database_advanced import (
    PathogenParameters, PathogenDatabase,
    BIOACCUMULATION_FACTORS, MORBIDITY_RATIOS
)


class TestPathogenDatabase(unittest.TestCase):
    """Test pathogen database functionality"""

    def setUp(self):
        self.db = PathogenDatabase()

    def test_database_initialization(self):
        """Test that database initializes with pathogens"""
        pathogens = self.db.get_all_pathogens()
        self.assertIsInstance(pathogens, list)
        self.assertTrue(len(pathogens) > 10)  # Should have many pathogens

        # Check key pathogens are present
        expected_pathogens = ['campylobacter', 'cryptosporidium', 'norovirus', 'ecoli']
        for pathogen in expected_pathogens:
            self.assertIn(pathogen, pathogens)

    def test_get_pathogen(self):
        """Test getting pathogen parameters"""
        # Test exact match
        params_list = self.db.get_pathogen('campylobacter')
        self.assertIsInstance(params_list, list)
        self.assertTrue(len(params_list) > 0)

        # Test partial match
        params_list = self.db.get_pathogen('crypto')
        self.assertIsInstance(params_list, list)
        self.assertTrue(len(params_list) > 0)

        # Test case insensitive
        params_list = self.db.get_pathogen('NOROVIRUS')
        self.assertIsInstance(params_list, list)
        self.assertTrue(len(params_list) > 0)

    def test_get_nonexistent_pathogen(self):
        """Test error handling for nonexistent pathogen"""
        with self.assertRaises(ValueError):
            self.db.get_pathogen('nonexistent_pathogen')

    def test_pathogen_parameters_structure(self):
        """Test structure of pathogen parameters"""
        params_list = self.db.get_pathogen('cryptosporidium')

        for params in params_list:
            self.assertIsInstance(params, PathogenParameters)
            self.assertIsInstance(params.name, str)
            self.assertIsInstance(params.model, str)
            self.assertIsInstance(params.parameters, dict)
            self.assertTrue(len(params.parameters) > 0)

    def test_get_pathogen_by_model(self):
        """Test getting pathogen by specific model"""
        # Get exponential model for Cryptosporidium
        params = self.db.get_pathogen_by_model('cryptosporidium', 'exponential')

        self.assertIsInstance(params, PathogenParameters)
        self.assertEqual(params.model, 'exponential')
        self.assertIn('r', params.parameters)

        # Test non-existent model
        params = self.db.get_pathogen_by_model('cryptosporidium', 'nonexistent_model')
        self.assertIsNone(params)

    def test_get_best_fit_model(self):
        """Test getting best-fit model for pathogen"""
        # Norovirus should prefer fractional_poisson
        params = self.db.get_best_fit_model('norovirus')
        self.assertEqual(params.model, 'fractional_poisson')

        # Cryptosporidium has multiple models
        params = self.db.get_best_fit_model('cryptosporidium')
        self.assertIn(params.model, ['fractional_poisson', 'beta_poisson', 'exponential'])

    def test_model_parameters_validity(self):
        """Test that model parameters are valid"""
        # Test exponential model parameters
        expo_pathogens = ['cryptosporidium', 'giardia', 'rotavirus']
        for pathogen in expo_pathogens:
            params_list = self.db.get_pathogen(pathogen)
            expo_params = [p for p in params_list if p.model == 'exponential']
            if expo_params:
                for params in expo_params:
                    self.assertIn('r', params.parameters)
                    r = params.parameters['r']
                    self.assertTrue(0 < r < 1)

        # Test beta-poisson model parameters
        bp_pathogens = ['campylobacter', 'ecoli']
        for pathogen in bp_pathogens:
            params_list = self.db.get_pathogen(pathogen)
            bp_params = [p for p in params_list if p.model == 'beta_poisson']
            if bp_params:
                for params in bp_params:
                    self.assertIn('alpha', params.parameters)
                    self.assertIn('beta', params.parameters)
                    self.assertTrue(params.parameters['alpha'] > 0)
                    self.assertTrue(params.parameters['beta'] > 0)

    def test_export_to_json(self):
        """Test JSON export functionality"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filepath = f.name

        try:
            self.db.export_to_json(filepath)

            # Check file exists
            self.assertTrue(os.path.exists(filepath))

            # Load and verify JSON
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.assertIsInstance(data, dict)
            self.assertIn('campylobacter', data)
            self.assertIn('norovirus', data)

            # Check structure
            for pathogen, params_list in data.items():
                self.assertIsInstance(params_list, list)
                for params in params_list:
                    self.assertIn('name', params)
                    self.assertIn('model', params)
                    self.assertIn('parameters', params)

        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

    def test_database_summary(self):
        """Test database summary generation"""
        summary = self.db.summary()

        self.assertIsInstance(summary, str)
        self.assertIn('Pathogen Database Summary', summary)
        self.assertIn('Total pathogens:', summary)
        self.assertIn('Total model parameterizations:', summary)

        # Check specific pathogens are mentioned
        self.assertIn('Campylobacter', summary)
        self.assertIn('Norovirus', summary)


class TestBioaccumulationFactors(unittest.TestCase):
    """Test bioaccumulation factors"""

    def test_bioaccumulation_factors_structure(self):
        """Test structure of bioaccumulation factors"""
        self.assertIsInstance(BIOACCUMULATION_FACTORS, dict)

        # Check key pathogens
        self.assertIn('norovirus', BIOACCUMULATION_FACTORS)
        self.assertIn('hepatitis', BIOACCUMULATION_FACTORS)
        self.assertIn('default', BIOACCUMULATION_FACTORS)

        # Check shellfish types
        for pathogen, factors in BIOACCUMULATION_FACTORS.items():
            self.assertIn('oysters', factors)
            self.assertIn('mussels', factors)
            self.assertIn('clams', factors)
            self.assertIn('default', factors)

    def test_bioaccumulation_values(self):
        """Test bioaccumulation factor values"""
        # All values should be positive
        for pathogen, factors in BIOACCUMULATION_FACTORS.items():
            for shellfish, factor in factors.items():
                self.assertTrue(factor > 0)
                self.assertTrue(factor <= 1000)  # Reasonable upper bound


class TestMorbidityRatios(unittest.TestCase):
    """Test morbidity ratios"""

    def test_morbidity_ratios_structure(self):
        """Test structure of morbidity ratios"""
        self.assertIsInstance(MORBIDITY_RATIOS, dict)

        # Check key pathogens
        expected_pathogens = ['campylobacter', 'cryptosporidium', 'norovirus', 'ecoli']
        for pathogen in expected_pathogens:
            self.assertIn(pathogen, MORBIDITY_RATIOS)

    def test_morbidity_values(self):
        """Test morbidity ratio values"""
        for pathogen, ratio in MORBIDITY_RATIOS.items():
            self.assertIsInstance(ratio, (int, float))
            self.assertTrue(0 < ratio <= 1)  # Between 0 and 1

    def test_specific_morbidity_ratios(self):
        """Test specific known morbidity ratios"""
        # Campylobacter typically 0.33
        self.assertAlmostEqual(MORBIDITY_RATIOS['campylobacter'], 0.33, places=2)

        # Norovirus typically 0.7
        self.assertAlmostEqual(MORBIDITY_RATIOS['norovirus'], 0.7, places=1)

        # Legionella typically 1.0 (all infections lead to illness)
        self.assertEqual(MORBIDITY_RATIOS['legionella'], 1.0)


class TestPathogenIntegration(unittest.TestCase):
    """Integration tests for pathogen database"""

    def setUp(self):
        self.db = PathogenDatabase()

    def test_complete_pathogen_workflow(self):
        """Test complete workflow for a pathogen"""
        pathogen = 'norovirus'

        # Get all parameters
        all_params = self.db.get_pathogen(pathogen)
        self.assertTrue(len(all_params) > 0)

        # Get best fit
        best_fit = self.db.get_best_fit_model(pathogen)
        self.assertIsInstance(best_fit, PathogenParameters)

        # Check morbidity ratio exists
        self.assertIn(pathogen, MORBIDITY_RATIOS)

        # Check bioaccumulation exists
        self.assertIn(pathogen, BIOACCUMULATION_FACTORS)

    def test_all_pathogens_have_parameters(self):
        """Test that all pathogens have valid parameters"""
        pathogens = self.db.get_all_pathogens()

        for pathogen in pathogens:
            params_list = self.db.get_pathogen(pathogen)
            self.assertTrue(len(params_list) > 0, f"No parameters for {pathogen}")

            # Each should have at least one valid model
            for params in params_list:
                self.assertTrue(len(params.parameters) > 0)


if __name__ == '__main__':
    unittest.main()