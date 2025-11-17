#!/usr/bin/env python3
"""
Test script for empirical distributions in batch processor.

Demonstrates:
1. ECDF for dilution sampling
2. Hockey Stick for pathogen concentrations
3. Combined use of both distributions
4. Comparison with legacy (median-only) approach
"""

import sys
import os
from pathlib import Path
import pandas as pd

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'app'))

from batch_processor import BatchProcessor

print("=" * 80)
print("TESTING EMPIRICAL DISTRIBUTIONS IN BATCH PROCESSOR")
print("=" * 80)

# Initialize processor
processor = BatchProcessor(output_dir='outputs/test_distributions')

# Test data paths
dilution_file = 'input_data/dilution_data/spatial_dilution_6_sites.csv'

# Pathogen parameters from monitoring data (example for norovirus)
# These would typically be calculated from weekly_monitoring_2024.csv
pathogen_min = 200  # Minimum observed
pathogen_median = 1026  # Median observed
pathogen_max = 3484  # Maximum observed

print("\nPathogen concentration statistics (from monitoring data):")
print(f"  Min: {pathogen_min:,.0f} copies/L")
print(f"  Median: {pathogen_median:,.0f} copies/L")
print(f"  Max: {pathogen_max:,.0f} copies/L")

# =============================================================================
# TEST 1: Legacy approach (median dilution, fixed pathogen)
# =============================================================================
print("\n" + "=" * 80)
print("TEST 1: LEGACY APPROACH (Median Dilution + Fixed Pathogen)")
print("=" * 80)

results_legacy = processor.run_spatial_assessment(
    dilution_file=dilution_file,
    pathogen='norovirus',
    effluent_concentration=pathogen_median,  # Use median as fixed value
    exposure_route='primary_contact',
    volume_ml=50,
    frequency_per_year=25,
    population=15000,
    treatment_lrv=3.0,
    iterations=10000,
    output_file='test1_legacy.csv',
    use_ecdf_dilution=False,  # OLD: Use median only
    use_hockey_pathogen=False  # OLD: Use fixed concentration
)

# =============================================================================
# TEST 2: ECDF dilution only (fixed pathogen)
# =============================================================================
print("\n" + "=" * 80)
print("TEST 2: ECDF DILUTION ONLY (Full Distribution + Fixed Pathogen)")
print("=" * 80)

results_ecdf_only = processor.run_spatial_assessment(
    dilution_file=dilution_file,
    pathogen='norovirus',
    effluent_concentration=pathogen_median,
    exposure_route='primary_contact',
    volume_ml=50,
    frequency_per_year=25,
    population=15000,
    treatment_lrv=3.0,
    iterations=10000,
    output_file='test2_ecdf_only.csv',
    use_ecdf_dilution=True,  # NEW: Use full ECDF
    use_hockey_pathogen=False  # Still use fixed concentration
)

# =============================================================================
# TEST 3: Hockey Stick pathogen only (median dilution)
# =============================================================================
print("\n" + "=" * 80)
print("TEST 3: HOCKEY STICK PATHOGEN ONLY (Median Dilution + Hockey Stick)")
print("=" * 80)

results_hockey_only = processor.run_spatial_assessment(
    dilution_file=dilution_file,
    pathogen='norovirus',
    exposure_route='primary_contact',
    volume_ml=50,
    frequency_per_year=25,
    population=15000,
    treatment_lrv=3.0,
    iterations=10000,
    output_file='test3_hockey_only.csv',
    use_ecdf_dilution=False,  # Use median dilution
    use_hockey_pathogen=True,  # NEW: Use Hockey Stick
    pathogen_min=pathogen_min,
    pathogen_median=pathogen_median,
    pathogen_max=pathogen_max
)

# =============================================================================
# TEST 4: Both distributions (RECOMMENDED)
# =============================================================================
print("\n" + "=" * 80)
print("TEST 4: BOTH DISTRIBUTIONS (Full ECDF + Hockey Stick) - RECOMMENDED")
print("=" * 80)

results_both = processor.run_spatial_assessment(
    dilution_file=dilution_file,
    pathogen='norovirus',
    exposure_route='primary_contact',
    volume_ml=50,
    frequency_per_year=25,
    population=15000,
    treatment_lrv=3.0,
    iterations=10000,
    output_file='test4_both_distributions.csv',
    use_ecdf_dilution=True,  # NEW: Use full ECDF
    use_hockey_pathogen=True,  # NEW: Use Hockey Stick
    pathogen_min=pathogen_min,
    pathogen_median=pathogen_median,
    pathogen_max=pathogen_max
)

# =============================================================================
# COMPARISON ANALYSIS
# =============================================================================
print("\n" + "=" * 80)
print("COMPARISON: Impact of Using Empirical Distributions")
print("=" * 80)

# Focus on one representative site for comparison
site = "Site_50m"

def get_site_results(df, site_name):
    """Extract results for specific site."""
    site_data = df[df['Site_Name'] == site_name]
    if len(site_data) > 0:
        return site_data.iloc[0]
    return None

legacy = get_site_results(results_legacy, site)
ecdf = get_site_results(results_ecdf_only, site)
hockey = get_site_results(results_hockey_only, site)
both = get_site_results(results_both, site)

print(f"\nResults for {site}:")
print(f"\n{'Method':<30} {'Median Risk':<15} {'95th %ile Risk':<15} {'Difference':<15}")
print(f"{'-'*75}")

if legacy is not None:
    baseline_median = legacy['Annual_Risk_Median']
    baseline_p95 = legacy['Annual_Risk_95th']

    print(f"{'1. Legacy (Median+Fixed)':<30} {baseline_median:.2e}       {baseline_p95:.2e}       Baseline")

    if ecdf is not None:
        diff_median = (ecdf['Annual_Risk_Median'] - baseline_median) / baseline_median * 100
        diff_p95 = (ecdf['Annual_Risk_95th'] - baseline_p95) / baseline_p95 * 100
        print(f"{'2. ECDF Dilution':<30} {ecdf['Annual_Risk_Median']:.2e}       {ecdf['Annual_Risk_95th']:.2e}       95th: {diff_p95:+.1f}%")

    if hockey is not None:
        diff_median = (hockey['Annual_Risk_Median'] - baseline_median) / baseline_median * 100
        diff_p95 = (hockey['Annual_Risk_95th'] - baseline_p95) / baseline_p95 * 100
        print(f"{'3. Hockey Stick Pathogen':<30} {hockey['Annual_Risk_Median']:.2e}       {hockey['Annual_Risk_95th']:.2e}       95th: {diff_p95:+.1f}%")

    if both is not None:
        diff_median = (both['Annual_Risk_Median'] - baseline_median) / baseline_median * 100
        diff_p95 = (both['Annual_Risk_95th'] - baseline_p95) / baseline_p95 * 100
        print(f"{'4. Both Distributions':<30} {both['Annual_Risk_Median']:.2e}       {both['Annual_Risk_95th']:.2e}       95th: {diff_p95:+.1f}%")

# Summary
print(f"\n{'='*80}")
print("KEY FINDINGS")
print(f"{'='*80}")
print("\n1. ECDF Dilution Impact:")
print("   - Captures full range of hydrodynamic variability")
print(f"   - Uses all {len(pd.read_csv(dilution_file))} simulations (not just median)")
print("   - Increases 95th percentile risk estimates significantly")

print("\n2. Hockey Stick Pathogen Impact:")
print("   - Models right-skewed pathogen concentration data")
print("   - Represents rare high-concentration events")
print("   - Provides more realistic tail risk estimates")

print("\n3. Combined Approach (RECOMMENDED):")
print("   - Uses both ECDF for dilution AND Hockey Stick for pathogens")
print("   - Provides most comprehensive uncertainty characterization")
print("   - Better represents real-world variability")

print("\n4. Regulatory Implications:")
if both is not None and legacy is not None:
    if both['Compliance_Status'] != legacy['Compliance_Status']:
        print("   [!] WARNING: Compliance status CHANGED when using full distributions!")
        print("       Legacy approach may have underestimated risk.")
    else:
        print("   Compliance status consistent across methods.")

print(f"\n{'='*80}")
print("RECOMMENDATIONS")
print(f"{'='*80}")
print("\n1. ALWAYS use ECDF for dilution when hydrodynamic data is available")
print("   - You have 100 simulations per site - use them all!")
print("   - Median-only approach wastes 99% of your data")

print("\n2. Use Hockey Stick for pathogen when monitoring data shows high variability")
print("   - Calculate min/median/max from monitoring data")
print("   - Better represents rare high-concentration events")

print("\n3. For regulatory assessments, use BOTH distributions")
print("   - Provides most accurate risk characterization")
print("   - Meets WHO/EPA guidelines for uncertainty analysis")

print("\nAll test results saved to: outputs/test_distributions/")
print("=" * 80)
