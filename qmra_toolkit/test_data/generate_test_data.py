#!/usr/bin/env python3
"""
Generate Comprehensive Test Data for QMRA Toolkit
===================================================

This script creates realistic dummy data files for testing the QMRA toolkit:
- Pathogen concentration data (raw and treated wastewater)
- Dilution/hydrodynamic data from modeling
- Exposure scenario configurations
- Treatment train configurations
- Monte Carlo parameter files
- MetOcean integration data

Author: NIWA Earth Sciences
Date: October 2025
"""

import numpy as np
import pandas as pd
import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta


def create_pathogen_concentration_data():
    """Generate realistic pathogen concentration monitoring data."""

    print("Creating pathogen concentration data...")

    # Set random seed for reproducibility
    np.random.seed(42)

    # Generate 52 weeks of weekly sampling data
    dates = pd.date_range(start='2024-01-01', periods=52, freq='W')

    # Norovirus concentrations (log-normal distribution)
    # Raw wastewater: mean ~1e6, treated: ~1e3
    norovirus_raw = np.random.lognormal(mean=13.8, sigma=1.5, size=52)  # ~1e6
    norovirus_treated = np.random.lognormal(mean=6.9, sigma=1.2, size=52)  # ~1e3

    # E. coli concentrations
    ecoli_raw = np.random.lognormal(mean=11.5, sigma=1.3, size=52)  # ~1e5
    ecoli_treated = np.random.lognormal(mean=4.6, sigma=1.0, size=52)  # ~1e2

    # Cryptosporidium concentrations (lower than bacteria/viruses)
    crypto_raw = np.random.lognormal(mean=6.9, sigma=1.2, size=52)  # ~1e3
    crypto_treated = np.random.lognormal(mean=2.3, sigma=0.8, size=52)  # ~10

    # Enterococcus concentrations (indicator organism)
    entero_raw = np.random.lognormal(mean=12.2, sigma=1.4, size=52)  # ~2e5
    entero_treated = np.random.lognormal(mean=5.3, sigma=1.1, size=52)  # ~2e2

    # Create raw wastewater dataset
    raw_data = pd.DataFrame({
        'Sample_Date': dates,
        'Sample_Type': 'Raw_Influent',
        'Norovirus_copies_per_L': norovirus_raw,
        'E_coli_MPN_per_100mL': ecoli_raw,
        'Cryptosporidium_oocysts_per_L': crypto_raw,
        'Enterococcus_MPN_per_100mL': entero_raw,
        'Sample_Volume_L': np.random.uniform(0.5, 2.0, size=52),
        'Detection_Limit': 10,
        'Laboratory': 'NIWA Christchurch',
        'QC_Flag': np.random.choice(['Pass', 'Pass', 'Pass', 'Warning'], size=52, p=[0.85, 0.1, 0.04, 0.01])
    })

    # Create treated wastewater dataset
    treated_data = pd.DataFrame({
        'Sample_Date': dates,
        'Sample_Type': 'Treated_Effluent',
        'Norovirus_copies_per_L': norovirus_treated,
        'E_coli_MPN_per_100mL': ecoli_treated,
        'Cryptosporidium_oocysts_per_L': crypto_treated,
        'Enterococcus_MPN_per_100mL': entero_treated,
        'Sample_Volume_L': np.random.uniform(1.0, 5.0, size=52),
        'Detection_Limit': 10,
        'Laboratory': 'NIWA Christchurch',
        'QC_Flag': np.random.choice(['Pass', 'Pass', 'Pass', 'Warning'], size=52, p=[0.85, 0.1, 0.04, 0.01])
    })

    # Combine datasets
    all_data = pd.concat([raw_data, treated_data], ignore_index=True)

    # Save to CSV
    output_dir = Path('pathogen_concentrations')
    all_data.to_csv(output_dir / 'wastewater_pathogen_monitoring_2024.csv', index=False)
    raw_data.to_csv(output_dir / 'raw_influent_pathogens_2024.csv', index=False)
    treated_data.to_csv(output_dir / 'treated_effluent_pathogens_2024.csv', index=False)

    print(f"  Created {len(all_data)} pathogen concentration records")
    return all_data


def create_dilution_data():
    """Generate hydrodynamic dilution data from modeling."""

    print("Creating dilution/hydrodynamic data...")

    np.random.seed(43)

    # Create dilution factors for multiple monitoring sites
    # Sites are at increasing distances from discharge point
    sites = ['Discharge', 'Site_50m', 'Site_100m', 'Site_250m', 'Site_500m', 'Site_1000m']

    # Number of model runs (e.g., different tidal/wind conditions)
    n_simulations = 1000

    dilution_data = []

    for site_idx, site in enumerate(sites):
        if site == 'Discharge':
            # No dilution at discharge point
            dilutions = np.ones(n_simulations)
        else:
            # Log-normal dilution factors (higher dilution with distance)
            # Mean dilution increases with distance
            mean_log_dilution = 1.0 + site_idx * 0.8  # 10x to 10000x range
            sd_log_dilution = 0.5 + site_idx * 0.1
            dilutions = np.random.lognormal(mean=mean_log_dilution, sigma=sd_log_dilution, size=n_simulations)

        for sim_idx, dilution in enumerate(dilutions):
            dilution_data.append({
                'Simulation_ID': sim_idx + 1,
                'Site_Name': site,
                'Distance_m': int(site.split('_')[-1].replace('m', '')) if '_' in site else 0,
                'Dilution_Factor': dilution,
                'Tidal_State': np.random.choice(['High', 'Mid', 'Low']),
                'Wind_Speed_ms': np.random.uniform(0, 15),
                'Current_Speed_ms': np.random.uniform(0.1, 1.5),
                'Model_Type': 'ROMS_Hydrodynamic',
                'Confidence': np.random.choice(['High', 'Medium'], p=[0.8, 0.2])
            })

    dilution_df = pd.DataFrame(dilution_data)

    # Save full dataset
    output_dir = Path('dilution_data')
    dilution_df.to_csv(output_dir / 'hydrodynamic_dilution_modeling_1000runs.csv', index=False)

    # Create summary statistics by site
    summary = dilution_df.groupby('Site_Name').agg({
        'Dilution_Factor': ['mean', 'median', 'std', 'min', 'max'],
        'Distance_m': 'first'
    }).round(2)
    summary.to_csv(output_dir / 'dilution_summary_by_site.csv')

    print(f"  Created {len(dilution_df)} dilution model results across {len(sites)} sites")
    return dilution_df


def create_exposure_scenarios():
    """Generate exposure scenario configuration files."""

    print("Creating exposure scenario configurations...")

    output_dir = Path('exposure_scenarios')

    # Scenario 1: Recreational swimming
    swimming_scenario = {
        'scenario_name': 'Recreational Swimming - Summer Season',
        'exposure_route': 'primary_contact',
        'description': 'Swimming at beach near wastewater outfall during summer',
        'population': {
            'size': 10000,
            'age_distribution': {
                'children_0_5': 0.10,
                'children_6_12': 0.15,
                'adults_13_64': 0.65,
                'elderly_65plus': 0.10
            }
        },
        'exposure_parameters': {
            'water_ingestion_volume_mL': {
                'distribution': 'lognormal',
                'meanlog': 3.5,  # ~50 mL
                'sdlog': 0.5,
                'source': 'Dufour et al. (2006)'
            },
            'exposure_duration_minutes': 60,
            'events_per_year': {
                'distribution': 'poisson',
                'lambda': 20,
                'description': 'Swimming events per summer season'
            },
            'season': 'November to March',
            'peak_usage_days': 90
        },
        'pathogen': 'norovirus',
        'site_locations': ['Site_100m', 'Site_250m', 'Site_500m'],
        'risk_threshold': 1e-3,  # 1 in 1000 per exposure (recreational water guideline)
        'assessment_year': 2024
    }

    with open(output_dir / 'swimming_scenario.yaml', 'w') as f:
        yaml.dump(swimming_scenario, f, default_flow_style=False, sort_keys=False)

    # Scenario 2: Shellfish consumption
    shellfish_scenario = {
        'scenario_name': 'Shellfish Harvesting and Consumption',
        'exposure_route': 'shellfish_consumption',
        'description': 'Consumption of recreationally harvested shellfish',
        'population': {
            'size': 5000,
            'description': 'Recreational shellfish harvesters'
        },
        'exposure_parameters': {
            'shellfish_consumption_grams': {
                'distribution': 'normal',
                'mean': 150,
                'sd': 50,
                'source': 'NZFSA consumption survey'
            },
            'consumption_frequency_per_year': {
                'distribution': 'poisson',
                'lambda': 12,
                'description': 'Monthly consumption average'
            },
            'bioaccumulation_factor': {
                'distribution': 'uniform',
                'min': 10,
                'max': 100,
                'description': 'Virus concentration in shellfish vs water'
            },
            'cooking_reduction': {
                'raw_shellfish_proportion': 0.3,
                'cooked_log_reduction': 2.0
            }
        },
        'pathogen': 'norovirus',
        'harvest_locations': ['Site_250m', 'Site_500m'],
        'risk_threshold': 1e-4,
        'closure_threshold': 1e-3
    }

    with open(output_dir / 'shellfish_scenario.yaml', 'w') as f:
        yaml.dump(shellfish_scenario, f, default_flow_style=False, sort_keys=False)

    # Scenario 3: Drinking water (post-treatment)
    drinking_water_scenario = {
        'scenario_name': 'Drinking Water from Treated Source',
        'exposure_route': 'drinking_water',
        'description': 'Drinking water supply with advanced treatment',
        'population': {
            'size': 50000,
            'description': 'Town water supply consumers'
        },
        'exposure_parameters': {
            'daily_consumption_L': {
                'distribution': 'lognormal',
                'meanlog': 0.7,  # ~2L per day
                'sdlog': 0.3,
                'source': 'WHO water consumption guidelines'
            },
            'consumption_days_per_year': 365,
            'vulnerable_populations': {
                'immunocompromised': 0.05,
                'elderly': 0.15,
                'children_under_5': 0.08
            }
        },
        'pathogen': 'cryptosporidium',
        'treatment_train': 'full_advanced_treatment',
        'risk_threshold': 1e-6,  # 1 in 1 million per year (drinking water standard)
        'daly_target': 1e-6
    }

    with open(output_dir / 'drinking_water_scenario.yaml', 'w') as f:
        yaml.dump(drinking_water_scenario, f, default_flow_style=False, sort_keys=False)

    # Scenario 4: Multi-pathogen comparison
    multi_pathogen_scenario = {
        'scenario_name': 'Multi-Pathogen Risk Comparison',
        'exposure_route': 'primary_contact',
        'description': 'Compare risks from multiple pathogens at same exposure',
        'pathogens': ['norovirus', 'cryptosporidium', 'campylobacter', 'e_coli'],
        'exposure_parameters': {
            'water_ingestion_volume_mL': 50,
            'events_per_year': 20
        },
        'population': 10000,
        'sites': ['Site_100m'],
        'analysis_type': 'comparative'
    }

    with open(output_dir / 'multi_pathogen_comparison.yaml', 'w') as f:
        yaml.dump(multi_pathogen_scenario, f, default_flow_style=False, sort_keys=False)

    print(f"  Created 4 exposure scenario configuration files")


def create_treatment_scenarios():
    """Generate treatment train configuration files."""

    print("Creating treatment scenario configurations...")

    output_dir = Path('treatment_scenarios')

    # Scenario 1: No treatment (bypass during storm)
    bypass_scenario = {
        'scenario_name': 'Emergency Bypass - No Treatment',
        'description': 'Storm overflow with no treatment',
        'treatment_barriers': [],
        'total_log_reduction': 0,
        'frequency_per_year': 5,
        'duration_hours': 6,
        'trigger_condition': 'Rainfall > 50mm in 24 hours'
    }

    with open(output_dir / 'bypass_no_treatment.yaml', 'w') as f:
        yaml.dump(bypass_scenario, f, default_flow_style=False, sort_keys=False)

    # Scenario 2: Primary treatment only
    primary_scenario = {
        'scenario_name': 'Primary Treatment Only',
        'description': 'Screening and primary settling',
        'treatment_barriers': [
            {
                'name': 'Screening',
                'type': 'physical',
                'lrv': 0.2,
                'variability': 0.1,
                'description': 'Coarse and fine screens'
            },
            {
                'name': 'Primary Settling',
                'type': 'physical',
                'lrv': 0.8,
                'variability': 0.3,
                'description': 'Gravity settling tank',
                'retention_time_hours': 2.5
            }
        ],
        'total_log_reduction': 1.0,
        'pathogen_specific_lrv': {
            'cryptosporidium': 1.2,  # Better settling for protozoa
            'norovirus': 0.5,        # Poor removal for viruses
            'bacteria': 1.0
        }
    }

    with open(output_dir / 'primary_treatment.yaml', 'w') as f:
        yaml.dump(primary_scenario, f, default_flow_style=False, sort_keys=False)

    # Scenario 3: Secondary (biological) treatment
    secondary_scenario = {
        'scenario_name': 'Secondary Biological Treatment',
        'description': 'Activated sludge with secondary clarification',
        'treatment_barriers': [
            {
                'name': 'Screening',
                'type': 'physical',
                'lrv': 0.2,
                'variability': 0.1
            },
            {
                'name': 'Primary Settling',
                'type': 'physical',
                'lrv': 0.8,
                'variability': 0.3
            },
            {
                'name': 'Activated Sludge',
                'type': 'biological',
                'lrv': 1.5,
                'variability': 0.5,
                'description': 'Aerobic biological treatment',
                'srt_days': 10,
                'hrt_hours': 8
            },
            {
                'name': 'Secondary Clarifier',
                'type': 'physical',
                'lrv': 0.5,
                'variability': 0.2
            }
        ],
        'total_log_reduction': 3.0,
        'pathogen_specific_lrv': {
            'cryptosporidium': 2.5,
            'norovirus': 2.0,
            'bacteria': 3.5
        }
    }

    with open(output_dir / 'secondary_treatment.yaml', 'w') as f:
        yaml.dump(secondary_scenario, f, default_flow_style=False, sort_keys=False)

    # Scenario 4: Advanced treatment with UV disinfection
    advanced_scenario = {
        'scenario_name': 'Advanced Treatment with UV Disinfection',
        'description': 'Full treatment train with tertiary filtration and UV',
        'treatment_barriers': [
            {
                'name': 'Screening',
                'type': 'physical',
                'lrv': 0.2,
                'variability': 0.1
            },
            {
                'name': 'Primary Settling',
                'type': 'physical',
                'lrv': 0.8,
                'variability': 0.3
            },
            {
                'name': 'Activated Sludge',
                'type': 'biological',
                'lrv': 1.5,
                'variability': 0.5,
                'srt_days': 15
            },
            {
                'name': 'Secondary Clarifier',
                'type': 'physical',
                'lrv': 0.5,
                'variability': 0.2
            },
            {
                'name': 'Sand Filtration',
                'type': 'physical',
                'lrv': 1.0,
                'variability': 0.3,
                'description': 'Rapid sand filtration',
                'filter_rate_m_per_hr': 5
            },
            {
                'name': 'UV Disinfection',
                'type': 'uv_disinfection',
                'lrv': 4.0,
                'variability': 0.5,
                'description': 'Medium pressure UV',
                'dose_mJ_cm2': 40,
                'validation_protocol': 'NWRI/AwwaRF 2012'
            }
        ],
        'total_log_reduction': 8.0,
        'pathogen_specific_lrv': {
            'cryptosporidium': 7.5,  # UV very effective
            'norovirus': 5.5,        # Moderate UV resistance
            'bacteria': 9.0          # Very susceptible to UV
        },
        'compliance_monitoring': {
            'uv_intensity_monitoring': 'continuous',
            'uv_dose_verification': 'online',
            'turbidity_limit_NTU': 2
        }
    }

    with open(output_dir / 'advanced_uv_treatment.yaml', 'w') as f:
        yaml.dump(advanced_scenario, f, default_flow_style=False, sort_keys=False)

    # Scenario 5: Chlorination alternative
    chlorination_scenario = {
        'scenario_name': 'Secondary Treatment with Chlorination',
        'description': 'Activated sludge with chlorine disinfection',
        'treatment_barriers': [
            {
                'name': 'Screening',
                'type': 'physical',
                'lrv': 0.2,
                'variability': 0.1
            },
            {
                'name': 'Primary Settling',
                'type': 'physical',
                'lrv': 0.8,
                'variability': 0.3
            },
            {
                'name': 'Activated Sludge',
                'type': 'biological',
                'lrv': 1.5,
                'variability': 0.5
            },
            {
                'name': 'Chlorination',
                'type': 'chlorination',
                'lrv': 2.5,
                'variability': 0.6,
                'description': 'Sodium hypochlorite disinfection',
                'contact_time_minutes': 30,
                'ct_value': 450,  # mg-min/L
                'target_residual_mg_L': 5.0
            },
            {
                'name': 'Dechlorination',
                'type': 'chemical',
                'lrv': 0,
                'description': 'Sodium bisulfite for residual removal'
            }
        ],
        'total_log_reduction': 5.0,
        'pathogen_specific_lrv': {
            'cryptosporidium': 1.0,  # Chlorine-resistant
            'norovirus': 3.5,
            'bacteria': 6.0
        },
        'dbp_formation': {
            'monitor': True,
            'thm_limit_ug_L': 100
        }
    }

    with open(output_dir / 'chlorination_treatment.yaml', 'w') as f:
        yaml.dump(chlorination_scenario, f, default_flow_style=False, sort_keys=False)

    print(f"  Created 5 treatment scenario configuration files")


def create_metocean_data():
    """Generate MetOcean integration test data."""

    print("Creating MetOcean dilution data...")

    np.random.seed(44)

    output_dir = Path('metocean_data')

    # Simulate MetOcean dilution CSV format
    # (Based on actual MetOcean output structure)

    sites = ['Beach_North', 'Beach_South', 'Offshore_1km', 'Nearshore_200m']
    n_timesteps = 8760  # Hourly for one year

    timestamps = pd.date_range(start='2024-01-01', periods=n_timesteps, freq='H')

    metocean_data = []

    for timestep_idx, timestamp in enumerate(timestamps[:100]):  # First 100 for demo
        # Environmental conditions
        wind_speed = np.random.uniform(0, 20)
        wave_height = np.random.uniform(0.5, 4.0)
        current_speed = np.random.uniform(0.1, 1.5)
        tide_level = 2.0 + 1.5 * np.sin(2 * np.pi * timestep_idx / 12.42)  # Semi-diurnal tide

        for site in sites:
            # Distance-dependent dilution
            if 'Offshore' in site:
                base_dilution = np.random.lognormal(mean=5.0, sigma=0.8)  # ~150x
            elif 'Nearshore' in site:
                base_dilution = np.random.lognormal(mean=3.0, sigma=0.6)  # ~20x
            else:
                base_dilution = np.random.lognormal(mean=2.0, sigma=0.5)  # ~7x

            # Wind/current effects
            dilution_factor = base_dilution * (1 + 0.1 * wind_speed / 10)

            metocean_data.append({
                'Timestamp': timestamp,
                'Site': site,
                'Dilution_Factor': dilution_factor,
                'Wind_Speed_ms': wind_speed,
                'Wind_Direction_deg': np.random.uniform(0, 360),
                'Wave_Height_m': wave_height,
                'Current_Speed_ms': current_speed,
                'Current_Direction_deg': np.random.uniform(0, 360),
                'Tide_Level_m': tide_level,
                'Water_Temp_C': 12 + 6 * np.sin(2 * np.pi * (timestep_idx / 8760)),  # Seasonal
                'Model_Run_ID': 'MetOcean_2024_Baseline'
            })

    metocean_df = pd.DataFrame(metocean_data)
    metocean_df.to_csv(output_dir / 'metocean_dilution_hourly_2024_sample.csv', index=False)

    # Create summary statistics
    summary = metocean_df.groupby('Site')['Dilution_Factor'].describe()
    summary.to_csv(output_dir / 'metocean_dilution_summary.csv')

    print(f"  Created MetOcean dilution data ({len(metocean_df)} records)")
    return metocean_df


def create_monte_carlo_params():
    """Generate Monte Carlo parameter configuration files."""

    print("Creating Monte Carlo parameter files...")

    output_dir = Path('monte_carlo_params')

    # Basic Monte Carlo settings
    basic_mc_config = {
        'simulation_name': 'Basic Monte Carlo Simulation',
        'n_iterations': 10000,
        'random_seed': 42,
        'parallel_processing': True,
        'n_cores': 4,
        'convergence_criteria': {
            'check_convergence': True,
            'tolerance': 0.01,
            'check_interval': 1000
        },
        'output_options': {
            'save_all_iterations': False,
            'save_percentiles': [5, 25, 50, 75, 95],
            'export_format': 'csv',
            'create_plots': True
        }
    }

    with open(output_dir / 'basic_monte_carlo_config.yaml', 'w') as f:
        yaml.dump(basic_mc_config, f, default_flow_style=False, sort_keys=False)

    # Advanced Monte Carlo with Latin Hypercube Sampling
    advanced_mc_config = {
        'simulation_name': 'Advanced Monte Carlo with LHS',
        'n_iterations': 50000,
        'sampling_method': 'latin_hypercube',
        'random_seed': 123,
        'parallel_processing': True,
        'n_cores': 8,
        'sensitivity_analysis': {
            'enabled': True,
            'method': 'sobol',
            'n_resample': 1000
        },
        'uncertainty_parameters': {
            'pathogen_concentration': {
                'distribution': 'lognormal',
                'parameters': {'meanlog': 6.9, 'sdlog': 1.2},
                'description': 'Treated effluent norovirus concentration'
            },
            'dilution_factor': {
                'distribution': 'lognormal',
                'parameters': {'meanlog': 2.3, 'sdlog': 0.7},
                'description': 'Near-field dilution'
            },
            'ingestion_volume': {
                'distribution': 'lognormal',
                'parameters': {'meanlog': 3.5, 'sdlog': 0.5},
                'description': 'Water ingestion during swimming (mL)'
            },
            'exposure_frequency': {
                'distribution': 'poisson',
                'parameters': {'lambda': 20},
                'description': 'Swimming events per year'
            }
        },
        'output_options': {
            'save_all_iterations': True,
            'save_percentiles': [1, 5, 10, 25, 50, 75, 90, 95, 99],
            'export_format': 'hdf5',
            'create_plots': True,
            'plot_types': ['histogram', 'cdf', 'tornado', 'scatter']
        }
    }

    with open(output_dir / 'advanced_monte_carlo_lhs.yaml', 'w') as f:
        yaml.dump(advanced_mc_config, f, default_flow_style=False, sort_keys=False)

    # Probabilistic treatment performance
    treatment_uncertainty_config = {
        'simulation_name': 'Treatment Performance Uncertainty Analysis',
        'description': 'Probabilistic assessment of treatment train LRV variability',
        'n_iterations': 20000,
        'treatment_barriers': {
            'primary_settling': {
                'lrv_distribution': 'uniform',
                'parameters': {'min': 0.5, 'max': 1.0},
                'failure_probability': 0.001
            },
            'activated_sludge': {
                'lrv_distribution': 'normal',
                'parameters': {'mean': 2.0, 'sd': 0.5},
                'min_lrv': 1.0,
                'max_lrv': 3.5,
                'failure_probability': 0.005
            },
            'uv_disinfection': {
                'lrv_distribution': 'normal',
                'parameters': {'mean': 4.0, 'sd': 0.6},
                'min_lrv': 2.0,
                'max_lrv': 5.0,
                'failure_probability': 0.01,
                'failure_lrv': 0.5
            }
        },
        'correlations': {
            'primary_activated_sludge': 0.3,
            'description': 'Partial correlation between treatment stages'
        }
    }

    with open(output_dir / 'treatment_uncertainty_mc.yaml', 'w') as f:
        yaml.dump(treatment_uncertainty_config, f, default_flow_style=False, sort_keys=False)

    print(f"  Created 3 Monte Carlo parameter configuration files")


def create_test_data_readme():
    """Create comprehensive README for test data."""

    print("Creating test data documentation...")

    readme_content = """# QMRA Toolkit Test Data Documentation
============================================

This directory contains comprehensive dummy test data for the QMRA toolkit.

## Directory Structure

```
test_data/
├── pathogen_concentrations/    # Monitoring data for pathogens in wastewater
├── dilution_data/               # Hydrodynamic dilution modeling results
├── exposure_scenarios/          # Exposure scenario configurations (YAML)
├── treatment_scenarios/         # Treatment train configurations (YAML)
├── metocean_data/               # MetOcean dilution integration data
├── monte_carlo_params/          # Monte Carlo simulation configurations
└── README.md                    # This file
```

## File Descriptions

### Pathogen Concentrations

**Files:**
- `wastewater_pathogen_monitoring_2024.csv` - Combined raw and treated wastewater data
- `raw_influent_pathogens_2024.csv` - Raw influent pathogen concentrations (52 weeks)
- `treated_effluent_pathogens_2024.csv` - Treated effluent pathogen concentrations (52 weeks)

**Contains:**
- Weekly sampling data for 2024
- Multiple pathogen types: Norovirus, E. coli, Cryptosporidium, Enterococcus
- Realistic log-normal distributions
- QC flags and laboratory metadata

**Usage:**
```python
import pandas as pd
data = pd.read_csv('test_data/pathogen_concentrations/wastewater_pathogen_monitoring_2024.csv')
norovirus_conc = data['Norovirus_copies_per_L']
```

### Dilution Data

**Files:**
- `hydrodynamic_dilution_modeling_1000runs.csv` - Monte Carlo dilution modeling results
- `dilution_summary_by_site.csv` - Summary statistics by monitoring site

**Contains:**
- 1,000 model runs across 6 sites (discharge to 1000m)
- Environmental conditions (tidal state, wind, currents)
- Dilution factors ranging from 1x (at discharge) to 1000x+ (far field)
- ROMS hydrodynamic model outputs

**Usage:**
```python
dilution_df = pd.read_csv('test_data/dilution_data/hydrodynamic_dilution_modeling_1000runs.csv')
site_100m = dilution_df[dilution_df['Site_Name'] == 'Site_100m']
median_dilution = site_100m['Dilution_Factor'].median()
```

### Exposure Scenarios

**Files:**
- `swimming_scenario.yaml` - Recreational swimming exposure
- `shellfish_scenario.yaml` - Shellfish harvesting and consumption
- `drinking_water_scenario.yaml` - Drinking water supply
- `multi_pathogen_comparison.yaml` - Multi-pathogen comparative assessment

**Format:** YAML configuration files

**Structure:**
```yaml
scenario_name: "Scenario Name"
exposure_route: primary_contact | shellfish_consumption | drinking_water
population:
  size: 10000
  age_distribution: {...}
exposure_parameters:
  water_ingestion_volume_mL:
    distribution: lognormal
    meanlog: 3.5
    sdlog: 0.5
pathogen: norovirus
risk_threshold: 1e-3
```

**Usage:**
```python
import yaml
with open('test_data/exposure_scenarios/swimming_scenario.yaml') as f:
    scenario = yaml.safe_load(f)
```

### Treatment Scenarios

**Files:**
- `bypass_no_treatment.yaml` - Emergency bypass (no treatment)
- `primary_treatment.yaml` - Screening + primary settling only
- `secondary_treatment.yaml` - Activated sludge biological treatment
- `advanced_uv_treatment.yaml` - Full train with UV disinfection
- `chlorination_treatment.yaml` - Secondary treatment with chlorination

**Format:** YAML configuration files

**Structure:**
```yaml
scenario_name: "Treatment Scenario Name"
treatment_barriers:
  - name: "Barrier Name"
    type: physical | biological | uv_disinfection | chlorination
    lrv: 2.0
    variability: 0.5
    description: "Description"
total_log_reduction: 3.0
pathogen_specific_lrv:
  cryptosporidium: 2.5
  norovirus: 2.0
  bacteria: 3.5
```

**Usage:**
```python
from dilution_model import DilutionModel, TreatmentBarrier, TreatmentType
import yaml

with open('test_data/treatment_scenarios/advanced_uv_treatment.yaml') as f:
    config = yaml.safe_load(f)

model = DilutionModel()
for barrier_config in config['treatment_barriers']:
    barrier = TreatmentBarrier(
        name=barrier_config['name'],
        treatment_type=TreatmentType(barrier_config['type']),
        log_reduction_value=barrier_config['lrv'],
        variability=barrier_config.get('variability')
    )
    model.add_treatment_barrier(barrier)
```

### MetOcean Data

**Files:**
- `metocean_dilution_hourly_2024_sample.csv` - Hourly dilution factors with environmental conditions
- `metocean_dilution_summary.csv` - Summary statistics by site

**Contains:**
- Hourly time series data (100 timesteps shown as example)
- Multiple monitoring sites
- Environmental parameters: wind, waves, currents, tides, temperature
- Model run identifiers

**Usage:**
```python
from metocean_dilution_parser import MetOceanDilutionParser

parser = MetOceanDilutionParser()
dilution_data = parser.parse_csv('test_data/metocean_data/metocean_dilution_hourly_2024_sample.csv')
```

### Monte Carlo Parameters

**Files:**
- `basic_monte_carlo_config.yaml` - Basic MC simulation settings
- `advanced_monte_carlo_lhs.yaml` - Latin Hypercube Sampling with sensitivity analysis
- `treatment_uncertainty_mc.yaml` - Treatment performance uncertainty

**Structure:**
```yaml
simulation_name: "Simulation Name"
n_iterations: 10000
sampling_method: random | latin_hypercube
uncertainty_parameters:
  parameter_name:
    distribution: lognormal | normal | uniform | poisson
    parameters: {...}
```

**Usage:**
```python
from monte_carlo import MonteCarloSimulator
import yaml

with open('test_data/monte_carlo_params/basic_monte_carlo_config.yaml') as f:
    config = yaml.safe_load(f)

simulator = MonteCarloSimulator(n_iterations=config['n_iterations'])
```

## Example Workflows

### 1. Complete QMRA Assessment

```python
from qmra_integration import QMRAAssessment
import pandas as pd
import yaml

# Load pathogen data
pathogen_data = pd.read_csv('test_data/pathogen_concentrations/treated_effluent_pathogens_2024.csv')
mean_concentration = pathogen_data['Norovirus_copies_per_L'].mean()

# Load dilution data
dilution_data = pd.read_csv('test_data/dilution_data/hydrodynamic_dilution_modeling_1000runs.csv')
site_dilutions = dilution_data[dilution_data['Site_Name'] == 'Site_100m']['Dilution_Factor']

# Load exposure scenario
with open('test_data/exposure_scenarios/swimming_scenario.yaml') as f:
    scenario = yaml.safe_load(f)

# Load treatment configuration
with open('test_data/treatment_scenarios/secondary_treatment.yaml') as f:
    treatment = yaml.safe_load(f)

# Run assessment
assessment = QMRAAssessment()
results = assessment.run_assessment(
    pathogen='norovirus',
    concentration=mean_concentration,
    dilution_factors=site_dilutions,
    treatment_lrv=treatment['total_log_reduction'],
    exposure_params=scenario['exposure_parameters'],
    population_size=scenario['population']['size']
)
```

### 2. Treatment Scenario Comparison

```python
import yaml
from pathogen_database import PathogenDatabase
from dilution_model import DilutionModel

# Compare different treatment scenarios
treatment_files = [
    'bypass_no_treatment.yaml',
    'primary_treatment.yaml',
    'secondary_treatment.yaml',
    'advanced_uv_treatment.yaml'
]

initial_concentration = 1e6  # organisms/L

for treatment_file in treatment_files:
    with open(f'test_data/treatment_scenarios/{treatment_file}') as f:
        config = yaml.safe_load(f)

    model = DilutionModel()
    # Add treatment barriers...

    final_conc = model.apply_complete_scenario(initial_concentration)
    print(f"{config['scenario_name']}: {final_conc:.2e} organisms/L")
```

### 3. MetOcean Integration

```python
from metocean_dilution_parser import MetOceanDilutionParser
from qmra_integration import QMRAAssessment

# Parse MetOcean data
parser = MetOceanDilutionParser()
dilution_df = parser.parse_csv('test_data/metocean_data/metocean_dilution_hourly_2024_sample.csv')

# Extract site-specific dilutions
site_dilutions = parser.get_site_dilutions(dilution_df, site_name='Beach_North')

# Use in QMRA
assessment = QMRAAssessment()
# ... run assessment with site_dilutions
```

## Data Generation

All test data was generated using `generate_test_data.py`. To regenerate:

```bash
cd test_data
python generate_test_data.py
```

## Data Characteristics

### Realistic Features:
- Log-normal distributions for pathogen concentrations (typical for environmental data)
- Seasonal variations in environmental parameters
- Realistic treatment LRV ranges based on literature
- Distance-dependent dilution gradients
- Variability consistent with real monitoring programs

### Simplifications:
- Fixed random seeds for reproducibility
- Simplified tidal cycles
- No extreme weather events
- Uniform QC pass rates
- Idealized treatment performance

## References

### Pathogen Concentrations:
- Rose, J.B., et al. (2004). "Quantitative Microbial Risk Assessment"
- WHO Guidelines for Drinking Water Quality (2017)

### Dilution Modeling:
- Roberts, P.J.W., et al. (2011). "Mixing in Coastal Waters"

### Treatment Performance:
- USEPA (2006). "Ultraviolet Disinfection Guidance Manual"
- Water Research Foundation (2012). "Pathogen Removal Processes"

### Dose-Response Models:
- Teunis et al. (2008) - Norovirus
- Haas et al. (1999) - Multiple pathogens
- WHO (2016) - QMRA guidelines

## Support

For questions about using this test data, see:
- Main QMRA Toolkit documentation
- Example scripts in `qmra_toolkit/examples/`
- API documentation

---

**Generated:** October 2025
**Version:** 1.0
**Maintainer:** NIWA Earth Sciences New Zealand
"""

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print("  Created comprehensive README.md")


def main():
    """Generate all test data files."""

    print("\n" + "="*80)
    print("QMRA Toolkit - Test Data Generator")
    print("="*80 + "\n")

    # Change to test_data directory
    test_data_dir = Path(__file__).parent
    import os
    os.chdir(test_data_dir)

    # Generate all test data
    create_pathogen_concentration_data()
    create_dilution_data()
    create_exposure_scenarios()
    create_treatment_scenarios()
    create_metocean_data()
    create_monte_carlo_params()
    create_test_data_readme()

    print("\n" + "="*80)
    print("TEST DATA GENERATION COMPLETE")
    print("="*80)
    print("\nGenerated files:")
    print("  - Pathogen concentration monitoring data (3 CSV files)")
    print("  - Hydrodynamic dilution modeling data (2 CSV files)")
    print("  - Exposure scenario configurations (4 YAML files)")
    print("  - Treatment scenario configurations (5 YAML files)")
    print("  - MetOcean integration data (2 CSV files)")
    print("  - Monte Carlo parameter files (3 YAML files)")
    print("  - Comprehensive README documentation")
    print("\nTotal: 20 test data files ready for toolkit testing")
    print("\nUsage: See README.md for example workflows and code snippets")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
