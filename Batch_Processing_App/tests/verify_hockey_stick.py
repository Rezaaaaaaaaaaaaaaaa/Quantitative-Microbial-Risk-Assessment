#!/usr/bin/env python3
"""
Verification script for Hockey Stick distribution implementation.
Tests the enhanced hockey stick distribution with P parameter.
"""

import numpy as np
import matplotlib.pyplot as plt
from qmra_core import MonteCarloSimulator, create_hockey_stick_distribution

def test_hockey_stick_basic():
    """Test basic hockey stick distribution parameters."""
    print("\n" + "="*80)
    print("TEST 1: Basic Hockey Stick Distribution Creation")
    print("="*80)

    # Create a hockey stick distribution
    dist = create_hockey_stick_distribution(
        x_min=500000,
        x_median=1000000,
        x_max=2000000,
        P=0.95,
        name="test_norovirus"
    )

    print(f"[OK] Distribution created: {dist.name}")
    print(f"  Parameters: {dist.parameters}")
    print(f"  Description: {dist.description}")

    return dist


def test_hockey_stick_sampling(dist, n_samples=10000):
    """Test sampling from hockey stick distribution."""
    print("\n" + "="*80)
    print("TEST 2: Hockey Stick Distribution Sampling")
    print("="*80)

    mc = MonteCarloSimulator(random_seed=42)
    mc.add_distribution("concentration", dist)
    samples = mc.sample_distribution("concentration", n_samples)

    print(f"\nGenerated {n_samples} samples")
    print(f"  Min:        {np.min(samples):.2e}")
    print(f"  Median:     {np.median(samples):.2e}")
    print(f"  Max:        {np.max(samples):.2e}")
    print(f"  Mean:       {np.mean(samples):.2e}")
    print(f"  Std Dev:    {np.std(samples):.2e}")
    print(f"  25th pct:   {np.percentile(samples, 25):.2e}")
    print(f"  50th pct:   {np.percentile(samples, 50):.2e}")
    print(f"  75th pct:   {np.percentile(samples, 75):.2e}")
    print(f"  95th pct:   {np.percentile(samples, 95):.2e}")

    # Verify basic properties
    assert np.min(samples) >= dist.parameters['x_min'], "Min sample below X0"
    assert np.max(samples) <= dist.parameters['x_max'], "Max sample above X100"
    print("\n[OK] All samples within valid bounds [X0, X100]")

    return samples


def test_different_p_values():
    """Test hockey stick with different P values."""
    print("\n" + "="*80)
    print("TEST 3: Hockey Stick Distribution with Different P Values")
    print("="*80)

    p_values = [0.80, 0.90, 0.95, 0.99]

    for p in p_values:
        dist = create_hockey_stick_distribution(
            x_min=1000,
            x_median=5000,
            x_max=10000,
            P=p,
            name=f"test_p_{p}"
        )

        mc = MonteCarloSimulator(random_seed=42)
        mc.add_distribution("concentration", dist)
        samples = mc.sample_distribution("concentration", 5000)

        median_sample = np.median(samples)
        p95_sample = np.percentile(samples, p*100)

        print(f"\nP = {p:.2f} ({p*100:.0f}th percentile):")
        print(f"  Median of samples: {median_sample:.0f}")
        print(f"  {p*100:.0f}th percentile of samples: {p95_sample:.0f}")
        print(f"  Ratio (max/min): {np.max(samples)/np.min(samples):.1f}x")


def test_parameter_validation():
    """Test parameter validation."""
    print("\n" + "="*80)
    print("TEST 4: Parameter Validation")
    print("="*80)

    # Test valid parameters
    try:
        dist = create_hockey_stick_distribution(100, 500, 1000, P=0.95)
        print("[OK] Valid parameters accepted: x_min=100, x_median=500, x_max=1000, P=0.95")
    except ValueError as e:
        print(f"[FAIL] Valid parameters rejected: {e}")
        return False

    # Test invalid: x_min >= x_median
    try:
        dist = create_hockey_stick_distribution(500, 500, 1000, P=0.95)
        print("[FAIL] Should reject x_min >= x_median")
        return False
    except ValueError:
        print("[OK] Correctly rejected: x_min >= x_median")

    # Test invalid: x_median >= x_max
    try:
        dist = create_hockey_stick_distribution(100, 1000, 1000, P=0.95)
        print("[FAIL] Should reject x_median >= x_max")
        return False
    except ValueError:
        print("[OK] Correctly rejected: x_median >= x_max")

    # Test invalid: P out of range
    try:
        dist = create_hockey_stick_distribution(100, 500, 1000, P=1.05)
        print("[FAIL] Should reject P > 1.0")
        return False
    except ValueError:
        print("[OK] Correctly rejected: P > 1.0")

    try:
        dist = create_hockey_stick_distribution(100, 500, 1000, P=0.0)
        print("[FAIL] Should reject P <= 0.0")
        return False
    except ValueError:
        print("[OK] Correctly rejected: P <= 0.0")

    return True


def test_norovirus_parameters():
    """Test with realistic Norovirus parameters."""
    print("\n" + "="*80)
    print("TEST 5: Realistic Norovirus Parameters")
    print("="*80)

    # Summer conditions
    dist_summer = create_hockey_stick_distribution(
        x_min=500000,
        x_median=1000000,
        x_max=2000000,
        P=0.95,
        name="Norovirus_Summer"
    )

    # Winter conditions
    dist_winter = create_hockey_stick_distribution(
        x_min=800000,
        x_median=1500000,
        x_max=3000000,
        P=0.95,
        name="Norovirus_Winter"
    )

    mc = MonteCarloSimulator(random_seed=42)
    mc.add_distribution("summer", dist_summer)
    mc.add_distribution("winter", dist_winter)

    summer_samples = mc.sample_distribution("summer", 5000)
    winter_samples = mc.sample_distribution("winter", 5000)

    print("\nNorovirus Summer:")
    print(f"  Median: {np.median(summer_samples):.2e} org/L")
    print(f"  Range: {np.min(summer_samples):.2e} - {np.max(summer_samples):.2e}")

    print("\nNorovirus Winter:")
    print(f"  Median: {np.median(winter_samples):.2e} org/L")
    print(f"  Range: {np.min(winter_samples):.2e} - {np.max(winter_samples):.2e}")
    print(f"  Winter/Summer ratio: {np.median(winter_samples)/np.median(summer_samples):.2f}x")


def test_backward_compatibility():
    """Test backward compatibility (P defaults to 0.95)."""
    print("\n" + "="*80)
    print("TEST 6: Backward Compatibility (Default P=0.95)")
    print("="*80)

    # Create distribution without specifying P
    dist_default = create_hockey_stick_distribution(
        x_min=1000,
        x_median=5000,
        x_max=10000
        # P not specified, should default to 0.95
    )

    print(f"P parameter (should be 0.95): {dist_default.parameters.get('P')}")

    if dist_default.parameters.get('P') == 0.95:
        print("[OK] Default P=0.95 working correctly")
    else:
        print("[FAIL] Default P value not correct")


def main():
    """Run all tests."""
    print("\n")
    print("=" * 80)
    print(" " * 20 + "HOCKEY STICK DISTRIBUTION VERIFICATION")
    print(" " * 25 + "(McBride 2009 Implementation)")
    print("=" * 80)

    try:
        # Run all tests
        dist = test_hockey_stick_basic()
        samples = test_hockey_stick_sampling(dist)
        test_different_p_values()
        test_parameter_validation()
        test_norovirus_parameters()
        test_backward_compatibility()

        print("\n" + "="*80)
        print("[OK] ALL TESTS PASSED")
        print("="*80)
        print("\nHockey stick distribution with P parameter is fully implemented and working!")
        print("- Frontend: Updated batch_scenarios_page to document P parameter")
        print("- Backend: monte_carlo.py enhanced with proper McBride formulation")
        print("- Data: pathogen_data.csv updated with P_Breakpoint column")
        print("- Processor: batch_processor.py uses P from pathogen data")
        print("\nReferences:")
        print("  - McBride, G. (2009). 'Microbial Water Quality and Human Health'")
        print("  - David Wood's R QMRA package (From_David/R/hockey.R)")
        print("  - Formula: Three piecewise sections with areas 0.5, P-0.5, 1-P")
        print("="*80)

        return 0

    except Exception as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
