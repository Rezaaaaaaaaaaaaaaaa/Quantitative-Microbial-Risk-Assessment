"""
Monte Carlo Simulation Engine for QMRA Toolkit

This module provides Monte Carlo simulation capabilities for uncertainty analysis
in quantitative microbial risk assessment, replacing @Risk functionality.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Union, Callable, Any, Tuple
from scipy import stats
import warnings
from dataclasses import dataclass
from enum import Enum
import time


class DistributionType(Enum):
    """Supported probability distributions for Monte Carlo sampling."""
    NORMAL = "normal"
    LOGNORMAL = "lognormal"
    UNIFORM = "uniform"
    TRIANGULAR = "triangular"
    BETA = "beta"
    GAMMA = "gamma"
    EXPONENTIAL = "exponential"
    WEIBULL = "weibull"
    POISSON = "poisson"
    BINOMIAL = "binomial"
    EMPIRICAL_CDF = "empirical_cdf"  # For sampling dilution data
    HOCKEY_STICK = "hockey_stick"  # For pathogen concentration estimation


@dataclass
class DistributionParameters:
    """Container for distribution parameters."""
    distribution_type: DistributionType
    parameters: Dict[str, float]
    name: Optional[str] = None
    description: Optional[str] = None

    def validate(self) -> None:
        """Validate distribution parameters."""
        required_params = {
            DistributionType.NORMAL: ["mean", "std"],
            DistributionType.LOGNORMAL: ["mean", "std"],
            DistributionType.UNIFORM: ["min", "max"],
            DistributionType.TRIANGULAR: ["min", "mode", "max"],
            DistributionType.BETA: ["alpha", "beta"],
            DistributionType.GAMMA: ["shape", "scale"],
            DistributionType.EXPONENTIAL: ["scale"],
            DistributionType.WEIBULL: ["shape", "scale"],
            DistributionType.POISSON: ["mu"],
            DistributionType.BINOMIAL: ["n", "p"],
            DistributionType.EMPIRICAL_CDF: ["x_values", "probabilities"],  # x values and cumulative probs
            DistributionType.HOCKEY_STICK: ["x_min", "x_median", "x_max"]  # min, median, max (P is optional)
        }

        required = required_params.get(self.distribution_type, [])
        missing = [param for param in required if param not in self.parameters]

        if missing:
            raise ValueError(f"Missing required parameters for {self.distribution_type.value}: {missing}")


@dataclass
class MonteCarloResults:
    """Container for Monte Carlo simulation results."""
    variable_name: str
    samples: np.ndarray
    statistics: Dict[str, float]
    percentiles: Dict[str, float]
    execution_time: float
    iterations: int
    random_seed: Optional[int] = None

    def get_summary(self) -> str:
        """Get a formatted summary of the results."""
        summary = f"Monte Carlo Results for {self.variable_name}\n"
        summary += "=" * (len(summary) - 1) + "\n"
        summary += f"Iterations: {self.iterations:,}\n"
        summary += f"Execution time: {self.execution_time:.3f} seconds\n\n"

        summary += "Statistics:\n"
        for stat, value in self.statistics.items():
            summary += f"  {stat}: {value:.6g}\n"

        summary += "\nPercentiles:\n"
        for perc, value in sorted(self.percentiles.items()):
            summary += f"  {perc}: {value:.6g}\n"

        return summary


class MonteCarloSimulator:
    """
    Monte Carlo simulation engine for QMRA uncertainty analysis.

    This class replaces @Risk functionality with native Python implementation.
    """

    def __init__(self, random_seed: Optional[int] = None):
        """
        Initialize Monte Carlo simulator.

        Args:
            random_seed: Random seed for reproducible results
        """
        self.random_seed = random_seed
        if random_seed is not None:
            np.random.seed(random_seed)

        self.distributions: Dict[str, DistributionParameters] = {}
        self.samples_cache: Dict[str, np.ndarray] = {}

    def add_distribution(self, name: str, dist_params: DistributionParameters) -> None:
        """
        Add a probability distribution for sampling.

        Args:
            name: Name of the variable
            dist_params: Distribution parameters
        """
        dist_params.validate()
        self.distributions[name] = dist_params
        # Clear cached samples when distribution changes
        if name in self.samples_cache:
            del self.samples_cache[name]

    def sample_distribution(self, name: str, n_samples: int) -> np.ndarray:
        """
        Generate samples from a named distribution.

        Args:
            name: Name of the distribution
            n_samples: Number of samples to generate

        Returns:
            Array of samples

        Raises:
            ValueError: If distribution not found
        """
        if name not in self.distributions:
            available = list(self.distributions.keys())
            raise ValueError(f"Distribution '{name}' not found. Available: {available}")

        dist_params = self.distributions[name]
        return self._generate_samples(dist_params, n_samples)

    def _generate_samples(self, dist_params: DistributionParameters, n_samples: int) -> np.ndarray:
        """Generate samples from distribution parameters."""
        dist_type = dist_params.distribution_type
        params = dist_params.parameters

        if dist_type == DistributionType.NORMAL:
            return np.random.normal(params["mean"], params["std"], n_samples)

        elif dist_type == DistributionType.LOGNORMAL:
            return np.random.lognormal(params["mean"], params["std"], n_samples)

        elif dist_type == DistributionType.UNIFORM:
            return np.random.uniform(params["min"], params["max"], n_samples)

        elif dist_type == DistributionType.TRIANGULAR:
            return np.random.triangular(params["min"], params["mode"], params["max"], n_samples)

        elif dist_type == DistributionType.BETA:
            return np.random.beta(params["alpha"], params["beta"], n_samples)

        elif dist_type == DistributionType.GAMMA:
            return np.random.gamma(params["shape"], params["scale"], n_samples)

        elif dist_type == DistributionType.EXPONENTIAL:
            return np.random.exponential(params["scale"], n_samples)

        elif dist_type == DistributionType.WEIBULL:
            # Note: numpy uses different parameterization than some sources
            return params["scale"] * np.random.weibull(params["shape"], n_samples)

        elif dist_type == DistributionType.POISSON:
            return np.random.poisson(params["mu"], n_samples)

        elif dist_type == DistributionType.BINOMIAL:
            return np.random.binomial(params["n"], params["p"], n_samples)

        elif dist_type == DistributionType.EMPIRICAL_CDF:
            # Sample from empirical cumulative distribution function
            # This is used for dilution data
            x_values = np.array(params["x_values"])
            probabilities = np.array(params["probabilities"])

            # Ensure values are sorted by x
            sorted_idx = np.argsort(x_values)
            x_sorted = x_values[sorted_idx]
            p_sorted = probabilities[sorted_idx]

            # Generate uniform random samples and interpolate
            uniform_samples = np.random.uniform(0, 1, n_samples)
            samples = np.interp(uniform_samples, p_sorted, x_sorted)

            # Apply optional bounds
            if "min" in params:
                samples = np.maximum(samples, params["min"])
            if "max" in params:
                samples = np.minimum(samples, params["max"])

            return samples

        elif dist_type == DistributionType.HOCKEY_STICK:
            # Hockey stick distribution for pathogen concentrations
            # Based on McBride's formulation (Graham McBride, 2009)
            # Reference: David Wood's R implementation (From_David package)

            x_min = params["x_min"]  # X₀ - minimum concentration
            x_median = params["x_median"]  # X₅₀ - median concentration
            x_max = params["x_max"]  # X₁₀₀ - maximum concentration
            P = params.get("P", 0.95)  # P - breakpoint percentile (default 0.95 = 95th percentile)

            # Validate inputs
            if x_min >= x_median or x_median >= x_max:
                raise ValueError(f"Hockey stick requires x_min ({x_min}) < x_median ({x_median}) < x_max ({x_max})")

            # Fixed area proportions (McBride convention)
            A = 0.5  # Area between X₀ and X₅₀ (left section)
            B = P - 0.5  # Area between X₅₀ and X_P (middle section)
            C = 1 - P  # Area between X_P and X₁₀₀ (right section)

            # Calculate peak height parameters (equations from McBride 9.9, 9.11)
            h1 = (2 * A) / (x_median - x_min)  # Height at median (left side peak)

            # Calculate X_P (the percentile breakpoint) using quadratic formula
            # From equation (9.10): X_P = (X₅₀ + X₁₀₀ + 1/h1 - sqrt(...)) / 2
            discriminant = ((x_max - x_median)**2 +
                          (1.0 / (h1**2)) +
                          ((x_median / h1) * (2 - 8*C)) +
                          ((x_max / h1) * (2 - 8*B)))
            x_p = (x_median + x_max + 1.0/h1 - np.sqrt(discriminant)) / 2.0

            h2 = (2 * C) / (x_max - x_p)  # Height at X_P (right side peak)

            # Calculate slope coefficients for piecewise linear PDF
            m1 = h1 / (x_median - x_min)  # Slope: X₀ to X₅₀
            m2 = (h2 - h1) / (x_p - x_median)  # Slope: X₅₀ to X_P
            m3 = -h2 / (x_max - x_p)  # Slope: X_P to X₁₀₀

            c1 = 0  # Intercept for section 1
            c2 = h1  # Intercept for section 2
            c3 = h2  # Intercept for section 3

            # Generate samples using inverse CDF method
            samples = np.zeros(n_samples)
            for i in range(n_samples):
                u = np.random.uniform(0, 1)

                if u <= 0.5:
                    # Section 1 (X₀ to X₅₀): Area = 0.5
                    # CDF: (m1 * (x - X₀)²) / 2 = u
                    # x = X₀ + sqrt(2*u / m1)
                    x_sample = x_min + np.sqrt(2.0 * u / m1) if m1 > 0 else x_min
                    samples[i] = x_sample

                elif u <= P:
                    # Section 2 (X₅₀ to X_P): Area = P - 0.5
                    # CDF: 0.5 + ((2*h1 + m2*(x - X₅₀)) / 2) * (x - X₅₀) = u
                    # This is quadratic: m2/2 * (x - X₅₀)² + h1 * (x - X₅₀) + 0.5 - u = 0
                    u_scaled = u - 0.5
                    if m2 != 0:
                        # Quadratic formula: ax² + bx + c = 0
                        a = m2 / 2.0
                        b = h1
                        c = -u_scaled
                        discriminant_quad = b**2 - 4*a*c
                        if discriminant_quad >= 0:
                            x_delta = (-b + np.sqrt(discriminant_quad)) / (2*a)
                            samples[i] = x_median + x_delta
                        else:
                            samples[i] = x_median  # Fallback
                    else:
                        # Linear case (shouldn't happen with hockey stick)
                        samples[i] = x_median + u_scaled / h1 if h1 > 0 else x_median

                else:
                    # Section 3 (X_P to X₁₀₀): Area = 1 - P
                    # CDF: P + ((2*h2 + m3*(x - X_P)) / 2) * (x - X_P) = u
                    # This is quadratic: m3/2 * (x - X_P)² + h2 * (x - X_P) + P - u = 0
                    u_scaled = u - P
                    if m3 != 0:
                        a = m3 / 2.0
                        b = h2
                        c = -u_scaled
                        discriminant_quad = b**2 - 4*a*c
                        if discriminant_quad >= 0:
                            x_delta = (-b + np.sqrt(discriminant_quad)) / (2*a)
                            samples[i] = x_p + x_delta
                        else:
                            samples[i] = x_p  # Fallback
                    else:
                        samples[i] = x_p + u_scaled / h2 if h2 > 0 else x_p

                # Ensure sample is within bounds
                samples[i] = np.clip(samples[i], x_min, x_max)

            return samples

        else:
            raise ValueError(f"Unsupported distribution type: {dist_type}")

    def run_simulation(self,
                      model_function: Callable,
                      n_iterations: int = 10000,
                      variable_name: str = "simulation_result") -> MonteCarloResults:
        """
        Run Monte Carlo simulation using a model function.

        Args:
            model_function: Function that takes sampled inputs and returns results
            n_iterations: Number of Monte Carlo iterations
            variable_name: Name for the output variable

        Returns:
            MonteCarloResults object containing simulation results
        """
        start_time = time.time()

        # Generate all input samples
        input_samples = {}
        for name in self.distributions.keys():
            input_samples[name] = self.sample_distribution(name, n_iterations)

        # Run model function for all iterations
        try:
            results = model_function(input_samples)
            if not isinstance(results, np.ndarray):
                results = np.array(results)
        except Exception as e:
            raise RuntimeError(f"Error in model function: {e}")

        end_time = time.time()

        # Calculate statistics
        statistics = self._calculate_statistics(results)
        percentiles = self._calculate_percentiles(results)

        return MonteCarloResults(
            variable_name=variable_name,
            samples=results,
            statistics=statistics,
            percentiles=percentiles,
            execution_time=end_time - start_time,
            iterations=n_iterations,
            random_seed=self.random_seed
        )

    def run_qmra_simulation(self,
                           dose_response_function: Callable[[np.ndarray], np.ndarray],
                           exposure_samples: Dict[str, np.ndarray],
                           n_iterations: int = 10000) -> MonteCarloResults:
        """
        Run QMRA-specific Monte Carlo simulation.

        Args:
            dose_response_function: Function that calculates infection probability from dose
            exposure_samples: Dictionary of exposure variable samples
            n_iterations: Number of iterations

        Returns:
            MonteCarloResults for infection probabilities
        """
        def qmra_model(samples):
            # Calculate total dose from exposure samples
            total_dose = np.zeros(n_iterations)

            for var_name, values in exposure_samples.items():
                if len(values) != n_iterations:
                    raise ValueError(f"Sample size mismatch for {var_name}: expected {n_iterations}, got {len(values)}")
                total_dose += values

            # Apply dose-response function
            return dose_response_function(total_dose)

        return self.run_simulation(qmra_model, n_iterations, "infection_probability")

    def _calculate_statistics(self, samples: np.ndarray) -> Dict[str, float]:
        """Calculate descriptive statistics for samples."""
        # Remove any NaN or infinite values
        clean_samples = samples[np.isfinite(samples)]

        if len(clean_samples) == 0:
            warnings.warn("All samples are NaN or infinite")
            return {}

        return {
            "mean": float(np.mean(clean_samples)),
            "median": float(np.median(clean_samples)),
            "std": float(np.std(clean_samples, ddof=1)),
            "variance": float(np.var(clean_samples, ddof=1)),
            "min": float(np.min(clean_samples)),
            "max": float(np.max(clean_samples)),
            "skewness": float(stats.skew(clean_samples)),
            "kurtosis": float(stats.kurtosis(clean_samples))
        }

    def _calculate_percentiles(self, samples: np.ndarray,
                             percentiles: List[float] = None) -> Dict[str, float]:
        """Calculate percentiles for samples."""
        if percentiles is None:
            percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]

        clean_samples = samples[np.isfinite(samples)]

        if len(clean_samples) == 0:
            return {}

        result = {}
        for p in percentiles:
            result[f"{p}%"] = float(np.percentile(clean_samples, p))

        return result

    def sensitivity_analysis(self,
                           base_model_function: Callable,
                           variable_ranges: Dict[str, float],
                           n_iterations: int = 1000) -> Dict[str, float]:
        """
        Perform sensitivity analysis by varying input parameters.

        Args:
            base_model_function: Base model function
            variable_ranges: Dictionary mapping variable names to percentage variation ranges
            n_iterations: Number of iterations per variable

        Returns:
            Dictionary mapping variable names to sensitivity coefficients
        """
        base_result = self.run_simulation(base_model_function, n_iterations)
        base_mean = base_result.statistics["mean"]

        sensitivity_coefficients = {}

        for var_name, variation_pct in variable_ranges.items():
            if var_name not in self.distributions:
                continue

            # Store original distribution
            original_dist = self.distributions[var_name]

            # Create varied distributions (±variation_pct%)
            varied_results = []
            for factor in [1 - variation_pct/100, 1 + variation_pct/100]:
                # Modify distribution parameters
                varied_params = original_dist.parameters.copy()

                # Scale relevant parameters based on distribution type
                if original_dist.distribution_type in [DistributionType.NORMAL, DistributionType.LOGNORMAL]:
                    varied_params["mean"] *= factor
                elif original_dist.distribution_type == DistributionType.UNIFORM:
                    varied_params["min"] *= factor
                    varied_params["max"] *= factor

                varied_dist = DistributionParameters(
                    distribution_type=original_dist.distribution_type,
                    parameters=varied_params
                )

                # Temporarily replace distribution
                self.distributions[var_name] = varied_dist
                result = self.run_simulation(base_model_function, n_iterations)
                varied_results.append(result.statistics["mean"])

            # Restore original distribution
            self.distributions[var_name] = original_dist

            # Calculate sensitivity coefficient
            delta_output = (varied_results[1] - varied_results[0]) / 2
            delta_input = base_mean * variation_pct / 100

            if delta_input != 0:
                sensitivity_coefficients[var_name] = abs(delta_output / delta_input)
            else:
                sensitivity_coefficients[var_name] = 0.0

        return sensitivity_coefficients

    def export_samples(self, output_file: str, format: str = "csv") -> None:
        """
        Export generated samples to file.

        Args:
            output_file: Output file path
            format: Export format ("csv" or "excel")
        """
        if not self.samples_cache:
            raise ValueError("No samples available to export. Run simulation first.")

        df = pd.DataFrame(self.samples_cache)

        if format.lower() == "csv":
            df.to_csv(output_file, index=False)
        elif format.lower() in ["excel", "xlsx"]:
            df.to_excel(output_file, index=False)
        else:
            raise ValueError(f"Unsupported export format: {format}")


# Convenience functions for common distributions
def create_normal_distribution(mean: float, std: float, name: str = None) -> DistributionParameters:
    """Create normal distribution parameters."""
    return DistributionParameters(
        distribution_type=DistributionType.NORMAL,
        parameters={"mean": mean, "std": std},
        name=name
    )

def create_lognormal_distribution(mean: float, std: float, name: str = None) -> DistributionParameters:
    """Create lognormal distribution parameters."""
    return DistributionParameters(
        distribution_type=DistributionType.LOGNORMAL,
        parameters={"mean": mean, "std": std},
        name=name
    )

def create_uniform_distribution(min_val: float, max_val: float, name: str = None) -> DistributionParameters:
    """Create uniform distribution parameters."""
    return DistributionParameters(
        distribution_type=DistributionType.UNIFORM,
        parameters={"min": min_val, "max": max_val},
        name=name
    )

def create_triangular_distribution(min_val: float, mode: float, max_val: float, name: str = None) -> DistributionParameters:
    """Create triangular distribution parameters."""
    return DistributionParameters(
        distribution_type=DistributionType.TRIANGULAR,
        parameters={"min": min_val, "mode": mode, "max": max_val},
        name=name
    )

def create_empirical_cdf_distribution(x_values: Union[List[float], np.ndarray],
                                      probabilities: Union[List[float], np.ndarray],
                                      min_val: Optional[float] = None,
                                      max_val: Optional[float] = None,
                                      name: str = None) -> DistributionParameters:
    """
    Create empirical cumulative distribution function parameters.

    This is used for sampling dilution data where we have empirical measurements.

    Args:
        x_values: Array of x values (e.g., dilution factors)
        probabilities: Array of cumulative probabilities (0 to 1)
        min_val: Optional minimum bound
        max_val: Optional maximum bound
        name: Optional name for the distribution

    Returns:
        DistributionParameters for ECDF sampling
    """
    params = {
        "x_values": np.array(x_values) if not isinstance(x_values, np.ndarray) else x_values,
        "probabilities": np.array(probabilities) if not isinstance(probabilities, np.ndarray) else probabilities
    }

    if min_val is not None:
        params["min"] = min_val
    if max_val is not None:
        params["max"] = max_val

    return DistributionParameters(
        distribution_type=DistributionType.EMPIRICAL_CDF,
        parameters=params,
        name=name,
        description="Empirical cumulative distribution function for dilution data"
    )

def create_hockey_stick_distribution(x_min: float, x_median: float, x_max: float,
                                     P: float = 0.95,
                                     name: str = None) -> DistributionParameters:
    """
    Create hockey stick distribution parameters for pathogen concentrations.

    Based on McBride's formulation for right-skewed environmental microbiological data.
    The hockey stick distribution has three sections:
    - Section 1 (X₀ to X₅₀): Linear increase, area = 0.5
    - Section 2 (X₅₀ to X_P): Linear continuation, area = P - 0.5
    - Section 3 (X_P to X₁₀₀): Linear decrease, area = 1 - P

    Args:
        x_min: Minimum concentration (X₀)
        x_median: Median concentration (X₅₀) - 50th percentile
        x_max: Maximum concentration (X₁₀₀)
        P: Breakpoint percentile as proportion (default 0.95 = 95th percentile)
           Recommended range: 0.90 to 0.99
        name: Optional name for the distribution

    Returns:
        DistributionParameters for hockey stick sampling

    Raises:
        ValueError: If parameters don't satisfy x_min < x_median < x_max or P not in (0, 1)

    Example:
        >>> # Norovirus concentration: 500k to 1M (median) to 2M org/L
        >>> dist = create_hockey_stick_distribution(
        ...     x_min=500000,
        ...     x_median=1000000,
        ...     x_max=2000000,
        ...     P=0.95
        ... )

    Reference:
        McBride, G. (2009), "Microbial Water Quality and Human Health"
        Section 9.3.2 - Hockey stick distribution
        David Wood's R QMRA package (hockey.R)
    """
    if x_min >= x_median or x_median >= x_max:
        raise ValueError(f"Must have x_min ({x_min}) < x_median ({x_median}) < x_max ({x_max})")

    if not 0 < P < 1:
        raise ValueError(f"P (breakpoint percentile) must be between 0 and 1, got {P}")

    return DistributionParameters(
        distribution_type=DistributionType.HOCKEY_STICK,
        parameters={
            "x_min": x_min,
            "x_median": x_median,
            "x_max": x_max,
            "P": P
        },
        name=name,
        description=f"Hockey stick distribution (P={P:.2%}) for right-skewed pathogen concentration data"
    )


def calculate_empirical_cdf(data: Union[List[float], np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculate empirical cumulative distribution function from data.

    This is the estDistribution function mentioned in the PDF for sampling dilution data.

    Args:
        data: Array of observed values (e.g., dilution factors from hydrodynamic modeling)

    Returns:
        Tuple of (sorted values, cumulative probabilities)
    """
    data_array = np.array(data) if not isinstance(data, np.ndarray) else data
    sorted_data = np.sort(data_array)
    n = len(sorted_data)
    # Use (i)/(n) for cumulative probabilities (Weibull plotting position)
    probs = np.arange(1, n + 1) / n
    return sorted_data, probs


def create_empirical_cdf_from_data(data: Union[List[float], np.ndarray],
                                   min_val: Optional[float] = None,
                                   max_val: Optional[float] = None,
                                   name: str = None) -> DistributionParameters:
    """
    Create empirical CDF distribution from raw data.

    This is a convenience function that calculates the ECDF and creates
    the distribution parameters in one step.

    Args:
        data: Array of observed values (e.g., dilution factors)
        min_val: Optional minimum bound
        max_val: Optional maximum bound
        name: Optional name for the distribution

    Returns:
        DistributionParameters for ECDF sampling

    Example:
        >>> dilution_data = [100, 250, 500, 1000, 2000]
        >>> dilution_dist = create_empirical_cdf_from_data(dilution_data, name="dilution")
        >>> mc = MonteCarloSimulator()
        >>> mc.add_distribution("dilution", dilution_dist)
    """
    x_values, probabilities = calculate_empirical_cdf(data)
    return create_empirical_cdf_distribution(x_values, probabilities, min_val, max_val, name)


if __name__ == "__main__":
    # Example usage and testing
    print("Testing Monte Carlo Simulation Engine")
    print("=" * 40)

    # Create simulator
    mc = MonteCarloSimulator(random_seed=42)

    # Add some test distributions
    pathogen_conc = create_lognormal_distribution(mean=2.0, std=1.0, name="pathogen_concentration")
    water_volume = create_normal_distribution(mean=50.0, std=10.0, name="water_volume")

    mc.add_distribution("pathogen_concentration", pathogen_conc)
    mc.add_distribution("water_volume", water_volume)

    # Define a simple QMRA model
    def simple_qmra_model(samples):
        concentration = samples["pathogen_concentration"]
        volume = samples["water_volume"]
        dose = concentration * volume / 1000  # Convert to organisms
        # Simple exponential dose-response with r=0.1
        infection_prob = 1 - np.exp(-0.1 * dose)
        return infection_prob

    # Run simulation
    results = mc.run_simulation(simple_qmra_model, n_iterations=5000, variable_name="infection_risk")

    print(results.get_summary())

    # Test sensitivity analysis
    print("\nSensitivity Analysis:")
    sensitivity = mc.sensitivity_analysis(
        simple_qmra_model,
        {"pathogen_concentration": 20, "water_volume": 20},
        n_iterations=1000
    )
    for var, coeff in sensitivity.items():
        print(f"  {var}: {coeff:.3f}")

    print(f"\nSimulation completed successfully!")