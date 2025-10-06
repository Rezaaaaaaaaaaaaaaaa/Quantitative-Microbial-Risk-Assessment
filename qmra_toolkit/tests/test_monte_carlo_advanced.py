"""
Test suite for advanced Monte Carlo framework
"""

import unittest
import numpy as np
import pandas as pd
from src.monte_carlo_advanced import (
    DistributionSampler, ConcentrationQMRA, IngestedQMRA,
    MonteCarloQMRA, HydrodynamicDilution, SimulationResults
)


class TestDistributionSampler(unittest.TestCase):
    """Test distribution sampling functionality"""

    def setUp(self):
        self.sampler = DistributionSampler()

    def test_triangular_sampling(self):
        """Test triangular distribution sampling"""
        n = 1000
        samples = self.sampler.sample_triangular(n, 10, 20, 30)

        self.assertEqual(len(samples), n)
        self.assertTrue(np.all(samples >= 10))
        self.assertTrue(np.all(samples <= 30))
        # Mode should be around 20
        self.assertTrue(15 < np.median(samples) < 25)

    def test_uniform_sampling(self):
        """Test uniform distribution sampling"""
        n = 1000
        samples = self.sampler.sample_uniform(n, 0, 100)

        self.assertEqual(len(samples), n)
        self.assertTrue(np.all(samples >= 0))
        self.assertTrue(np.all(samples <= 100))
        # Mean should be around 50
        self.assertTrue(45 < np.mean(samples) < 55)

    def test_lognormal_sampling(self):
        """Test lognormal distribution sampling"""
        n = 1000
        samples = self.sampler.sample_lognormal(n, 3, 1)

        self.assertEqual(len(samples), n)
        self.assertTrue(np.all(samples > 0))

    def test_cumulative_sampling(self):
        """Test empirical cumulative distribution sampling"""
        x = np.array([0, 1, 2, 3, 4])
        p = np.array([0, 0.25, 0.5, 0.75, 1.0])
        n = 1000

        samples = self.sampler.sample_cumulative(n, x, p, min_val=0, max_val=4)

        self.assertEqual(len(samples), n)
        self.assertTrue(np.all(samples >= 0))
        self.assertTrue(np.all(samples <= 4))

    def test_get_sim_value(self):
        """Test general simulation value getter"""
        # Triangular
        params = {'min': 10, 'mode': 20, 'max': 30}
        samples = self.sampler.get_sim_value('triangular', params, n=100)
        self.assertEqual(len(samples), 100)

        # Fixed value
        params = {'value': 42}
        samples = self.sampler.get_sim_value('fixed', params, n=5)
        self.assertTrue(np.all(samples == 42))


class TestConcentrationQMRA(unittest.TestCase):
    """Test concentration QMRA calculations"""

    def setUp(self):
        self.conc_qmra = ConcentrationQMRA()

    def test_simulate_with_uniform_efficacy(self):
        """Test simulation with uniform efficacy"""
        efficacy = {'min': 2, 'max': 4}  # log reduction
        microbe_influent = {
            'distribution': 'lognormal',
            'params': {'meanlog': 5, 'sdlog': 1}
        }
        dilution_exposure = {
            'x': np.array([0.001, 0.01, 0.1, 1.0]),
            'p': np.array([0.25, 0.5, 0.75, 1.0]),
            'min': 0.001,
            'max': 1.0
        }

        result = self.conc_qmra.simulate(efficacy, microbe_influent, dilution_exposure)

        self.assertIn('microbe_exposure', result)
        self.assertIn('sim', result)
        self.assertIsInstance(result['microbe_exposure'], float)
        self.assertTrue(result['microbe_exposure'] >= 0)

    def test_simulate_with_fixed_efficacy(self):
        """Test simulation with fixed efficacy"""
        efficacy = 3.0  # fixed log reduction
        microbe_influent = {
            'distribution': 'fixed',
            'params': {'value': 1e6}
        }
        dilution_exposure = {
            'x': np.array([0.1]),
            'p': np.array([1.0]),
            'min': 0.1,
            'max': 0.1
        }

        result = self.conc_qmra.simulate(efficacy, microbe_influent, dilution_exposure)

        # Check log reduction: 1e6 * 10^(-3) * 0.1 = 100
        expected = 1e6 * (10 ** -3) * 0.1
        self.assertAlmostEqual(result['microbe_exposure'], expected, places=2)


class TestIngestedQMRA(unittest.TestCase):
    """Test ingested volume calculations"""

    def setUp(self):
        self.ingested_qmra = IngestedQMRA()

    def test_simulate_ingestion(self):
        """Test ingestion simulation"""
        duration = {
            'distribution': 'triangular',
            'params': {'min': 15, 'mode': 30, 'max': 60}
        }
        vol_rate = {
            'distribution': 'uniform',
            'params': {'min': 0.001, 'max': 0.01}
        }

        result = self.ingested_qmra.simulate(duration, vol_rate)

        self.assertIn('vol_ingested', result)
        self.assertIn('sim', result)
        self.assertEqual(
            result['vol_ingested'],
            result['sim']['duration'] * result['sim']['volume']
        )


class TestMonteCarloQMRA(unittest.TestCase):
    """Test full Monte Carlo QMRA simulation"""

    def setUp(self):
        self.mc_qmra = MonteCarloQMRA()

    def test_simple_simulation(self):
        """Test simple Monte Carlo simulation"""
        config = {
            'nsim': 100,
            'efficacy': {'min': 2, 'max': 4},
            'microbe_influent': {
                'distribution': 'lognormal',
                'params': {'meanlog': 5, 'sdlog': 1}
            },
            'dilution_exposure': {
                'x': np.array([0.001, 0.01, 0.1, 1.0]),
                'p': np.array([0.25, 0.5, 0.75, 1.0]),
                'min': 0.001,
                'max': 1.0
            },
            'duration': {
                'distribution': 'triangular',
                'params': {'min': 15, 'mode': 30, 'max': 60}
            },
            'vol_rate': {
                'distribution': 'uniform',
                'params': {'min': 0.001, 'max': 0.01}
            }
        }

        results = self.mc_qmra.simulate(**config)

        self.assertIsInstance(results, SimulationResults)
        self.assertEqual(len(results.concentrations), 100)
        self.assertEqual(len(results.exposures), 100)
        self.assertEqual(results.doses.shape, (100, 100))

    def test_separate_nsim(self):
        """Test with separate nsim for concentration and exposure"""
        config = {
            'nsim': {'nsim_conc': 50, 'nsim_exposure': 20},
            'efficacy': 3.0,
            'microbe_influent': {
                'distribution': 'fixed',
                'params': {'value': 1e5}
            },
            'dilution_exposure': {
                'x': np.array([0.1]),
                'p': np.array([1.0])
            },
            'duration': {
                'distribution': 'fixed',
                'params': {'value': 30}
            },
            'vol_rate': {
                'distribution': 'fixed',
                'params': {'value': 0.005}
            }
        }

        results = self.mc_qmra.simulate(**config)

        self.assertEqual(len(results.concentrations), 50)
        self.assertEqual(len(results.exposures), 20)
        self.assertEqual(results.doses.shape, (50, 20))

    def test_results_summary(self):
        """Test results summary generation"""
        # Create mock results
        results = SimulationResults(
            concentrations=np.random.lognormal(5, 1, 100),
            exposures=np.random.uniform(0.1, 1, 100),
            doses=np.random.lognormal(4, 2, (100, 100)),
            inputs={},
            simulated_values={}
        )

        summary = results.summary()

        self.assertIsInstance(summary, pd.DataFrame)
        self.assertIn('Concentration', summary.columns)
        self.assertIn('Exposure', summary.columns)
        self.assertIn('Dose', summary.columns)
        self.assertEqual(len(summary), 9)  # 9 statistics


class TestHydrodynamicDilution(unittest.TestCase):
    """Test hydrodynamic dilution processing"""

    def setUp(self):
        self.hydro = HydrodynamicDilution()

    def test_process_dilution_data(self):
        """Test dilution data processing"""
        concentration_data = pd.DataFrame({
            'Site1': [100, 200, 300],
            'Site2': [50, 100, 150]
        })
        baseline_load = 1000

        dilution_data = self.hydro.process_dilution_data(concentration_data, baseline_load)

        self.assertEqual(dilution_data.shape, concentration_data.shape)
        # Check dilution calculation
        self.assertEqual(dilution_data.iloc[0, 0], 10)  # 1000/100
        self.assertEqual(dilution_data.iloc[0, 1], 20)  # 1000/50

    def test_empirical_cdf(self):
        """Test empirical CDF calculation"""
        data = np.array([1, 2, 3, 4, 5])
        x, p = self.hydro.get_empirical_cdf(data)

        self.assertEqual(len(x), len(data))
        self.assertEqual(len(p), len(data))
        self.assertTrue(np.all(p >= 0) and np.all(p <= 1))
        self.assertTrue(np.all(np.diff(p) >= 0))  # Monotonic

    def test_prepare_dilution_distribution(self):
        """Test dilution distribution preparation"""
        dilution_data = np.array([0.1, 0.5, 1.0, 2.0, 5.0])
        dist = self.hydro.prepare_dilution_distribution(dilution_data)

        self.assertIn('x', dist)
        self.assertIn('p', dist)
        self.assertIn('min', dist)
        self.assertIn('max', dist)
        self.assertEqual(dist['min'], 0.1)
        self.assertEqual(dist['max'], 5.0)


if __name__ == '__main__':
    unittest.main()