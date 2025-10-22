#!/usr/bin/env python3
"""
SIMPLE EXAMPLE: Recommended Way to Use Empirical Distributions

This is the SIMPLEST way to get started with the new distributions.
Just run this script and it will show you the recommended approach.
"""

import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch_processor import BatchProcessor

print("="*80)
print("SIMPLE EXAMPLE: Using Empirical Distributions (RECOMMENDED APPROACH)")
print("="*80)

# =============================================================================
# STEP 1: Calculate pathogen parameters from your monitoring data
# =============================================================================
print("\n[STEP 1] Calculating pathogen parameters from monitoring data...")

monitoring_file = 'input_data/pathogen_concentrations/multi_pathogen_data.csv'
monitoring = pd.read_csv(monitoring_file)

# For Norovirus
norovirus_data = monitoring['Norovirus_copies_per_L'].dropna()
noro_min = norovirus_data.min()
noro_median = norovirus_data.median()
noro_max = norovirus_data.max()
noro_cv = norovirus_data.std() / norovirus_data.mean()

print(f"\n  Norovirus (from {len(norovirus_data)} samples):")
print(f"    Min:    {noro_min:>10,.0f} copies/L")
print(f"    Median: {noro_median:>10,.0f} copies/L")
print(f"    Max:    {noro_max:>10,.0f} copies/L")
print(f"    CV:     {noro_cv:>10.2f}")
print(f"    Recommendation: {'Hockey Stick (high variability)' if noro_cv > 0.5 else 'Fixed concentration OK'}")

# =============================================================================
# STEP 2: Run spatial assessment with BOTH distributions (RECOMMENDED)
# =============================================================================
print("\n[STEP 2] Running spatial assessment with BOTH distributions...")

processor = BatchProcessor(output_dir='outputs/simple_example')

# This is the RECOMMENDED way - use both ECDF and Hockey Stick
results = processor.run_spatial_assessment(
    dilution_file='input_data/dilution_data/spatial_dilution_6_sites.csv',
    pathogen='norovirus',

    # DISTRIBUTION SETTINGS (This is the key part!)
    use_ecdf_dilution=True,       # Use all 100 hydrodynamic simulations
    use_hockey_pathogen=True,      # Use Hockey Stick for pathogen

    # Pathogen parameters (from monitoring data above)
    pathogen_min=noro_min,
    pathogen_median=noro_median,
    pathogen_max=noro_max,

    # Standard QMRA parameters
    treatment_lrv=3.0,
    exposure_route='primary_contact',
    volume_ml=50,
    frequency_per_year=25,
    population=15000,
    iterations=10000,
    output_file='recommended_approach_results.csv'
)

# =============================================================================
# STEP 3: Review results
# =============================================================================
print("\n[STEP 3] Results summary...")

print(f"\n{'Site':<15} {'Distance':<10} {'Median Risk':<15} {'95th Risk':<15} {'Status':<15}")
print("-"*75)

for _, row in results.iterrows():
    print(f"{row['Site_Name']:<15} {row['Distance_m']:<10.0f} "
          f"{row['Annual_Risk_Median']:<15.2e} {row['Annual_Risk_95th']:<15.2e} "
          f"{row['Compliance_Status']:<15}")

# =============================================================================
# COMPARISON: Show what you would have gotten with old approach
# =============================================================================
print("\n" + "="*80)
print("COMPARISON: What difference do the distributions make?")
print("="*80)

print("\nRunning legacy approach for comparison...")

results_legacy = processor.run_spatial_assessment(
    dilution_file='input_data/dilution_data/spatial_dilution_6_sites.csv',
    pathogen='norovirus',

    # OLD APPROACH
    use_ecdf_dilution=False,           # Just use median dilution
    use_hockey_pathogen=False,         # Just use fixed concentration
    effluent_concentration=noro_median,  # Use median as fixed value

    treatment_lrv=3.0,
    exposure_route='primary_contact',
    volume_ml=50,
    frequency_per_year=25,
    population=15000,
    iterations=10000,
    output_file='legacy_approach_results.csv'
)

# Compare one site
site = 'Site_50m'
new = results[results['Site_Name'] == site].iloc[0]
old = results_legacy[results_legacy['Site_Name'] == site].iloc[0]

print(f"\nComparison for {site}:")
print(f"\n{'Method':<30} {'Median Risk':<15} {'95th Risk':<15}")
print("-"*60)
print(f"{'Old (Median + Fixed)':<30} {old['Annual_Risk_Median']:<15.2e} {old['Annual_Risk_95th']:<15.2e}")
print(f"{'New (ECDF + Hockey)':<30} {new['Annual_Risk_Median']:<15.2e} {new['Annual_Risk_95th']:<15.2e}")

change_median = (new['Annual_Risk_Median'] - old['Annual_Risk_Median']) / old['Annual_Risk_Median'] * 100
change_95th = (new['Annual_Risk_95th'] - old['Annual_Risk_95th']) / old['Annual_Risk_95th'] * 100

print(f"\nDifference:")
print(f"  Median risk: {change_median:+.1f}%")
print(f"  95th percentile: {change_95th:+.1f}%")

# =============================================================================
# EXPLANATION
# =============================================================================
print("\n" + "="*80)
print("WHAT JUST HAPPENED?")
print("="*80)

print("""
The RECOMMENDED approach (what you just ran):

1. ECDF for Dilution (use_ecdf_dilution=True):
   - Uses ALL 100 hydrodynamic simulations per site
   - Not just the median!
   - Captures variability in ocean conditions

2. Hockey Stick for Pathogen (use_hockey_pathogen=True):
   - Uses min/median/max from your monitoring data
   - Models right-skewed concentration distribution
   - Represents rare high-concentration events

3. Result:
   - More realistic risk estimates
   - Better captures tail risks (95th percentile)
   - Uses 100% of your data (not 1%)

The OLD approach (for comparison):
   - Used only median dilution (wasted 99% of data)
   - Used fixed pathogen concentration
   - Simpler but less accurate
""")

print("="*80)
print("RECOMMENDATION")
print("="*80)
print("""
For production analyses, use the RECOMMENDED approach:

    results = processor.run_spatial_assessment(
        dilution_file='your_dilution_file.csv',
        pathogen='norovirus',
        use_ecdf_dilution=True,      # <-- Use full ECDF
        use_hockey_pathogen=True,     # <-- Use Hockey Stick
        pathogen_min=...,             # <-- From monitoring data
        pathogen_median=...,          # <-- From monitoring data
        pathogen_max=...,             # <-- From monitoring data
        treatment_lrv=3.0,
        iterations=10000
    )

This gives you the most defensible risk estimates for regulatory purposes.
""")

print("\nResults saved to: outputs/simple_example/")
print("="*80)
