# Monte Carlo Module

Monte Carlo Simulation Engine for QMRA Toolkit

This module provides Monte Carlo simulation capabilities for uncertainty analysis
in quantitative microbial risk assessment, replacing @Risk functionality.

## Classes

### DistributionParameters

Container for distribution parameters.

### DistributionType

Supported probability distributions for Monte Carlo sampling.

### MonteCarloResults

Container for Monte Carlo simulation results.

### MonteCarloSimulator

Monte Carlo simulation engine for QMRA uncertainty analysis.

This class replaces @Risk functionality with native Python implementation.

## Functions

### create_lognormal_distribution(mean: float, std: float, name: str = None) -> monte_carlo.DistributionParameters

Create lognormal distribution parameters.

### create_normal_distribution(mean: float, std: float, name: str = None) -> monte_carlo.DistributionParameters

Create normal distribution parameters.

### create_triangular_distribution(min_val: float, mode: float, max_val: float, name: str = None) -> monte_carlo.DistributionParameters

Create triangular distribution parameters.

### create_uniform_distribution(min_val: float, max_val: float, name: str = None) -> monte_carlo.DistributionParameters

Create uniform distribution parameters.

