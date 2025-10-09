#!/usr/bin/env python3
"""
NIWA QMRA Toolkit - Quick Start Example
========================================

This script demonstrates basic usage of the QMRA Toolkit with the provided test data.

Usage:
    python quick_start_example.py

Requirements:
    - Python 3.8+
    - numpy, pandas, matplotlib
    - QMRA toolkit modules in qmra_toolkit/src/
"""

import sys
import os
import numpy as np
import pandas as pd
import json
from pathlib import Path

# Add QMRA toolkit to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'qmra_toolkit', 'src'))

# Import QMRA modules
from pathogen_database import PathogenDatabase
from dose_response import create_dose_response_model
from monte_carlo import MonteCarloSimulator, create_lognormal_distribution, create_uniform_distribution
from risk_characterization import RiskCharacterization


def print_header(title):
    """Print formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def example1_basic_risk_calculation():
    """Example 1: Basic infection risk calculation."""
    print_header("Example 1: Basic Infection Risk Calculation")

    # Initialize pathogen database
    pathogen_db = PathogenDatabase()

    # Get norovirus parameters
    pathogen = 'norovirus'
    model_type = pathogen_db.get_default_model_type(pathogen)
    dr_params = pathogen_db.get_dose_response_parameters(pathogen, model_type)
    health_data = pathogen_db.get_health_impact_data(pathogen)

    print(f"\nPathogen: {pathogen_db.get_pathogen_info(pathogen)['name']}")
    print(f"Model: {model_type}")
    print(f"Parameters: alpha={dr_params['alpha']}, beta={dr_params['beta']}")

    # Create dose-response model
    dr_model = create_dose_response_model(model_type, dr_params)

    # Calculate risk at different doses
    doses = [1, 10, 100, 1000]
    print("\nInfection Probabilities:")
    print(f"{'Dose (organisms)':>20} | {'P(infection)':>15} | {'P(illness)':>15}")
    print("-" * 55)

    for dose in doses:
        p_infection = dr_model.calculate_infection_probability(dose)
        p_illness = p_infection * health_data['illness_to_infection_ratio']
        print(f"{dose:>20} | {p_infection:>15.6f} | {p_illness:>15.6f}")

    # Calculate dose for WHO guideline risk
    target_risk = 1e-4  # 1 in 10,000
    required_dose = dr_model.calculate_dose_for_risk(target_risk)
    print(f"\nDose for WHO guideline risk (1 in 10,000): {required_dose:.2f} organisms")


def example2_monte_carlo_uncertainty():
    """Example 2: Monte Carlo uncertainty analysis."""
    print_header("Example 2: Monte Carlo Uncertainty Analysis")

    # Initialize components
    pathogen_db = PathogenDatabase()
    pathogen = 'campylobacter'
    model_type = pathogen_db.get_default_model_type(pathogen)
    dr_params = pathogen_db.get_dose_response_parameters(pathogen, model_type)
    dr_model = create_dose_response_model(model_type, dr_params)

    print(f"\nPathogen: {pathogen_db.get_pathogen_info(pathogen)['name']}")
    print(f"Running Monte Carlo simulation with uncertainty...")

    # Create Monte Carlo simulator
    mc_sim = MonteCarloSimulator(random_seed=42)

    # Add uncertainty distributions
    mean_concentration = 50  # organisms/L
    conc_dist = create_lognormal_distribution(
        mean=np.log(mean_concentration),
        std=0.5,  # moderate uncertainty
        name="concentration"
    )
    mc_sim.add_distribution("concentration", conc_dist)

    mean_volume = 50  # mL
    vol_dist = create_uniform_distribution(
        min_val=25,   # 50% of mean
        max_val=75,   # 150% of mean
        name="volume"
    )
    mc_sim.add_distribution("volume", vol_dist)

    # Define QMRA model
    def qmra_model(samples):
        conc = samples["concentration"]
        vol = samples["volume"]
        dose = (conc * vol) / 1000.0  # Convert to organisms
        return dr_model.calculate_infection_probability(dose)

    # Run simulation
    iterations = 5000
    print(f"Iterations: {iterations}")
    results = mc_sim.run_simulation(
        qmra_model,
        n_iterations=iterations,
        variable_name="infection_probability"
    )

    # Display results
    print("\nResults:")
    print(f"  Mean:              {results.statistics['mean']:.6e}")
    print(f"  Median:            {results.statistics['median']:.6e}")
    print(f"  Std Dev:           {results.statistics['std']:.6e}")
    print(f"  5th percentile:    {results.percentiles['5%']:.6e}")
    print(f"  95th percentile:   {results.percentiles['95%']:.6e}")
    print(f"  95% CI width:      {results.percentiles['95%'] - results.percentiles['5%']:.6e}")


def example3_load_test_data():
    """Example 3: Load and analyze test data."""
    print_header("Example 3: Working with Test Data")

    # Check if test data exists
    data_file = 'test_data/pathogen_concentrations/wastewater_monitoring.csv'
    if not os.path.exists(data_file):
        print(f"\nTest data not found at: {data_file}")
        print("Please ensure test data files are in the test_data/ directory")
        return

    # Load wastewater monitoring data
    print(f"\nLoading: {data_file}")
    ww_data = pd.read_csv(data_file)

    print(f"Records loaded: {len(ww_data)}")
    print(f"\nDataset overview:")
    print(ww_data.head())

    # Calculate summary statistics
    print("\n\nPathogen Concentration Summary:")
    summary = ww_data.groupby('pathogen')['concentration_per_L'].agg(['count', 'mean', 'std', 'min', 'max'])
    print(summary)

    # Focus on norovirus
    norovirus_data = ww_data[ww_data['pathogen'] == 'norovirus']
    mean_conc = norovirus_data['concentration_per_L'].mean()
    std_conc = norovirus_data['concentration_per_L'].std()

    print(f"\n\nNorovirus Statistics:")
    print(f"  Mean concentration: {mean_conc:.1f} organisms/L")
    print(f"  Std deviation:      {std_conc:.1f} organisms/L")
    print(f"  Coefficient of variation: {(std_conc/mean_conc)*100:.1f}%")


def example4_load_scenario():
    """Example 4: Load and run scenario from JSON."""
    print_header("Example 4: Running Assessment from Scenario File")

    # Check if scenario file exists
    scenario_file = 'test_data/scenarios/recreational_swimming.json'
    if not os.path.exists(scenario_file):
        print(f"\nScenario file not found at: {scenario_file}")
        print("Please ensure scenario files are in the test_data/scenarios/ directory")
        return

    # Load scenario
    print(f"\nLoading scenario: {scenario_file}")
    with open(scenario_file, 'r') as f:
        scenario = json.load(f)

    print(f"\nScenario: {scenario['scenario_name']}")
    print(f"Description: {scenario['description']}")

    # Extract parameters
    pathogen = scenario['pathogen']
    exposure_route = scenario['exposure_route']
    concentration = scenario['exposure_parameters']['concentration_per_L']
    volume = scenario['exposure_parameters']['ingestion_volume_mL']
    frequency = scenario['exposure_parameters']['exposure_frequency_per_year']
    population = scenario['population']['total_population']

    print(f"\nParameters:")
    print(f"  Pathogen:       {pathogen}")
    print(f"  Exposure route: {exposure_route}")
    print(f"  Concentration:  {concentration} organisms/L")
    print(f"  Volume:         {volume} mL")
    print(f"  Frequency:      {frequency} events/year")
    print(f"  Population:     {population:,} people")

    # Run assessment
    print(f"\nRunning QMRA assessment...")
    risk_calc = RiskCharacterization()

    try:
        result = risk_calc.run_comprehensive_assessment(
            pathogen=pathogen,
            exposure_route=exposure_route,
            concentration=concentration,
            volume=volume,
            frequency=frequency,
            population=population,
            iterations=5000  # Reduced for faster demo
        )

        # Display results
        print(f"\nResults:")
        print(f"  Single exposure infection risk:")
        print(f"    Mean:   {result['infection_risk']['mean']:.6e}")
        print(f"    Median: {result['infection_risk']['median']:.6e}")
        print(f"    95% CI: [{result['infection_risk']['percentile_5']:.6e}, {result['infection_risk']['percentile_95']:.6e}]")

        print(f"\n  Annual infection risk:")
        print(f"    Mean:   {result['annual_risk']['mean']:.6e}")

        print(f"\n  Population impact:")
        cases = result['annual_risk']['mean'] * population
        print(f"    Expected cases/year: {cases:.0f}")

        # Regulatory compliance
        who_guideline = 1e-4
        compliant = result['annual_risk']['mean'] <= who_guideline
        print(f"\n  WHO Guideline Compliance:")
        print(f"    Target:    {who_guideline:.6e}")
        print(f"    Actual:    {result['annual_risk']['mean']:.6e}")
        print(f"    Status:    {'COMPLIANT' if compliant else 'NON-COMPLIANT'}")

    except Exception as e:
        print(f"\nError running assessment: {str(e)}")
        print("This may be because risk_characterization module is not available.")
        print("You can still use the basic functions shown in Examples 1-2.")


def example5_compare_pathogens():
    """Example 5: Compare multiple pathogens."""
    print_header("Example 5: Multi-Pathogen Comparison")

    pathogen_db = PathogenDatabase()
    available_pathogens = ['norovirus', 'campylobacter', 'cryptosporidium', 'e_coli']

    # Common scenario parameters
    concentration = 100  # organisms/L
    volume = 50  # mL
    dose = (concentration * volume) / 1000.0

    print(f"\nScenario: {dose} organisms ingested")
    print(f"(Concentration: {concentration} org/L, Volume: {volume} mL)")

    print(f"\n{'Pathogen':<20} | {'Model':<15} | {'P(infection)':<15} | {'P(illness)':<15}")
    print("-" * 70)

    for pathogen in available_pathogens:
        try:
            # Get parameters
            model_type = pathogen_db.get_default_model_type(pathogen)
            dr_params = pathogen_db.get_dose_response_parameters(pathogen, model_type)
            health_data = pathogen_db.get_health_impact_data(pathogen)

            # Create model and calculate risks
            dr_model = create_dose_response_model(model_type, dr_params)
            p_infection = dr_model.calculate_infection_probability(dose)
            p_illness = p_infection * health_data['illness_to_infection_ratio']

            # Get pathogen name
            info = pathogen_db.get_pathogen_info(pathogen)

            print(f"{info['name']:<20} | {model_type:<15} | {p_infection:<15.6e} | {p_illness:<15.6e}")

        except Exception as e:
            print(f"{pathogen:<20} | Error: {str(e)}")

    print("\nInterpretation:")
    print("  - Higher P(infection) means more infectious at the same dose")
    print("  - P(illness) accounts for asymptomatic infections")
    print("  - Different pathogens show vastly different infectivity")


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("  NIWA QMRA TOOLKIT - QUICK START EXAMPLES")
    print("=" * 70)
    print("\nThis script demonstrates basic usage of the QMRA Toolkit.")
    print("Each example shows a different aspect of the toolkit functionality.")

    try:
        # Run examples
        example1_basic_risk_calculation()
        example2_monte_carlo_uncertainty()
        example3_load_test_data()
        example4_load_scenario()
        example5_compare_pathogens()

        # Summary
        print_header("Summary")
        print("\n[SUCCESS] Quick start examples completed successfully!")
        print("\nNext steps:")
        print("  1. Review the examples above to understand basic usage")
        print("  2. Read QMRA_TOOLKIT_USER_GUIDE.md for comprehensive documentation")
        print("  3. Explore test_data/ directory for more example data")
        print("  4. Try the web app: streamlit run qmra_toolkit/web_app.py")
        print("  5. Try the GUI: python qmra_toolkit/src/enhanced_qmra_gui.py")
        print("\nFor questions or support:")
        print("  Email: reza.moghaddam@niwa.co.nz")

    except ImportError as e:
        print("\n" + "=" * 70)
        print("  ERROR: Missing Dependencies")
        print("=" * 70)
        print(f"\nImport error: {str(e)}")
        print("\nPlease ensure all required modules are installed:")
        print("  pip install numpy pandas matplotlib scipy python-docx PyYAML")
        print("\nAnd that you're running from the correct directory:")
        print("  cd 'C:\\Users\\moghaddamr\\OneDrive - NIWA\\Quantitative Microbial Risk Assessment'")
        print("  python quick_start_example.py")

    except Exception as e:
        print("\n" + "=" * 70)
        print("  ERROR")
        print("=" * 70)
        print(f"\nUnexpected error: {str(e)}")
        print("\nPlease check:")
        print("  1. You're in the correct directory")
        print("  2. All required modules are in qmra_toolkit/src/")
        print("  3. Test data files are in test_data/ (if using Example 3-4)")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
