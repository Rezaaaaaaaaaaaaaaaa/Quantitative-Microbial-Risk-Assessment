"""
Test script to verify web app QMRA integration works correctly.

This script tests:
1. Pathogen database loading for all 6 pathogens
2. Dose-response model creation
3. Monte Carlo simulation execution
4. Complete QMRA calculation pipeline
"""

import sys
import os

# Add qmra_toolkit/src to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'qmra_toolkit', 'src'))

import numpy as np
from pathogen_database import PathogenDatabase
from dose_response import create_dose_response_model
from monte_carlo import MonteCarloSimulator, create_lognormal_distribution, create_uniform_distribution


def test_pathogen_database():
    """Test that all 6 pathogens are in the database."""
    print("=" * 60)
    print("TEST 1: Pathogen Database Verification")
    print("=" * 60)

    pathogen_db = PathogenDatabase()
    required_pathogens = ['norovirus', 'campylobacter', 'cryptosporidium', 'e_coli', 'salmonella', 'rotavirus']

    for pathogen in required_pathogens:
        try:
            pathogen_info = pathogen_db.get_pathogen_info(pathogen)
            model_type = pathogen_db.get_default_model_type(pathogen)
            dr_params = pathogen_db.get_dose_response_parameters(pathogen, model_type)
            health_data = pathogen_db.get_health_impact_data(pathogen)

            print(f"\n[OK] {pathogen.upper()}")
            print(f"  Name: {pathogen_info['name']}")
            print(f"  Type: {pathogen_info['pathogen_type']}")
            print(f"  Default model: {model_type}")
            print(f"  Illness/Infection ratio: {health_data['illness_to_infection_ratio']}")
            print(f"  DALYs per case: {health_data['dalys_per_case']}")

        except Exception as e:
            print(f"\n[FAIL] {pathogen.upper()} - ERROR: {str(e)}")
            return False

    print("\n[OK] All pathogens successfully loaded from database!")
    return True


def test_dose_response_models():
    """Test dose-response model creation for all pathogens."""
    print("\n" + "=" * 60)
    print("TEST 2: Dose-Response Model Creation")
    print("=" * 60)

    pathogen_db = PathogenDatabase()
    required_pathogens = ['norovirus', 'campylobacter', 'cryptosporidium', 'e_coli', 'salmonella', 'rotavirus']

    test_dose = 100.0  # Test with 100 organisms

    for pathogen in required_pathogens:
        try:
            model_type = pathogen_db.get_default_model_type(pathogen)
            dr_params = pathogen_db.get_dose_response_parameters(pathogen, model_type)
            dr_model = create_dose_response_model(model_type, dr_params)

            # Calculate infection probability for test dose
            prob = dr_model.calculate_infection_probability(test_dose)

            print(f"\n[OK] {pathogen.upper()}")
            print(f"  Model: {model_type}")
            print(f"  P(infection) at dose=100: {prob:.6f}")

        except Exception as e:
            print(f"\n[FAIL] {pathogen.upper()} - ERROR: {str(e)}")
            return False

    print("\n[OK] All dose-response models working correctly!")
    return True


def test_monte_carlo_simulation():
    """Test Monte Carlo simulation with sample pathogen."""
    print("\n" + "=" * 60)
    print("TEST 3: Monte Carlo Simulation")
    print("=" * 60)

    try:
        # Use norovirus as test case
        pathogen_db = PathogenDatabase()
        model_type = pathogen_db.get_default_model_type('norovirus')
        dr_params = pathogen_db.get_dose_response_parameters('norovirus', model_type)
        dr_model = create_dose_response_model(model_type, dr_params)
        health_data = pathogen_db.get_health_impact_data('norovirus')

        # Initialize Monte Carlo simulator
        mc_simulator = MonteCarloSimulator(random_seed=42)

        # Test parameters
        concentration = 100.0  # organisms per L
        volume = 50.0  # mL
        iterations = 1000  # Reduced for faster testing

        # Add distributions
        concentration_dist = create_lognormal_distribution(
            mean=np.log(concentration),
            std=0.5,
            name="pathogen_concentration"
        )
        mc_simulator.add_distribution("pathogen_concentration", concentration_dist)

        volume_dist = create_uniform_distribution(
            min_val=volume * 0.5,
            max_val=volume * 1.5,
            name="ingestion_volume"
        )
        mc_simulator.add_distribution("ingestion_volume", volume_dist)

        # Define QMRA model
        def qmra_model(samples):
            conc_samples = samples["pathogen_concentration"]
            vol_samples = samples["ingestion_volume"]
            dose_samples = (conc_samples * vol_samples) / 1000.0
            pinf_samples = dr_model.calculate_infection_probability(dose_samples)
            return pinf_samples

        # Run simulation
        print(f"\nRunning {iterations} Monte Carlo iterations...")
        infection_results = mc_simulator.run_simulation(
            qmra_model,
            n_iterations=iterations,
            variable_name="infection_probability"
        )

        # Calculate statistics
        pinf_samples = infection_results.samples
        pill_samples = pinf_samples * health_data["illness_to_infection_ratio"]

        print(f"\n[OK] NOROVIRUS Monte Carlo Results:")
        print(f"  Iterations: {iterations}")
        print(f"  Mean P(infection): {np.mean(pinf_samples):.6e}")
        print(f"  Mean P(illness): {np.mean(pill_samples):.6e}")
        print(f"  Median P(infection): {np.median(pinf_samples):.6e}")
        print(f"  95th percentile: {np.percentile(pinf_samples, 95):.6e}")

        print("\n[OK] Monte Carlo simulation working correctly!")
        return True

    except Exception as e:
        print(f"\n[FAIL] Monte Carlo simulation - ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_full_qmra_pipeline():
    """Test complete QMRA calculation for multiple pathogens."""
    print("\n" + "=" * 60)
    print("TEST 4: Full QMRA Pipeline")
    print("=" * 60)

    test_pathogens = ['norovirus', 'campylobacter', 'e_coli']

    for pathogen in test_pathogens:
        try:
            print(f"\n--- Testing {pathogen.upper()} ---")

            # Initialize components
            pathogen_db = PathogenDatabase()
            model_type = pathogen_db.get_default_model_type(pathogen)
            dr_params = pathogen_db.get_dose_response_parameters(pathogen, model_type)
            dr_model = create_dose_response_model(model_type, dr_params)
            health_data = pathogen_db.get_health_impact_data(pathogen)

            mc_simulator = MonteCarloSimulator(random_seed=42)

            # Scenario parameters
            concentration = 100.0
            volume = 50.0
            frequency = 7
            population = 50000

            # Add distributions
            conc_dist = create_lognormal_distribution(np.log(concentration), 0.5, "pathogen_concentration")
            vol_dist = create_uniform_distribution(volume * 0.5, volume * 1.5, "ingestion_volume")
            mc_simulator.add_distribution("pathogen_concentration", conc_dist)
            mc_simulator.add_distribution("ingestion_volume", vol_dist)

            # Define and run model
            def qmra_model(samples):
                conc = samples["pathogen_concentration"]
                vol = samples["ingestion_volume"]
                dose = (conc * vol) / 1000.0
                return dr_model.calculate_infection_probability(dose)

            results = mc_simulator.run_simulation(qmra_model, n_iterations=500, variable_name="infection_probability")

            # Calculate risks
            pinf = np.mean(results.samples)
            pill = pinf * health_data["illness_to_infection_ratio"]
            annual_risk = 1 - np.power(1 - pinf, frequency)
            population_impact = annual_risk * population

            print(f"  P(infection): {pinf:.6e}")
            print(f"  P(illness): {pill:.6e}")
            print(f"  Annual risk: {annual_risk:.6e}")
            print(f"  Population impact: {population_impact:.1f} cases/year")
            print(f"  [OK] Success")

        except Exception as e:
            print(f"  [FAIL] ERROR: {str(e)}")
            return False

    print("\n[OK] Full QMRA pipeline working correctly!")
    return True


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("QMRA WEB APP INTEGRATION TEST SUITE")
    print("=" * 60)
    print("\nTesting proper QMRA toolkit integration...")

    all_passed = True

    # Run tests
    all_passed &= test_pathogen_database()
    all_passed &= test_dose_response_models()
    all_passed &= test_monte_carlo_simulation()
    all_passed &= test_full_qmra_pipeline()

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    if all_passed:
        print("\n*** ALL TESTS PASSED ***")
        print("\nThe web app QMRA integration is working correctly!")
        print("All 6 pathogens are properly configured in the database.")
        print("Dose-response models, Monte Carlo simulation, and full QMRA pipeline are functional.")
        return 0
    else:
        print("\n*** SOME TESTS FAILED ***")
        print("\nPlease review the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
