# NIWA QMRA Assessment Toolkit - User Manual
## Professional Quantitative Microbial Risk Assessment Software

**Version 2.0**
**NIWA Earth Sciences, New Zealand**
**October 2025**

---

## Table of Contents

1. [Introduction](#introduction)
2. [Understanding QMRA](#understanding-qmra)
3. [Getting Started](#getting-started)
4. [Interface Overview](#interface-overview)
5. [Step-by-Step Workflows](#step-by-step-workflows)
6. [Understanding Results](#understanding-results)
7. [Advanced Features](#advanced-features)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)
10. [References and Resources](#references-and-resources)

---

## Introduction

### What is the QMRA Toolkit?

The NIWA QMRA Assessment Toolkit is a professional software application designed for conducting Quantitative Microbial Risk Assessments. It provides a comprehensive, scientifically validated framework for assessing public health risks from waterborne pathogens.

### Key Features

- **🦠 Comprehensive Pathogen Database** - Pre-loaded with validated dose-response models for major waterborne pathogens
- **💧 Multiple Exposure Routes** - Primary contact, shellfish consumption, drinking water, and aerosol inhalation
- **🔬 Treatment Scenario Comparison** - Evaluate current vs. proposed treatment effectiveness
- **📊 Monte Carlo Simulation** - Advanced uncertainty analysis with 10,000+ iterations
- **📋 Automated Reporting** - Generate professional PDF/Word reports for regulatory compliance
- **🎨 Professional GUI** - Intuitive interface with real-time visualization

### Who Should Use This Tool?

- **Environmental Scientists** - Conducting water quality risk assessments
- **Public Health Officials** - Evaluating pathogen exposure risks
- **Water Treatment Professionals** - Comparing treatment scenario effectiveness
- **Regulatory Consultants** - Preparing compliance documentation
- **Researchers** - Performing academic QMRA studies

---

## Understanding QMRA

### What is Quantitative Microbial Risk Assessment?

QMRA is a systematic approach to estimating the probability and magnitude of adverse health effects from exposure to pathogenic microorganisms. It follows a four-step framework established by the US National Research Council (NRC, 1983):

#### 1. **Hazard Identification**
Identifying the pathogenic microorganisms of concern (e.g., Norovirus, Campylobacter, Cryptosporidium)

#### 2. **Exposure Assessment**
Estimating the concentration and volume of pathogen exposure through different routes:
- **Primary Contact** - Recreational water contact (swimming, surfing)
- **Shellfish Consumption** - Eating contaminated shellfish
- **Drinking Water** - Consuming contaminated water
- **Aerosol Inhalation** - Breathing aerosolized water particles

#### 3. **Dose-Response Assessment**
Relating the dose of pathogens to the probability of infection or illness using validated mathematical models:
- **Exponential Model** - Used for many viruses (e.g., Norovirus)
- **Beta-Poisson Model** - Used for bacteria (e.g., Campylobacter)
- **Approximate Beta-Poisson** - Used for protozoa (e.g., Cryptosporidium)

#### 4. **Risk Characterization**
Combining exposure and dose-response to calculate:
- **Infection Risk** - Probability of becoming infected
- **Illness Risk** - Probability of developing symptoms
- **Annual Risk** - Risk over a year accounting for exposure frequency
- **Population Impact** - Expected number of cases in the at-risk population

### New Zealand Regulatory Context

The toolkit is designed to comply with:
- **Drinking Water Standards for New Zealand 2005 (Revised 2008)**
- **Guidelines for Drinking-Water Quality Management for New Zealand 2015-2018**
- **Resource Management Act 1991** requirements
- **Health Act 1956** provisions
- **WHO Guidelines for Safe Recreational Water Environments**

**Key Regulatory Benchmark**: The acceptable annual infection risk for drinking water is **1 in 1,000,000 (10⁻⁶ DALY/person/year)** based on New Zealand and WHO guidelines.

---

## Getting Started

### System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: Version 3.8 or higher
- **RAM**: Minimum 4GB (8GB recommended for large Monte Carlo simulations)
- **Disk Space**: 500MB for software and data

### Installation

1. **Ensure Python is installed**:
   ```bash
   python --version
   ```

2. **Navigate to the toolkit directory**:
   ```bash
   cd qmra_toolkit
   ```

3. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Launching the Application

**Windows**:
- Double-click `Launch_QMRA_GUI.bat`
- Or run: `python launch_enhanced_gui.py`

**macOS/Linux**:
```bash
python launch_enhanced_gui.py
```

The professional GUI will open in a new window.

---

## Interface Overview

### Main Window Components

The QMRA Toolkit features a modern, tabbed interface with 8 main sections:

#### **Header Section**
- **NIWA Logo** - Branding and professional identity
- **Title** - "QMRA Assessment Toolkit"
- **Project Buttons**:
  - 📁 **New Project** - Start a fresh assessment
  - 📂 **Open Project** - Load an existing .qmra project file
  - 💾 **Save Project** - Save your current work

#### **Tab 1: 📋 Project Setup**
Define basic project information:
- **Project Name** - A descriptive name for your assessment
- **Lead Assessor** - Your name or the primary analyst
- **Client Organization** - The organization requesting the assessment
- **Assessment Date** - Date of analysis (auto-populated)
- **Population at Risk** - Number of people potentially exposed

**Example**:
```
Project Name: Auckland Mangere WWTP Assessment
Lead Assessor: Dr. Jane Smith
Client Organization: Auckland Council
Assessment Date: 2025-10-06
Population at Risk: 500,000 people
```

#### **Tab 2: 🧬 Assessment Parameters**

**Pathogen Selection**:
- **Primary Pathogen** - Choose from:
  - Norovirus (most common cause of gastroenteritis)
  - Campylobacter (bacterial pathogen)
  - Cryptosporidium (parasitic protozoan)
  - E. coli (indicator organism)
  - Salmonella (bacterial pathogen)
  - Rotavirus (viral pathogen)

- **Multi-Pathogen Assessment** - Enable to assess multiple pathogens simultaneously

**Exposure Parameters**:
- **Exposure Route**:
  - Primary Contact (swimming, water sports)
  - Shellfish Consumption
  - Drinking Water
  - Aerosol Inhalation

- **Pathogen Concentration** - Copies per liter (copies/L)
  - Click 📊 for typical concentration ranges
  - Raw wastewater: 10³ - 10⁷ copies/L
  - Treated effluent: 10¹ - 10⁴ copies/L
  - Surface water: 10⁰ - 10² copies/L

- **Volume per Exposure** - Milliliters (mL) ingested/contacted per event
  - Swimming: 50-100 mL typical
  - Drinking water: 2000 mL (2 liters) typical
  - Shellfish: 50-100 g consumption

- **Exposure Frequency** - Events per year
  - Recreational swimming: 7-20 events/year
  - Daily drinking water: 365 events/year
  - Seasonal activities: 10-50 events/year

**Analysis Options**:
- **Monte Carlo Iterations** - Number of simulations (recommended: 10,000)
- **Confidence Level** - Percentage for confidence intervals (typically 95%)

#### **Tab 3: 🔬 Treatment Scenarios**

Compare effectiveness of different treatment approaches:

**Current Treatment**:
- Treatment Type: Primary, Secondary, Advanced Secondary, or Tertiary
- Log Reduction Value (LRV): Effectiveness of current treatment

**Proposed Treatment**:
- Treatment Type: Proposed upgrade or alternative
- Log Reduction Value (LRV): Expected effectiveness

**Environmental Factors**:
- Dilution Factor: How much the effluent is diluted in receiving water

**Action Buttons**:
- 🔄 **Compare Scenarios** - Calculate risk for both scenarios
- 📊 **Generate Comparison Plot** - Visualize treatment effectiveness

**LRV Guidelines**:
- Primary Treatment: 0.5-1.0 log
- Secondary Treatment: 1.0-2.0 log
- Advanced Secondary: 2.0-3.0 log
- Tertiary Treatment: 3.0-5.0 log
- Advanced Tertiary: 5.0+ log

#### **Tab 4: 📈 Results**

Three sub-tabs display your assessment outcomes:

**Summary Tab**:
- Key risk metrics (infection risk, illness risk, annual risk)
- Population impact estimates
- Compliance with regulatory benchmarks

**Detailed Results Tab**:
- Full Monte Carlo simulation statistics
- Percentile distributions (5th, 50th, 95th)
- Uncertainty bounds

**Regulatory Compliance Tab**:
- Comparison to NZ drinking water standards (10⁻⁶ DALY/person/year)
- WHO guideline comparisons
- Compliance status and recommendations

**Result Controls**:
- 🔄 **Refresh** - Update results display
- 📋 **Copy to Clipboard** - Copy results as text
- 💾 **Export Results** - Save to CSV, Excel, or JSON

#### **Tab 5: 📊 Plots & Visualizations**

Generate professional publication-quality plots:

- **📊 Risk Comparison** - Bar charts comparing pathogens or scenarios
- **📈 Dose-Response** - Dose-response curves for selected pathogen
- **🎲 Monte Carlo** - Histogram of simulation results with percentiles
- **💾 Save All** - Export all plots to selected directory

All plots include:
- Professional formatting
- Regulatory guideline reference lines
- Statistical annotations
- High-resolution output (300 DPI)

#### **Tab 6: 📄 Professional Reports**

Generate formatted reports for stakeholders:

**Report Templates**:
- **📋 Executive Summary** - 2-3 page summary for decision-makers
- **🔬 Technical Assessment** - Detailed report with methodology
- **⚖️ Regulatory Compliance** - Compliance with NZ health guidelines

**Report Options**:
- ✓ Include Risk Comparison Plots
- ✓ Include Data Tables
- ✓ Include Uncertainty Analysis
- ✓ Include Literature References

**Generation**:
- **📄 Generate Report** - Create PDF or Word document
- **👁️ Preview Report** - Preview before final generation

#### **Tab 7: 🗃️ Pathogen Database**

View and manage the pathogen database:
- Dose-response parameters
- Infection-to-illness ratios
- Literature references
- Update pathogen data

#### **Tab 8: ⚙️ Settings**

Configure application preferences:
- ✓ Generate plots automatically
- ✓ Save intermediate results
- ✓ Enable uncertainty analysis by default

---

## Step-by-Step Workflows

### Workflow 1: Basic Single-Pathogen Assessment

**Scenario**: Assess Norovirus risk from swimming in treated wastewater discharge area

**Steps**:

1. **Launch the Application**
   - Open the QMRA Toolkit GUI

2. **Set Up Project** (Tab 1)
   - Project Name: "Beach Swimming Risk Assessment"
   - Lead Assessor: Your name
   - Client Organization: "Coastal City Council"
   - Population at Risk: 100,000

3. **Configure Assessment Parameters** (Tab 2)
   - Primary Pathogen: Norovirus
   - Exposure Route: Primary Contact
   - Pathogen Concentration: 1000 copies/L
   - Volume per Exposure: 100 mL
   - Exposure Frequency: 7 events/year
   - Monte Carlo Iterations: 10,000
   - Confidence Level: 95%

4. **View Results** (Tab 4)
   - Navigate to Results tab
   - Review Summary for key risk metrics
   - Check Regulatory Compliance status

5. **Generate Visualizations** (Tab 5)
   - Click "📊 Risk Comparison"
   - Click "🎲 Monte Carlo" for distribution
   - Click "💾 Save All" to export plots

6. **Create Report** (Tab 6)
   - Select "Executive Summary Report"
   - Check all report options
   - Click "📄 Generate Report"
   - Save as PDF

7. **Save Project** (Header)
   - Click "💾 Save Project"
   - Choose filename: "Beach_Swimming_Assessment.qmra"

### Workflow 2: Treatment Scenario Comparison

**Scenario**: Compare current secondary treatment vs. proposed tertiary treatment

**Steps**:

1. **Set Up Project** (Tab 1)
   - Complete basic project information
   - Population at Risk: 500,000

2. **Configure Base Parameters** (Tab 2)
   - Primary Pathogen: Norovirus
   - Exposure Route: Primary Contact
   - Concentration: 10,000 copies/L (raw influent)
   - Volume: 50 mL
   - Frequency: 10 events/year

3. **Define Treatment Scenarios** (Tab 3)
   - **Current Treatment**:
     - Type: Secondary Treatment
     - LRV: 1.5 log
   - **Proposed Treatment**:
     - Type: Tertiary Treatment
     - LRV: 3.5 log
   - Dilution Factor: 100

4. **Compare Scenarios**
   - Click "🔄 Compare Scenarios"
   - Review risk reduction calculations
   - Click "📊 Generate Comparison Plot"

5. **Generate Technical Report** (Tab 6)
   - Select "Technical Assessment Report"
   - Include all options
   - Generate PDF for engineering team

### Workflow 3: Multi-Pathogen Assessment

**Scenario**: Assess multiple pathogens for drinking water safety

**Steps**:

1. **Enable Multi-Pathogen Mode** (Tab 2)
   - Check "Enable Multi-Pathogen Assessment"
   - Additional pathogen selection fields appear

2. **Select Pathogens**
   - Primary: Norovirus
   - Secondary: Campylobacter
   - Tertiary: Cryptosporidium

3. **Set Common Parameters**
   - Exposure Route: Drinking Water
   - Volume: 2000 mL (2 liters/day)
   - Frequency: 365 events/year

4. **Define Pathogen-Specific Concentrations**
   - Norovirus: 10 copies/L
   - Campylobacter: 100 copies/L
   - Cryptosporidium: 1 copies/L

5. **Run Assessment**
   - System calculates individual and combined risks
   - Results show which pathogen dominates risk

6. **Create Comparison Visualization** (Tab 5)
   - "📊 Risk Comparison" shows all three pathogens
   - Identify which pathogen requires most attention

---

## Understanding Results

### Key Risk Metrics Explained

#### **1. Infection Risk (Pinf)**
- Probability of becoming infected per exposure event
- Calculated using dose-response models
- Range: 0.0 (no risk) to 1.0 (certain infection)
- **Example**: Pinf = 0.05 means 5% chance of infection per exposure

#### **2. Illness Risk (Pill)**
- Probability of developing symptoms given infection
- Calculated as: Pill = Pinf × Pill|inf ratio
- Pill|inf ratio varies by pathogen (e.g., Norovirus ≈ 0.7)
- **Example**: Pill = 0.035 means 3.5% chance of illness per exposure

#### **3. Annual Risk (Pannual)**
- Probability of at least one infection/illness per year
- Accounts for multiple exposures: Pannual = 1 - (1 - Pinf)^frequency
- **Example**: With 7 exposures/year at Pinf=0.05, Pannual = 0.30 (30%)

#### **4. Population Impact**
- Expected number of cases in the at-risk population
- Calculated as: Cases = Population × Pannual
- **Example**: 100,000 people × 0.30 = 30,000 expected cases/year

#### **5. Percentile Distributions**

Monte Carlo simulations produce distributions showing uncertainty:
- **5th Percentile** - Lower bound (conservative estimate)
- **50th Percentile (Median)** - Most likely value
- **95th Percentile** - Upper bound (worst-case scenario)

**Interpretation**:
```
Annual Risk Results:
  5th percentile:  2.5 × 10⁻⁷ (1 in 4 million)
  Median:          1.2 × 10⁻⁶ (1 in 833,000)
  95th percentile: 5.8 × 10⁻⁶ (1 in 172,000)
```

### Regulatory Compliance Interpretation

#### **New Zealand Drinking Water Standard**: 10⁻⁶ DALY/person/year

**Compliance Status**:
- ✅ **COMPLIANT** - Risk ≤ 10⁻⁶ (meets standard)
- ⚠️ **MARGINAL** - Risk between 10⁻⁶ and 10⁻⁵ (requires attention)
- ❌ **NON-COMPLIANT** - Risk > 10⁻⁵ (exceeds standard)

**Example Interpretation**:
```
Median Annual Risk: 1.2 × 10⁻⁶
Status: ⚠️ MARGINAL - Just above guideline
Recommendation: Consider treatment upgrade or exposure reduction
```

### Understanding Uncertainty

QMRA results include uncertainty from:
1. **Pathogen concentration variability** - Water quality fluctuations
2. **Dose-response parameter uncertainty** - Model fitting uncertainty
3. **Exposure behavior variability** - Different people, different exposures
4. **Environmental factors** - Temperature, survival, dilution

**How to Use Uncertainty Information**:
- Use **median** for best estimate
- Use **95th percentile** for conservative/protective decisions
- Use **5th percentile** for optimistic scenarios
- Report **confidence intervals** to stakeholders for transparency

---

## Advanced Features

### Custom Dose-Response Models

You can add custom pathogens or modify existing models:

1. Navigate to **Pathogen Database** tab
2. Click "Add Custom Pathogen"
3. Enter pathogen name and dose-response parameters
4. Choose model type (Exponential, Beta-Poisson, etc.)
5. Provide literature reference
6. Save to database

### Batch Processing

For multiple scenarios, use the command-line interface:

```bash
python src/qmra_toolkit.py batch --config scenarios.json
```

**scenarios.json example**:
```json
{
  "scenarios": [
    {
      "name": "Scenario 1",
      "pathogen": "norovirus",
      "concentration": 1000,
      "volume": 100,
      "frequency": 7
    },
    {
      "name": "Scenario 2",
      "pathogen": "norovirus",
      "concentration": 100,
      "volume": 100,
      "frequency": 7
    }
  ]
}
```

### Sensitivity Analysis

Identify which parameters most affect risk:

1. Go to **Settings** tab
2. Enable "Sensitivity Analysis"
3. Run assessment
4. View tornado plot showing parameter importance

### Integration with External Data

Import monitoring data:

1. Prepare CSV file with columns: `date`, `pathogen`, `concentration`
2. Use **Import Data** in Assessment Parameters tab
3. System will automatically calculate statistics and run Monte Carlo

---

## Troubleshooting

### Common Issues and Solutions

#### **Issue: Application Won't Launch**
**Symptoms**: Double-clicking launcher does nothing or error message appears

**Solutions**:
1. Verify Python installation: `python --version`
2. Check dependencies: `pip install -r requirements.txt`
3. Try manual launch: `python launch_enhanced_gui.py`
4. Check error log in `qmra_toolkit/logs/`

#### **Issue: Results Seem Unrealistic**
**Symptoms**: Risk values too high or too low

**Solutions**:
1. Verify pathogen concentration units (copies/L)
2. Check exposure volume (mL not L)
3. Confirm LRV is applied correctly (should reduce concentration)
4. Review exposure frequency (events/year, not per day)
5. Use "📊 Concentration Helper" for typical ranges

#### **Issue: Monte Carlo Takes Too Long**
**Symptoms**: Simulation doesn't complete or freezes

**Solutions**:
1. Reduce iterations (try 1,000 instead of 10,000 for testing)
2. Close other applications to free RAM
3. Disable auto-plotting during calculation
4. Check for very large population values

#### **Issue: Can't Generate Report**
**Symptoms**: Report generation fails or produces blank document

**Solutions**:
1. Ensure results exist (run assessment first)
2. Check write permissions in output directory
3. Verify Word/PDF libraries installed: `pip install python-docx reportlab`
4. Try different report format (PDF vs Word)

#### **Issue: Plots Not Displaying**
**Symptoms**: Blank plot area or error when clicking plot buttons

**Solutions**:
1. Verify matplotlib installation: `pip install matplotlib`
2. Update matplotlib: `pip install --upgrade matplotlib`
3. Check "Generate plots automatically" in Settings
4. Try refreshing: Close and reopen Plots tab

### Error Messages

| Error Message | Meaning | Solution |
|---------------|---------|----------|
| `PathogenDatabase not found` | Missing database file | Reinstall or download pathogen_database.json |
| `Invalid concentration value` | Non-numeric input | Enter numbers only (e.g., 1000 not 1,000) |
| `LRV out of range` | LRV too high/low | Use LRV between 0 and 8 |
| `Monte Carlo failed` | Simulation error | Check all parameters are positive numbers |
| `Memory error` | Insufficient RAM | Reduce iterations or population size |

### Getting Help

1. **Check this manual** - Search for your issue in Table of Contents
2. **Review examples** - Look at example projects in `qmra_toolkit/examples/`
3. **Contact support** - Email NIWA QMRA team with:
   - Screenshot of error
   - Your project file (.qmra)
   - Description of what you were trying to do

---

## Best Practices

### Data Quality

✅ **DO**:
- Use recent monitoring data (<3 months old when possible)
- Collect multiple samples for Monte Carlo input
- Document data sources and collection methods
- Use peer-reviewed dose-response models
- Report both median and 95th percentile results

❌ **DON'T**:
- Use single grab sample for risk assessment
- Extrapolate far beyond measured concentrations
- Ignore seasonal variations in water quality
- Mix different pathogen measurement methods
- Report only point estimates without uncertainty

### Project Documentation

Always include in your assessment:
1. **Data Sources** - Where pathogen concentrations came from
2. **Assumptions** - All exposure and treatment assumptions
3. **Model Selection** - Why you chose specific dose-response models
4. **Limitations** - Known limitations and uncertainties
5. **Quality Assurance** - Verification steps taken

### Regulatory Submissions

For regulatory compliance reports:
1. Use **Technical Assessment Report** template
2. Include all uncertainty analyses
3. Compare to both NZ and WHO guidelines
4. Provide raw data in appendix
5. Have independent peer review
6. Include QA/QC documentation

### Model Validation

Before finalizing assessments:
1. **Check units** - Ensure all units are correct (L not mL, copies not CFU)
2. **Benchmark** - Compare to published studies with similar scenarios
3. **Sensitivity test** - Vary key parameters to test robustness
4. **Peer review** - Have colleague review approach and results
5. **Reality check** - Do results make intuitive sense?

### Archiving Projects

Maintain project archives:
- Save project file (.qmra) with version number
- Export results to CSV for long-term storage
- Save all plots as high-res PNG and PDF
- Keep PDF copy of final report
- Document any custom parameters or modifications

---

## References and Resources

### Key Literature

1. **Haas, C. N., Rose, J. B., & Gerba, C. P. (2014)**. *Quantitative Microbial Risk Assessment* (2nd ed.). John Wiley & Sons.
   - Foundational textbook on QMRA methodology

2. **WHO (2011)**. *Guidelines for Drinking-water Quality* (4th ed.). World Health Organization.
   - International standards for drinking water safety

3. **Ministry of Health (2008)**. *Drinking-water Standards for New Zealand 2005 (Revised 2008)*. Wellington: Ministry of Health.
   - NZ-specific regulatory requirements

4. **Teunis, P. F., et al. (2008)**. Norwalk virus: How infectious is it? *Journal of Medical Virology*, 80(8), 1468-1476.
   - Norovirus dose-response model

5. **Medema, G. J., et al. (1996)**. Risk assessment of Cryptosporidium in drinking water. *Water Supply*, 14(3-4), 143-148.
   - Cryptosporidium dose-response model

### Online Resources

- **NIWA QMRA Homepage**: [Internal NIWA link]
- **US EPA QMRA Wiki**: https://qmrawiki.org/
- **WHO Water Safety Portal**: https://www.who.int/water_sanitation_health/
- **QMRAwiki Database**: Repository of dose-response models

### Training and Support

- **NIWA Internal Training**: Contact QMRA team for workshops
- **External Courses**: Water Research Foundation offers QMRA courses
- **Webinars**: US EPA and WHO periodic webinars on risk assessment

### Software Updates

Check for updates:
```bash
cd qmra_toolkit
git pull origin master
```

Or visit the NIWA QMRA repository for latest version.

### Citing This Software

If you use this toolkit in publications:

```
Moghaddam, R., Wood, D., & Hughes, A. (2025). NIWA QMRA Assessment Toolkit
(Version 2.0) [Computer software]. NIWA Earth Sciences, New Zealand.
```

---

## Appendix A: Pathogen-Specific Information

### Norovirus
- **Type**: Enteric virus
- **Dose-Response Model**: Exponential
- **Parameter (α)**: 0.04
- **Pill|inf**: 0.7 (70% of infections symptomatic)
- **Incubation**: 12-48 hours
- **Duration**: 12-60 hours
- **Severity**: Gastroenteritis, vomiting, diarrhea
- **Typical Concentration**: 10³-10⁷ copies/L in wastewater

### Campylobacter
- **Type**: Bacterial pathogen
- **Dose-Response Model**: Beta-Poisson
- **Parameters**: α = 0.145, β = 7.59
- **Pill|inf**: 0.33 (33% of infections symptomatic)
- **Incubation**: 2-5 days
- **Duration**: 2-10 days
- **Severity**: Diarrheal disease, fever
- **Typical Concentration**: 10²-10⁵ CFU/100mL in wastewater

### Cryptosporidium
- **Type**: Protozoan parasite
- **Dose-Response Model**: Exponential
- **Parameter (r)**: 0.09
- **Pill|inf**: 0.39 (39% of infections symptomatic)
- **Incubation**: 7-10 days
- **Duration**: 1-3 weeks
- **Severity**: Severe diarrhea, especially in immunocompromised
- **Typical Concentration**: 10-10³ oocysts/L in wastewater

---

## Appendix B: Glossary

**Annual Risk (Pannual)**: Probability of at least one infection or illness over a year, accounting for multiple exposures

**CFU**: Colony Forming Units - unit for measuring bacterial concentration

**Confidence Interval**: Range of values likely to contain true value with specified probability (e.g., 95%)

**Copies/L**: Concentration unit for viruses/parasites measured by molecular methods (qPCR)

**DALY**: Disability-Adjusted Life Year - measure combining morbidity and mortality

**Dose-Response**: Mathematical relationship between pathogen dose and probability of infection

**LRV**: Log Reduction Value - log₁₀ of pathogen reduction (3-log = 99.9% removal)

**Monte Carlo Simulation**: Computational method using repeated random sampling to estimate uncertainty

**Pinf**: Probability of infection per single exposure event

**Pill**: Probability of illness (symptomatic infection) per exposure

**Percentile**: Value below which a given percentage of observations fall (50th = median)

**QMRA**: Quantitative Microbial Risk Assessment

**WWTP**: Wastewater Treatment Plant

---

## Document Information

**Version**: 2.0
**Last Updated**: October 6, 2025
**Authors**: Reza Moghaddam, David Wood
**Organization**: NIWA Earth Sciences, New Zealand
**Contact**: [NIWA QMRA Team]

**Document History**:
- v1.0 (Sep 2025): Initial release
- v2.0 (Oct 2025): Added advanced features, troubleshooting, and enhanced GUI documentation

---

**© 2025 NIWA (National Institute of Water & Atmospheric Research Ltd)**
*This manual is provided for use with the NIWA QMRA Assessment Toolkit*
