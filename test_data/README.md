# QMRA Toolkit - Test Data

This directory contains dummy/test data for demonstrating and testing the QMRA Toolkit functionality.

## Directory Structure

```
test_data/
├── pathogen_concentrations/    # Monitoring data from various sources
│   ├── wastewater_monitoring.csv
│   ├── treated_effluent.csv
│   └── beach_monitoring.csv
├── scenarios/                   # Pre-configured assessment scenarios
│   ├── recreational_swimming.json
│   ├── shellfish_consumption.json
│   └── drinking_water.json
└── population_data/            # Population and demographic data
    └── auckland_population.csv
```

## Data Files Description

### 1. Pathogen Concentrations

#### `wastewater_monitoring.csv`

Raw wastewater influent monitoring data from two treatment plants.

**Columns**:
- `date`: Sampling date
- `site_id`: Treatment plant identifier
- `pathogen`: Pathogen name (norovirus, campylobacter, e_coli, etc.)
- `concentration_per_L`: Organisms per liter
- `sample_volume_mL`: Sample volume analyzed
- `detection_method`: qPCR, Culture, or Microscopy
- `notes`: Additional information

**Example Usage**:
```python
import pandas as pd
data = pd.read_csv('test_data/pathogen_concentrations/wastewater_monitoring.csv')
norovirus = data[data['pathogen'] == 'norovirus']
print(f"Mean concentration: {norovirus['concentration_per_L'].mean():.1f} org/L")
```

#### `treated_effluent.csv`

Treated wastewater effluent with dilution and distance information.

**Columns**:
- `date`: Sampling date
- `site_id`: Treatment plant identifier
- `pathogen`: Pathogen name
- `concentration_per_L`: Organisms per liter (post-treatment)
- `treatment_type`: Secondary or Tertiary
- `dilution_factor`: Dilution from raw influent
- `distance_from_discharge_m`: Distance from discharge point
- `notes`: Additional information

**Example Usage**:
```python
import pandas as pd
data = pd.read_csv('test_data/pathogen_concentrations/treated_effluent.csv')
# Calculate reduction from treatment
discharge_point = data[data['distance_from_discharge_m'] == 0]
print(discharge_point.groupby('pathogen')['concentration_per_L'].mean())
```

#### `beach_monitoring.csv`

Recreational beach water quality monitoring data.

**Columns**:
- `date`: Sampling date
- `beach_name`: Beach name
- `location_code`: Monitoring location code
- `pathogen`: Pathogen name
- `concentration_per_L`: Organisms per liter
- `water_temp_C`: Water temperature (°C)
- `salinity_ppt`: Salinity (parts per thousand)
- `weather_condition`: Weather during sampling
- `notes`: Additional information (e.g., proximity to outlets)

**Example Usage**:
```python
import pandas as pd
data = pd.read_csv('test_data/pathogen_concentrations/beach_monitoring.csv')
takapuna = data[data['beach_name'] == 'Takapuna Beach']
print(f"Mean norovirus: {takapuna[takapuna['pathogen']=='norovirus']['concentration_per_L'].mean():.2f} org/L")
```

### 2. Scenarios

#### `recreational_swimming.json`

Complete recreational swimming assessment scenario for Auckland beaches.

**Key Parameters**:
- **Pathogen**: Norovirus
- **Exposure Route**: Primary contact (swimming)
- **Concentration**: 0.5 org/L
- **Volume**: 50 mL per swim
- **Frequency**: 20 swims per summer
- **Population**: 100,000 beach visitors

**Includes**:
- Uncertainty distributions (lognormal, uniform)
- Environmental conditions (temperature, salinity)
- Dilution modeling parameters
- Regulatory targets (WHO guidelines)
- Age-stratified population data

**Example Usage**:
```python
import json
with open('test_data/scenarios/recreational_swimming.json', 'r') as f:
    scenario = json.load(f)
print(f"Scenario: {scenario['scenario_name']}")
print(f"Target risk: {scenario['regulatory_targets']['target_annual_risk']}")
```

#### `shellfish_consumption.json`

Shellfish (mussels, oysters) harvesting and consumption scenario.

**Key Parameters**:
- **Pathogen**: Norovirus
- **Exposure Route**: Shellfish consumption
- **Concentration**: 10 org/g in shellfish tissue
- **Serving Size**: 100 g
- **Frequency**: 12 servings per year (monthly)
- **Population**: 75,000 consumers

**Includes**:
- Bioaccumulation factors
- Depuration time (48 hours)
- Cooking reduction factors
- Shellfish quality standards
- Harvesting area information

**Example Usage**:
```python
import json
with open('test_data/scenarios/shellfish_consumption.json', 'r') as f:
    scenario = json.load(f)
shellfish_conc = scenario['exposure_parameters']['pathogen_concentration_in_shellfish_per_g']
serving = scenario['exposure_parameters']['shellfish_serving_size_g']
dose = shellfish_conc * serving
print(f"Dose per serving: {dose} organisms")
```

#### `drinking_water.json`

Municipal drinking water supply assessment scenario.

**Key Parameters**:
- **Pathogen**: Cryptosporidium (primary), also includes Campylobacter and E. coli
- **Raw Water**: 5.0 oocysts/L
- **Treated Water**: 0.001 oocysts/L (5 log removal)
- **Daily Consumption**: 2 L per person
- **Frequency**: 365 days per year
- **Population**: 500,000 served

**Includes**:
- Multi-barrier treatment system
  - Coagulation/flocculation: 2 log removal
  - Filtration: 3 log removal
  - UV disinfection: 4 log inactivation
- Source water characterization
- Vulnerable population subgroups
- NZ Drinking Water Standards compliance

**Example Usage**:
```python
import json
with open('test_data/scenarios/drinking_water.json', 'r') as f:
    scenario = json.load(f)
treatment = scenario['treatment_barriers']
total_log_removal = sum([
    treatment['coagulation_flocculation']['log_removal'],
    treatment['filtration']['log_removal'],
    treatment['disinfection']['log_inactivation']
])
print(f"Total log removal: {total_log_removal}")
```

### 3. Population Data

#### `auckland_population.csv`

Demographic data for Auckland regions with exposure activity estimates.

**Columns**:
- `area_name`: Region name
- `area_code`: Region code
- `total_population`: Total population
- `households`: Number of households
- `age_0_5`, `age_6_12`, `age_13_18`, `age_19_65`, `age_65plus`: Age-stratified population
- `swimmers_estimate`: Estimated number of swimmers
- `shellfish_consumers`: Estimated shellfish consumers
- `water_consumers`: People on municipal water supply

**Example Usage**:
```python
import pandas as pd
pop_data = pd.read_csv('test_data/population_data/auckland_population.csv')
total_row = pop_data[pop_data['area_code'] == 'AKL-ALL']
print(f"Total Auckland population: {total_row['total_population'].values[0]:,}")
print(f"Swimmers: {total_row['swimmers_estimate'].values[0]:,}")
```

## Data Generation

All data in this directory is **dummy/synthetic data** created for testing and demonstration purposes.

Values are realistic and based on typical ranges from published literature, but should not be used for actual regulatory submissions or decision-making.

## Creating Custom Test Data

### CSV Files

You can create custom CSV files with the same format:

```python
import pandas as pd

custom_data = pd.DataFrame({
    'date': ['2025-01-15', '2025-01-16'],
    'pathogen': ['norovirus', 'norovirus'],
    'concentration_per_L': [120.0, 135.0]
})

custom_data.to_csv('test_data/my_custom_data.csv', index=False)
```

### JSON Scenarios

Create custom scenarios by modifying the templates:

```python
import json

custom_scenario = {
    "scenario_name": "My Custom Scenario",
    "pathogen": "campylobacter",
    "exposure_route": "primary_contact",
    "exposure_parameters": {
        "concentration_per_L": 50,
        "ingestion_volume_mL": 30,
        "exposure_frequency_per_year": 15
    },
    "population": {
        "total_population": 25000
    }
}

with open('test_data/scenarios/my_custom_scenario.json', 'w') as f:
    json.dump(custom_scenario, f, indent=2)
```

## Using Test Data in Assessments

### Web Application

1. Start the web app: `streamlit run qmra_toolkit/web_app.py`
2. Navigate to "Batch Assessment" tab
3. Upload CSV file from `pathogen_concentrations/`
4. Or use "Load Scenario" to import JSON files

### Python API

```python
import pandas as pd
import json
import sys
sys.path.insert(0, 'qmra_toolkit/src')

from risk_characterization import RiskCharacterization

# Load scenario
with open('test_data/scenarios/recreational_swimming.json', 'r') as f:
    scenario = json.load(f)

# Run assessment
risk_calc = RiskCharacterization()
result = risk_calc.run_comprehensive_assessment(
    pathogen=scenario['pathogen'],
    exposure_route=scenario['exposure_route'],
    concentration=scenario['exposure_parameters']['concentration_per_L'],
    volume=scenario['exposure_parameters']['ingestion_volume_mL'],
    frequency=scenario['exposure_parameters']['exposure_frequency_per_year'],
    population=scenario['population']['total_population'],
    iterations=10000
)

print(f"Annual risk: {result['annual_risk']['mean']:.6e}")
```

### Desktop GUI

1. Launch GUI: `python qmra_toolkit/src/enhanced_qmra_gui.py`
2. Go to "Setup" tab
3. Click "Load Scenario" button
4. Select JSON file from `scenarios/`
5. Parameters will auto-populate

## Data Validation

Test data has been validated for:
- ✓ Realistic concentration ranges (based on literature)
- ✓ Proper units and formatting
- ✓ Consistent pathogen names
- ✓ Valid date formats (YYYY-MM-DD)
- ✓ Positive values for concentrations
- ✓ Proper JSON structure for scenarios

## References

Concentration ranges based on:

1. **Norovirus**: Teunis et al. (2008), Sano et al. (2016)
   - Raw wastewater: 10^5 - 10^7 copies/L
   - Treated effluent: 10^2 - 10^4 copies/L
   - Recreational water: 10^0 - 10^2 copies/L

2. **Campylobacter**: Savichtcheva & Okabe (2006)
   - Raw wastewater: 10^4 - 10^6 CFU/L
   - Treated effluent: 10^1 - 10^3 CFU/L

3. **Cryptosporidium**: Medema et al. (2006)
   - Raw wastewater: 10^1 - 10^3 oocysts/L
   - Surface water: 10^-1 - 10^1 oocysts/L

4. **E. coli O157:H7**: Haas et al. (1999)
   - Raw wastewater: 10^4 - 10^6 CFU/L
   - Recreational water: 10^0 - 10^2 CFU/L

## Support

For questions about test data or to request additional scenarios:
- Email: reza.moghaddam@niwa.co.nz
- See: QMRA_TOOLKIT_USER_GUIDE.md for comprehensive usage examples

---

**Last Updated**: October 2025
**Version**: 1.0.0
