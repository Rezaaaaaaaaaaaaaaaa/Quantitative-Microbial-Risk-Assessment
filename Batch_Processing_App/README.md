# QMRA Batch Processing Web Application

**Interactive Web-Based Quantitative Microbial Risk Assessment Tool**

Version 1.0 | October 2025 | NIWA Earth Sciences New Zealand

---

## Overview

This web-based application provides an intuitive interface for running multiple QMRA scenarios with comprehensive visualizations and downloadable results.

### Features

- **5 Assessment Modes:**
  - Batch Scenarios - Run multiple pre-configured scenarios
  - Spatial Assessment - Multiple sites with different dilution factors
  - Temporal Assessment - Time-series pathogen monitoring analysis
  - Treatment Comparison - Evaluate different treatment technologies
  - Multi-Pathogen Assessment - Simultaneous evaluation of multiple pathogens

- **Interactive Visualizations:**
  - Risk Overview charts
  - Compliance Distribution
  - Risk Distribution histograms
  - Population Impact analysis

- **Comprehensive Downloads:**
  - Individual plots (PNG, 300 DPI)
  - Individual tables (CSV/Excel)
  - Complete results package (ZIP)
  - PDF reports
  - Excel workbooks with multiple sheets

---

## 🚀 Quick Start

### 1. Install Requirements

```bash
pip install streamlit pandas numpy matplotlib pyyaml openpyxl
```

### 2. Launch the Application

**Windows:**
```bash
# Double-click this file:
launch_web_gui.bat

# Or run manually:
streamlit run web_app.py
```

**Mac/Linux:**
```bash
streamlit run web_app.py
```

The application will open automatically in your browser at `http://localhost:8502`

---

## 📂 Application Structure

```
Batch_Processing_App/
├── web_app.py                    # Main web application
├── batch_processor.py            # Core QMRA processing engine
├── pdf_report_generator.py       # PDF report generation
├── launch_web_gui.bat           # Windows launcher
│
├── input_data/                   # Example input files
│   ├── pathogen_concentrations/
│   │   ├── weekly_monitoring_2024.csv           (52 weeks)
│   │   └── multi_pathogen_data.csv              (6 pathogens)
│   │
│   ├── dilution_data/
│   │   └── spatial_dilution_6_sites.csv         (600 records)
│   │
│   ├── treatment_scenarios/
│   │   ├── bypass_no_treatment.yaml
│   │   ├── primary_treatment.yaml
│   │   ├── secondary_treatment.yaml
│   │   ├── advanced_uv_treatment.yaml
│   │   └── tertiary_mbr_treatment.yaml
│   │
│   ├── exposure_scenarios/
│   │   ├── swimming_summer.yaml
│   │   ├── swimming_winter.yaml
│   │   └── shellfish_consumption.yaml
│   │
│   └── batch_scenarios/
│       └── master_batch_scenarios.csv           (15 scenarios)
│
└── outputs/                      # Results directory
    └── results/                  # CSV, PDF, and Excel outputs
```

---

## 🎯 How to Use

### Step 1: Select Assessment Mode

In the sidebar, choose from 5 assessment types:
- **Batch Scenarios** - Best for comprehensive multi-scenario analysis
- **Spatial Assessment** - For site-by-site risk evaluation
- **Temporal Assessment** - For seasonal/temporal risk trends
- **Treatment Comparison** - To compare treatment options
- **Multi-Pathogen Assessment** - To identify dominant risk pathogens

### Step 2: Configure Parameters

Each mode has specific inputs:
- Upload your own data files, or use the provided examples
- Set exposure parameters (volume, frequency, population)
- Configure treatment settings (LRV values)
- Select pathogens and exposure routes

### Step 3: Run Assessment

Click the **Run** button and wait for processing to complete.

### Step 4: View Results

- Interactive data tables
- 4 visualization tabs
- Summary statistics
- Risk classifications

### Step 5: Download Results

**Main Downloads:**
- 📄 **Download Full CSV** - Complete results table
- 📑 **Generate PDF Report** - Comprehensive PDF report
- 📦 **Download All (ZIP)** - Complete package with all plots, tables, and README

**Individual Downloads (Expandable Sections):**
- 📊 **Download Individual Plots** - Each plot as high-res PNG
- 📋 **Download Individual Tables** - Filtered data subsets (CSV/Excel)

---

## 📊 Input File Formats

### 1. Pathogen Concentration CSV

Required columns:
- `Sample_ID` or date column
- Pathogen concentration columns (e.g., `Norovirus_copies_per_L`)

**Example:**
```csv
Sample_ID,Sample_Date,Norovirus_copies_per_L,Campylobacter_MPN_per_100mL
S001,2024-01-01,850000,120000
S002,2024-01-08,920000,145000
```

### 2. Dilution Data CSV

Required columns:
- `Site_ID` - Unique site identifier
- `Dilution_Factor` - Dilution at that site (≥ 1.0)

**Example:**
```csv
Site_ID,Distance_m,Dilution_Factor
Discharge,0,1.0
Site_100m,100,15.2
Site_500m,500,125.3
```

### 3. Treatment Scenario YAML

**Structure:**
```yaml
treatment_name: Secondary Treatment + UV
treatment_type: secondary
description: Conventional activated sludge plus UV disinfection

treatment_processes:
  - name: Activated Sludge
    type: biological
    log_reduction: 2.0

  - name: UV Disinfection
    type: disinfection
    log_reduction: 4.0

total_log_reduction: 6.0
```

### 4. Batch Scenario CSV

All parameters in one spreadsheet:

```csv
Scenario_ID,Scenario_Name,Pathogen,Exposure_Route,Effluent_Conc,Treatment_LRV,Dilution_Factor,Volume_mL,Frequency_Year,Population
S001,Beach_A_Summer,norovirus,primary_contact,1000000,3.0,100,50,20,10000
S002,Beach_B_Winter,norovirus,primary_contact,1500000,3.0,50,30,5,2000
```

---

## 📥 Download Options Explained

### 1. Full CSV Results
Complete data table with all scenarios and metrics.

### 2. PDF Report
Comprehensive report including:
- Executive summary
- All visualizations
- Detailed results tables
- Risk classifications
- Compliance status

### 3. ZIP Package
Contains:
- All 4 plots (high-resolution PNG)
- 5+ data tables (CSV format)
- Summary statistics
- README with metadata

### 4. Individual Plots
- Risk Overview
- Compliance Distribution
- Risk Distribution
- Population Impact

Each as 300 DPI PNG, publication-ready.

### 5. Individual Tables
- High-Risk Scenarios
- Compliant/Non-Compliant Scenarios
- Top 10 Highest Risk
- Summary Statistics
- Full Excel Workbook (multi-sheet)

---

## 🔧 Troubleshooting

### App won't start

**Issue:** `streamlit: command not found`

**Solution:**
```bash
pip install streamlit
```

---

### Port already in use

**Issue:** Port 8502 is already in use

**Solution:**
```bash
# Specify a different port:
streamlit run web_app.py --server.port 8503
```

---

### Risk values seem incorrect

**Check:**
1. **Concentration units** - Ensure consistency (copies/L or MPN/100mL)
2. **Dilution factors** - Should be ≥ 1.0 (higher = more dilution)
3. **Treatment LRV** - Should be positive (3.0 = 99.9% removal)
4. **Exposure volume** - mL ingested per event (typically 10-100 mL)
5. **Frequency** - Events per year (not per day)

---

### File upload fails

**Solution:**
- Check file format (CSV or YAML)
- Ensure required columns exist
- Verify no special characters in column names
- Check for missing values in key columns

---

## 📚 Understanding Results

### Risk Metrics

- **Mean_Annual_Risk** - Average probability of infection per person per year
- **Median_Annual_Risk** - 50th percentile (less influenced by outliers)
- **P95_Annual_Risk** - 95th percentile (captures uncertainty)
- **Population_Impact** - Expected annual illnesses

### Risk Classification

| Annual Risk | Classification | Action Required |
|-------------|----------------|-----------------|
| < 1e-6      | Negligible     | None            |
| 1e-6 to 1e-4 | Very Low      | Monitoring      |
| 1e-4 to 1e-3 | Low           | Monitoring      |
| 1e-3 to 1e-2 | Medium        | Consider action |
| > 1e-2       | High          | Immediate action |

### Compliance Status

- **COMPLIANT** - Meets WHO guideline (annual risk < 1e-4)
- **NON-COMPLIANT** - Exceeds WHO guideline

---

## 📖 Example Use Cases

### Use Case 1: Seasonal Risk Analysis
1. Select **Temporal Assessment**
2. Upload weekly monitoring data
3. Review seasonal trends
4. Download risk distribution plot

### Use Case 2: Treatment Upgrade Decision
1. Select **Treatment Comparison**
2. Choose current and proposed treatment scenarios
3. Compare annual risk reduction
4. Download comparison table for cost-benefit analysis

### Use Case 3: Multi-Site Risk Mapping
1. Select **Spatial Assessment**
2. Upload hydrodynamic model dilution data
3. Identify high-risk locations
4. Download spatial risk map

### Use Case 4: Dominant Pathogen Identification
1. Select **Multi-Pathogen Assessment**
2. Upload multi-pathogen concentration data
3. Review pathogen ranking
4. Download pathogen comparison plot

---

## 🔬 Technical Details

### Assessment Methods

- **Dose-Response Models:**
  - Beta-Poisson (Norovirus, Rotavirus)
  - Exponential (Campylobacter, Cryptosporidium)

- **Monte Carlo Simulation:**
  - 10,000 iterations (default)
  - Uncertainty quantification
  - Percentile-based risk estimates

- **Risk Calculation:**
  - Per-event infection risk
  - Annual infection risk
  - Population impact (expected illnesses)
  - DALYs (Disability-Adjusted Life Years)

### Data Processing

- Automatic column detection
- Robust error handling
- Missing value management
- Unit conversion support

---

## 📞 Support & Documentation

**Developer:** NIWA Earth Sciences New Zealand
**Version:** 1.0
**Release Date:** October 2025

**Additional Resources:**
- See `BATCH_PROCESSING_INPUTS_GUIDE.md` for detailed input file specifications
- Check example files in `input_data/` directory
- Review sample outputs in `outputs/results/`

**For Questions:**
- Review example scenarios
- Check input file formats
- Verify parameter units
- Consult QMRA literature (WHO, US EPA)

---

## 📄 References

- WHO (2016). Quantitative Microbial Risk Assessment: Application for Water Safety Management
- U.S. EPA (2019). Method for Assessing the Public Health Risk from Waterborne Pathogens
- Haas et al. (2014). Quantitative Microbial Risk Assessment, 2nd Edition

---

## 🎉 Get Started Now!

1. Double-click `launch_web_gui.bat` (Windows) or run `streamlit run web_app.py`
2. Select an assessment mode from the sidebar
3. Use example data or upload your own
4. Run assessment and explore results
5. Download results in your preferred format

**The application will guide you through each step!**

---

**End of README**
