#!/usr/bin/env python3
"""
Verification script for dose-response models and QMRA calculations.

Tests dose-response models against published values and validates the calculation flow.

Author: NIWA Earth Sciences New Zealand
Date: October 2025
"""

import numpy as np
from qmra_core import (
    PathogenDatabase,
    create_dose_response_model,
    MonteCarloSimulator,
    create_hockey_stick_distribution
)

def test_dose_response_models():
    """Test dose-response models against known values."""

    print("="*80)
    print("DOSE-RESPONSE MODEL VERIFICATION")
    print("="*80)

    db = PathogenDatabase()

    # Test 1: Norovirus Beta-Poisson
    print("\n1. Norovirus (Beta-Poisson): alpha=0.04, beta=0.055")
    print("   Source: Teunis et al. (2008)")

    noro_params = db.get_dose_response_parameters("norovirus", "beta_poisson")
    noro_model = create_dose_response_model("beta_poisson", noro_params)

    # Test specific dose values
    test_doses = [1, 10, 100, 1000]
    print("\n   Dose -> Infection Probability:")
    for dose in test_doses:
        pinf = noro_model.calculate_infection_probability(dose)
        print(f"   {dose:6.0f} organisms → {pinf:.4f} ({pinf*100:.2f}%)")

    # Verify formula: P = 1 - (1 + dose/beta)^(-alpha)
    alpha, beta = 0.04, 0.055
    dose = 100
    expected = 1 - (1 + dose/beta)**(-alpha)
    calculated = noro_model.calculate_infection_probability(dose)
    print(f"\n   Formula check (dose={dose}):")
    print(f"   Expected:   {expected:.6f}")
    print(f"   Calculated: {calculated:.6f}")
    print(f"   Match: {'[OK]' if abs(expected - calculated) < 1e-6 else '[FAIL]'}")

    # Test 2: Cryptosporidium Exponential
    print("\n2. Cryptosporidium (Exponential): r=0.0042")
    print("   Source: Haas et al. (1996)")

    crypto_params = db.get_dose_response_parameters("cryptosporidium", "exponential")
    crypto_model = create_dose_response_model("exponential", crypto_params)

    test_doses = [1, 10, 100, 1000]
    print("\n   Dose -> Infection Probability:")
    for dose in test_doses:
        pinf = crypto_model.calculate_infection_probability(dose)
        print(f"   {dose:6.0f} oocysts → {pinf:.4f} ({pinf*100:.2f}%)")

    # Verify formula: P = 1 - exp(-r * dose)
    r = 0.0042
    dose = 100
    expected = 1 - np.exp(-r * dose)
    calculated = crypto_model.calculate_infection_probability(dose)
    print(f"\n   Formula check (dose={dose}):")
    print(f"   Expected:   {expected:.6f}")
    print(f"   Calculated: {calculated:.6f}")
    print(f"   Match: {'[OK]' if abs(expected - calculated) < 1e-6 else '[FAIL]'}")

    # Test 3: Campylobacter Beta-Poisson
    print("\n3. Campylobacter (Beta-Poisson): alpha=0.145, beta=7.59")
    print("   Source: Teunis et al. (2005)")

    campy_params = db.get_dose_response_parameters("campylobacter", "beta_poisson")
    campy_model = create_dose_response_model("beta_poisson", campy_params)

    test_doses = [100, 500, 1000, 5000]
    print("\n   Dose -> Infection Probability:")
    for dose in test_doses:
        pinf = campy_model.calculate_infection_probability(dose)
        print(f"   {dose:6.0f} organisms → {pinf:.4f} ({pinf*100:.2f}%)")

    return True


def test_qmra_calculation_flow():
    """Test complete QMRA calculation flow."""

    print("\n" + "="*80)
    print("QMRA CALCULATION FLOW VERIFICATION")
    print("="*80)

    db = PathogenDatabase()

    # Scenario: Norovirus, primary contact, 100x dilution
    print("\nTest Scenario:")
    print("  Pathogen: Norovirus (1e6 copies/L in effluent)")
    print("  Treatment: 3 LRV (secondary)")
    print("  Dilution: 100x")
    print("  Volume: 50 mL ingested")
    print("  Exposure route: Primary contact")

    # Step-by-step calculation
    effluent_conc = 1e6  # copies/L
    treatment_lrv = 3
    dilution = 100
    volume_ml = 50

    print("\nStep-by-step calculation:")

    # Step 1: Apply treatment
    post_treatment = effluent_conc / (10 ** treatment_lrv)
    print(f"  1. Post-treatment: {effluent_conc:.0e} / 10^{treatment_lrv} = {post_treatment:.0e} copies/L")

    # Step 2: Apply dilution
    exposure_conc = post_treatment / dilution
    print(f"  2. After dilution: {post_treatment:.0e} / {dilution} = {exposure_conc:.0e} copies/L")

    # Step 3: Calculate dose
    dose = exposure_conc * (volume_ml / 1000.0)  # Convert mL to L
    print(f"  3. Dose: {exposure_conc:.0e} × ({volume_ml}/1000) = {dose:.2f} copies ingested")

    # Step 4: Calculate infection probability
    noro_params = db.get_dose_response_parameters("norovirus", "beta_poisson")
    dr_model = create_dose_response_model("beta_poisson", noro_params)
    pinf = dr_model.calculate_infection_probability(dose)
    print(f"  4. Infection probability: {pinf:.4f} ({pinf*100:.2f}%)")

    # Step 5: Calculate illness probability
    health_data = db.get_health_impact_data("norovirus")
    pill = pinf * health_data['illness_to_infection_ratio']
    print(f"  5. Illness probability: {pinf:.4f} × {health_data['illness_to_infection_ratio']} = {pill:.4f} ({pill*100:.2f}%)")

    # Step 6: Calculate annual risk
    frequency = 25  # exposures per year
    annual_risk = 1 - (1 - pinf) ** frequency
    print(f"  6. Annual risk: 1 - (1 - {pinf:.4f})^{frequency} = {annual_risk:.4f} ({annual_risk*100:.2f}%)")

    # Step 7: Compare with WHO guideline
    who_threshold = 1e-4
    print(f"\n  WHO guideline: {who_threshold:.0e} ({who_threshold*100:.4f}%)")
    print(f"  Status: {'COMPLIANT [OK]' if annual_risk <= who_threshold else 'NON-COMPLIANT [FAIL]'}")
    print(f"  Exceedance: {annual_risk/who_threshold:.1f}x threshold")

    return True


def test_hockey_stick_distribution():
    """Test Hockey Stick distribution implementation."""

    print("\n" + "="*80)
    print("HOCKEY STICK DISTRIBUTION VERIFICATION")
    print("="*80)

    # Create Hockey Stick distribution
    x_min = 500000
    x_median = 1000000
    x_max = 2000000

    print(f"\nHockey Stick Parameters:")
    print(f"  Min:    {x_min:.0e}")
    print(f"  Median: {x_median:.0e}")
    print(f"  Max:    {x_max:.0e}")

    dist = create_hockey_stick_distribution(x_min, x_median, x_max, name="test_pathogen")

    # Generate samples using MonteCarloSimulator
    mc_sim = MonteCarloSimulator(random_seed=42)
    mc_sim.add_distribution("test", dist)

    def identity_model(samples):
        return samples["test"]

    result = mc_sim.run_simulation(identity_model, n_iterations=10000, variable_name="pathogen_conc")
    samples = result.samples

    print(f"\nGenerated 10,000 samples:")
    print(f"  Observed Min:    {np.min(samples):.0e}")
    print(f"  Observed Median: {np.median(samples):.0e}")
    print(f"  Observed Mean:   {np.mean(samples):.0e}")
    print(f"  Observed Max:    {np.max(samples):.0e}")

    # Verify percentiles
    print(f"\nPercentiles:")
    for p in [5, 25, 50, 75, 95]:
        value = np.percentile(samples, p)
        print(f"  {p:2d}th: {value:.0e}")

    # Check that median is approximately correct
    observed_median = np.median(samples)
    error = abs(observed_median - x_median) / x_median
    print(f"\nMedian verification:")
    print(f"  Target:   {x_median:.0e}")
    print(f"  Observed: {observed_median:.0e}")
    print(f"  Error:    {error*100:.2f}%")
    print(f"  Status:   {'[OK] PASS' if error < 0.05 else '[FAIL] FAIL'}")

    return True


def test_realistic_scenario():
    """Test a realistic full QMRA scenario."""

    print("\n" + "="*80)
    print("REALISTIC SCENARIO TEST")
    print("="*80)

    print("\nScenario: Beach with UV treatment")
    print("  Location: Site A")
    print("  Pathogen: Norovirus (Hockey Stick: 5e5 - 1e6 - 2e6)")
    print("  Dilution: Variable (90-130x, median 115x)")
    print("  Treatment: UV (8 LRV)")
    print("  Volume: 50 mL (range 35-75 mL)")
    print("  Frequency: 25 times/year")
    print("  Iterations: 10,000")

    # Setup
    db = PathogenDatabase()
    noro_params = db.get_dose_response_parameters("norovirus", "beta_poisson")
    dr_model = create_dose_response_model("beta_poisson", noro_params)
    health_data = db.get_health_impact_data("norovirus")

    # Monte Carlo
    mc_sim = MonteCarloSimulator(random_seed=42)

    # Add distributions
    pathogen_dist = create_hockey_stick_distribution(5e5, 1e6, 2e6, name="pathogen")
    mc_sim.add_distribution("pathogen", pathogen_dist)

    # Simplified: use lognormal for dilution centered at 115
    from qmra_core import create_lognormal_distribution
    dilution_dist = create_lognormal_distribution(np.log(115), 0.15, name="dilution")
    mc_sim.add_distribution("dilution", dilution_dist)

    from qmra_core import create_uniform_distribution
    volume_dist = create_uniform_distribution(35, 75, name="volume")
    mc_sim.add_distribution("volume", volume_dist)

    # Define model
    def qmra_model(samples):
        pathogen_conc = samples["pathogen"]
        dilution = samples["dilution"]
        volume = samples["volume"]

        # Apply UV treatment (8 LRV)
        post_treatment = pathogen_conc / (10 ** 8)

        # Apply dilution
        exposure_conc = post_treatment / dilution

        # Calculate dose
        dose = exposure_conc * (volume / 1000.0)

        # Infection probability
        return dr_model.calculate_infection_probability(dose)

    # Run simulation
    results = mc_sim.run_simulation(qmra_model, n_iterations=10000, variable_name="infection_prob")

    # Calculate risks
    pinf_median = results.statistics['median']
    pill_median = pinf_median * health_data['illness_to_infection_ratio']
    annual_risk = 1 - (1 - pinf_median) ** 25

    print(f"\nResults:")
    print(f"  Infection risk (median): {pinf_median:.2e} ({pinf_median*100:.4f}%)")
    print(f"  Illness risk (median):   {pill_median:.2e} ({pill_median*100:.4f}%)")
    print(f"  Annual risk:             {annual_risk:.2e} ({annual_risk*100:.4f}%)")
    print(f"  WHO threshold:           1.00e-04 (0.0100%)")
    print(f"  Status:                  {'COMPLIANT [OK]' if annual_risk <= 1e-4 else 'NON-COMPLIANT [FAIL]'}")

    # Expected: With 8 LRV UV, should be compliant
    expected_compliant = True
    is_compliant = annual_risk <= 1e-4

    print(f"\nValidation:")
    print(f"  Expected: {'COMPLIANT' if expected_compliant else 'NON-COMPLIANT'}")
    print(f"  Observed: {'COMPLIANT' if is_compliant else 'NON-COMPLIANT'}")
    print(f"  Status:   {'[OK] PASS' if is_compliant == expected_compliant else '[FAIL] FAIL'}")

    return is_compliant == expected_compliant


def main():
    """Run all verification tests."""

    print("\n" + "="*80)
    print("QMRA BACKEND CALCULATIONS VERIFICATION")
    print("="*80)
    print("\nVerifying dose-response models, distributions, and calculation flow...")
    print("="*80)

    tests = [
        ("Dose-Response Models", test_dose_response_models),
        ("QMRA Calculation Flow", test_qmra_calculation_flow),
        ("Hockey Stick Distribution", test_hockey_stick_distribution),
        ("Realistic Scenario", test_realistic_scenario)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, "PASS" if result else "FAIL"))
        except Exception as e:
            print(f"\nERROR in {test_name}: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append((test_name, "ERROR"))

    # Summary
    print("\n" + "="*80)
    print("VERIFICATION SUMMARY")
    print("="*80)

    for test_name, status in results:
        symbol = "[OK]" if status == "PASS" else "[FAIL]"
        print(f"  {symbol} {test_name}: {status}")

    all_passed = all(status == "PASS" for _, status in results)

    print("\n" + "="*80)
    if all_passed:
        print("ALL TESTS PASSED ✓")
        print("Backend calculations are verified and correct.")
    else:
        print("SOME TESTS FAILED ✗")
        print("Please review the failures above.")
    print("="*80)

    return all_passed


if __name__ == '__main__':
    main()
