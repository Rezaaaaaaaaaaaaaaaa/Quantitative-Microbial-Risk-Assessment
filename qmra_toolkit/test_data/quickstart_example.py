#!/usr/bin/env python3
"""
Quick Start Example - Using QMRA Toolkit with Test Data
========================================================

This script demonstrates how to use the QMRA toolkit with the generated test data.

It performs a complete risk assessment using:
- Pathogen concentration monitoring data
- Treatment scenario configuration
- Dilution modeling results
- Exposure scenario parameters

Author: NIWA Earth Sciences
Date: October 2025
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import yaml
import matplotlib.pyplot as plt
import seaborn as sns

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

# Import QMRA modules
from pathogen_database import PathogenDatabase
from dose_response import create_dose_response_model
from exposure_assessment import create_exposure_assessment, ExposureRoute
from dilution_model import DilutionModel, TreatmentBarrier, TreatmentType
from monte_carlo import MonteCarloSimulator
from risk_characterization import RiskCharacterization

# Set plotting style
sns.set_style("whitegrid")


def load_test_data():
    """Load all test data files."""

    print("Loading test data...")

    test_data_dir = Path(__file__).parent

    # Load pathogen concentration data
    pathogen_file = test_data_dir / 'pathogen_concentrations' / 'treated_effluent_pathogens_2024.csv'
    pathogen_data = pd.read_csv(pathogen_file)
    print(f"  Loaded {len(pathogen_data)} pathogen concentration measurements")

    # Load dilution data
    dilution_file = test_data_dir / 'dilution_data' / 'hydrodynamic_dilution_modeling_1000runs.csv'
    dilution_data = pd.read_csv(dilution_file)
    print(f"  Loaded {len(dilution_data)} dilution model results")

    # Load exposure scenario
    exposure_file = test_data_dir / 'exposure_scenarios' / 'swimming_scenario.yaml'
    with open(exposure_file, 'r') as f:
        exposure_scenario = yaml.safe_load(f)
    print(f"  Loaded exposure scenario: {exposure_scenario['scenario_name']}")

    # Load treatment configuration
    treatment_file = test_data_dir / 'treatment_scenarios' / 'secondary_treatment.yaml'
    with open(treatment_file, 'r') as f:
        treatment_config = yaml.safe_load(f)
    print(f"  Loaded treatment scenario: {treatment_config['scenario_name']}")

    return pathogen_data, dilution_data, exposure_scenario, treatment_config


def setup_treatment_model(treatment_config):
    """Set up treatment model from configuration."""

    print(f"\nSetting up treatment train...")

    model = DilutionModel()

    for barrier_config in treatment_config['treatment_barriers']:
        barrier = TreatmentBarrier(
            name=barrier_config['name'],
            treatment_type=TreatmentType(barrier_config['type']),
            log_reduction_value=barrier_config['lrv'],
            variability=barrier_config.get('variability'),
            description=barrier_config.get('description')
        )
        model.add_treatment_barrier(barrier)
        print(f"  Added: {barrier.name} (LRV: {barrier.log_reduction_value})")

    total_lrv = sum(b['lrv'] for b in treatment_config['treatment_barriers'])
    print(f"  Total Log Reduction: {total_lrv}")

    return model


def run_qmra_assessment(pathogen_data, dilution_data, exposure_scenario, treatment_config):
    """Run complete QMRA assessment with test data."""

    print("\n" + "="*80)
    print("RUNNING QMRA ASSESSMENT WITH TEST DATA")
    print("="*80)

    # 1. Calculate mean pathogen concentration from monitoring data
    pathogen = 'norovirus'
    concentration_col = 'Norovirus_copies_per_L'

    mean_conc = pathogen_data[concentration_col].mean()
    median_conc = pathogen_data[concentration_col].median()
    p95_conc = pathogen_data[concentration_col].quantile(0.95)

    print(f"\nPathogen: {pathogen.title()}")
    print(f"  Mean concentration: {mean_conc:.2e} copies/L")
    print(f"  Median concentration: {median_conc:.2e} copies/L")
    print(f"  95th percentile: {p95_conc:.2e} copies/L")

    # 2. Apply treatment
    treatment_model = setup_treatment_model(treatment_config)
    treated_conc = treatment_model.apply_treatment_train(
        initial_concentration=mean_conc,
        pathogen_name=pathogen,
        include_uncertainty=False  # Use mean values for this example
    )
    print(f"\nPost-treatment concentration: {treated_conc:.2e} copies/L")

    # 3. Get dilution factors for specific site
    target_site = 'Site_100m'
    site_dilutions = dilution_data[dilution_data['Site_Name'] == target_site]['Dilution_Factor'].values

    median_dilution = np.median(site_dilutions)
    print(f"\nDilution at {target_site}:")
    print(f"  Median dilution factor: {median_dilution:.1f}x")
    print(f"  Range: {site_dilutions.min():.1f}x to {site_dilutions.max():.1f}x")

    # Apply median dilution
    final_conc = treated_conc / median_dilution
    print(f"  Final concentration at exposure point: {final_conc:.2e} copies/L")

    # 4. Set up exposure assessment
    exposure_route = ExposureRoute(exposure_scenario['exposure_route'])

    # Get ingestion volume parameters
    ingestion_params = exposure_scenario['exposure_parameters']['water_ingestion_volume_mL']
    mean_ingestion = np.exp(ingestion_params['meanlog'])  # Convert from log scale

    exposure_params = {
        "water_ingestion_volume": mean_ingestion,
        "exposure_frequency": exposure_scenario['exposure_parameters']['events_per_year']['lambda']
    }

    print(f"\nExposure Parameters:")
    print(f"  Route: {exposure_scenario['exposure_route']}")
    print(f"  Water ingestion: {mean_ingestion:.1f} mL per event")
    print(f"  Events per year: {exposure_params['exposure_frequency']}")

    exposure_model = create_exposure_assessment(exposure_route, exposure_params)
    exposure_model.set_pathogen_concentration(final_conc)

    # 5. Run risk characterization
    print(f"\nRunning Monte Carlo simulation ({exposure_scenario['population']['size']} population)...")

    pathogen_db = PathogenDatabase()
    risk_calc = RiskCharacterization(pathogen_db)

    results = risk_calc.run_comprehensive_assessment(
        pathogen_name=pathogen,
        exposure_assessment=exposure_model,
        population_size=exposure_scenario['population']['size'],
        n_samples=5000
    )

    # 6. Display results
    print("\n" + "="*80)
    print("RISK ASSESSMENT RESULTS")
    print("="*80)

    for metric_name, result in results.items():
        print(f"\n{metric_name.replace('_', ' ').title()}:")
        print(f"  Mean: {result.statistics['mean']:.2e}")
        print(f"  Median: {result.statistics['median']:.2e}")
        print(f"  95th Percentile: {result.statistics['p95']:.2e}")

        if result.population_risks and exposure_scenario['population']['size']:
            expected_cases = result.population_risks['expected_cases_per_year']
            print(f"  Expected cases per year ({exposure_scenario['population']['size']} people): {expected_cases:.1f}")

    # 7. Check compliance
    annual_result = results['annual_risk']
    risk_threshold = exposure_scenario['risk_threshold']

    print(f"\nRegulatory Compliance:")
    print(f"  Risk threshold: {risk_threshold:.0e}")
    print(f"  Median annual risk: {annual_result.statistics['median']:.2e}")

    if annual_result.statistics['median'] <= risk_threshold:
        print(f"  Status: COMPLIANT")
    else:
        print(f"  Status: NON-COMPLIANT")
        exceedance = annual_result.statistics['median'] / risk_threshold
        print(f"  Exceedance factor: {exceedance:.1f}x")

    return results


def create_visualizations(pathogen_data, dilution_data):
    """Create visualization plots from test data."""

    print("\nCreating visualization plots...")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Pathogen concentration time series
    ax1 = axes[0, 0]
    ax1.plot(pathogen_data['Sample_Date'], pathogen_data['Norovirus_copies_per_L'],
             marker='o', linestyle='-', alpha=0.6, color='blue')
    ax1.set_yscale('log')
    ax1.set_xlabel('Sample Date')
    ax1.set_ylabel('Norovirus Concentration (copies/L)')
    ax1.set_title('Treated Effluent Norovirus Monitoring - 2024')
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)

    # 2. Pathogen concentration distribution
    ax2 = axes[0, 1]
    log_conc = np.log10(pathogen_data['Norovirus_copies_per_L'])
    ax2.hist(log_conc, bins=20, color='steelblue', edgecolor='black', alpha=0.7)
    ax2.set_xlabel('Log10(Norovirus Concentration)')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Norovirus Concentration Distribution')
    ax2.axvline(log_conc.mean(), color='red', linestyle='--', label=f'Mean: {log_conc.mean():.2f}')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. Dilution by site
    ax3 = axes[1, 0]
    sites = dilution_data['Site_Name'].unique()
    site_medians = [dilution_data[dilution_data['Site_Name'] == site]['Dilution_Factor'].median()
                    for site in sites]
    distances = [dilution_data[dilution_data['Site_Name'] == site]['Distance_m'].iloc[0]
                for site in sites]

    ax3.plot(distances, site_medians, marker='o', markersize=8, linewidth=2, color='green')
    ax3.set_xlabel('Distance from Discharge (m)')
    ax3.set_ylabel('Median Dilution Factor')
    ax3.set_title('Dilution vs Distance from Outfall')
    ax3.set_yscale('log')
    ax3.grid(True, alpha=0.3)

    # 4. Dilution distribution at 100m site
    ax4 = axes[1, 1]
    site_100m = dilution_data[dilution_data['Site_Name'] == 'Site_100m']['Dilution_Factor']
    log_dilution = np.log10(site_100m)
    ax4.hist(log_dilution, bins=30, color='coral', edgecolor='black', alpha=0.7)
    ax4.set_xlabel('Log10(Dilution Factor)')
    ax4.set_ylabel('Frequency')
    ax4.set_title('Dilution Distribution at Site 100m')
    ax4.axvline(log_dilution.median(), color='darkred', linestyle='--',
                label=f'Median: {10**log_dilution.median():.1f}x')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()

    output_file = Path(__file__).parent / 'test_data_visualizations.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"  Saved visualization: {output_file}")

    plt.close()


def main():
    """Main execution function."""

    print("\n" + "="*80)
    print("QMRA TOOLKIT - QUICK START EXAMPLE WITH TEST DATA")
    print("="*80 + "\n")

    # Load test data
    pathogen_data, dilution_data, exposure_scenario, treatment_config = load_test_data()

    # Run QMRA assessment
    results = run_qmra_assessment(pathogen_data, dilution_data, exposure_scenario, treatment_config)

    # Create visualizations
    create_visualizations(pathogen_data, dilution_data)

    print("\n" + "="*80)
    print("QUICK START EXAMPLE COMPLETE")
    print("="*80)
    print("\nThis example demonstrated:")
    print("  1. Loading pathogen concentration monitoring data")
    print("  2. Applying treatment train configuration")
    print("  3. Using hydrodynamic dilution modeling results")
    print("  4. Setting up exposure scenarios")
    print("  5. Running Monte Carlo risk assessment")
    print("  6. Evaluating regulatory compliance")
    print("  7. Creating visualization plots")
    print("\nFor more examples, see:")
    print("  - qmra_toolkit/examples/")
    print("  - test_data/README.md")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
