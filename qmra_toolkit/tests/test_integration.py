#!/usr/bin/env python3
"""
Integration tests for QMRA toolkit - testing complete workflows.
"""

import unittest
import numpy as np
from pathlib import Path
import sys
import tempfile

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from pathogen_database import PathogenDatabase
from dose_response import create_dose_response_model
from exposure_assessment import create_exposure_assessment, ExposureRoute
from dilution_model import DilutionModel, TreatmentBarrier, TreatmentType, DilutionScenario
from monte_carlo import MonteCarloSimulator, create_lognormal_distribution
from risk_characterization import RiskCharacterization
from report_generator import ReportGenerator


class TestQMRAWorkflow(unittest.TestCase):
    """Integration tests for complete QMRA workflows."""

    def setUp(self):
        """Set up test components."""
        try:
            self.pathogen_db = PathogenDatabase()
            self.risk_calc = RiskCharacterization(self.pathogen_db)
            self.available_pathogens = self.pathogen_db.get_available_pathogens()
        except FileNotFoundError:
            self.skipTest("Pathogen database file not found")

    def test_primary_contact_workflow(self):
        """Test complete primary contact exposure workflow."""
        if 'norovirus' not in self.available_pathogens:
            self.skipTest("Norovirus data not available")

        # Set up exposure assessment
        params = {
            "water_ingestion_volume": 50.0,  # mL per event
            "exposure_frequency": 10  # events per year
        }

        exposure_model = create_exposure_assessment(
            ExposureRoute.PRIMARY_CONTACT,
            params
        )
        exposure_model.set_pathogen_concentration(10.0)  # organisms per 100mL

        # Calculate exposure doses
        doses = exposure_model.calculate_dose(100)
        annual_doses = exposure_model.calculate_annual_dose(100)

        self.assertEqual(len(doses), 100)
        self.assertEqual(len(annual_doses), 100)
        self.assertTrue(np.all(annual_doses >= doses))

        # Calculate infection risks
        infection_result = self.risk_calc.calculate_infection_probability('norovirus', doses)

        self.assertEqual(len(infection_result.individual_risks), 100)
        self.assertTrue(np.all(infection_result.individual_risks >= 0))
        self.assertTrue(np.all(infection_result.individual_risks <= 1))

        # Calculate annual risk
        annual_result = self.risk_calc.calculate_annual_risk('norovirus', doses, 10)

        self.assertTrue(np.all(annual_result.individual_risks >= infection_result.individual_risks))

    def test_shellfish_consumption_workflow(self):
        """Test shellfish consumption workflow."""
        if 'norovirus' not in self.available_pathogens:
            self.skipTest("Norovirus data not available")

        # Set up exposure assessment
        params = {
            "shellfish_consumption": 150.0,  # grams per serving
            "consumption_frequency": 12  # servings per year
        }

        exposure_model = create_exposure_assessment(
            ExposureRoute.SHELLFISH_CONSUMPTION,
            params,
            bioaccumulation_factor=2.0
        )
        exposure_model.set_pathogen_concentration(100.0)  # organisms per 100g

        # Run assessment
        doses = exposure_model.calculate_dose(50)
        illness_result = self.risk_calc.calculate_illness_probability('norovirus', doses)

        self.assertEqual(len(illness_result.individual_risks), 50)
        self.assertIn('mean', illness_result.statistics)

    def test_treatment_dilution_workflow(self):
        """Test treatment and dilution modeling workflow."""
        # Create dilution model with treatment train
        dilution_model = DilutionModel()

        # Add treatment barriers
        dilution_model.add_treatment_barrier(TreatmentBarrier(
            name="Primary Treatment",
            treatment_type=TreatmentType.PHYSICAL,
            log_reduction_value=0.5
        ))

        dilution_model.add_treatment_barrier(TreatmentBarrier(
            name="UV Disinfection",
            treatment_type=TreatmentType.UV,
            log_reduction_value=3.0
        ))

        # Set dilution scenario
        scenario = DilutionScenario(
            initial_flow=1.0,  # m³/s
            receiving_flow=20.0  # m³/s
        )
        dilution_model.set_dilution_scenario(scenario)

        # Test treatment and dilution
        initial_conc = 1e6  # organisms/L
        results = dilution_model.apply_complete_scenario(initial_conc)

        self.assertIn('initial', results)
        self.assertIn('after_treatment', results)
        self.assertIn('after_dilution', results)
        self.assertIn('final', results)

        # Verify concentration reduction
        self.assertLess(results['final'], results['initial'])
        self.assertLess(results['after_treatment'], results['initial'])
        self.assertLess(results['after_dilution'], results['after_treatment'])

    def test_monte_carlo_uncertainty_analysis(self):
        """Test Monte Carlo uncertainty analysis."""
        if 'norovirus' not in self.available_pathogens:
            self.skipTest("Norovirus data not available")

        # Set up Monte Carlo simulation
        mc_sim = MonteCarloSimulator(random_seed=42)

        # Add uncertain parameters
        pathogen_conc = create_lognormal_distribution(mean=2.0, std=1.0)
        mc_sim.add_distribution("pathogen_concentration", pathogen_conc)

        # Define QMRA model function
        def qmra_model(samples):
            concentration = samples["pathogen_concentration"]
            dose = concentration * 0.05  # 50 mL ingestion in L
            # Use norovirus parameters
            dr_params = self.pathogen_db.get_dose_response_parameters('norovirus')
            dr_model = create_dose_response_model('beta_poisson', dr_params)
            return dr_model.calculate_infection_probability(dose)

        # Run simulation
        results = mc_sim.run_simulation(qmra_model, n_iterations=1000)

        self.assertEqual(results.iterations, 1000)
        self.assertEqual(len(results.samples), 1000)
        self.assertIn('mean', results.statistics)
        self.assertIn('95%', results.percentiles)

    def test_comprehensive_assessment(self):
        """Test comprehensive risk assessment with all components."""
        if 'norovirus' not in self.available_pathogens:
            self.skipTest("Norovirus data not available")

        # Set up exposure model
        exposure_params = {
            "water_ingestion_volume": 50.0,
            "exposure_frequency": 10
        }
        exposure_model = create_exposure_assessment(
            ExposureRoute.PRIMARY_CONTACT,
            exposure_params
        )
        exposure_model.set_pathogen_concentration(10.0)

        # Run comprehensive assessment
        results = self.risk_calc.run_comprehensive_assessment(
            pathogen_name='norovirus',
            exposure_assessment=exposure_model,
            population_size=10000,
            n_samples=500  # Smaller for faster testing
        )

        # Check all expected metrics are calculated
        expected_metrics = ['infection_probability', 'illness_probability', 'annual_risk', 'dalys']
        for metric in expected_metrics:
            self.assertIn(metric, results)
            self.assertIn('mean', results[metric].statistics)
            self.assertIsNotNone(results[metric].population_risks)

        # Check regulatory compliance
        compliance = self.risk_calc.evaluate_regulatory_compliance(results['annual_risk'])
        self.assertIsInstance(compliance, dict)

    def test_report_generation_workflow(self):
        """Test report generation workflow."""
        if 'norovirus' not in self.available_pathogens:
            self.skipTest("Norovirus data not available")

        # Generate sample results
        test_doses = np.random.lognormal(1, 0.5, 100)
        risk_results = {
            'infection_probability': self.risk_calc.calculate_infection_probability('norovirus', test_doses),
            'annual_risk': self.risk_calc.calculate_annual_risk('norovirus', test_doses, 5)
        }

        # Test report generation
        report_gen = ReportGenerator()

        project_info = {
            'title': 'Test QMRA Report',
            'project_name': 'Integration Test',
            'author': 'Test Suite'
        }

        exposure_params = {
            'water_ingestion': '50 mL',
            'frequency': '5 events/year'
        }

        # Generate report to temporary file
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_file:
            report_path = report_gen.create_regulatory_report(
                project_info=project_info,
                risk_results=risk_results,
                exposure_params=exposure_params,
                output_filename=tmp_file.name
            )

            # Check file was created
            self.assertTrue(Path(report_path).exists())
            self.assertGreater(Path(report_path).stat().st_size, 1000)  # Should be non-empty

            # Clean up
            Path(report_path).unlink()


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases."""

    def setUp(self):
        """Set up test components."""
        try:
            self.pathogen_db = PathogenDatabase()
            self.risk_calc = RiskCharacterization(self.pathogen_db)
        except FileNotFoundError:
            self.skipTest("Pathogen database file not found")

    def test_invalid_pathogen(self):
        """Test handling of invalid pathogen names."""
        with self.assertRaises(ValueError):
            self.risk_calc.calculate_infection_probability('invalid_pathogen', [1, 10, 100])

    def test_zero_doses(self):
        """Test handling of zero doses."""
        if 'norovirus' not in self.pathogen_db.get_available_pathogens():
            self.skipTest("Norovirus data not available")

        zero_doses = np.zeros(10)
        result = self.risk_calc.calculate_infection_probability('norovirus', zero_doses)

        # All probabilities should be zero
        self.assertTrue(np.all(result.individual_risks == 0))

    def test_extreme_doses(self):
        """Test handling of extremely high doses."""
        if 'norovirus' not in self.pathogen_db.get_available_pathogens():
            self.skipTest("Norovirus data not available")

        extreme_doses = np.array([1e10, 1e20, 1e50])
        result = self.risk_calc.calculate_infection_probability('norovirus', extreme_doses)

        # Probabilities should be capped at 1.0
        self.assertTrue(np.all(result.individual_risks <= 1.0))
        self.assertTrue(np.all(result.individual_risks >= 0.0))

    def test_empty_arrays(self):
        """Test handling of empty input arrays."""
        if 'norovirus' not in self.pathogen_db.get_available_pathogens():
            self.skipTest("Norovirus data not available")

        empty_doses = np.array([])
        result = self.risk_calc.calculate_infection_probability('norovirus', empty_doses)

        self.assertEqual(len(result.individual_risks), 0)


class TestBenchmarkValidation(unittest.TestCase):
    """Test validation against known benchmarks and literature values."""

    def setUp(self):
        """Set up test components."""
        try:
            self.pathogen_db = PathogenDatabase()
        except FileNotFoundError:
            self.skipTest("Pathogen database file not found")

    def test_who_benchmark_recreational_water(self):
        """Test against WHO recreational water benchmarks."""
        if 'norovirus' not in self.pathogen_db.get_available_pathogens():
            self.skipTest("Norovirus data not available")

        # WHO benchmark: 1% illness risk from 10^(-3) DALYs per person per year
        # This corresponds to specific pathogen concentrations

        risk_calc = RiskCharacterization(self.pathogen_db)

        # Test scenario approximating WHO conditions
        test_dose = 10.0  # organisms
        illness_result = risk_calc.calculate_illness_probability('norovirus', [test_dose])

        # Result should be in reasonable range for recreational water exposure
        illness_prob = illness_result.individual_risks[0]
        self.assertGreater(illness_prob, 1e-6)  # Should be > 1 in million
        self.assertLess(illness_prob, 0.1)      # Should be < 10%

    def test_epa_drinking_water_benchmark(self):
        """Test against EPA drinking water benchmarks."""
        if 'cryptosporidium' not in self.pathogen_db.get_available_pathogens():
            self.skipTest("Cryptosporidium data not available")

        # EPA benchmark for Cryptosporidium: 1 in 10,000 annual risk
        risk_calc = RiskCharacterization(self.pathogen_db)

        # Calculate dose that should give approximately 1e-4 annual risk
        # This is an approximate validation
        test_doses = np.logspace(-1, 2, 50)  # 0.1 to 100 organisms
        annual_results = risk_calc.calculate_annual_risk('cryptosporidium', test_doses, 365)

        # Check that we can achieve the target risk level
        min_risk = np.min(annual_results.individual_risks)
        max_risk = np.max(annual_results.individual_risks)

        self.assertLess(min_risk, 1e-4)   # Should be able to go below target
        self.assertGreater(max_risk, 1e-4)  # Should be able to go above target


if __name__ == '__main__':
    # Run tests with higher verbosity
    unittest.main(verbosity=2)