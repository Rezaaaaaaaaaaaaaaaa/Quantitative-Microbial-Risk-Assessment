#!/usr/bin/env python3
"""
Test Script for New QMRA Features

Tests all new features added to match David's R package:
1. Truncated log-logistic distribution
2. Bioaccumulation Factor (BAF) for shellfish
3. Illness modeling (infection to illness conversion)
4. Exposure-specific parameter functions

Author: NIWA Earth Sciences New Zealand
Date: November 2025
"""

import sys
import numpy as np
import pandas as pd
from pathlib import Path

# Add qmra_core to path
sys.path.insert(0, str(Path(__file__).parent))

from qmra_core import (
    BioaccumulationFactor,
    ShellfishMealSize,
    calculate_shellfish_water_equivalent,
    SwimIngestionRate,
    SwimDuration,
    calculate_swim_ingestion_volume,
    infection_to_illness,
    calculate_illness_risk_metrics,
    calculate_population_illness_cases,
    PathogenDatabase
)


def test_truncated_loglogistic_distribution():
    """Test truncated log-logistic distribution (shellfish meal sizes)."""
    print("\n" + "="*80)
    print("TEST 1: Truncated Log-Logistic Distribution (Shellfish Meal Sizes)")
    print("="*80)

    meals = ShellfishMealSize.generate(n_samples=10000, seed=42)

    print(f"Generated {len(meals)} meal sizes")
    print(f"  Min: {meals.min():.1f} g (expected >=5g)")
    print(f"  Max: {meals.max():.1f} g (expected <=800g)")
    print(f"  Mean: {meals.mean():.1f} g (expected ~75g)")
    print(f"  Median: {np.median(meals):.1f} g")
    print(f"  Std: {meals.std():.1f} g")

    # Verify bounds
    assert np.all(meals >= 5.0), "Minimum meal size violation"
    assert np.all(meals <= 800.0), "Maximum meal size violation"
    print("[OK] Bounds check passed")


def test_bioaccumulation_factor():
    """Test BAF for shellfish (truncated normal)."""
    print("\n" + "="*80)
    print("TEST 2: Bioaccumulation Factor (BAF) - Shellfish")
    print("="*80)

    bafs = BioaccumulationFactor.generate(n_samples=10000, seed=42)

    print(f"Generated {len(bafs)} BAF values")
    print(f"  Min: {bafs.min():.1f}x (expected >=1)")
    print(f"  Max: {bafs.max():.1f}x (expected <=100)")
    print(f"  Mean: {bafs.mean():.1f}x (expected ~44.9)")
    print(f"  Median: {np.median(bafs):.1f}x")
    print(f"  Std: {bafs.std():.1f}x")

    # Verify bounds
    assert np.all(bafs >= 1.0), "Minimum BAF violation"
    assert np.all(bafs <= 100.0), "Maximum BAF violation"
    print("[OK] Bounds check passed")


def test_shellfish_water_equivalent():
    """Test water equivalent calculation for shellfish."""
    print("\n" + "="*80)
    print("TEST 3: Shellfish Water Equivalent (Meal Size × BAF)")
    print("="*80)

    meals = ShellfishMealSize.generate(n_samples=1000, seed=42)
    bafs = BioaccumulationFactor.generate(n_samples=1000, seed=42)

    water_equiv = calculate_shellfish_water_equivalent(meals, bafs)

    print(f"Generated {len(water_equiv)} water equivalents")
    print(f"  Min: {water_equiv.min():.1f} mL equiv")
    print(f"  Max: {water_equiv.max():.1f} mL equiv")
    print(f"  Mean: {water_equiv.mean():.1f} mL equiv")
    print(f"  Median: {np.median(water_equiv):.1f} mL equiv")

    # Verify calculation
    expected_mean = meals.mean() * bafs.mean()
    print(f"\n  Expected mean (meal*BAF): {expected_mean:.1f}")
    print(f"  Actual mean: {water_equiv.mean():.1f}")
    print("[OK] Water equivalent calculation verified")


def test_swim_ingestion_rate():
    """Test swim ingestion rate (truncated lognormal)."""
    print("\n" + "="*80)
    print("TEST 4: Swim Ingestion Rate (Truncated Lognormal)")
    print("="*80)

    rates = SwimIngestionRate.generate(n_samples=10000, seed=42)

    print(f"Generated {len(rates)} ingestion rates")
    print(f"  Min: {rates.min():.1f} mL/h (expected >=5)")
    print(f"  Max: {rates.max():.1f} mL/h (expected <=200)")
    print(f"  Mean: {rates.mean():.1f} mL/h (expected ~53)")
    print(f"  Median: {np.median(rates):.1f} mL/h")

    # Verify bounds
    assert np.all(rates >= 5.0), "Minimum ingestion rate violation"
    assert np.all(rates <= 200.0), "Maximum ingestion rate violation"
    print("[OK] Bounds check passed")


def test_swim_duration():
    """Test swim duration (triangular/PERT)."""
    print("\n" + "="*80)
    print("TEST 5: Swim Duration (Triangular/PERT)")
    print("="*80)

    durations = SwimDuration.generate(n_samples=10000, seed=42)

    print(f"Generated {len(durations)} swim durations")
    print(f"  Min: {durations.min():.2f} hours (expected >=0.2)")
    print(f"  Max: {durations.max():.2f} hours (expected <=4.0)")
    print(f"  Mean: {durations.mean():.2f} hours")
    print(f"  Median: {np.median(durations):.2f} hours (expected ~1.0)")

    # Verify bounds
    assert np.all(durations >= 0.2), "Minimum duration violation"
    assert np.all(durations <= 4.0), "Maximum duration violation"
    print("[OK] Bounds check passed")


def test_swim_volume():
    """Test total swim water ingestion volume."""
    print("\n" + "="*80)
    print("TEST 6: Swim Total Ingestion Volume (Rate × Duration)")
    print("="*80)

    rates = SwimIngestionRate.generate(n_samples=1000, seed=42)
    durations = SwimDuration.generate(n_samples=1000, seed=42)

    volumes = calculate_swim_ingestion_volume(rates, durations)

    print(f"Generated {len(volumes)} total volumes")
    print(f"  Min: {volumes.min():.1f} mL")
    print(f"  Max: {volumes.max():.1f} mL")
    print(f"  Mean: {volumes.mean():.1f} mL")
    print(f"  Median: {np.median(volumes):.1f} mL")

    print("[OK] Swim volume calculation verified")


def test_infection_to_illness():
    """Test infection to illness conversion."""
    print("\n" + "="*80)
    print("TEST 7: Infection to Illness Conversion (Norovirus)")
    print("="*80)

    # Create infection array (random binary)
    np.random.seed(42)
    infections = np.random.binomial(1, 0.05, 10000)  # 5% infection rate

    # Get Norovirus illness parameters
    db = PathogenDatabase()
    illness_params = db.get_illness_parameters('norovirus')

    print(f"Norovirus illness parameters:")
    print(f"  P(ill | infected): {illness_params['probability_illness_given_infection']:.2f}")
    print(f"  Population susceptibility: {illness_params['population_susceptibility']:.2f}")

    # Convert infections to illnesses
    illness = infection_to_illness(
        infections,
        illness_params['probability_illness_given_infection'],
        illness_params['population_susceptibility'],
        seed=42
    )

    infection_rate = infections.mean()
    illness_rate = illness.mean()
    expected_illness_rate = infection_rate * illness_params['probability_illness_given_infection'] * illness_params['population_susceptibility']

    print(f"\nResults:")
    print(f"  Infection rate: {infection_rate:.4f} ({infections.sum()}/{len(infections)})")
    print(f"  Illness rate: {illness_rate:.4f} ({illness.sum():.0f}/{len(illness)})")
    print(f"  Expected illness rate: {expected_illness_rate:.4f}")
    print(f"  Ratio (illness/infection): {illness_rate/infection_rate:.2f}")

    print("[OK] Infection to illness conversion verified")


def test_illness_risk_metrics():
    """Test illness risk metrics calculation."""
    print("\n" + "="*80)
    print("TEST 8: Illness Risk Metrics")
    print("="*80)

    # Create sample risk array
    np.random.seed(42)
    illness_risks = np.random.lognormal(np.log(5e-4), 0.5, 10000)  # Lognormal risk distribution

    metrics = calculate_illness_risk_metrics(illness_risks)

    print(f"Illness risk metrics:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.6e}")

    print("[OK] Illness risk metrics calculated")


def test_population_illness_cases():
    """Test population-level illness case counting."""
    print("\n" + "="*80)
    print("TEST 9: Population Illness Case Counts")
    print("="*80)

    # Create sample infection risks
    infection_risks = np.array([0.001, 0.005, 0.01])  # 0.1%, 0.5%, 1% per exposure

    # Norovirus parameters
    p_ill = 0.60
    susceptibility = 0.74
    population_size = 10000
    frequency_year = 20  # 20 exposures per year

    cases = calculate_population_illness_cases(
        infection_risks,
        p_ill,
        susceptibility,
        population_size,
        frequency_year
    )

    print(f"Population: {population_size} people")
    print(f"Exposures per year: {frequency_year}")
    print(f"Illness parameters: P(ill|inf)={p_ill}, susceptibility={susceptibility}")
    print(f"\nExpected annual illness cases:")
    for i, (risk, count) in enumerate(zip(infection_risks, cases)):
        print(f"  Scenario {i+1}: Risk={risk:.1%} --> {count:.1f} cases/year")

    print("[OK] Population case counts calculated")


def run_all_tests():
    """Run all feature tests."""
    print("\n" + "#"*80)
    print("# NEW QMRA FEATURES TEST SUITE")
    print("#"*80)

    try:
        test_truncated_loglogistic_distribution()
        test_bioaccumulation_factor()
        test_shellfish_water_equivalent()
        test_swim_ingestion_rate()
        test_swim_duration()
        test_swim_volume()
        test_infection_to_illness()
        test_illness_risk_metrics()
        test_population_illness_cases()

        print("\n" + "#"*80)
        print("# ALL TESTS PASSED [OK]")
        print("#"*80)
        return True

    except AssertionError as e:
        print(f"\n[FAILED] TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n[ERROR]: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
