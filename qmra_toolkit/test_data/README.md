# QMRA Toolkit Test Data Documentation
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
