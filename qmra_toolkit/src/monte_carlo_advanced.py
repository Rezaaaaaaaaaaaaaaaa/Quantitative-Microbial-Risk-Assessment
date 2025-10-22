"""
Advanced Monte Carlo Simulation Framework for QMRA
Ported from Charlotte Jones-Todd's R QMRA package
Implements concentration and exposure simulation methods
"""

import numpy as np
from scipy import stats
from typing import Dict, Union, Optional, Tuple, List
import pandas as pd
from dataclasses import dataclass


@dataclass
class SimulationResults:
    """Container for Monte Carlo simulation results"""
    concentrations: np.ndarray
    exposures: np.ndarray
    doses: np.ndarray
    inputs: Dict
    simulated_values: Dict[str, np.ndarray]

    def summary(self) -> pd.DataFrame:
        """Generate summary statistics"""
        return pd.DataFrame({
            'Metric': ['Mean', 'Median', 'Std', 'Min', 'Max', 'P5', 'P25', 'P75', 'P95'],
            'Concentration': [
                np.mean(self.concentrations),
                np.median(self.concentrations),
                np.std(self.concentrations),
                np.min(self.concentrations),
                np.max(self.concentrations),
                np.percentile(self.concentrations, 5),
                np.percentile(self.concentrations, 25),
                np.percentile(self.concentrations, 75),
                np.percentile(self.concentrations, 95)
            ],
            'Exposure': [
                np.mean(self.exposures),
                np.median(self.exposures),
                np.std(self.exposures),
                np.min(self.exposures),
                np.max(self.exposures),
                np.percentile(self.exposures, 5),
                np.percentile(self.exposures, 25),
                np.percentile(self.exposures, 75),
                np.percentile(self.exposures, 95)
            ],
            'Dose': [
                np.mean(self.doses),
                np.median(self.doses),
                np.std(self.doses),
                np.min(self.doses),
                np.max(self.doses),
                np.percentile(self.doses, 5),
                np.percentile(self.doses, 25),
                np.percentile(self.doses, 75),
                np.percentile(self.doses, 95)
            ]
        })


class DistributionSampler:
    """Sample from various probability distributions"""

    @staticmethod
    def sample_triangular(n: int, min_val: float, mode: float, max_val: float) -> np.ndarray:
        """Sample from triangular distribution"""
        return stats.triang.rvs(
            c=(mode - min_val) / (max_val - min_val),
            loc=min_val,
            scale=max_val - min_val,
            size=n
        )

    @staticmethod
    def sample_uniform(n: int, min_val: float, max_val: float) -> np.ndarray:
        """Sample from uniform distribution"""
        return stats.uniform.rvs(loc=min_val, scale=max_val - min_val, size=n)

    @staticmethod
    def sample_lognormal(n: int, mean_log: float, sd_log: float) -> np.ndarray:
        """Sample from lognormal distribution"""
        return stats.lognorm.rvs(s=sd_log, scale=np.exp(mean_log), size=n)

    @staticmethod
    def sample_normal(n: int, mean: float, sd: float) -> np.ndarray:
        """Sample from normal distribution"""
        return stats.norm.rvs(loc=mean, scale=sd, size=n)

    @staticmethod
    def sample_gamma(n: int, shape: float, rate: float) -> np.ndarray:
        """Sample from gamma distribution"""
        return stats.gamma.rvs(a=shape, scale=1/rate, size=n)

    @staticmethod
    def sample_beta(n: int, alpha: float, beta: float) -> np.ndarray:
        """Sample from beta distribution"""
        return stats.beta.rvs(a=alpha, b=beta, size=n)

    @staticmethod
    def sample_hockey_stick(n: int, x_min: float, x_median: float, x_max: float,
                           percentile: float = 95.0) -> np.ndarray:
        """
        Sample from hockey stick distribution for pathogen concentrations.

        Based on McBride's formulation for right-skewed environmental microbiological data.
        The distribution joins the median and maximum with a "hockey stick" shape.

        Args:
            n: Number of samples
            x_min: Minimum value (X₀)
            x_median: Median value (X₅₀)
            x_max: Maximum value (X₁₀₀)
            percentile: Percentile for the "toe" of the hockey stick (default 95)

        Returns:
            Array of samples from the hockey stick distribution

        Reference:
            McBride (2009), "Microbial Water Quality and Human Health"
            Section 9.3.2 - Hockey stick distribution
        """
        if x_min >= x_median or x_median >= x_max:
            raise ValueError("Must have x_min < x_median < x_max")

        if not 0 < percentile < 100:
            raise ValueError("Percentile must be between 0 and 100")

        # Calculate h1 and h2 from equations (9.9) and (9.11)
        h1 = 1.0 / (x_median - x_min)
        h2 = 2.0 * (1 - percentile/100.0) / (x_max - x_median)

        # Calculate X_P (the Pth percentile position) using equation (9.10)
        # This is a simplified version - full equation is quadratic
        sq = percentile / 100.0
        x_p = 0.5 * (x_median + x_max + 1.0/h1 -
                    np.sqrt((x_max - x_median)**2 +
                           (x_median * (2 - 8*sq) + x_max * (2 - 8*sq))/(h1) +
                           1.0/(h1**2)))

        samples = np.zeros(n)
        for i in range(n):
            u = np.random.uniform(0, 1)

            if u <= 0.5:
                # Left triangle (A-B region): uniform probability
                # Linear interpolation from x_min to x_median
                samples[i] = x_min + (x_median - x_min) * (u / 0.5)
            elif u <= percentile/100.0:
                # Middle region (B-C): proportional area
                # Linear interpolation from x_median to x_p
                u_scaled = (u - 0.5) / (percentile/100.0 - 0.5)
                samples[i] = x_median + (x_p - x_median) * u_scaled
            else:
                # Right tail (C-D): remaining probability
                # Linear interpolation from x_p to x_max
                u_scaled = (u - percentile/100.0) / (1 - percentile/100.0)
                samples[i] = x_p + (x_max - x_p) * u_scaled

        return samples

    @staticmethod
    def sample_cumulative(n: int, x: np.ndarray, p: np.ndarray,
                         min_val: Optional[float] = None,
                         max_val: Optional[float] = None) -> np.ndarray:
        """
        Sample from empirical cumulative distribution

        Args:
            n: Number of samples
            x: Values
            p: Cumulative probabilities
            min_val: Minimum value
            max_val: Maximum value

        Returns:
            Samples from the distribution
        """
        # Ensure probabilities are sorted and normalized
        sorted_idx = np.argsort(x)
        x_sorted = x[sorted_idx]
        p_sorted = p[sorted_idx]

        # Interpolate to get values
        uniform_samples = np.random.uniform(0, 1, n)
        samples = np.interp(uniform_samples, p_sorted, x_sorted)

        # Apply bounds if specified
        if min_val is not None:
            samples = np.maximum(samples, min_val)
        if max_val is not None:
            samples = np.minimum(samples, max_val)

        return samples

    def get_sim_value(self, distribution: str, params: Dict[str, float], n: int = 1) -> np.ndarray:
        """
        General function to sample from any distribution

        Args:
            distribution: Name of distribution
            params: Distribution parameters
            n: Number of samples

        Returns:
            Samples from the distribution
        """
        dist_map = {
            'triangular': lambda: self.sample_triangular(n, params['min'], params['mode'], params['max']),
            'uniform': lambda: self.sample_uniform(n, params['min'], params['max']),
            'lognormal': lambda: self.sample_lognormal(n, params['meanlog'], params['sdlog']),
            'normal': lambda: self.sample_normal(n, params['mean'], params['sd']),
            'gamma': lambda: self.sample_gamma(n, params['shape'], params['rate']),
            'beta': lambda: self.sample_beta(n, params['alpha'], params['beta']),
            'hockey_stick': lambda: self.sample_hockey_stick(n, params['x_min'], params['x_median'],
                                                            params['x_max'], params.get('percentile', 95)),
            'fixed': lambda: np.full(n, params['value'])
        }

        if distribution not in dist_map:
            raise ValueError(f"Unknown distribution: {distribution}")

        return dist_map[distribution]()


class ConcentrationQMRA:
    """
    Calculate microbe concentration at exposure site
    Implements the conc_qmra function from R package
    """

    def __init__(self):
        self.sampler = DistributionSampler()

    def simulate(self,
                efficacy: Union[Dict[str, float], float],
                microbe_influent: Dict[str, Union[str, Dict]],
                dilution_exposure: Dict[str, np.ndarray]) -> Dict[str, float]:
        """
        Simulate microbe concentration at exposure site

        Args:
            efficacy: Either a dict with 'min' and 'max' for uniform sampling,
                     or a fixed value
            microbe_influent: Dict with 'distribution' and 'params'
            dilution_exposure: Dict with 'x', 'p', 'min', 'max' for cumulative distribution

        Returns:
            Dict with microbe_exposure and simulation details
        """
        # Simulate microbe at influent
        influent = self.sampler.get_sim_value(
            microbe_influent['distribution'],
            microbe_influent['params'],
            n=1
        )[0]

        # Get efficacy value
        if isinstance(efficacy, dict):
            eff_val = np.random.uniform(efficacy['min'], efficacy['max'])
        else:
            eff_val = efficacy

        # Calculate microbe after treatment (log reduction)
        microbe_effluent = 10 ** (np.log10(influent) - eff_val)

        # Simulate dilution
        dilution = self.sampler.sample_cumulative(
            n=1,
            x=dilution_exposure['x'],
            p=dilution_exposure['p'],
            min_val=dilution_exposure.get('min'),
            max_val=dilution_exposure.get('max')
        )[0]

        # Calculate microbe at exposure site
        microbe_exposure = microbe_effluent * dilution

        return {
            'microbe_exposure': microbe_exposure,
            'sim': {
                'influent_val': influent,
                'efficacy_val': eff_val,
                'dilution': dilution
            }
        }


class IngestedQMRA:
    """
    Calculate volume ingested for QMRA models
    Implements the ingested_qmra function from R package
    """

    def __init__(self):
        self.sampler = DistributionSampler()

    def simulate(self,
                duration: Dict[str, Union[str, Dict]],
                vol_rate: Dict[str, Union[str, Dict]]) -> Dict[str, float]:
        """
        Simulate ingested volume

        Args:
            duration: Dict with 'distribution' and parameters
            vol_rate: Dict with 'distribution' and parameters

        Returns:
            Dict with vol_ingested and simulation details
        """
        # Simulate volume rate
        vol = self.sampler.get_sim_value(
            vol_rate['distribution'],
            vol_rate['params'],
            n=1
        )[0]

        # Simulate duration
        dur = self.sampler.get_sim_value(
            duration['distribution'],
            duration['params'],
            n=1
        )[0]

        # Calculate volume ingested
        vol_ingested = dur * vol

        return {
            'vol_ingested': vol_ingested,
            'sim': {
                'volume': vol,
                'duration': dur
            }
        }


class MonteCarloQMRA:
    """
    Main Monte Carlo QMRA simulation class
    Implements the mc_qmra function from R package
    """

    def __init__(self):
        self.conc_qmra = ConcentrationQMRA()
        self.ingested_qmra = IngestedQMRA()

    def simulate(self,
                nsim: Union[int, Dict[str, int]],
                efficacy: Union[Dict[str, float], float],
                microbe_influent: Dict[str, Union[str, Dict]],
                dilution_exposure: Dict[str, np.ndarray],
                duration: Dict[str, Union[str, Dict]],
                vol_rate: Dict[str, Union[str, Dict]]) -> SimulationResults:
        """
        Run Monte Carlo QMRA simulation

        Args:
            nsim: Number of simulations (int) or dict with 'nsim_conc' and 'nsim_exposure'
            efficacy: Treatment efficacy parameters
            microbe_influent: Microbe influent distribution parameters
            dilution_exposure: Dilution distribution parameters
            duration: Exposure duration parameters
            vol_rate: Volume rate parameters

        Returns:
            SimulationResults object
        """
        # Parse nsim parameter
        if isinstance(nsim, dict):
            nsim_conc = nsim['nsim_conc']
            nsim_exposure = nsim['nsim_exposure']
        else:
            nsim_conc = nsim_exposure = nsim

        # Initialize arrays for results
        conc = np.zeros(nsim_conc)
        sim_influent = np.zeros(nsim_conc)
        sim_efficacy = np.zeros(nsim_conc)
        sim_dilution = np.zeros(nsim_conc)

        expos = np.zeros(nsim_exposure)
        sim_vol = np.zeros(nsim_exposure)
        sim_dur = np.zeros(nsim_exposure)

        # Run concentration simulations
        for i in range(nsim_conc):
            tmp = self.conc_qmra.simulate(efficacy, microbe_influent, dilution_exposure)
            conc[i] = tmp['microbe_exposure']
            sim_influent[i] = tmp['sim']['influent_val']
            sim_efficacy[i] = tmp['sim']['efficacy_val']
            sim_dilution[i] = tmp['sim']['dilution']

        # Run exposure simulations
        for j in range(nsim_exposure):
            tmp2 = self.ingested_qmra.simulate(duration, vol_rate)
            expos[j] = tmp2['vol_ingested']
            sim_vol[j] = tmp2['sim']['volume']
            sim_dur[j] = tmp2['sim']['duration']

        # Calculate dose matrix (outer product)
        dose = np.outer(conc, expos)

        # Create results object
        results = SimulationResults(
            concentrations=conc,
            exposures=expos,
            doses=dose,
            inputs={
                'nsim': nsim,
                'efficacy': efficacy,
                'microbe_influent': microbe_influent,
                'dilution_exposure': dilution_exposure,
                'duration': duration,
                'vol_rate': vol_rate
            },
            simulated_values={
                'sim_influent': sim_influent,
                'sim_efficacy': sim_efficacy,
                'sim_dilution': sim_dilution,
                'sim_vol': sim_vol,
                'sim_dur': sim_dur
            }
        )

        return results


class HydrodynamicDilution:
    """
    Process hydrodynamic dilution data
    Based on the R package's dilution data processing
    """

    @staticmethod
    def process_dilution_data(concentration_data: pd.DataFrame,
                            baseline_load: float = 1000) -> pd.DataFrame:
        """
        Convert concentration data to dilution factors

        Args:
            concentration_data: DataFrame with concentration values
            baseline_load: Baseline load used in simulation (MPN/m3)

        Returns:
            DataFrame with dilution factors
        """
        dilution_data = baseline_load / concentration_data
        return dilution_data

    @staticmethod
    def get_empirical_cdf(data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate empirical CDF from data

        Args:
            data: Array of values

        Returns:
            Tuple of (sorted values, cumulative probabilities)
        """
        sorted_data = np.sort(data)
        n = len(sorted_data)
        probs = np.arange(1, n + 1) / n
        return sorted_data, probs

    @staticmethod
    def prepare_dilution_distribution(dilution_data: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Prepare dilution data for use in Monte Carlo simulation

        Args:
            dilution_data: Array of dilution values

        Returns:
            Dict with x, p, min, max for cumulative distribution sampling
        """
        x, p = HydrodynamicDilution.get_empirical_cdf(dilution_data)
        return {
            'x': x,
            'p': p,
            'min': np.min(dilution_data),
            'max': np.max(dilution_data)
        }


def run_qmra_monte_carlo(config: Dict) -> SimulationResults:
    """
    High-level function to run QMRA Monte Carlo simulation

    Args:
        config: Configuration dictionary with all parameters

    Returns:
        SimulationResults object

    Example config:
        {
            'nsim': 10000,
            'efficacy': {'min': 2, 'max': 4},  # log reduction
            'microbe_influent': {
                'distribution': 'lognormal',
                'params': {'meanlog': 5, 'sdlog': 1}
            },
            'dilution_exposure': {
                'x': array([...]),
                'p': array([...]),
                'min': 0.001,
                'max': 1000
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
    """
    mc_qmra = MonteCarloQMRA()
    return mc_qmra.simulate(**config)