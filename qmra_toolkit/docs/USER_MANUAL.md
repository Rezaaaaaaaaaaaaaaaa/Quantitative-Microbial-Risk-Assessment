# NIWA QMRA Assessment Toolkit - User Manual
## How to Use the QMRA Application

**Version 2.0**
**NIWA Earth Sciences, New Zealand**
**October 2025**

---

## Table of Contents

1. [Quick Start Guide](#quick-start-guide)
2. [Installation & Launch](#installation--launch)
3. [Your First Assessment - Step by Step](#your-first-assessment---step-by-step)
4. [Interface Guide](#interface-guide)
5. [Common Tasks & Workflows](#common-tasks--workflows)
6. [Working with Results](#working-with-results)
7. [Generating Reports](#generating-reports)
8. [Troubleshooting](#troubleshooting)
9. [Tips & Best Practices](#tips--best-practices)
10. [Appendix: QMRA Background](#appendix-qmra-background)

---

## Quick Start Guide

**Get up and running in 5 minutes:**

1. **Install Python** (if not already installed): Download Python 3.8+ from python.org
2. **Install Dependencies**: Open terminal/command prompt and run:
   ```bash
   cd qmra_toolkit
   pip install -r requirements.txt
   ```
3. **Launch the App**:
   - **Windows**: Double-click `Launch_QMRA_GUI.bat`
   - **Mac/Linux**: Run `python launch_enhanced_gui.py`
4. **Run Your First Assessment**: See [Your First Assessment](#your-first-assessment---step-by-step) below

---

## Installation & Launch

### System Requirements

- **Python**: Version 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 500MB

### Step-by-Step Installation

1. **Verify Python is installed**:
   ```bash
   python --version
   ```
   If not installed, download from [python.org](https://www.python.org/downloads/)

2. **Navigate to the toolkit folder**:
   ```bash
   cd qmra_toolkit
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

### How to Launch

**Windows Users:**
- **Easiest**: Double-click `Launch_QMRA_GUI.bat`
- **Alternative**: Open Command Prompt, navigate to qmra_toolkit folder, run: `python launch_enhanced_gui.py`

**Mac/Linux Users:**
```bash
python launch_enhanced_gui.py
```

The application window will open automatically.

---

## Your First Assessment - Step by Step

**Scenario**: You want to assess Norovirus risk from swimming at a beach near a wastewater discharge.

### Step 1: Launch & Setup Project

1. Launch the application (see above)
2. Click **📁 New Project** in the header
3. Fill in **Project Setup** (Tab 1):
   - **Project Name**: "Beach Swimming Assessment"
   - **Lead Assessor**: Your name
   - **Client Organization**: Your organization
   - **Population at Risk**: 10000 (ten thousand beach users)

### Step 2: Set Assessment Parameters

Go to **📋 Assessment Parameters** (Tab 2):

1. **Pathogen Selection**:
   - Select **Norovirus** from dropdown
   - Leave multi-pathogen unchecked for now

2. **Exposure Route**:
   - Select **Primary Contact** (swimming)

3. **Pathogen Concentration**:
   - Enter **1000** copies/L
   - *Tip: Click 📊 button to see typical ranges*

4. **Volume per Exposure**:
   - Enter **100** mL (typical for swimming)

5. **Exposure Frequency**:
   - Enter **7** events/year (summer swimming)

6. **Monte Carlo Settings**:
   - Leave at **10,000** iterations (default)
   - Leave confidence at **95%**

### Step 3: View Results

1. Click the **📈 Results** tab
2. The **Summary** sub-tab shows:
   - Annual infection risk
   - Expected cases per year
   - Compliance status (meets WHO guidelines or not)

3. Click **Detailed Results** sub-tab to see:
   - 5th, 50th, 95th percentile values
   - Uncertainty ranges

### Step 4: Generate Visualizations

1. Go to **📊 Plots & Visualizations** (Tab 5)
2. Click **📈 Dose-Response** to see dose-response curve
3. Click **🎲 Monte Carlo** to see risk distribution histogram
4. Click **💾 Save All** to export plots to a folder

### Step 5: Create a Report

1. Go to **📄 Professional Reports** (Tab 6)
2. Select **Executive Summary Report**
3. Check the boxes for what to include:
   - ✓ Risk Comparison Plots
   - ✓ Data Tables
   - ✓ Uncertainty Analysis
4. Click **📄 Generate Report**
5. Choose location and save as PDF

### Step 6: Save Your Project

1. Click **💾 Save Project** in the header
2. Choose a filename: "Beach_Swimming_Assessment.qmra"
3. Your work is now saved and can be reopened later

**Congratulations!** You've completed your first QMRA assessment.

---

## Interface Guide

### Application Layout

The QMRA Toolkit has **8 tabs** across the top. Here's what each one does:

| Tab | What It Does |
|-----|--------------|
| **📋 Project Setup** | Enter project name, your name, client, and population at risk |
| **🧬 Assessment Parameters** | Choose pathogen, exposure route, concentrations, and frequencies |
| **🔬 Treatment Scenarios** | Compare current vs. proposed treatment effectiveness |
| **📈 Results** | View risk calculations, statistics, and compliance status |
| **📊 Plots & Visualizations** | Generate and export charts and graphs |
| **📄 Professional Reports** | Create PDF/Word reports for stakeholders |
| **🗃️ Pathogen Database** | View/edit pathogen parameters (advanced users) |
| **⚙️ Settings** | Configure application preferences |

**Project Controls** (top of window):
- **📁 New Project**: Start fresh
- **📂 Open Project**: Load saved .qmra file
- **💾 Save Project**: Save your work

### Key Input Fields Explained

**Tab 2 - Assessment Parameters** is where you'll spend most of your time:

| Field | What to Enter | Example Values |
|-------|---------------|----------------|
| **Primary Pathogen** | Select from dropdown | Norovirus, Campylobacter, Cryptosporidium |
| **Exposure Route** | How people are exposed | Primary Contact (swimming), Shellfish, Drinking Water |
| **Pathogen Concentration** | Pathogens per liter (copies/L) | 1000 for treated effluent, 100000 for raw sewage |
| **Volume per Exposure** | mL ingested per event | 100 mL (swimming), 2000 mL (drinking) |
| **Exposure Frequency** | Times per year | 7 (summer swimming), 365 (daily drinking) |
| **Monte Carlo Iterations** | Simulation runs | 10,000 (default - don't change unless needed) |

*Tip: Click the 📊 button next to concentration fields to see typical values for different water types.*

**Tab 3 - Treatment Scenarios** (optional):

| Field | What to Enter | Example Values |
|-------|---------------|----------------|
| **Treatment Type** | Level of treatment | Primary, Secondary, Tertiary |
| **Log Reduction Value (LRV)** | Pathogen removal effectiveness | 1.0 log = 90%, 2.0 log = 99%, 3.0 log = 99.9% |
| **Dilution Factor** | Mixing in receiving water | 100 (moderate dilution), 1000 (high dilution) |

---

## Common Tasks & Workflows

### Task 1: Quick Risk Assessment (10 minutes)

**When to use**: You need a quick estimate of risk for a single scenario.

1. Launch app → Click **New Project**
2. Fill in **Tab 1** (project info)
3. Fill in **Tab 2**:
   - Choose pathogen (e.g., Norovirus)
   - Choose exposure route (e.g., Primary Contact)
   - Enter concentration (e.g., 1000 copies/L)
   - Enter volume (e.g., 100 mL)
   - Enter frequency (e.g., 7 events/year)
4. Click **Tab 4** to see results immediately
5. Done! See if risk is acceptable or needs action.

### Task 2: Compare Two Treatment Options

**When to use**: Decision-makers want to know if upgrading treatment is worthwhile.

1. Complete basic setup (Tabs 1-2)
2. Go to **Tab 3 - Treatment Scenarios**
3. **Current Treatment**:
   - Select treatment type (e.g., Secondary)
   - Enter current LRV (e.g., 2.0)
4. **Proposed Treatment**:
   - Select upgrade (e.g., Tertiary)
   - Enter proposed LRV (e.g., 4.0)
5. Click **🔄 Compare Scenarios**
6. Click **📊 Generate Comparison Plot**
7. Go to **Tab 4** to see risk reduction
8. Export results for cost-benefit analysis

### Task 3: Generate Report for Stakeholders

**When to use**: You need a professional document for clients or regulators.

1. Complete your assessment (Tabs 1-2, run calculations)
2. Go to **Tab 6 - Professional Reports**
3. Choose report type:
   - **Executive Summary**: For managers/decision-makers (short, non-technical)
   - **Technical Assessment**: For engineers/scientists (detailed methodology)
   - **Regulatory Compliance**: For regulatory submissions
4. Check boxes for what to include (recommend checking all)
5. Click **📄 Generate Report**
6. Choose location and filename
7. PDF will be created automatically

### Task 4: Assess Multiple Pathogens at Once

**When to use**: You want to know which pathogen poses the highest risk.

1. Complete basic setup (**Tab 1**)
2. In **Tab 2**, check **"Enable Multi-Pathogen Assessment"**
3. Select 2-3 pathogens (e.g., Norovirus, Campylobacter, Cryptosporidium)
4. Enter concentration for each pathogen
5. Set common exposure parameters (volume, frequency)
6. Go to **Tab 4** to see results for all pathogens
7. Go to **Tab 5**, click **📊 Risk Comparison** to see which pathogen dominates
8. Focus treatment efforts on the highest-risk pathogen

### Task 5: Export Data for Further Analysis

**When to use**: You want to analyze results in Excel or share raw data.

1. After running assessment, go to **Tab 4 - Results**
2. Click **💾 Export Results** button
3. Choose format:
   - **CSV**: For Excel/spreadsheet analysis
   - **Excel**: For formatted workbook
   - **JSON**: For programming/scripting
4. Choose location and save
5. Open in Excel or other analysis tool

### Task 6: Reopen and Modify Saved Project

**When to use**: You need to update a previous assessment with new data.

1. Click **📂 Open Project** (header)
2. Browse to your .qmra file
3. Project loads with all previous settings
4. Modify values as needed (e.g., update concentration based on new monitoring)
5. Results update automatically
6. Click **💾 Save Project** to overwrite or save with new name

---

## Working with Results

### Understanding Your Results

When you click **Tab 4 - Results**, you'll see several numbers. Here's what they mean in plain language:

| Result | What It Means | How to Use It |
|--------|---------------|---------------|
| **Per-Event Infection Risk** | Chance of getting infected each time exposed | Compare to other scenarios |
| **Annual Infection Risk** | Chance of getting infected at least once per year | Compare to guidelines (see below) |
| **Population Cases/Year** | How many people would get sick per year | Estimate public health impact |
| **5th Percentile** | Best-case scenario (low estimate) | Optimistic estimate |
| **Median (50th)** | Most likely value | Your best estimate - **use this** |
| **95th Percentile** | Worst-case scenario (high estimate) | Conservative/protective estimate |

### How to Interpret Risk Numbers

**Annual Risk Examples:**
- **1 × 10⁻⁷** = 1 in 10 million chance per year → Very low risk
- **1 × 10⁻⁶** = 1 in 1 million → Regulatory guideline threshold
- **1 × 10⁻⁴** = 1 in 10,000 → Moderate risk, action recommended
- **1 × 10⁻²** = 1 in 100 → High risk, immediate action needed

### Is My Result Acceptable?

The app shows a **Compliance Status**:

| Status | What It Means | What to Do |
|--------|---------------|------------|
| ✅ **COMPLIANT** | Risk below guideline (< 10⁻⁶) | OK to proceed, continue monitoring |
| ⚠️ **MARGINAL** | Risk near guideline (10⁻⁶ to 10⁻⁵) | Consider improvements, increased monitoring |
| ❌ **NON-COMPLIANT** | Risk above guideline (> 10⁻⁵) | Action required - upgrade treatment or reduce exposure |

*Note: Guideline is 10⁻⁶ annual risk (1 in 1 million) based on WHO and NZ drinking water standards*

### Why Are There Three Numbers (5th, Median, 95th)?

Real-world conditions vary (weather, water quality, human behavior). The three values show this uncertainty:

- **5th percentile**: "Good conditions" - low pathogen levels, less exposure
- **Median**: "Typical conditions" - average scenario
- **95th percentile**: "Bad conditions" - high pathogen levels, more exposure

**Which one to use?**
- **Decision-making**: Use **median** as your best estimate
- **Protective/conservative**: Use **95th percentile**
- **Reporting to stakeholders**: Report all three to show uncertainty range

---

## Generating Reports

### Creating a PDF Report

The app can generate professional reports automatically:

1. **Complete your assessment** (Tabs 1-4 must have data)
2. Go to **Tab 6 - Professional Reports**
3. **Choose report type**:
   - **Executive Summary**: Short, non-technical (for managers)
   - **Technical Assessment**: Detailed with methodology (for engineers/scientists)
   - **Regulatory Compliance**: Focused on meeting guidelines (for regulators)
4. **Select what to include** (check boxes):
   - ✓ Risk Comparison Plots (recommended)
   - ✓ Data Tables (recommended)
   - ✓ Uncertainty Analysis (recommended for technical reports)
   - ✓ Literature References (recommended for regulatory submissions)
5. Click **📄 Generate Report**
6. Choose save location and filename
7. Report generates as PDF (opens automatically when done)

### What's in the Report?

All reports include:
- Project information (name, assessor, client)
- Assessment parameters (pathogen, exposure, concentrations)
- Risk results with interpretation
- Compliance status
- Recommendations (if applicable)

**Technical Assessment** also includes:
- Methodology explanation
- Monte Carlo simulation details
- Uncertainty analysis
- Literature references

---

## Troubleshooting

### Problem: App Won't Start

**Try this:**
1. Check Python is installed: Open terminal/command prompt and type `python --version`
2. If Python is missing, download from [python.org](https://www.python.org/downloads/)
3. Reinstall dependencies: `pip install -r requirements.txt`
4. Try running manually: `python launch_enhanced_gui.py`

### Problem: Results Look Wrong (Too High or Too Low)

**Check these common mistakes:**

| Mistake | What to Check | Correct Example |
|---------|---------------|-----------------|
| **Wrong units** | Concentration should be per LITER, not per 100 mL | 1000 copies/L (not /100mL) |
| **Volume wrong** | Volume should be in mL, not L | 100 mL (not 0.1 L) |
| **Frequency wrong** | Frequency is per YEAR, not per week or day | 7 events/year (not 7/week) |
| **LRV backwards** | LRV reduces risk (higher LRV = lower risk) | 3.0 log = 99.9% removal |

**Still wrong?** Click the 📊 button next to concentration fields to see typical values.

### Problem: App is Slow or Freezes

**Quick fixes:**
- Reduce Monte Carlo iterations to 1,000 (instead of 10,000) for testing
- Close other programs to free up memory
- Check population size isn't extremely large (billions)

### Problem: Can't Generate Report

**Checklist:**
1. Have you run the assessment first? (Tab 4 must show results)
2. Do you have write permission to the save location?
3. Try saving to Desktop or Documents folder instead

**Still failing?** Reinstall report libraries: `pip install python-docx reportlab`

### Problem: Plots Don't Show Up

1. Go to **Tab 8 - Settings**
2. Check box "✓ Generate plots automatically"
3. Close and reopen **Tab 5 - Plots & Visualizations**
4. If still failing, reinstall: `pip install matplotlib`

### Common Error Messages

| Error | What It Means | How to Fix |
|-------|---------------|------------|
| "PathogenDatabase not found" | Missing database file | Reinstall toolkit or download pathogen_parameters.json |
| "Invalid concentration value" | You entered text instead of number | Use numbers only: 1000 (not "1,000" or "high") |
| "LRV out of range" | LRV should be 0-8 | Enter realistic LRV (most treatment is 0.5-5.0) |
| "Monte Carlo failed" | Bad input parameter | Check all numbers are positive, non-zero |

### Still Need Help?

1. Check this manual's Table of Contents for your topic
2. Look at example projects in `qmra_toolkit/examples/` folder
3. Contact NIWA QMRA team with:
   - Screenshot of the problem
   - Your project file (.qmra)
   - What you were trying to do

---

## Tips & Best Practices

### Before You Start

- **Gather your data first**: Know your pathogen concentrations before opening the app
- **Use recent data**: Water quality data should be < 3 months old if possible
- **Multiple samples better than one**: Don't base assessment on a single measurement
- **Save often**: Click **💾 Save Project** regularly to avoid losing work

### Choosing Input Values

| Parameter | How to Choose | Tips |
|-----------|---------------|------|
| **Pathogen Concentration** | Use monitoring data average | Click 📊 for typical ranges; use conservative (high) values if uncertain |
| **Exposure Volume** | Use literature values for activity type | Swimming: 50-100 mL; Drinking: 2000 mL daily |
| **Exposure Frequency** | Estimate realistically | Summer swimming: 5-20/year; Year-round: 50-100/year |
| **Population at Risk** | Count actual exposed population | Beach users, water supply customers, shellfish consumers |

### Making Good Assessments

✅ **DO**:
- Document where your data came from
- Use **median** result as your best estimate
- Report uncertainty (5th-95th percentile range)
- Compare results to similar published studies
- Have a colleague review before submitting

❌ **DON'T**:
- Use outdated data (>1 year old)
- Ignore seasonal variation (summer vs winter)
- Mix different measurement units
- Report only one number without uncertainty
- Skip saving your project

### For Regulatory Submissions

Use this checklist:
- ☐ Use **Technical Assessment Report** template
- ☐ Include all three percentiles (5th, median, 95th)
- ☐ Show compliance with NZ/WHO guidelines
- ☐ Include monitoring data in appendix
- ☐ Document all assumptions
- ☐ Get independent peer review

### Saving and Archiving

**Save your work in multiple formats:**
1. **Save project**: Click 💾 Save Project → Creates .qmra file (can reopen later)
2. **Export results**: Tab 4 → Export Results → Save as Excel/CSV
3. **Save plots**: Tab 5 → Save All → Creates PNG files
4. **Generate report**: Tab 6 → Generate Report → Creates PDF

**Naming convention suggestion:**
- `ProjectName_Date_Version.qmra` (e.g., "Beach_Swimming_2025-10-15_v1.qmra")
- Update version number when revising

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
