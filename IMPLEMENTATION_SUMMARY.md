# Implementation Summary: Empirical Distributions for QMRA

## Overview

This document summarizes the implementation of empirical distribution methods for QMRA calculations based on the requirements outlined in `Disttribution.pdf`.

## Implemented Features

### 1. Empirical Cumulative Distribution Function (ECDF)

**Purpose**: Sample dilution data from hydrodynamic modeling

**Implementation Location**:
- `Batch_Processing_App/qmra_core/monte_carlo.py`
- `qmra_toolkit/src/monte_carlo_advanced.py`

**Key Functions**:
- `calculate_empirical_cdf(data)` - Calculates ECDF from raw data (the `estDistribution` function mentioned in PDF)
- `create_empirical_cdf_from_data(data, min_val, max_val, name)` - Creates distribution parameters from data
- `create_empirical_cdf_distribution(x_values, probabilities, min_val, max_val, name)` - Creates distribution from pre-calculated ECDF

**Usage Example**:
```python
from qmra_core.monte_carlo import (
    MonteCarloSimulator,
    create_empirical_cdf_from_data
)

# Dilution data from hydrodynamic modeling (e.g., Nelson North example)
dilution_data = [100, 250, 500, 1000, 2000, 5000, 10000]

# Create ECDF distribution
dilution_dist = create_empirical_cdf_from_data(
    data=dilution_data,
    name="dilution_factor"
)

# Add to Monte Carlo simulator
mc = MonteCarloSimulator()
mc.add_distribution("dilution_factor", dilution_dist)

# Generate samples
samples = mc.sample_distribution("dilution_factor", n_samples=10000)
```

**How it works**:
1. Sorts the input data
2. Calculates cumulative probabilities using Weibull plotting position: P(i) = i/n
3. Uses linear interpolation to sample from the empirical CDF
4. Optional min/max bounds can be applied

### 2. Hockey Stick Distribution

**Purpose**: Estimate pathogen concentrations with right-skewed distributions

**Implementation Location**:
- `Batch_Processing_App/qmra_core/monte_carlo.py`
- `qmra_toolkit/src/monte_carlo_advanced.py`

**Key Functions**:
- `create_hockey_stick_distribution(x_min, x_median, x_max, percentile, name)` - Creates hockey stick distribution
- `sample_hockey_stick(n, x_min, x_median, x_max, percentile)` - Samples from the distribution

**Usage Example**:
```python
from qmra_core.monte_carlo import (
    MonteCarloSimulator,
    create_hockey_stick_distribution
)

# Pathogen concentration parameters from monitoring data
pathogen_dist = create_hockey_stick_distribution(
    x_min=1e4,       # Minimum concentration (X_0)
    x_median=1e6,    # Median concentration (X_50)
    x_max=1e8,       # Maximum concentration (X_100)
    percentile=95,   # Toe of hockey stick (default: 95)
    name="pathogen_concentration"
)

# Add to Monte Carlo simulator
mc = MonteCarloSimulator()
mc.add_distribution("pathogen_concentration", pathogen_dist)

# Generate samples
samples = mc.sample_distribution("pathogen_concentration", n_samples=10000)
```

**How it works** (based on McBride, Section 9.3.2):
1. Constructs a distribution with three regions:
   - Left triangle (A-B): From X_0 to X_50 with 50% probability
   - Middle region (B-C): From X_50 to X_P with (P-50)% probability
   - Right tail (C-D): From X_P to X_100 with (100-P)% probability
2. Calculates the position of point C (X_P) using equations (9.9)-(9.11)
3. Uses inverse transform sampling with linear interpolation in each region

**Key Parameters**:
- `x_min` (X_0): Minimum value from data
- `x_median` (X_50): Median value from data
- `x_max` (X_100): Maximum value from data
- `percentile` (P): Percentile for toe of hockey stick (default 95, as recommended by McBride)

### 3. Integration in QMRA Calculations

Both distributions can be used together in a complete QMRA workflow:

```python
from qmra_core.monte_carlo import (
    MonteCarloSimulator,
    create_hockey_stick_distribution,
    create_empirical_cdf_from_data
)

# Setup pathogen concentration (Hockey Stick)
pathogen_dist = create_hockey_stick_distribution(
    x_min=1e4, x_median=1e6, x_max=1e8,
    name="influent_concentration"
)

# Setup dilution (ECDF from hydrodynamic data)
dilution_data = [100, 500, 1000, 2000, 5000]
dilution_dist = create_empirical_cdf_from_data(
    dilution_data, name="dilution_factor"
)

# Create simulator and add distributions
mc = MonteCarloSimulator(random_seed=42)
mc.add_distribution("influent_concentration", pathogen_dist)
mc.add_distribution("dilution_factor", dilution_dist)

# Define QMRA model
def qmra_model(samples):
    influent = samples["influent_concentration"]
    dilution = samples["dilution_factor"]

    # Concentration at exposure = influent / dilution
    exposure_concentration = influent / dilution

    return exposure_concentration

# Run simulation
results = mc.run_simulation(
    qmra_model,
    n_iterations=10000,
    variable_name="exposure_concentration"
)

print(f"Mean exposure: {results.statistics['mean']:.2e}")
print(f"95th percentile: {results.percentiles['95%']:.2e}")
```

## Files Modified

### Batch Processing App
1. **`Batch_Processing_App/qmra_core/monte_carlo.py`**
   - Added `DistributionType.EMPIRICAL_CDF` enum
   - Added `DistributionType.HOCKEY_STICK` enum
   - Implemented ECDF sampling in `_generate_samples()`
   - Implemented Hockey Stick sampling in `_generate_samples()`
   - Added helper functions:
     - `calculate_empirical_cdf()`
     - `create_empirical_cdf_distribution()`
     - `create_empirical_cdf_from_data()`
     - `create_hockey_stick_distribution()`

### Main Toolkit
2. **`qmra_toolkit/src/monte_carlo_advanced.py`**
   - Added `sample_hockey_stick()` method to `DistributionSampler` class
   - Updated `get_sim_value()` to support 'hockey_stick' distribution
   - ECDF already existed as `sample_cumulative()` method

## Testing

A comprehensive test script has been created: `test_empirical_distributions.py`

**Test Results**:
- Test 1 (ECDF for Dilution): **PASS**
  - Generated 10,000 samples from ECDF
  - Verified statistical properties
  - Created visualization plots

- Test 2 (Hockey Stick for Pathogen): **PASS**
  - Generated 10,000 samples
  - Verified median matches X_50 (error < 2%)
  - Created distribution plots (linear and log scale)

- Test 3 (Integrated QMRA): **PASS**
  - Combined both distributions in QMRA calculation
  - Calculated exposure concentrations
  - Generated results plots

**Generated Plots**:
- `test_ecdf_dilution.png` - ECDF visualization and sample distribution
- `test_hockey_stick_pathogen.png` - Hockey stick distribution plots
- `test_integrated_qmra.png` - Integrated QMRA results

## Reference

The implementations are based on:

1. **Empirical CDF**: As described in `Disttribution.pdf`, pages 2-4
   - The `estDistribution` function for sampling dilution data
   - Examples from Nelson North hydrodynamic modeling

2. **Hockey Stick Distribution**: McBride (2009), "Microbial Water Quality and Human Health"
   - Section 9.3.2 - Hockey stick distribution
   - Equations (9.9)-(9.11) for calculating distribution parameters
   - As referenced in `Disttribution.pdf`, pages 5-7

## Usage in Model Input

These distributions can be used in QMRA model inputs:

### For Dilution Data
When you have dilution data from hydrodynamic modeling:
```python
# Read dilution data from CSV or modeling output
dilution_data = pd.read_csv('dilution_results.csv')['dilution_factor']

# Create ECDF distribution
dilution_dist = create_empirical_cdf_from_data(
    data=dilution_data.values,
    name="site_dilution"
)
```

### For Pathogen Concentrations
When you have min, median, max from monitoring data:
```python
# From historical monitoring data
pathogen_dist = create_hockey_stick_distribution(
    x_min=monitoring_data['min'],
    x_median=monitoring_data['median'],
    x_max=monitoring_data['max'],
    percentile=95,
    name="influent_pathogens"
)
```

## Next Steps

The implementations are now integrated into both:
1. Batch Processing App (`qmra_core` module)
2. Main QMRA Toolkit (`monte_carlo_advanced.py`)

Users can now:
- Sample dilution data using ECDF (as mentioned in the PDF)
- Model pathogen concentrations using Hockey Stick distribution
- Integrate both methods in complete QMRA calculations

All functionality has been tested and validated with the test script.
