# QMRA Batch Processing Application

**Standalone Application for Automated Quantitative Microbial Risk Assessment**

Version 1.0 | October 2025 | NIWA Earth Sciences New Zealand

---

## Overview

This standalone batch processing application automates multiple QMRA scenarios, enabling efficient evaluation of:

- **Spatial Risk Assessment** - Multiple sites with different dilution factors
- **Temporal Risk Assessment** - Seasonal and time-series pathogen monitoring
- **Treatment Comparison** - Multiple treatment scenarios (bypass, primary, UV, MBR)
- **Multi-Pathogen Assessment** - Simultaneous evaluation of multiple pathogens
- **Batch Scenario Execution** - Run dozens of scenarios from master configuration file

The application includes complete dummy input files for immediate testing and demonstration.

---

## 🚀 Quick Start - Web GUI (Recommended)

### Option 1: Web Application (Easiest)

**Launch the interactive web interface with one click:**

```bash
# Windows
launch_web_gui.bat

# Or manually:
streamlit run web_app.py
```

The web application will open in your browser with:
- 📊 **Interactive dashboards** - Real-time results visualization
- 📑 **PDF Report Generation** - Comprehensive reports with charts and analysis
- 📁 **File Upload** - Drag-and-drop your own data files
- 🎯 **All Assessment Modes** - Spatial, temporal, treatment comparison, multi-pathogen, batch scenarios
- 💾 **Easy Downloads** - CSV results and PDF reports

**Features:**
- No command line needed
- Visual parameter configuration
- Interactive charts and tables
- One-click PDF report generation
- File upload functionality
- Real-time progress tracking

---

## Quick Start - Command Line

### Option 2: Command Line Interface

For scripting and automation, use the command-line interface:

### 1. Installation

Install required Python packages:

```bash
# Check Python version (3.7+ required)
python --version

# Install packages for CLI only
pip install numpy pandas pyyaml

# For web GUI, also install:
pip install streamlit matplotlib
```

### 2. Run Your First Assessment

Navigate to the application directory and run a batch assessment:

```bash
cd Batch_Processing_App

# Run batch scenarios (15 pre-configured scenarios)
python run_batch_assessment.py batch

# Or run spatial assessment
python run_batch_assessment.py spatial
```

### 3. Generate PDF Report

```bash
# Generate comprehensive PDF report from results
python pdf_report_generator.py outputs/results/batch_scenarios_results.csv

# Output: outputs/results/batch_scenarios_report.pdf
```

### 4. View Results

Results are saved as CSV files in `outputs/results/` with comprehensive risk metrics.

---

## Application Structure

```
Batch_Processing_App/
├── web_app.py                        # 🌐 Streamlit Web GUI (MAIN INTERFACE)
├── launch_web_gui.bat                # Windows launcher for web app
├── run_batch_assessment.py           # CLI application
├── batch_processor.py                # Core BatchProcessor class
├── pdf_report_generator.py           # PDF report generation module
├── README.md                         # This file
│
├── input_data/                       # All input files
│   ├── pathogen_concentrations/
│   │   ├── weekly_monitoring_2024.csv           # 52 weeks of monitoring
│   │   └── multi_pathogen_data.csv              # 6 pathogens, 12 samples
│   │
│   ├── dilution_data/
│   │   └── spatial_dilution_6_sites.csv         # 600 dilution records
│   │
│   ├── treatment_scenarios/
│   │   ├── bypass_no_treatment.yaml             # LRV 0.0
│   │   ├── primary_treatment.yaml               # LRV 1.0
│   │   ├── secondary_treatment.yaml             # LRV 3.0
│   │   ├── advanced_uv_treatment.yaml           # LRV 8.0
│   │   └── tertiary_mbr_treatment.yaml          # LRV 9.3
│   │
│   ├── exposure_scenarios/
│   │   ├── swimming_summer.yaml                 # 15,000 population, 25 events/yr
│   │   ├── swimming_winter.yaml                 # 2,000 population, 8 events/yr
│   │   └── shellfish_consumption.yaml           # 5,000 population, 24 servings/yr
│   │
│   └── batch_scenarios/
│       └── master_batch_scenarios.csv           # 15 complete scenarios
│
└── outputs/                          # Results directory
    └── results/                      # CSV and PDF output files
```

---

## Command Reference

### Help

```bash
python run_batch_assessment.py --help
python run_batch_assessment.py spatial --help
python run_batch_assessment.py temporal --help
```

### 1. Spatial Assessment

Evaluate risk across multiple sites with different dilution factors.

**Basic Usage:**
```bash
python run_batch_assessment.py spatial
```

**Custom Parameters:**
```bash
python run_batch_assessment.py spatial \
    --dilution-file input_data/dilution_data/spatial_dilution_6_sites.csv \
    --pathogen norovirus \
    --concentration 1e6 \
    --exposure-route primary_contact \
    --volume 50 \
    --frequency 25 \
    --population 15000 \
    --treatment-lrv 3.0 \
    --iterations 10000 \
    --output spatial_risk_results.csv
```

**Parameters:**
- `--dilution-file`: CSV file with Site_ID and Dilution_Factor columns
- `--pathogen`: norovirus, campylobacter, cryptosporidium, e_coli, rotavirus, salmonella
- `--concentration`: Effluent concentration (organisms/L)
- `--exposure-route`: primary_contact, shellfish_consumption
- `--volume`: Ingestion volume (mL)
- `--frequency`: Exposure events per year
- `--population`: Population size
- `--treatment-lrv`: Log reduction value from treatment
- `--iterations`: Monte Carlo iterations (default 10,000)
- `--output`: Output filename

**Output Columns:**
- Site_ID, Dilution_Factor
- Mean_Annual_Risk, Median_Annual_Risk, P95_Annual_Risk
- Mean_Infection_Risk_Per_Event
- Annual_DALYs, DALYs_Per_Person_Per_Year
- Expected_Annual_Illnesses
- Risk_Classification (Negligible/Very Low/Low/Medium/High)

---

### 2. Temporal Assessment

Analyze risk over time using pathogen monitoring data.

**Basic Usage:**
```bash
python run_batch_assessment.py temporal
```

**Custom Parameters:**
```bash
python run_batch_assessment.py temporal \
    --monitoring-file input_data/pathogen_concentrations/weekly_monitoring_2024.csv \
    --pathogen norovirus \
    --concentration-column Norovirus_copies_per_L \
    --exposure-route primary_contact \
    --treatment-lrv 3.0 \
    --dilution 100 \
    --volume 50 \
    --frequency 20 \
    --population 10000 \
    --iterations 10000 \
    --output temporal_risk_results.csv
```

**Parameters:**
- `--monitoring-file`: CSV with date and pathogen concentration columns
- `--concentration-column`: Name of concentration column (auto-detected if None)
- Other parameters same as spatial assessment

**Output Columns:**
- Sample_ID, Sample_Date, Raw_Concentration
- Treated_Concentration, Diluted_Concentration
- Risk metrics (same as spatial)
- Month, Season (for temporal analysis)

---

### 3. Treatment Comparison

Compare multiple treatment scenarios side-by-side.

**Basic Usage (all treatment files):**
```bash
python run_batch_assessment.py treatment
```

**Specific Treatment Files:**
```bash
python run_batch_assessment.py treatment \
    --treatment-files \
        input_data/treatment_scenarios/secondary_treatment.yaml \
        input_data/treatment_scenarios/advanced_uv_treatment.yaml \
        input_data/treatment_scenarios/tertiary_mbr_treatment.yaml \
    --pathogen norovirus \
    --concentration 1e6 \
    --dilution 100 \
    --output treatment_comparison.csv
```

**Output Columns:**
- Treatment_Scenario, Treatment_Type, Total_LRV
- Process_1_Name, Process_1_LRV
- Process_2_Name, Process_2_LRV (if applicable)
- Risk metrics for each treatment scenario
- Cost_Relative_To_Primary (if included in YAML)

---

### 4. Multi-Pathogen Assessment

Evaluate multiple pathogens simultaneously.

**Basic Usage:**
```bash
python run_batch_assessment.py multi-pathogen
```

**Custom Pathogens:**
```bash
python run_batch_assessment.py multi-pathogen \
    --concentration-file input_data/pathogen_concentrations/multi_pathogen_data.csv \
    --pathogens norovirus,campylobacter,cryptosporidium,e_coli \
    --exposure-route primary_contact \
    --treatment-lrv 3.0 \
    --dilution 100 \
    --volume 50 \
    --frequency 20 \
    --population 10000 \
    --iterations 10000 \
    --output multi_pathogen_results.csv
```

**Input File Format:**

The CSV must have columns: Sample_ID and one column per pathogen (e.g., Norovirus_copies_per_L, Campylobacter_MPN_per_100mL).

**Output Columns:**
- Sample_ID, Pathogen
- Raw_Concentration, Treated_Concentration, Diluted_Concentration
- Risk metrics for each pathogen
- Relative_Risk_Rank (1 = highest risk pathogen)

---

### 5. Batch Scenarios

Run multiple scenarios from master configuration file.

**Basic Usage:**
```bash
python run_batch_assessment.py batch
```

**Custom Scenario File:**
```bash
python run_batch_assessment.py batch \
    --scenario-file input_data/batch_scenarios/master_batch_scenarios.csv
```

**Master Scenario File Format:**

| Column | Description | Example |
|--------|-------------|---------|
| Scenario_ID | Unique identifier | S001 |
| Scenario_Name | Descriptive name | Beach_A_Summer_Norovirus |
| Pathogen | Pathogen name | norovirus |
| Exposure_Route | Route of exposure | primary_contact |
| Effluent_Conc | Effluent concentration | 1000000 |
| Treatment_LRV | Treatment log reduction | 3.0 |
| Dilution_Factor | Dilution factor | 100 |
| Volume_mL | Ingestion volume | 50 |
| Frequency_Year | Events per year | 25 |
| Population | Population size | 15000 |
| Priority | High/Medium/Low | High |
| Monte_Carlo_Iterations | Iterations | 10000 |
| Notes | Additional info | Main tourist beach |

**Output:**

Single consolidated CSV with all scenarios: `outputs/results/batch_scenarios_results.csv`

**Included Example Scenarios:**

The dummy data includes 15 scenarios covering:
- **S001-S004**: Different beaches with varying conditions
- **S005-S006**: Shellfish consumption areas
- **S007-S009**: Multi-pathogen assessments at same location
- **S010**: Worst case - treatment bypass scenario
- **S011-S012**: Treatment upgrade scenarios (UV, MBR)
- **S013-S014**: Poor vs. excellent dilution comparison
- **S015**: Peak summer weekend high-use scenario

---

## Input File Specifications

### 1. Pathogen Concentration CSV

**Required Columns:**
- `Sample_ID` or similar identifier
- One or more pathogen concentration columns (e.g., `Norovirus_copies_per_L`)

**Optional Columns:**
- `Sample_Date`, `Week`, `Month`, `Season`
- `Temperature_C`, `Rainfall_mm`
- `QC_Flag`, `Notes`

**Example:**
```csv
Sample_ID,Sample_Date,Norovirus_copies_per_L,Campylobacter_MPN_per_100mL
S001,2024-01-01,850000,120000
S002,2024-01-08,920000,145000
```

---

### 2. Dilution Data CSV

**Required Columns:**
- `Site_ID` - Unique site identifier
- `Dilution_Factor` - Dilution factor at that site

**Optional Columns:**
- `Distance_m` - Distance from discharge
- `Simulation_Run` - For multiple model runs
- `Current_Speed_m_per_s`, `Wave_Height_m`

**Example:**
```csv
Site_ID,Distance_m,Dilution_Factor
Discharge,0,1.0
Site_100m,100,15.2
Site_500m,500,125.3
```

---

### 3. Treatment Scenario YAML

**Structure:**
```yaml
treatment_name: Secondary Treatment + Chlorination
treatment_type: secondary
description: Conventional activated sludge + chlorine disinfection

treatment_processes:
  - name: Activated Sludge
    type: biological
    log_reduction: 2.0

  - name: Chlorine Disinfection
    type: disinfection
    log_reduction: 1.0

total_log_reduction: 3.0

operational_parameters:
  HRT_hours: 8
  SRT_days: 10
  chlorine_contact_time_min: 30
  chlorine_dose_mg_per_L: 5

cost_relative_to_primary: 2.5
notes: Standard secondary treatment
```

---

### 4. Exposure Scenario YAML

**Structure:**
```yaml
scenario_name: Swimming - Summer Season
exposure_route: primary_contact
description: Recreational swimming during summer
season: Summer (November - March)

population:
  size: 15000
  description: Regular summer beach users
  age_distribution:
    children_0_5: 0.12
    children_6_12: 0.18
    adults_13_64: 0.60
    elderly_65plus: 0.10

exposure_parameters:
  water_ingestion_volume_mL: 50
  exposure_duration_minutes: 90
  events_per_year: 25
  peak_usage_days: 90

pathogen: norovirus
risk_threshold: 0.001
notes: High exposure frequency during peak season
```

---

## Example Workflows

### Workflow 1: Spatial Risk Assessment for Coastal Discharge

**Objective:** Assess risk at multiple beach locations with different dilution factors.

**Steps:**

1. Prepare dilution data from hydrodynamic model:
```csv
Site_ID,Distance_m,Dilution_Factor
Discharge,0,1.0
Beach_A,250,45.0
Beach_B,500,120.0
Beach_C,1000,380.0
```

2. Run spatial assessment:
```bash
python run_batch_assessment.py spatial \
    --dilution-file my_dilution_data.csv \
    --pathogen norovirus \
    --concentration 1200000 \
    --treatment-lrv 3.0 \
    --population 15000 \
    --output coastal_risk_assessment.csv
```

3. Review results to identify sites exceeding risk thresholds.

---

### Workflow 2: Seasonal Monitoring Analysis

**Objective:** Analyze risk trends from weekly pathogen monitoring over one year.

**Steps:**

1. Prepare monitoring data:
```csv
Week,Sample_Date,Norovirus_copies_per_L,Season
1,2024-01-01,1500000,Summer
2,2024-01-08,1200000,Summer
...
26,2024-06-30,800000,Winter
```

2. Run temporal assessment:
```bash
python run_batch_assessment.py temporal \
    --monitoring-file weekly_monitoring_2024.csv \
    --pathogen norovirus \
    --treatment-lrv 3.0 \
    --dilution 100 \
    --output seasonal_risk_2024.csv
```

3. Plot annual risk trends, identify seasonal peaks.

---

### Workflow 3: Treatment Upgrade Evaluation

**Objective:** Compare current treatment (secondary) with proposed UV upgrade.

**Steps:**

1. Ensure treatment YAML files exist for both scenarios.

2. Run comparison:
```bash
python run_batch_assessment.py treatment \
    --treatment-files \
        input_data/treatment_scenarios/secondary_treatment.yaml \
        input_data/treatment_scenarios/advanced_uv_treatment.yaml \
    --pathogen norovirus \
    --concentration 1000000 \
    --dilution 100 \
    --output treatment_upgrade_comparison.csv
```

3. Calculate risk reduction and cost-benefit ratio.

---

### Workflow 4: Comprehensive Multi-Scenario Assessment

**Objective:** Run all 15 pre-configured scenarios for comprehensive risk evaluation.

**Steps:**

1. Review and customize `master_batch_scenarios.csv` if needed.

2. Run batch processing:
```bash
python run_batch_assessment.py batch
```

3. Results saved to `outputs/results/batch_scenarios_results.csv` (single consolidated file).

4. Filter by Priority (High/Medium/Low) and analyze risk rankings.

---

## Understanding Results

### Risk Metrics

- **Mean_Annual_Risk**: Average probability of infection per person per year
- **Median_Annual_Risk**: 50th percentile (less influenced by outliers)
- **P95_Annual_Risk**: 95th percentile (captures uncertainty)
- **Mean_Infection_Risk_Per_Event**: Risk per exposure event

### Risk Classification

| Annual Risk | Classification | Description |
|-------------|----------------|-------------|
| < 1e-6 | Negligible | Meets stringent guidelines |
| 1e-6 to 1e-4 | Very Low | Below WHO threshold |
| 1e-4 to 1e-3 | Low | Acceptable for most uses |
| 1e-3 to 1e-2 | Medium | May require action |
| > 1e-2 | High | Requires immediate action |

### DALYs (Disability-Adjusted Life Years)

- **Annual_DALYs**: Total disease burden for population
- **DALYs_Per_Person_Per_Year**: Burden per capita
- WHO guideline: < 1e-6 DALYs per person per year

### Expected Illnesses

- **Expected_Annual_Illnesses**: Predicted cases per year
- Calculated as: Annual_Risk × Population × Morbidity_Rate

---

## Troubleshooting

### Problem: "No module named 'numpy'"

**Solution:**
```bash
pip install numpy pandas pyyaml
```

---

### Problem: "FileNotFoundError: input_data/..."

**Solution:**
- Ensure you're running from the `Batch_Processing_App` directory
- Check input file paths in command arguments
- Verify input files exist

---

### Problem: Output shows "ERROR" in results

**Cause:** Input data issues (negative values, missing columns)

**Solution:**
- Check input CSV files for required columns
- Ensure concentration values are positive
- Verify dilution factors are ≥ 1.0

---

### Problem: Risk values seem too high/low

**Check:**
1. **Concentration units**: Ensure consistency (copies/L, MPN/100mL)
2. **Dilution factors**: Should be ≥ 1.0 (higher = more dilution)
3. **Treatment LRV**: Should be positive (3.0 = 99.9% removal)
4. **Exposure volume**: mL ingested per event (typically 10-100 mL)
5. **Frequency**: Exposure events per year (not per day)

---

### Problem: Slow performance for large datasets

**Solutions:**
- Reduce Monte Carlo iterations (e.g., 5000 instead of 10000)
- Process fewer scenarios at once
- Use smaller temporal datasets (monthly instead of daily)

---

### Problem: Different results each run

**Explanation:** Monte Carlo simulation uses random sampling

**Solutions:**
- This is expected behavior representing uncertainty
- Use more iterations (e.g., 20000) for more stable results
- Report median and 95th percentile, not just mean
- For reproducibility, set random seed in `batch_processor.py`

---

## Advanced Usage

### Modifying the BatchProcessor

The `batch_processor.py` module can be customized for specific needs:

**Example: Add custom output columns**

Edit `_create_result_dict()` method to include additional metrics.

**Example: Change risk calculation method**

Edit `_simplified_qmra_calculation()` to modify dose-response models.

**Example: Add new batch type**

Add new method to `BatchProcessor` class and corresponding subparser in `run_batch_assessment.py`.

---

### Integration with Full QMRA Toolkit

This application includes simplified calculations for standalone use. For advanced features:

1. Install full QMRA Toolkit (parent directory)
2. BatchProcessor will automatically use full modules if available
3. Provides uncertainty distributions, sensitivity analysis, advanced visualizations

---

## Contact and Support

**Developer:** NIWA Earth Sciences New Zealand
**Date:** October 2025
**Application Version:** 1.0

For questions, issues, or feature requests:
- Review this README
- Check input file formats
- Examine example dummy files in `input_data/`
- Consult parent QMRA Toolkit documentation

---

## References

- WHO (2016). Quantitative Microbial Risk Assessment: Application for Water Safety Management
- U.S. EPA (2019). Method for Assessing the Public Health Risk from Waterborne Pathogens
- Haas et al. (2014). Quantitative Microbial Risk Assessment, 2nd Edition

---

## Version History

**Version 1.0 (October 2025)**
- Initial release
- 5 batch processing modes
- Complete dummy input files
- Comprehensive documentation

---

**End of README**
