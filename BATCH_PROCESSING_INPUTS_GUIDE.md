# QMRA Toolkit - Batch Processing Inputs Guide

**Version**: 1.0
**Date**: October 2025
**Author**: NIWA Earth Sciences New Zealand

---

## Table of Contents

1. [Overview](#overview)
2. [Batch Processing Use Cases](#batch-processing-use-cases)
3. [Input File Formats](#input-file-formats)
4. [Batch Input Types](#batch-input-types)
5. [Complete Examples](#complete-examples)
6. [Best Practices](#best-practices)

---

## Overview

Batch processing allows you to run multiple QMRA assessments automatically by providing structured input files. This is ideal for:

- **Multi-site assessments** (comparing risks at different locations)
- **Treatment scenario comparison** (evaluating different treatment options)
- **Temporal analysis** (analyzing risks across time periods)
- **Sensitivity analysis** (testing parameter variations)
- **Regulatory reporting** (generating comprehensive risk profiles)

---

## Batch Processing Use Cases

### Use Case 1: Multi-Site Risk Assessment
**Goal**: Assess risk at multiple locations along a coastline
**Inputs**: Dilution factors for each site, single pathogen concentration
**Output**: Risk comparison table and spatial risk profile

### Use Case 2: Treatment Scenario Comparison
**Goal**: Compare effectiveness of different treatment systems
**Inputs**: Multiple treatment configurations (LRV values), baseline concentration
**Output**: Cost-benefit analysis, compliance status per scenario

### Use Case 3: Multi-Pathogen Assessment
**Goal**: Assess risks from multiple pathogens simultaneously
**Inputs**: Concentrations for 6 pathogens, same exposure parameters
**Output**: Dominant pathogen identification, combined risk profile

### Use Case 4: Temporal Risk Analysis
**Goal**: Understand seasonal risk variations
**Inputs**: Weekly monitoring data (52 weeks), seasonal dilution
**Output**: Seasonal risk trends, peak risk periods

### Use Case 5: Sensitivity Analysis
**Goal**: Identify most influential parameters
**Inputs**: Parameter ranges (concentration, LRV, dilution, volume)
**Output**: Parameter importance ranking, tornado diagrams

---

## Input File Formats

### 1. CSV Format (Tabular Data)

Best for:
- Time-series data
- Multi-site dilution factors
- Pathogen monitoring results
- Multiple scenarios with similar structure

**Advantages**: Easy to create in Excel, compatible with databases
**Limitations**: Cannot represent hierarchical relationships

### 2. YAML Format (Configuration Files)

Best for:
- Complex scenario definitions
- Treatment barrier configurations
- Exposure parameter distributions
- Hierarchical data structures

**Advantages**: Human-readable, supports comments, hierarchical structure
**Limitations**: Requires careful indentation, less familiar to non-programmers

### 3. JSON Format (Data Exchange)

Best for:
- API integrations
- Automated workflows
- Programmatic generation
- Data exchange between systems

**Advantages**: Machine-readable, widely supported, structured
**Limitations**: Less human-readable, no comments

---

## Batch Input Types

### Type 1: Pathogen Concentration Batch Input (CSV)

**Purpose**: Run assessments for multiple monitoring samples or time periods

**File Structure**:
```csv
Sample_Date,Sample_Type,Norovirus_copies_per_L,E_coli_MPN_per_100mL,Cryptosporidium_oocysts_per_L,Enterococcus_MPN_per_100mL,Sample_Volume_L,Detection_Limit,Laboratory,QC_Flag
2024-01-07,Treated_Effluent,440.40,642.76,4.75,428.02,3.35,10,NIWA Christchurch,Pass
2024-01-14,Treated_Effluent,2067.33,159.79,9.51,128.85,3.98,10,NIWA Christchurch,Pass
2024-01-21,Treated_Effluent,3419.33,30.23,0.75,256.34,2.73,10,NIWA Christchurch,Pass
```

**Required Columns**:
- `Sample_Date` (YYYY-MM-DD format)
- `Sample_Type` (e.g., Raw_Influent, Treated_Effluent, Receiving_Water)
- `[Pathogen]_copies_per_L` or `[Pathogen]_MPN_per_100mL` (numeric, > 0)
- `QC_Flag` (Pass/Fail) - optional but recommended

**Optional Columns**:
- `Sample_Volume_L` - volume analyzed
- `Detection_Limit` - analytical detection limit
- `Laboratory` - lab performing analysis
- `Temperature_C` - water temperature
- `pH` - pH value

**Usage**:
```python
import pandas as pd
from qmra_toolkit import batch_processor

# Load pathogen concentration data
pathogen_data = pd.read_csv('treated_effluent_pathogens_2024.csv')

# Run batch assessment for each sample
results = batch_processor.run_temporal_assessment(
    concentration_file='treated_effluent_pathogens_2024.csv',
    pathogen='norovirus',
    exposure_route='primary_contact',
    dilution_factor=100,
    volume_ml=50,
    frequency_per_year=20,
    population=10000,
    output_file='temporal_risk_results.csv'
)
```

**Output**:
```csv
Sample_Date,Concentration,Infection_Risk_Median,Illness_Risk_Median,Annual_Risk_Median,Population_Impact,Compliance_Status
2024-01-07,440.40,1.23e-03,8.61e-04,2.45e-02,245,NON-COMPLIANT
2024-01-14,2067.33,5.67e-03,3.97e-03,1.08e-01,1080,NON-COMPLIANT
```

---

### Type 2: Multi-Site Dilution Batch Input (CSV)

**Purpose**: Assess risk at multiple locations with different dilution factors

**File Structure**:
```csv
Simulation_ID,Site_Name,Distance_m,Dilution_Factor,Tidal_State,Wind_Speed_ms,Current_Speed_ms,Model_Type,Confidence
1,Discharge,0,1.0,High,7.45,0.24,ROMS_Hydrodynamic,High
101,Site_50m,50,7.4,High,7.45,0.24,ROMS_Hydrodynamic,High
201,Site_100m,100,13.6,High,7.45,0.24,ROMS_Hydrodynamic,High
301,Site_250m,250,41.8,High,7.45,0.24,ROMS_Hydrodynamic,High
401,Site_500m,500,125.3,High,7.45,0.24,ROMS_Hydrodynamic,High
501,Site_1000m,1000,387.5,High,7.45,0.24,ROMS_Hydrodynamic,High
```

**Required Columns**:
- `Site_Name` - unique identifier for each location
- `Distance_m` - distance from discharge point
- `Dilution_Factor` - dilution at this site (≥ 1.0)

**Optional Columns**:
- `Tidal_State` - High, Mid, Low
- `Wind_Speed_ms` - wind speed in m/s
- `Current_Speed_ms` - current speed in m/s
- `Model_Type` - hydrodynamic model used
- `Confidence` - High, Medium, Low

**Usage**:
```python
from qmra_toolkit import batch_processor

# Run multi-site assessment
results = batch_processor.run_spatial_assessment(
    dilution_file='hydrodynamic_dilution_modeling_1000runs.csv',
    pathogen='norovirus',
    effluent_concentration=1e6,  # 1 million copies/L
    exposure_route='primary_contact',
    volume_ml=50,
    frequency_per_year=20,
    population=10000,
    output_file='spatial_risk_profile.csv'
)
```

**Output**:
```csv
Site_Name,Distance_m,Dilution_Factor,Receiving_Water_Conc,Infection_Risk,Annual_Risk,Population_Impact,Compliance_Status,Required_Additional_LRV
Discharge,0,1.0,1.00e+06,9.99e-01,1.00e+00,10000,NON-COMPLIANT,6.0
Site_50m,50,7.4,1.35e+05,9.85e-01,1.00e+00,10000,NON-COMPLIANT,5.1
Site_100m,100,13.6,7.35e+04,9.65e-01,1.00e+00,9650,NON-COMPLIANT,4.9
Site_250m,250,41.8,2.39e+04,8.92e-01,1.00e+00,8920,NON-COMPLIANT,4.4
Site_500m,500,125.3,7.98e+03,7.25e-01,1.00e+00,7250,NON-COMPLIANT,3.9
Site_1000m,1000,387.5,2.58e+03,3.98e-01,1.00e+00,3980,NON-COMPLIANT,3.6
```

---

### Type 3: Treatment Scenario Batch Input (YAML)

**Purpose**: Compare multiple treatment configurations

**File Structure** - `secondary_treatment.yaml`:
```yaml
scenario_name: Secondary Biological Treatment
description: Activated sludge with secondary clarification
treatment_barriers:
  - name: Screening
    type: physical
    lrv: 0.2
    variability: 0.1

  - name: Primary Settling
    type: physical
    lrv: 0.8
    variability: 0.3

  - name: Activated Sludge
    type: biological
    lrv: 1.5
    variability: 0.5
    description: Aerobic biological treatment
    srt_days: 10
    hrt_hours: 8

  - name: Secondary Clarifier
    type: physical
    lrv: 0.5
    variability: 0.2

total_log_reduction: 3.0

pathogen_specific_lrv:
  cryptosporidium: 2.5
  norovirus: 2.0
  bacteria: 3.5
```

**File Structure** - `advanced_uv_treatment.yaml`:
```yaml
scenario_name: Advanced UV Disinfection
description: Secondary treatment plus UV disinfection
treatment_barriers:
  - name: Screening
    type: physical
    lrv: 0.2
    variability: 0.1

  - name: Primary Settling
    type: physical
    lrv: 0.8
    variability: 0.3

  - name: Activated Sludge
    type: biological
    lrv: 1.5
    variability: 0.5

  - name: Secondary Clarifier
    type: physical
    lrv: 0.5
    variability: 0.2

  - name: UV Disinfection
    type: chemical
    lrv: 5.0
    variability: 0.3
    uv_dose_mj_cm2: 100
    transmission_percent: 65

total_log_reduction: 8.0

pathogen_specific_lrv:
  cryptosporidium: 7.5
  norovirus: 6.0
  bacteria: 8.5
```

**Required Fields**:
- `scenario_name` - descriptive name
- `treatment_barriers` - list of treatment steps
  - `name` - barrier name
  - `type` - physical, biological, chemical
  - `lrv` - log reduction value (0-10)
- `total_log_reduction` - sum of all LRVs

**Optional Fields**:
- `variability` - uncertainty in LRV (standard deviation)
- `pathogen_specific_lrv` - different LRV per pathogen type
- Treatment-specific parameters (srt_days, hrt_hours, uv_dose, etc.)

**Usage**:
```python
from qmra_toolkit import batch_processor

# List of treatment scenario files
treatment_scenarios = [
    'bypass_no_treatment.yaml',
    'primary_treatment.yaml',
    'secondary_treatment.yaml',
    'advanced_uv_treatment.yaml'
]

# Run batch treatment comparison
results = batch_processor.run_treatment_comparison(
    treatment_files=treatment_scenarios,
    pathogen='norovirus',
    raw_concentration=1e6,
    dilution_factor=100,
    exposure_route='primary_contact',
    volume_ml=50,
    frequency_per_year=20,
    population=10000,
    output_file='treatment_comparison_results.xlsx'
)
```

**Output**:
```csv
Treatment_Scenario,Total_LRV,Post_Treatment_Conc,Final_Conc_After_Dilution,Infection_Risk,Annual_Risk,Population_Impact,Compliance_Status,Cost_Benefit_Ratio
Bypass (No Treatment),0.0,1.00e+06,1.00e+04,9.99e-01,1.00e+00,10000,NON-COMPLIANT,N/A
Primary Treatment,1.0,1.00e+05,1.00e+03,9.85e-01,1.00e+00,9850,NON-COMPLIANT,Low
Secondary Treatment,3.0,1.00e+03,1.00e+01,3.41e-01,1.00e+00,3410,NON-COMPLIANT,Medium
Advanced UV Treatment,8.0,1.00e-02,1.00e-04,2.06e-06,4.12e-05,0.4,COMPLIANT,High
```

---

### Type 4: Exposure Scenario Batch Input (YAML)

**Purpose**: Define complex exposure scenarios with distributions

**File Structure** - `swimming_scenario.yaml`:
```yaml
scenario_name: Recreational Swimming - Summer Season
exposure_route: primary_contact
description: Swimming at beach near wastewater outfall during summer

population:
  size: 10000
  age_distribution:
    children_0_5: 0.1
    children_6_12: 0.15
    adults_13_64: 0.65
    elderly_65plus: 0.1

exposure_parameters:
  water_ingestion_volume_mL:
    distribution: lognormal
    meanlog: 3.5
    sdlog: 0.5
    source: Dufour et al. (2006)

  exposure_duration_minutes: 60

  events_per_year:
    distribution: poisson
    lambda: 20
    description: Swimming events per summer season

  season: November to March
  peak_usage_days: 90

pathogen: norovirus

site_locations:
  - Site_100m
  - Site_250m
  - Site_500m

risk_threshold: 0.001
assessment_year: 2024
```

**Required Fields**:
- `scenario_name` - descriptive name
- `exposure_route` - primary_contact, shellfish_consumption, drinking_water
- `population.size` - number of exposed people
- `exposure_parameters` - ingestion volume, frequency, etc.
- `pathogen` - target pathogen

**Optional Fields**:
- `age_distribution` - demographics
- `season` - temporal definition
- `site_locations` - list of sites to assess
- Parameter distributions (lognormal, poisson, etc.)

---

### Type 5: Batch Scenario Master File (CSV)

**Purpose**: Define multiple complete scenarios in a single spreadsheet

**File Structure** - `batch_scenarios.csv`:
```csv
Scenario_ID,Scenario_Name,Pathogen,Exposure_Route,Effluent_Conc,Treatment_LRV,Dilution_Factor,Volume_mL,Frequency_Year,Population,Priority
S001,Beach_A_Summer,norovirus,primary_contact,1000000,3.0,100,50,20,10000,High
S002,Beach_A_Winter,norovirus,primary_contact,1500000,3.0,50,30,5,2000,Medium
S003,Beach_B_Summer,norovirus,primary_contact,800000,3.0,200,50,25,15000,High
S004,Shellfish_Area_1,norovirus,shellfish_consumption,1000000,3.0,800,100,12,500,High
S005,Shellfish_Area_2,norovirus,shellfish_consumption,1200000,3.0,500,100,12,1000,Medium
S006,Campylo_Beach_A,campylobacter,primary_contact,500000,3.5,100,50,20,10000,Low
S007,Crypto_Beach_A,cryptosporidium,primary_contact,50000,2.5,100,50,20,10000,Medium
```

**Required Columns**:
- `Scenario_ID` - unique identifier
- `Scenario_Name` - descriptive name
- `Pathogen` - norovirus, campylobacter, cryptosporidium, e_coli, salmonella, rotavirus
- `Exposure_Route` - primary_contact, shellfish_consumption
- `Effluent_Conc` - pathogen concentration in effluent (copies/L or MPN/100mL)
- `Treatment_LRV` - log reduction value from treatment
- `Dilution_Factor` - environmental dilution (≥ 1.0)
- `Volume_mL` - ingestion volume per exposure event
- `Frequency_Year` - exposure events per year
- `Population` - number of exposed people

**Optional Columns**:
- `Priority` - High, Medium, Low
- `Monte_Carlo_Iterations` - simulation iterations (default 10000)
- `Confidence_Level` - 90, 95, 99 (default 95)
- `Notes` - free text description

**Usage**:
```python
from qmra_toolkit import batch_processor

# Run all scenarios from master file
results = batch_processor.run_batch_scenarios(
    scenario_file='batch_scenarios.csv',
    output_directory='results/',
    generate_individual_reports=True,
    generate_summary_report=True
)
```

**Output Files**:
- `results/S001_Beach_A_Summer_results.csv` - individual results
- `results/S002_Beach_A_Winter_results.csv`
- ...
- `results/batch_summary_report.xlsx` - combined summary with all scenarios

---

## Complete Examples

### Example 1: Seasonal Risk Analysis (52 Weeks)

**Goal**: Understand how risk varies throughout the year

**Input File**: `weekly_monitoring_2024.csv`
```csv
Week,Start_Date,End_Date,Norovirus_Mean,Norovirus_Std,Samples_N,Temperature_C,Rainfall_mm
1,2024-01-01,2024-01-07,1250,420,7,18,25
2,2024-01-08,2024-01-14,1580,510,7,19,15
3,2024-01-15,2024-01-21,2100,680,7,20,8
...
52,2024-12-23,2024-12-29,950,340,7,17,45
```

**Python Code**:
```python
from qmra_toolkit import batch_processor
import matplotlib.pyplot as plt

# Run temporal assessment
results = batch_processor.run_temporal_assessment(
    monitoring_file='weekly_monitoring_2024.csv',
    pathogen='norovirus',
    concentration_column='Norovirus_Mean',
    date_column='Start_Date',
    exposure_route='primary_contact',
    treatment_lrv=3.0,
    dilution_factor=100,
    volume_ml=50,
    frequency_per_year=20,  # applied to each week proportionally
    population=10000,
    output_file='seasonal_risk_2024.csv'
)

# Plot seasonal trends
plt.figure(figsize=(14, 6))
plt.plot(results['Week'], results['Annual_Risk_Median'], marker='o')
plt.axhline(y=1e-6, color='r', linestyle='--', label='WHO Guideline')
plt.xlabel('Week of Year')
plt.ylabel('Annual Risk')
plt.title('Seasonal Microbial Risk Profile - 2024')
plt.legend()
plt.yscale('log')
plt.grid(True, alpha=0.3)
plt.savefig('seasonal_risk_plot.png', dpi=300)
```

**Output Summary**:
- Identify peak risk weeks
- Seasonal patterns (summer vs winter)
- Correlation with rainfall/temperature
- Recommended beach closure periods

---

### Example 2: Multi-Pathogen Comparison

**Goal**: Determine which pathogen poses greatest risk

**Input File**: `multi_pathogen_concentrations.csv`
```csv
Sample_ID,Date,Norovirus,Campylobacter,Cryptosporidium,E_coli,Salmonella,Rotavirus
MP001,2024-06-15,1200,45000,8.5,550000,2500,180
MP002,2024-06-22,1580,62000,12.2,720000,3200,250
MP003,2024-06-29,950,38000,6.8,480000,1800,140
```

**Python Code**:
```python
from qmra_toolkit import batch_processor

pathogens = ['norovirus', 'campylobacter', 'cryptosporidium',
             'e_coli', 'salmonella', 'rotavirus']

# Run assessment for each pathogen
results = batch_processor.run_multi_pathogen_assessment(
    concentration_file='multi_pathogen_concentrations.csv',
    pathogens=pathogens,
    exposure_route='primary_contact',
    treatment_lrv=3.0,
    dilution_factor=100,
    volume_ml=50,
    frequency_per_year=20,
    population=10000,
    output_file='multi_pathogen_comparison.xlsx'
)

# Generate comparison report
batch_processor.generate_pathogen_ranking_report(
    results=results,
    output_file='pathogen_risk_ranking.pdf',
    include_sensitivity_analysis=True
)
```

**Output**:
```
Pathogen Risk Ranking (by median annual risk):
1. Norovirus: 3.41e-01 (DOMINANT RISK)
2. Campylobacter: 1.85e-02
3. Cryptosporidium: 8.92e-04
4. E. coli: 2.45e-04
5. Rotavirus: 1.12e-04
6. Salmonella: 5.67e-05

Recommended Priority: Focus treatment on viral removal (Norovirus)
```

---

### Example 3: Treatment Cost-Benefit Analysis

**Goal**: Evaluate treatment upgrade options with cost considerations

**Input File**: `treatment_options_with_costs.yaml`
```yaml
treatment_scenarios:
  - name: Current - Secondary Only
    total_lrv: 3.0
    capital_cost_nzd: 0
    annual_opex_nzd: 250000
    barriers:
      - {name: Primary, lrv: 0.8}
      - {name: Activated Sludge, lrv: 1.5}
      - {name: Clarifier, lrv: 0.7}

  - name: Option A - Add UV
    total_lrv: 7.0
    capital_cost_nzd: 2500000
    annual_opex_nzd: 380000
    barriers:
      - {name: Primary, lrv: 0.8}
      - {name: Activated Sludge, lrv: 1.5}
      - {name: Clarifier, lrv: 0.7}
      - {name: UV Disinfection, lrv: 4.0}

  - name: Option B - Add MBR
    total_lrv: 8.5
    capital_cost_nzd: 5800000
    annual_opex_nzd: 520000
    barriers:
      - {name: Primary, lrv: 0.8}
      - {name: MBR, lrv: 4.5}
      - {name: UV Disinfection, lrv: 3.2}
```

**Python Code**:
```python
from qmra_toolkit import batch_processor

results = batch_processor.run_treatment_cost_benefit_analysis(
    treatment_config='treatment_options_with_costs.yaml',
    pathogen='norovirus',
    raw_concentration=1e6,
    dilution_factor=100,
    exposure_route='primary_contact',
    population=10000,
    daly_cost_per_case=50000,  # NZD value of statistical life-year
    discount_rate=0.06,
    analysis_period_years=30,
    output_file='cost_benefit_analysis.xlsx'
)
```

**Output**:
```
Cost-Benefit Analysis Results (30-year NPV):

Treatment         Capital    Annual OPEX   Total Cost  Cases Avoided  DALYs Avoided  NPV Benefit  Benefit:Cost
Current           $0         $250k        $3.4M       0 (baseline)   0             $0           Baseline
Option A - UV     $2.5M      $380k        $8.0M       3,200/yr       96,000        $135M        16.9:1  ✓ RECOMMENDED
Option B - MBR    $5.8M      $520k        $13.3M      3,380/yr       101,400       $143M        10.7:1  ✓ Viable

Recommendation: Option A (UV) provides best cost-effectiveness
Additional cases avoided vs cost: $2,500 per case (highly cost-effective)
Payback period: 4.2 years
```

---

## Best Practices

### 1. Data Quality
- ✅ Always include QC flags in monitoring data
- ✅ Use detection limits and handle non-detects properly
- ✅ Include metadata (sample volume, laboratory, method)
- ✅ Document data sources and dates

### 2. File Organization
```
project_root/
├── inputs/
│   ├── pathogen_data/
│   │   ├── 2024_monitoring.csv
│   │   └── historical_data.csv
│   ├── dilution_data/
│   │   ├── site_A_dilution.csv
│   │   └── site_B_dilution.csv
│   ├── treatment_scenarios/
│   │   ├── current.yaml
│   │   ├── option_A.yaml
│   │   └── option_B.yaml
│   └── batch_scenarios/
│       └── master_scenario_list.csv
├── outputs/
│   ├── results/
│   ├── reports/
│   └── figures/
└── scripts/
    └── run_batch_assessment.py
```

### 3. Naming Conventions
- Use ISO date format: `YYYY-MM-DD`
- Include version numbers: `treatment_scenarios_v2.yaml`
- Descriptive names: `beach_A_summer_2024.csv` not `data1.csv`
- Consistent pathogen names: `norovirus` not `Noro` or `NV`

### 4. Error Handling
```python
# Always validate inputs before batch processing
from qmra_toolkit import validators

# Validate CSV structure
validators.validate_pathogen_csv('monitoring_data.csv',
                                 required_columns=['Sample_Date', 'Norovirus_copies_per_L'])

# Validate YAML syntax
validators.validate_treatment_yaml('secondary_treatment.yaml')

# Check for missing values
validators.check_data_completeness('batch_scenarios.csv')
```

### 5. Documentation
Always include a README with:
- Data source and collection methods
- Units and conventions
- Quality control procedures
- Assumptions and limitations
- Contact information

**Example README.md**:
```markdown
# Beach Monitoring Data 2024

## Data Source
NIWA Christchurch Laboratory
Samples collected weekly January-December 2024

## Methods
- PCR quantification (ISO 15216-1:2017)
- Sample volume: 1-5 L
- Detection limit: 10 copies/L

## Quality Control
- All samples passed QC checks
- Negative controls included
- Recovery efficiency: 85-110%

## Contact
Dr. Jane Smith - jane.smith@niwa.co.nz
```

### 6. Iterative Processing
For large batch jobs, use checkpointing:
```python
# Process in chunks with progress saving
batch_processor.run_batch_scenarios(
    scenario_file='large_batch.csv',
    checkpoint_frequency=10,  # Save every 10 scenarios
    resume_from_checkpoint=True,  # Resume if interrupted
    output_directory='results/'
)
```

---

## Quick Reference

### Command-Line Batch Processing

```bash
# Multi-site assessment
qmra batch-spatial --dilution hydrodynamic_dilution.csv --pathogen norovirus --output spatial_results.csv

# Temporal assessment
qmra batch-temporal --monitoring weekly_data.csv --pathogen norovirus --output temporal_results.csv

# Treatment comparison
qmra batch-treatment --scenarios treatment_dir/ --pathogen norovirus --output treatment_comparison.xlsx

# Full batch from master file
qmra batch-run --scenarios batch_scenarios.csv --output-dir results/
```

### Python API Quick Start

```python
from qmra_toolkit import batch_processor

# Spatial assessment
results = batch_processor.run_spatial_assessment(
    dilution_file='dilution.csv',
    pathogen='norovirus',
    effluent_concentration=1e6,
    exposure_route='primary_contact',
    output_file='spatial_results.csv'
)

# Temporal assessment
results = batch_processor.run_temporal_assessment(
    monitoring_file='monitoring.csv',
    pathogen='norovirus',
    exposure_route='primary_contact',
    output_file='temporal_results.csv'
)

# Treatment comparison
results = batch_processor.run_treatment_comparison(
    treatment_files=['option1.yaml', 'option2.yaml'],
    pathogen='norovirus',
    output_file='treatment_results.xlsx'
)
```

---

## Support

For questions or issues with batch processing:
- **Email**: reza.moghaddam@niwa.co.nz
- **Documentation**: See `QMRA_TOOLKIT_USER_GUIDE.md`
- **Examples**: Check `qmra_toolkit/examples/` directory

---

**Document Version**: 1.0
**Last Updated**: October 2025
**NIWA Earth Sciences New Zealand**
