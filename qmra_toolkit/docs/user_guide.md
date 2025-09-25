# QMRA Assessment Toolkit - User Guide

## Overview

The QMRA Assessment Toolkit is a comprehensive Python-based solution for Quantitative Microbial Risk Assessment, developed by NIWA Earth Sciences New Zealand. This toolkit replaces @Risk Excel functionality with automated, reproducible workflows.

## Key Features

- **Pathogen Database**: Comprehensive database with dose-response models for key pathogens
- **Exposure Assessment**: Models for various exposure routes (primary contact, shellfish consumption, drinking water)
- **Dilution Modeling**: Integration with NIWA's dilution modeling capabilities (key differentiator)
- **Monte Carlo Simulation**: Advanced uncertainty analysis replacing @Risk functionality
- **Risk Characterization**: Complete risk metrics calculation (infection, illness, DALYs)
- **Automated Reporting**: Generate regulatory compliance reports in Word format
- **Command-Line Interface**: Easy-to-use CLI for common workflows

## Installation

### Requirements

- Python 3.8 or higher
- Required packages listed in `requirements.txt`

### Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Verify installation:**
```bash
python tests/run_all_tests.py
```

3. **Test CLI:**
```bash
python src/qmra_toolkit.py --help
```

## Quick Start

### Example 1: Basic Risk Assessment

Run a complete QMRA assessment for recreational water exposure:

```bash
python src/qmra_toolkit.py assess \
  --pathogen norovirus \
  --exposure-route primary_contact \
  --concentration 10.0 \
  --volume 50.0 \
  --frequency 10 \
  --population 10000 \
  --report
```

This command:
- Assesses norovirus exposure from recreational water
- Uses 10 organisms per 100mL water concentration
- Assumes 50 mL water ingestion per swimming event
- Calculates risk for 10 swimming events per year
- Applies results to a population of 10,000
- Generates a comprehensive compliance report

### Example 2: Dose-Response Analysis

Calculate infection probabilities for specific doses:

```bash
python src/qmra_toolkit.py dose-response \
  --pathogen norovirus \
  --dose 1 --dose 10 --dose 100 --dose 1000 \
  --model beta_poisson \
  --output dose_response_results.json
```

### Example 3: List Available Pathogens

```bash
python src/qmra_toolkit.py list-pathogens
```

### Example 4: Get Pathogen Information

```bash
python src/qmra_toolkit.py pathogen-info --pathogen norovirus
```

## Detailed Usage

### Command-Line Interface

The toolkit provides several commands:

#### `assess` - Complete Risk Assessment

**Required Parameters:**
- `--pathogen` / `-p`: Pathogen name (e.g., norovirus, cryptosporidium)
- `--exposure-route` / `-e`: Exposure route (primary_contact, shellfish_consumption, drinking_water)
- `--concentration` / `-c`: Pathogen concentration (organisms per unit)

**Optional Parameters:**
- `--volume`: Exposure volume (mL for water, grams for food)
- `--frequency`: Exposure frequency (events per year)
- `--population`: Population size for population risk calculations
- `--iterations` / `-n`: Number of Monte Carlo iterations (default: 10,000)
- `--output` / `-o`: Output file for results (JSON format)
- `--report` / `-r`: Generate comprehensive Word report

#### `dose-response` - Dose-Response Analysis

**Parameters:**
- `--pathogen` / `-p`: Pathogen name
- `--dose` / `-d`: Dose values (can specify multiple)
- `--model` / `-m`: Model type (beta_poisson, exponential, hypergeometric)
- `--output` / `-o`: Output file for results

#### `treatment` - Treatment and Dilution Modeling

**Parameters:**
- `--initial-concentration` / `-c`: Initial pathogen concentration
- `--treatment-config` / `-t`: Treatment configuration file (YAML)
- `--dilution-flow`: Discharge flow rate (m³/s)
- `--receiving-flow`: Receiving water flow rate (m³/s)
- `--output` / `-o`: Output file for results

### Python API Usage

For more advanced usage, you can use the toolkit directly in Python:

```python
from pathogen_database import PathogenDatabase
from exposure_assessment import create_exposure_assessment, ExposureRoute
from risk_characterization import RiskCharacterization

# Initialize components
pathogen_db = PathogenDatabase()
risk_calc = RiskCharacterization(pathogen_db)

# Set up exposure assessment
exposure_params = {
    "water_ingestion_volume": 50.0,  # mL per event
    "exposure_frequency": 10         # events per year
}

exposure_model = create_exposure_assessment(
    ExposureRoute.PRIMARY_CONTACT,
    exposure_params
)
exposure_model.set_pathogen_concentration(10.0)

# Run comprehensive assessment
results = risk_calc.run_comprehensive_assessment(
    pathogen_name="norovirus",
    exposure_assessment=exposure_model,
    population_size=10000,
    n_samples=10000
)

# Print results
for metric_name, result in results.items():
    print(f"{metric_name}: {result.statistics['mean']:.2e}")
```

## Exposure Routes

### Primary Contact (Recreational Water)

Models inadvertent water ingestion during swimming, surfing, or other water activities.

**Required Parameters:**
- `water_ingestion_volume`: Volume ingested per event (mL)
- `exposure_frequency`: Number of exposure events per year

**Example concentrations:**
- Beach water: 1-100 organisms per 100 mL
- River water: 10-1000 organisms per 100 mL

### Shellfish Consumption

Models pathogen exposure through shellfish consumption (oysters, mussels, clams).

**Required Parameters:**
- `shellfish_consumption`: Mass consumed per serving (grams)
- `consumption_frequency`: Number of servings per year

**Optional Parameters:**
- `bioaccumulation_factor`: Factor for pathogen concentration in shellfish vs. water

**Example concentrations:**
- Raw shellfish: 100-10,000 organisms per 100g

### Drinking Water

Models exposure through treated or untreated drinking water consumption.

**Required Parameters:**
- `daily_consumption_volume`: Daily consumption volume (mL)

**Example concentrations:**
- Treated water: 0.1-10 organisms per L
- Untreated water: 10-10,000 organisms per L

## Pathogen Database

### Available Pathogens

The toolkit includes dose-response models for:

- **Norovirus**: Beta-Poisson model (α=0.04, β=0.055)
- **Campylobacter jejuni**: Beta-Poisson model (α=0.145, β=7.59)
- **Cryptosporidium parvum**: Exponential model (r=0.0042)

### Adding Custom Pathogens

You can add custom pathogens through the Python API:

```python
from pathogen_database import PathogenDatabase

db = PathogenDatabase()

custom_pathogen = {
    "name": "Custom Pathogen",
    "pathogen_type": "bacteria",
    "dose_response_models": {
        "beta_poisson": {
            "alpha": 0.2,
            "beta": 100.0,
            "source": "Custom study"
        }
    },
    "illness_to_infection_ratio": 0.6,
    "dalys_per_case": 0.005
}

db.add_custom_pathogen("custom_pathogen", custom_pathogen)
```

## Dilution and Treatment Modeling

### NIWA's Key Differentiator

The toolkit includes sophisticated dilution modeling capabilities that integrate:

- Engineer-provided Log Reduction Values (LRVs)
- Multi-barrier treatment trains
- Far-field dilution modeling
- Natural die-off processes

### Treatment Configuration

Create a YAML configuration file for treatment trains:

```yaml
treatment_barriers:
  - name: "Primary Settling"
    type: "physical"
    lrv: 0.5
    variability: 0.2

  - name: "Activated Sludge"
    type: "biological"
    lrv: 2.0
    variability: 0.5

  - name: "UV Disinfection"
    type: "uv"
    lrv: 3.0
    variability: 0.3
```

### Usage Example

```python
from dilution_model import DilutionModel, TreatmentBarrier, TreatmentType

# Create dilution model
model = DilutionModel()

# Add treatment barriers
model.add_treatment_barrier(TreatmentBarrier(
    name="UV Treatment",
    treatment_type=TreatmentType.UV,
    log_reduction_value=3.0,
    variability=0.2
))

# Apply to concentration
initial_conc = 1e6  # organisms/L
results = model.apply_complete_scenario(initial_conc)
```

## Monte Carlo Uncertainty Analysis

The toolkit includes comprehensive uncertainty analysis capabilities:

### Basic Usage

```python
from monte_carlo import MonteCarloSimulator, create_lognormal_distribution

# Create simulator
mc_sim = MonteCarloSimulator(random_seed=42)

# Add uncertain parameters
conc_dist = create_lognormal_distribution(mean=2.0, std=1.0)
mc_sim.add_distribution("concentration", conc_dist)

# Define model function
def model_function(samples):
    conc = samples["concentration"]
    dose = conc * 0.05  # 50 mL exposure
    # Apply dose-response model
    return 1 - np.exp(-0.1 * dose)

# Run simulation
results = mc_sim.run_simulation(model_function, n_iterations=10000)
```

### Supported Distributions

- Normal
- Lognormal
- Uniform
- Triangular
- Beta
- Gamma
- Exponential
- Weibull
- Poisson
- Binomial

## Report Generation

The toolkit automatically generates comprehensive regulatory compliance reports:

### Report Contents

1. **Executive Summary**
2. **Introduction and Objectives**
3. **Methodology**
4. **Risk Assessment Results**
5. **Uncertainty Analysis**
6. **Regulatory Compliance Assessment**
7. **Conclusions and Recommendations**
8. **Appendices with Detailed Data**

### Custom Reports

```python
from report_generator import ReportGenerator

report_gen = ReportGenerator()

project_info = {
    'title': 'Beach Safety Assessment',
    'project_name': 'Recreational Water QMRA',
    'location': 'Wellington Harbour',
    'client': 'Regional Council'
}

report_path = report_gen.create_regulatory_report(
    project_info=project_info,
    risk_results=results,
    exposure_params=exposure_params
)
```

## Regulatory Compliance

### Default Thresholds

The toolkit includes standard regulatory thresholds:

- **Acceptable annual risk**: 1 in 1,000,000 per year (1×10⁻⁶)
- **Recreational water risk**: 1 in 1,000 per exposure (1×10⁻³)
- **Drinking water annual risk**: 1 in 10,000 per year (1×10⁻⁴)

### Compliance Checking

```python
# Evaluate compliance
compliance = risk_calc.evaluate_regulatory_compliance(annual_risk_result)

for threshold, is_compliant in compliance.items():
    status = "PASS" if is_compliant else "FAIL"
    print(f"{threshold}: {status}")
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed (`pip install -r requirements.txt`)

2. **Pathogen Not Found**: Check available pathogens with `list-pathogens` command

3. **Configuration Issues**: Verify YAML syntax in treatment configuration files

4. **Memory Issues**: Reduce Monte Carlo iterations for large simulations

5. **Report Generation Fails**: Ensure write permissions for output directory

### Getting Help

- Check the test suite: `python tests/run_all_tests.py`
- Run example: `python src/qmra_toolkit.py example`
- View CLI help: `python src/qmra_toolkit.py --help`

## Best Practices

### Model Selection

1. **Use Beta-Poisson models** for most viral and bacterial pathogens
2. **Use Exponential models** for highly infectious pathogens or conservative estimates
3. **Validate parameters** against published literature

### Uncertainty Analysis

1. **Use at least 10,000 iterations** for robust uncertainty estimates
2. **Include parameter uncertainty** in LRV values
3. **Document assumptions** clearly in reports

### Quality Assurance

1. **Run validation tests** regularly
2. **Compare results** with previous assessments
3. **Review reports** before submission
4. **Archive model inputs** with results

## Advanced Topics

### Custom Dose-Response Models

For specialized applications, you can implement custom dose-response models:

```python
from dose_response import DoseResponseModel

class CustomModel(DoseResponseModel):
    def calculate_infection_probability(self, dose):
        # Implement custom model logic
        return custom_probability_function(dose, self.parameters)
```

### Integration with External Models

The toolkit can integrate with external dilution or treatment models:

```python
# Example integration with external dilution model
def apply_external_dilution(concentration, flow_data):
    # Call external model
    return diluted_concentration

# Use in QMRA workflow
initial_conc = 1e6
diluted_conc = apply_external_dilution(initial_conc, flow_data)
# Continue with risk assessment...
```

### Batch Processing

For multiple scenarios, use batch processing:

```python
scenarios = [
    {"pathogen": "norovirus", "concentration": 10, "frequency": 5},
    {"pathogen": "norovirus", "concentration": 50, "frequency": 10},
    # ... more scenarios
]

results = {}
for i, scenario in enumerate(scenarios):
    results[f"scenario_{i}"] = risk_calc.run_comprehensive_assessment(**scenario)
```

## Version History

- **v1.0.0**: Initial release with core QMRA functionality
  - Pathogen database with key pathogens
  - Multiple exposure assessment models
  - Dilution and treatment modeling
  - Monte Carlo uncertainty analysis
  - Automated report generation
  - Command-line interface

## Support and Contributing

This toolkit was developed by NIWA Earth Sciences New Zealand as part of the Strategic Investment Programme to replace @Risk Excel functionality with Python-based automation.

For technical support or feature requests, contact the NIWA QMRA team.

---

*Generated by QMRA Assessment Toolkit v1.0.0*
*© NIWA Earth Sciences New Zealand*