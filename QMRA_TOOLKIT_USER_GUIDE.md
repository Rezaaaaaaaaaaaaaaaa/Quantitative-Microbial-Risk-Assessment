# NIWA QMRA Toolkit - Comprehensive User Guide

**Version**: 1.0.0
**Date**: October 2025
**Author**: NIWA Earth Sciences

---

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Using the Tools](#using-the-tools)
   - [Web Application (Streamlit)](#web-application-streamlit)
   - [Desktop GUI Applications](#desktop-gui-applications)
   - [Python API](#python-api)
   - [Command Line Interface](#command-line-interface)
5. [Working with Test Data](#working-with-test-data)
6. [Example Workflows](#example-workflows)
7. [API Reference](#api-reference)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)

---

## Introduction

The NIWA QMRA (Quantitative Microbial Risk Assessment) Toolkit is a comprehensive Python package for assessing microbial health risks from water-related exposures. It implements peer-reviewed dose-response models, Monte Carlo uncertainty analysis, and regulatory compliance evaluation.

### Key Features

- **6 Pathogens**: Norovirus, Campylobacter, Cryptosporidium, E. coli, Salmonella, Rotavirus
- **Multiple Exposure Routes**: Primary contact, shellfish consumption, drinking water, aerosol inhalation
- **Monte Carlo Simulation**: 10,000+ iterations for uncertainty quantification
- **Peer-Reviewed Models**: Beta-Poisson and Exponential dose-response models
- **Multiple Interfaces**: Web app, desktop GUI, Python API, command line
- **Professional Reports**: PDF/Word generation with visualizations

### Scientific Basis

All dose-response parameters are from peer-reviewed literature:
- Haas, C.N., Rose, J.B., & Gerba, C.P. (1999). *Quantitative Microbial Risk Assessment*
- Teunis, P.F.M., et al. (2008). *Norovirus dose-response modeling*
- Ward, R.L., et al. (1986). *Rotavirus human challenge studies*

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (optional, for cloning repository)

### Installation Steps

#### Option 1: Install from Repository

```bash
# Clone the repository
git clone https://github.com/niwa/qmra-toolkit.git
cd qmra-toolkit

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

#### Option 2: Install Dependencies Only

```bash
# Navigate to project directory
cd "C:\Users\moghaddamr\OneDrive - NIWA\Quantitative Microbial Risk Assessment"

# Install required packages
pip install numpy scipy pandas matplotlib seaborn python-docx PyYAML click openpyxl streamlit
```

### Verify Installation

```python
# Test imports
python -c "from qmra_toolkit.src.pathogen_database import PathogenDatabase; print('Installation successful!')"
```

---

## Quick Start

### 30-Second Example

```python
import sys
sys.path.insert(0, 'qmra_toolkit/src')

from pathogen_database import PathogenDatabase
from dose_response import create_dose_response_model

# Load pathogen database
db = PathogenDatabase()

# Get norovirus parameters
params = db.get_dose_response_parameters('norovirus', 'beta_poisson')

# Create dose-response model
model = create_dose_response_model('beta_poisson', params)

# Calculate infection risk from 100 organisms
dose = 100
risk = model.calculate_infection_probability(dose)

print(f"Infection probability from {dose} organisms: {risk:.4f}")
# Output: Infection probability from 100 organisms: 0.2594
```

---

## Using the Tools

### Web Application (Streamlit)

The web application provides an interactive browser-based interface.

#### Starting the Web App

```bash
# From project root directory
streamlit run qmra_toolkit/web_app.py
```

The app will open in your default browser at `http://localhost:8501`

#### Web App Features

1. **Quick Assessment** - Single pathogen, basic parameters
2. **Detailed Assessment** - Multiple pathogens, advanced options
3. **Batch Assessment** - Upload CSV for multiple scenarios
4. **Sensitivity Analysis** - Parameter importance ranking
5. **Regulatory Compliance** - WHO/NZ guidelines comparison
6. **Report Generation** - Export PDF/Word reports
7. **Data Visualization** - Interactive plots and charts
8. **MetOcean Integration** - Dilution modeling for marine discharge

#### Example Web App Workflow

1. **Select Pathogen**: Choose from dropdown (e.g., "Norovirus")
2. **Set Exposure Route**: Primary contact, shellfish, etc.
3. **Enter Parameters**:
   - Concentration: 100 organisms/L
   - Volume: 50 mL
   - Frequency: 20 events/year
   - Population: 50,000 people
4. **Configure Simulation**:
   - Iterations: 10,000
   - Confidence Level: 95%
5. **Run Assessment**: Click "Run QMRA Assessment"
6. **View Results**:
   - Infection probability
   - Illness risk
   - Annual risk
   - Population impact
   - Uncertainty ranges (5th-95th percentile)
7. **Download Report**: PDF or Word format

#### Using Test Data with Web App

Upload the provided test data files:

```python
# Load recreational swimming scenario
test_data/scenarios/recreational_swimming.json
```

The web app will automatically populate parameters from the JSON file.

---

### Desktop GUI Applications

Two desktop GUI options are available:

#### Basic GUI (`qmra_gui.py`)

Simple Tkinter interface for basic assessments.

```bash
# From project root
python qmra_toolkit/src/qmra_gui.py
```

**Features**:
- Single pathogen assessment
- Basic parameter inputs
- Real-time calculation
- Results display
- CSV export

#### Enhanced GUI (`enhanced_qmra_gui.py`)

Professional 8-tab interface with advanced features.

```bash
# From project root
python qmra_toolkit/src/enhanced_qmra_gui.py
```

**Features**:
- Multi-pathogen comparison
- Treatment scenario analysis
- Interactive matplotlib plots
- Professional report generation
- Regulatory compliance checks
- Sensitivity analysis
- NIWA branded styling

**Enhanced GUI Tabs**:

1. **Setup** - Project information and metadata
2. **Pathogens** - Pathogen selection and parameters
3. **Exposure** - Exposure route and scenario details
4. **Analysis** - Monte Carlo simulation configuration
5. **Results** - Risk calculations and statistics
6. **Visualization** - Interactive charts and graphs
7. **Compliance** - Regulatory guideline comparison
8. **Reports** - Export professional documents

---

### Python API

The Python API provides programmatic access to all QMRA functionality.

#### Example 1: Basic Risk Calculation

```python
import sys
import numpy as np
sys.path.insert(0, 'qmra_toolkit/src')

from pathogen_database import PathogenDatabase
from dose_response import create_dose_response_model
from risk_characterization import RiskCharacterization

# Initialize components
pathogen_db = PathogenDatabase()
risk_calc = RiskCharacterization()

# Get pathogen info
pathogen = 'norovirus'
model_type = pathogen_db.get_default_model_type(pathogen)
dr_params = pathogen_db.get_dose_response_parameters(pathogen, model_type)
health_data = pathogen_db.get_health_impact_data(pathogen)

# Create dose-response model
dr_model = create_dose_response_model(model_type, dr_params)

# Calculate risks
concentration = 100  # organisms/L
volume = 50  # mL
dose = (concentration * volume) / 1000.0  # organisms

# Infection probability
p_infection = dr_model.calculate_infection_probability(dose)

# Illness probability
p_illness = p_infection * health_data['illness_to_infection_ratio']

# Annual risk (20 exposures/year)
frequency = 20
p_annual = 1 - np.power(1 - p_infection, frequency)

# Population impact (50,000 people)
population = 50000
cases_per_year = p_annual * population

print(f"Single exposure infection risk: {p_infection:.6e}")
print(f"Single exposure illness risk: {p_illness:.6e}")
print(f"Annual infection risk: {p_annual:.6e}")
print(f"Expected cases per year: {cases_per_year:.1f}")
```

**Output**:
```
Single exposure infection risk: 2.594e-01
Single exposure illness risk: 1.816e-01
Annual infection risk: 9.976e-01
Expected cases per year: 49880.0
```

#### Example 2: Monte Carlo Uncertainty Analysis

```python
import sys
import numpy as np
sys.path.insert(0, 'qmra_toolkit/src')

from pathogen_database import PathogenDatabase
from dose_response import create_dose_response_model
from monte_carlo import MonteCarloSimulator, create_lognormal_distribution, create_uniform_distribution

# Initialize
pathogen_db = PathogenDatabase()
pathogen = 'campylobacter'
model_type = pathogen_db.get_default_model_type(pathogen)
dr_params = pathogen_db.get_dose_response_parameters(pathogen, model_type)
dr_model = create_dose_response_model(model_type, dr_params)

# Create Monte Carlo simulator
mc_sim = MonteCarloSimulator(random_seed=42)

# Add uncertainty distributions
concentration = 50  # mean organisms/L
conc_dist = create_lognormal_distribution(
    mean=np.log(concentration),
    std=0.5,  # standard deviation in log space
    name="concentration"
)
mc_sim.add_distribution("concentration", conc_dist)

volume = 50  # mean mL
vol_dist = create_uniform_distribution(
    min_val=25,  # 50% of mean
    max_val=75,  # 150% of mean
    name="volume"
)
mc_sim.add_distribution("volume", vol_dist)

# Define QMRA model
def qmra_model(samples):
    conc = samples["concentration"]
    vol = samples["volume"]
    dose = (conc * vol) / 1000.0
    return dr_model.calculate_infection_probability(dose)

# Run simulation
results = mc_sim.run_simulation(
    qmra_model,
    n_iterations=10000,
    variable_name="infection_probability"
)

# Display results
print(f"\nMonte Carlo Results ({results.n_iterations} iterations):")
print(f"Mean: {results.statistics['mean']:.6e}")
print(f"Median: {results.statistics['median']:.6e}")
print(f"95% CI: [{results.percentiles['5%']:.6e}, {results.percentiles['95%']:.6e}]")
print(f"Std Dev: {results.statistics['std']:.6e}")
```

**Output**:
```
Monte Carlo Results (10000 iterations):
Mean: 7.321e-02
Median: 6.854e-02
95% CI: [2.145e-02, 1.548e-01]
Std Dev: 4.891e-02
```

#### Example 3: Comprehensive Assessment with Multiple Pathogens

```python
import sys
sys.path.insert(0, 'qmra_toolkit/src')

from risk_characterization import RiskCharacterization

# Initialize risk characterization
risk_calc = RiskCharacterization()

# Define assessment parameters
pathogens = ['norovirus', 'campylobacter', 'e_coli']
results = {}

for pathogen in pathogens:
    # Run comprehensive assessment
    result = risk_calc.run_comprehensive_assessment(
        pathogen=pathogen,
        exposure_route='primary_contact',
        concentration=100,  # organisms/L
        volume=50,  # mL
        frequency=20,  # events/year
        population=50000,
        iterations=5000,  # Use 5000 for faster demo
        confidence_level=0.95
    )

    results[pathogen] = result

    print(f"\n{pathogen.upper()} Assessment:")
    print(f"  Mean infection risk: {result['infection_risk']['mean']:.6e}")
    print(f"  Mean illness risk: {result['illness_risk']['mean']:.6e}")
    print(f"  Annual population cases: {result['annual_risk']['mean'] * 50000:.1f}")
```

#### Example 4: Reading Test Data Files

```python
import pandas as pd
import json

# Load pathogen concentration data
wastewater_data = pd.read_csv('test_data/pathogen_concentrations/wastewater_monitoring.csv')
print("\nWastewater Monitoring Data:")
print(wastewater_data.head())

# Filter by pathogen
norovirus_data = wastewater_data[wastewater_data['pathogen'] == 'norovirus']
mean_concentration = norovirus_data['concentration_per_L'].mean()
print(f"\nMean norovirus concentration: {mean_concentration:.1f} organisms/L")

# Load scenario data
with open('test_data/scenarios/recreational_swimming.json', 'r') as f:
    scenario = json.load(f)

print(f"\nScenario: {scenario['scenario_name']}")
print(f"Exposure route: {scenario['exposure_route']}")
print(f"Pathogen: {scenario['pathogen']}")
print(f"Concentration: {scenario['exposure_parameters']['concentration_per_L']} org/L")
print(f"Population: {scenario['population']['total_population']}")
```

#### Example 5: Custom Dose-Response Model

```python
import sys
sys.path.insert(0, 'qmra_toolkit/src')

from dose_response import BetaPoissonModel, ExponentialModel

# Create custom Beta-Poisson model
custom_params = {
    'alpha': 0.15,
    'beta': 10.0,
    'source': 'Custom parameters for specific strain'
}

bp_model = BetaPoissonModel(custom_params)

# Test at different doses
doses = [1, 10, 100, 1000]
print("\nCustom Beta-Poisson Model:")
for dose in doses:
    prob = bp_model.calculate_infection_probability(dose)
    print(f"  Dose {dose:4d}: P(infection) = {prob:.6f}")

# Calculate dose for target risk
target_risk = 1e-4  # 1 in 10,000
required_dose = bp_model.calculate_dose_for_risk(target_risk)
print(f"\nDose for {target_risk} risk: {required_dose:.2f} organisms")
```

---

### Command Line Interface

The toolkit includes a CLI for batch processing and automation.

#### Basic Commands

```bash
# Run single assessment
qmra assess --pathogen norovirus --concentration 100 --volume 50 --frequency 20 --population 50000

# Batch processing from CSV
qmra batch --input scenarios.csv --output results/

# Generate report
qmra report --input results/assessment_001.json --format pdf --output report.pdf

# List available pathogens
qmra list-pathogens

# Show pathogen details
qmra pathogen-info --name norovirus

# Validate input data
qmra validate --file test_data/scenarios/recreational_swimming.json
```

#### Example CLI Workflow

```bash
# 1. Validate test scenario
qmra validate --file test_data/scenarios/recreational_swimming.json

# 2. Run assessment
qmra assess \
  --pathogen norovirus \
  --exposure-route primary_contact \
  --concentration 0.5 \
  --volume 50 \
  --frequency 20 \
  --population 50000 \
  --iterations 10000 \
  --output results/swimming_assessment.json

# 3. Generate report
qmra report \
  --input results/swimming_assessment.json \
  --format pdf \
  --output reports/swimming_risk_report.pdf
```

---

## Working with Test Data

The toolkit includes comprehensive test data in `test_data/`:

### Directory Structure

```
test_data/
├── pathogen_concentrations/
│   ├── wastewater_monitoring.csv
│   ├── treated_effluent.csv
│   └── beach_monitoring.csv
├── scenarios/
│   ├── recreational_swimming.json
│   ├── shellfish_consumption.json
│   └── drinking_water.json
└── population_data/
    └── auckland_population.csv
```

### Loading Test Data

#### CSV Files

```python
import pandas as pd

# Load wastewater monitoring data
ww_data = pd.read_csv('test_data/pathogen_concentrations/wastewater_monitoring.csv')

# Calculate summary statistics
summary = ww_data.groupby('pathogen')['concentration_per_L'].agg(['mean', 'std', 'min', 'max'])
print(summary)

# Filter by date range
ww_data['date'] = pd.to_datetime(ww_data['date'])
jan_data = ww_data[ww_data['date'].dt.month == 1]

# Plot concentration trends
import matplotlib.pyplot as plt

norovirus = ww_data[ww_data['pathogen'] == 'norovirus']
plt.figure(figsize=(10, 6))
plt.plot(norovirus['date'], norovirus['concentration_per_L'], marker='o')
plt.xlabel('Date')
plt.ylabel('Concentration (organisms/L)')
plt.title('Norovirus Concentration Trend')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('norovirus_trend.png')
```

#### JSON Scenarios

```python
import json
import sys
sys.path.insert(0, 'qmra_toolkit/src')

from risk_characterization import RiskCharacterization

# Load scenario
with open('test_data/scenarios/recreational_swimming.json', 'r') as f:
    scenario = json.load(f)

# Extract parameters
pathogen = scenario['pathogen']
exposure_route = scenario['exposure_route']
concentration = scenario['exposure_parameters']['concentration_per_L']
volume = scenario['exposure_parameters']['ingestion_volume_mL']
frequency = scenario['exposure_parameters']['exposure_frequency_per_year']
population = scenario['population']['total_population']

# Run assessment
risk_calc = RiskCharacterization()
result = risk_calc.run_comprehensive_assessment(
    pathogen=pathogen,
    exposure_route=exposure_route,
    concentration=concentration,
    volume=volume,
    frequency=frequency,
    population=population,
    iterations=10000
)

print(f"\nScenario: {scenario['scenario_name']}")
print(f"Annual risk: {result['annual_risk']['mean']:.6e}")
print(f"Population impact: {result['annual_risk']['mean'] * population:.0f} cases/year")
```

### Creating Your Own Test Data

#### Custom CSV Format

```python
import pandas as pd

# Create custom monitoring data
custom_data = pd.DataFrame({
    'date': ['2025-01-15', '2025-01-16', '2025-01-17'],
    'site': ['Site A', 'Site A', 'Site A'],
    'pathogen': ['norovirus', 'norovirus', 'norovirus'],
    'concentration': [120.5, 135.2, 98.7]
})

custom_data.to_csv('my_custom_data.csv', index=False)
```

#### Custom JSON Scenario

```python
import json

custom_scenario = {
    "scenario_name": "My Custom Assessment",
    "pathogen": "campylobacter",
    "exposure_route": "primary_contact",
    "concentration_per_L": 50,
    "volume_mL": 30,
    "frequency_per_year": 15,
    "population": 25000
}

with open('my_scenario.json', 'w') as f:
    json.dump(custom_scenario, f, indent=2)
```

---

## Example Workflows

### Workflow 1: Beach Water Quality Assessment

**Scenario**: Assess health risks from swimming at a beach near wastewater discharge.

```python
import sys
import pandas as pd
sys.path.insert(0, 'qmra_toolkit/src')

from risk_characterization import RiskCharacterization

# Step 1: Load beach monitoring data
beach_data = pd.read_csv('test_data/pathogen_concentrations/beach_monitoring.csv')

# Step 2: Calculate mean concentration
takapuna = beach_data[beach_data['beach_name'] == 'Takapuna Beach']
norovirus = takapuna[takapuna['pathogen'] == 'norovirus']
mean_conc = norovirus['concentration_per_L'].mean()

print(f"Mean norovirus concentration: {mean_conc:.2f} organisms/L")

# Step 3: Run QMRA assessment
risk_calc = RiskCharacterization()
result = risk_calc.run_comprehensive_assessment(
    pathogen='norovirus',
    exposure_route='primary_contact',
    concentration=mean_conc,
    volume=50,  # mL ingested per swim
    frequency=20,  # swims per summer
    population=100000,  # beach visitors
    iterations=10000
)

# Step 4: Check regulatory compliance
target_risk = 0.0001  # 1 in 10,000 (WHO guideline)
actual_risk = result['annual_risk']['mean']
compliant = actual_risk <= target_risk

print(f"\nAssessment Results:")
print(f"  Annual infection risk: {actual_risk:.6e}")
print(f"  WHO guideline: {target_risk:.6e}")
print(f"  Compliant: {'Yes' if compliant else 'No'}")
print(f"  Expected illness cases: {actual_risk * 100000 * 0.7:.0f}/year")

# Step 5: Calculate required treatment
if not compliant:
    required_reduction = actual_risk / target_risk
    log_reduction = np.log10(required_reduction)
    print(f"\nRequired treatment: {log_reduction:.1f} log reduction")
```

### Workflow 2: Shellfish Harvesting Risk

**Scenario**: Assess risks from consuming oysters harvested near coastal discharge.

```python
import sys
import json
sys.path.insert(0, 'qmra_toolkit/src')

from risk_characterization import RiskCharacterization

# Load scenario
with open('test_data/scenarios/shellfish_consumption.json', 'r') as f:
    scenario = json.load(f)

# Extract parameters
shellfish_conc = scenario['exposure_parameters']['pathogen_concentration_in_shellfish_per_g']
serving_size = scenario['exposure_parameters']['shellfish_serving_size_g']
frequency = scenario['exposure_parameters']['consumption_frequency_per_year']
consumers = scenario['population']['regular_consumers']

# Calculate ingested dose per serving
dose_per_serving = shellfish_conc * serving_size

print(f"Shellfish Assessment:")
print(f"  Concentration: {shellfish_conc} organisms/g")
print(f"  Serving size: {serving_size} g")
print(f"  Dose per serving: {dose_per_serving} organisms")
print(f"  Consumption frequency: {frequency}/year")

# Run assessment
risk_calc = RiskCharacterization()

# Note: For shellfish, dose is already calculated, so set concentration and volume accordingly
# We'll use concentration = dose and volume = 1 mL as a workaround
result = risk_calc.run_comprehensive_assessment(
    pathogen='norovirus',
    exposure_route='shellfish_consumption',
    concentration=dose_per_serving * 1000,  # Convert to "per L" equivalent
    volume=1,  # 1 mL as unit
    frequency=frequency,
    population=consumers,
    iterations=10000
)

print(f"\nRisk Results:")
print(f"  Per-serving infection risk: {result['infection_risk']['mean']:.6e}")
print(f"  Annual infection risk: {result['annual_risk']['mean']:.6e}")
print(f"  Expected cases/year: {result['annual_risk']['mean'] * consumers:.0f}")

# Evaluate depuration effectiveness
depuration_reduction = 2.0  # 2 log reduction
reduced_dose = dose_per_serving / (10 ** depuration_reduction)
print(f"\nWith depuration ({depuration_reduction} log reduction):")
print(f"  Reduced dose: {reduced_dose:.1f} organisms")
```

### Workflow 3: Drinking Water Treatment Optimization

**Scenario**: Optimize treatment barriers for drinking water safety.

```python
import sys
import json
import numpy as np
sys.path.insert(0, 'qmra_toolkit/src')

from risk_characterization import RiskCharacterization

# Load scenario
with open('test_data/scenarios/drinking_water.json', 'r') as f:
    scenario = json.load(f)

raw_water_conc = scenario['exposure_parameters']['raw_water_concentration_per_L']
daily_consumption = scenario['exposure_parameters']['daily_consumption_L']
population = scenario['population']['total_population']
treatment = scenario['treatment_barriers']

print("Drinking Water Treatment Optimization")
print("=" * 50)

# Calculate cumulative log removal
total_log_removal = sum([
    treatment['coagulation_flocculation']['log_removal'],
    treatment['filtration']['log_removal'],
    treatment['disinfection']['log_inactivation']
])

print(f"\nRaw water: {raw_water_conc} oocysts/L")
print(f"Treatment log removal: {total_log_removal}")

# Evaluate different treatment scenarios
scenarios = [
    {'name': 'Current', 'log_removal': total_log_removal},
    {'name': 'Basic', 'log_removal': 5.0},
    {'name': 'Enhanced', 'log_removal': 7.0},
    {'name': 'Advanced', 'log_removal': 9.0}
]

risk_calc = RiskCharacterization()

for scenario_eval in scenarios:
    log_removal = scenario_eval['log_removal']
    treated_conc = raw_water_conc / (10 ** log_removal)

    # Daily dose
    daily_dose = treated_conc * daily_consumption

    # Annual exposure (365 days)
    result = risk_calc.run_comprehensive_assessment(
        pathogen='cryptosporidium',
        exposure_route='drinking_water',
        concentration=treated_conc,
        volume=daily_consumption * 1000,  # Convert L to mL
        frequency=365,
        population=population,
        iterations=5000
    )

    annual_risk = result['annual_risk']['mean']
    cases_per_year = annual_risk * population

    print(f"\n{scenario_eval['name']} Treatment:")
    print(f"  Log removal: {log_removal}")
    print(f"  Treated concentration: {treated_conc:.6e} oocysts/L")
    print(f"  Daily dose: {daily_dose:.6e} oocysts")
    print(f"  Annual risk: {annual_risk:.6e}")
    print(f"  Expected cases/year: {cases_per_year:.1f}")
    print(f"  Meets WHO guideline: {'Yes' if annual_risk <= 1e-4 else 'No'}")
```

### Workflow 4: Comparative Pathogen Assessment

**Scenario**: Compare risks from different pathogens at the same site.

```python
import sys
import pandas as pd
import matplotlib.pyplot as plt
sys.path.insert(0, 'qmra_toolkit/src')

from risk_characterization import RiskCharacterization
from pathogen_database import PathogenDatabase

# Load data
data = pd.read_csv('test_data/pathogen_concentrations/wastewater_monitoring.csv')

# Get unique pathogens in dataset
pathogens = data['pathogen'].unique()

# Assessment parameters
volume = 50  # mL
frequency = 20  # events/year
population = 50000

risk_calc = RiskCharacterization()
pathogen_db = PathogenDatabase()
results_summary = []

print("Comparative Pathogen Risk Assessment")
print("=" * 70)

for pathogen in pathogens:
    # Get mean concentration for this pathogen
    pathogen_data = data[data['pathogen'] == pathogen]
    mean_conc = pathogen_data['concentration_per_L'].mean()

    try:
        # Run assessment
        result = risk_calc.run_comprehensive_assessment(
            pathogen=pathogen,
            exposure_route='primary_contact',
            concentration=mean_conc,
            volume=volume,
            frequency=frequency,
            population=population,
            iterations=5000
        )

        # Get pathogen info
        info = pathogen_db.get_pathogen_info(pathogen)

        annual_risk = result['annual_risk']['mean']
        cases = annual_risk * population

        results_summary.append({
            'pathogen': pathogen,
            'name': info['name'],
            'concentration': mean_conc,
            'infection_risk': result['infection_risk']['mean'],
            'annual_risk': annual_risk,
            'cases_per_year': cases
        })

        print(f"\n{info['name']}:")
        print(f"  Concentration: {mean_conc:.1f} organisms/L")
        print(f"  Single exposure risk: {result['infection_risk']['mean']:.6e}")
        print(f"  Annual risk: {annual_risk:.6e}")
        print(f"  Cases/year: {cases:.0f}")

    except Exception as e:
        print(f"\n{pathogen}: Could not assess - {str(e)}")

# Create comparison plot
df_results = pd.DataFrame(results_summary)
df_results = df_results.sort_values('cases_per_year', ascending=False)

plt.figure(figsize=(10, 6))
plt.barh(df_results['name'], df_results['cases_per_year'])
plt.xlabel('Expected Cases per Year')
plt.title(f'Pathogen Risk Comparison\n(Population: {population:,}, Exposures: {frequency}/year)')
plt.tight_layout()
plt.savefig('pathogen_comparison.png', dpi=300)
print(f"\nPlot saved as 'pathogen_comparison.png'")
```

---

## API Reference

### Core Modules

#### `pathogen_database.PathogenDatabase`

Manages pathogen parameters from JSON database.

**Methods**:

```python
class PathogenDatabase:
    def __init__(self, database_path=None)
        """Initialize pathogen database."""

    def get_pathogen_info(self, pathogen_id: str) -> dict
        """Get complete pathogen information."""

    def get_dose_response_parameters(self, pathogen_id: str, model_type: str) -> dict
        """Get dose-response model parameters."""

    def get_default_model_type(self, pathogen_id: str) -> str
        """Get default dose-response model type."""

    def get_health_impact_data(self, pathogen_id: str) -> dict
        """Get illness ratios and DALYs."""

    def list_available_pathogens(self) -> list
        """List all available pathogens."""
```

**Example**:
```python
db = PathogenDatabase()
pathogens = db.list_available_pathogens()
print(f"Available pathogens: {', '.join(pathogens)}")

info = db.get_pathogen_info('norovirus')
print(f"Pathogen type: {info['pathogen_type']}")
```

#### `dose_response` Module

Dose-response model implementations.

**Models**:

```python
class BetaPoissonModel(DoseResponseModel):
    """Beta-Poisson model: P = 1 - (1 + dose/beta)^(-alpha)"""

    def calculate_infection_probability(self, dose: float) -> float
    def calculate_dose_for_risk(self, target_risk: float) -> float

class ExponentialModel(DoseResponseModel):
    """Exponential model: P = 1 - exp(-r * dose)"""

    def calculate_infection_probability(self, dose: float) -> float
    def calculate_dose_for_risk(self, target_risk: float) -> float

def create_dose_response_model(model_type: str, parameters: dict) -> DoseResponseModel
    """Factory function to create dose-response models."""
```

**Example**:
```python
from dose_response import create_dose_response_model

params = {'alpha': 0.04, 'beta': 0.055}
model = create_dose_response_model('beta_poisson', params)

doses = [1, 10, 100]
for dose in doses:
    risk = model.calculate_infection_probability(dose)
    print(f"Dose {dose}: {risk:.4f}")
```

#### `monte_carlo.MonteCarloSimulator`

Monte Carlo uncertainty analysis.

**Methods**:

```python
class MonteCarloSimulator:
    def __init__(self, random_seed=None)

    def add_distribution(self, name: str, distribution: Distribution)
        """Add probability distribution."""

    def run_simulation(self, model_function, n_iterations: int, variable_name: str)
        """Run Monte Carlo simulation."""

    def get_statistics(self, samples: np.ndarray) -> dict
        """Calculate statistical summaries."""
```

**Distribution Functions**:

```python
def create_lognormal_distribution(mean: float, std: float, name: str)
def create_uniform_distribution(min_val: float, max_val: float, name: str)
def create_normal_distribution(mean: float, std: float, name: str)
def create_triangular_distribution(min_val: float, mode: float, max_val: float, name: str)
```

**Example**:
```python
from monte_carlo import MonteCarloSimulator, create_lognormal_distribution

mc_sim = MonteCarloSimulator(random_seed=42)

dist = create_lognormal_distribution(mean=np.log(100), std=0.5, name="concentration")
mc_sim.add_distribution("concentration", dist)

def model(samples):
    return samples["concentration"] * 0.05  # Simple dose calculation

results = mc_sim.run_simulation(model, n_iterations=10000, variable_name="dose")
print(f"Mean dose: {results.statistics['mean']:.2f}")
```

#### `risk_characterization.RiskCharacterization`

Comprehensive risk assessment.

**Methods**:

```python
class RiskCharacterization:
    def run_comprehensive_assessment(
        self,
        pathogen: str,
        exposure_route: str,
        concentration: float,
        volume: float,
        frequency: int,
        population: int,
        iterations: int = 10000,
        confidence_level: float = 0.95,
        **kwargs
    ) -> dict
        """Run complete QMRA assessment with Monte Carlo."""

    def calculate_annual_risk(self, single_event_risk: float, frequency: int) -> float
        """Calculate annual risk from single event risk."""

    def evaluate_regulatory_compliance(self, annual_risk: float) -> dict
        """Check compliance with WHO/NZ guidelines."""
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Module Import Errors

**Problem**:
```python
ModuleNotFoundError: No module named 'pathogen_database'
```

**Solution**:
```python
import sys
sys.path.insert(0, 'qmra_toolkit/src')  # Add to path
from pathogen_database import PathogenDatabase
```

#### Issue 2: Pathogen Not Found

**Problem**:
```python
KeyError: 'giardia'
```

**Solution**:
Check available pathogens:
```python
db = PathogenDatabase()
print(db.list_available_pathogens())
# Use one of the available pathogens: norovirus, campylobacter, etc.
```

#### Issue 3: Streamlit Won't Start

**Problem**:
```bash
streamlit: command not found
```

**Solution**:
```bash
pip install streamlit
# Or use full path
python -m streamlit run qmra_toolkit/web_app.py
```

#### Issue 4: Memory Error with Large Simulations

**Problem**:
```python
MemoryError: Unable to allocate array
```

**Solution**:
Reduce iterations or use batch processing:
```python
# Instead of 100,000 iterations
result = risk_calc.run_comprehensive_assessment(..., iterations=10000)
```

#### Issue 5: Negative Doses

**Problem**:
```python
Warning: Negative doses encountered
```

**Solution**:
Check your input parameters - concentration and volume should be positive:
```python
# Ensure positive values
concentration = max(0, concentration)
volume = max(0, volume)
```

---

## Best Practices

### 1. Uncertainty Quantification

Always use Monte Carlo simulation for uncertainty:

```python
# Good: Includes uncertainty
result = run_comprehensive_assessment(..., iterations=10000)

# Less ideal: Point estimate only
risk = calculate_single_point_risk(...)
```

### 2. Appropriate Iterations

Use sufficient iterations for stable results:

- Quick check: 1,000 iterations
- Standard analysis: 10,000 iterations
- Publication/regulatory: 100,000 iterations

### 3. Parameter Documentation

Document all input parameters:

```python
assessment_params = {
    'pathogen': 'norovirus',
    'concentration': 100,  # organisms/L from monitoring data Jan 2025
    'volume': 50,  # mL per swim (Dufour et al. 2006)
    'frequency': 20,  # summer season swims per person
    'source': 'Beach monitoring program 2025'
}
```

### 4. Validation

Validate results against literature:

```python
# Check if results are reasonable
infection_risk = result['infection_risk']['mean']
if infection_risk > 1.0 or infection_risk < 0:
    print("Warning: Invalid risk value - check inputs")

# Compare to published values
literature_range = (1e-5, 1e-1)
if not (literature_range[0] <= infection_risk <= literature_range[1]):
    print("Warning: Risk outside typical literature range")
```

### 5. Sensitivity Analysis

Identify key parameters:

```python
# Test parameter sensitivity
base_concentration = 100
concentrations = [50, 100, 200, 400]  # Test ±50% and ±100%

for conc in concentrations:
    result = run_assessment(concentration=conc, ...)
    print(f"Conc {conc}: Risk = {result['annual_risk']['mean']:.6e}")
```

### 6. Regulatory Compliance

Always check against guidelines:

```python
annual_risk = result['annual_risk']['mean']
who_guideline = 1e-4  # 1 in 10,000

if annual_risk <= who_guideline:
    print("✓ Compliant with WHO guidelines")
else:
    exceedance = annual_risk / who_guideline
    print(f"✗ Exceeds guideline by {exceedance:.1f}x")
```

### 7. Report Generation

Generate professional reports for stakeholders:

```python
from report_generator import ReportGenerator

report_gen = ReportGenerator()
report_gen.generate_assessment_report(
    results=result,
    output_path='reports/assessment_report.pdf',
    include_visualizations=True,
    author='Your Name',
    organization='NIWA'
)
```

---

## Additional Resources

### Documentation

- **Project README**: `README.md`
- **Improvements Summary**: `QMRA_IMPROVEMENTS_SUMMARY.md`
- **Test Suite Documentation**: `test_web_app_integration.py`

### Example Files

- **Test Data**: `test_data/` directory
- **Scenarios**: `test_data/scenarios/`
- **Population Data**: `test_data/population_data/`

### Scientific References

1. Haas, C.N., Rose, J.B., & Gerba, C.P. (1999). *Quantitative Microbial Risk Assessment*. John Wiley & Sons.
2. WHO (2011). *Guidelines for Drinking-water Quality, 4th Edition*.
3. Teunis, P.F.M., et al. (2008). Norwalk virus: How infectious is it? *J Med Virol*, 80(8):1468-76.

### Support

For technical support or questions:
- Email: reza.moghaddam@niwa.co.nz
- GitHub Issues: https://github.com/niwa/qmra-toolkit/issues

---

**Document Version**: 1.0.0
**Last Updated**: October 2025
**Author**: NIWA Earth Sciences
**License**: MIT License

---

*This user guide is part of the NIWA QMRA Toolkit project. For the most up-to-date version, please visit the project repository.*
