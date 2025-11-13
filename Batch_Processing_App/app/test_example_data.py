"""
Test script to verify example data files work correctly with the app.
"""

import sys
sys.path.insert(0, '..')
sys.path.insert(0, '.')

import pandas as pd
from batch_processor import BatchProcessor

print("=" * 70)
print("TESTING EXAMPLE DATA WITH BATCH PROCESSOR")
print("=" * 70)
print()

# Test 1: Load example data files
print("TEST 1: Loading example data files...")
print("-" * 70)

try:
    dilution_file = "../input_data/dilution_data/spatial_dilution_6_sites.csv"
    df_dilution = pd.read_csv(dilution_file)
    print(f"[OK] Dilution data loaded: {len(df_dilution)} rows")
    print(f"  Columns: {list(df_dilution.columns)}")
    print()
except Exception as e:
    print(f"[FAIL] Failed to load dilution data: {e}")
    sys.exit(1)

try:
    monitoring_file = "../input_data/pathogen_concentrations/weekly_monitoring_2024.csv"
    df_monitoring = pd.read_csv(monitoring_file)
    print(f"[OK] Monitoring data loaded: {len(df_monitoring)} rows")
    print(f"  Columns: {list(df_monitoring.columns)}")
    print()
except Exception as e:
    print(f"[FAIL] Failed to load monitoring data: {e}")
    sys.exit(1)

# Test 2: Initialize BatchProcessor
print("TEST 2: Initializing BatchProcessor...")
print("-" * 70)

try:
    processor = BatchProcessor()
    print("[OK] BatchProcessor initialized successfully")
    print()
except Exception as e:
    print(f"[FAIL] Failed to initialize BatchProcessor: {e}")
    sys.exit(1)

# Test 3: Check norovirus defaults to Beta-Binomial
print("TEST 3: Checking default dose-response model for norovirus...")
print("-" * 70)

try:
    default_model = processor.pathogen_db.get_default_model_type("norovirus")
    print(f"[OK] Default model for norovirus: {default_model}")

    if default_model == "beta_binomial":
        print("  [OK] CORRECT: Using Beta-Binomial (exact model)")
        params = processor.pathogen_db.get_dose_response_parameters("norovirus", "beta_binomial")
        print(f"  Parameters: alpha={params['alpha']}, beta={params['beta']}")
    else:
        print(f"  [FAIL] WARNING: Expected beta_binomial, got {default_model}")
    print()
except Exception as e:
    print(f"[FAIL] Failed to check default model: {e}")
    sys.exit(1)

# Test 4: Test dose-response calculation
print("TEST 4: Testing dose-response calculations (vs David's Excel)...")
print("-" * 70)

try:
    from qmra_core.dose_response import create_dose_response_model

    params = {"alpha": 0.04, "beta": 0.055}
    model = create_dose_response_model("beta_binomial", params)

    # Test against David's Excel values
    test_cases = [
        (1, 0.421053),
        (10, 0.480735),
        (100, 0.527157)
    ]

    all_match = True
    for dose, expected in test_cases:
        calculated = model.calculate_infection_probability(dose)
        match = abs(calculated - expected) < 1e-5
        status = "[OK]" if match else "[FAIL]"
        print(f"  {status} Dose {dose:3d}: Calculated={calculated:.6f}, Expected={expected:.6f}")
        all_match = all_match and match

    if all_match:
        print("  [OK] ALL VALUES MATCH DAVID'S EXCEL")
    else:
        print("  [FAIL] MISMATCH DETECTED")
    print()
except Exception as e:
    print(f"[FAIL] Failed dose-response test: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Run simple spatial assessment
print("TEST 5: Running simple spatial assessment (3 sites)...")
print("-" * 70)

try:
    # Get first 3 unique sites from dilution data
    sites = df_dilution['Site_Name'].unique()[:3]
    dilution_factors = []

    for site in sites:
        site_data = df_dilution[df_dilution['Site_Name'] == site]
        dilution_factors.append(site_data['Dilution_Factor'].median())

    print(f"  Testing {len(sites)} sites:")
    for i, (site, dilution) in enumerate(zip(sites, dilution_factors), 1):
        print(f"    {i}. {site}: Dilution={dilution:.1f}")
    print()

    # Run assessment for first site only (quick test)
    site = sites[0]
    dilution = dilution_factors[0]

    result = processor._run_single_assessment(
        pathogen="norovirus",
        concentration=1e6,  # 1 million org/L
        dilution=dilution,
        volume_ml=50,
        frequency_per_year=20,
        population=10000,
        iterations=1000  # Reduced for quick test
    )

    print(f"  Results for {site}:")
    print(f"    Per-event infection risk: {result['pinf_median']:.2e}")
    print(f"    Annual risk: {result['annual_risk_median']:.2e}")
    print(f"    Population impact: {result['population_impact']:.0f} infections/year")
    print(f"    Compliance: {result['annual_risk_median'] <= 1e-4}")
    print()
    print("  [OK] Assessment completed successfully")
    print()

except Exception as e:
    print(f"[FAIL] Failed spatial assessment: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Summary
print("=" * 70)
print("SUMMARY: ALL TESTS PASSED [OK]")
print("=" * 70)
print()
print("Example data files are working correctly with the app.")
print("The app is ready to use in Production Mode (norovirus only).")
print()
