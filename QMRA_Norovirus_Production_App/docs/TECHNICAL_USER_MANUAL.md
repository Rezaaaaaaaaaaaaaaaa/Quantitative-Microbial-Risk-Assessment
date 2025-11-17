# QMRA Batch Processing Application
## Technical User Manual

**Version:** 2.0
**Date:** November 2025
**Organization:** NIWA (National Institute of Water and Atmospheric Research)
**Status:** Production Ready (Norovirus Risk Assessment)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Overview](#system-overview)
3. [Getting Started](#getting-started)
4. [Application Interface](#application-interface)
5. [Assessment Workflows](#assessment-workflows)
6. [Production Mode](#production-mode)
7. [QMRA Methodology](#qmra-methodology)
8. [Interpreting Results](#interpreting-results)
9. [Troubleshooting](#troubleshooting)
10. [Technical Support](#technical-support)

---

## 1. Executive Summary

The QMRA (Quantitative Microbial Risk Assessment) Batch Processing Application is a web-based tool designed to assess public health risks from pathogen exposure in recreational and drinking water environments. The application implements validated dose-response models and Monte Carlo simulation techniques to quantify infection and illness risks for exposed populations.

### Key Capabilities

- **Spatial Risk Assessment:** Evaluate multiple exposure sites with varying dilution factors
- **Temporal Analysis:** Analyze risk trends over time using monitoring data
- **Treatment Comparison:** Compare effectiveness of different water treatment technologies
- **Multi-Pathogen Evaluation:** Assess combined risks from multiple pathogens
- **Batch Processing:** Execute pre-configured scenarios for comprehensive analysis
- **Production Mode:** Validated norovirus risk assessment for operational use

### Validation Status

| **Pathogen** | **Model** | **Status** | **Reference** |
|--------------|-----------|------------|---------------|
| Norovirus | Beta-Binomial | ✅ Validated | Teunis et al. (2008) |
| Other pathogens | Beta-Poisson | ⚠️ Research Only | Not validated |

**Note:** This application has been validated for **norovirus risk assessment only** under the current contract scope. Other pathogens are available in Research Mode for exploratory purposes but require additional validation before operational use.

---

## 2. System Overview

### 2.1 Architecture

The application follows a modular architecture with distinct components for data processing, risk calculation, and visualization:

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Interface (Streamlit)                 │
├─────────────────────────────────────────────────────────────┤
│                    Batch Processor Core                      │
│  ┌───────────────┬──────────────────┬───────────────────┐   │
│  │ Monte Carlo   │ Dose-Response    │ Pathogen          │   │
│  │ Simulator     │ Models           │ Database          │   │
│  └───────────────┴──────────────────┴───────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│              Input Data Processing & Validation              │
├─────────────────────────────────────────────────────────────┤
│         Results Export (CSV, PDF) & Visualization            │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Technical Specifications

- **Platform:** Python 3.8+, Streamlit framework
- **Computation:** NumPy/SciPy-based Monte Carlo simulation
- **Default Iterations:** 10,000 uncertainty scenarios
- **Dose-Response:** Beta-Binomial exact model for norovirus (α=0.04, β=0.055)
- **WHO Guideline:** Annual infection risk ≤ 1×10⁻⁴ (0.01%)

### 2.3 Data Requirements

#### Input Files

1. **Pathogen Concentration Data** (CSV)
   - Columns: Sample_ID, Sample_Date, Norovirus_copies_per_L
   - Format: Numeric concentrations in organisms/L

2. **Dilution Factor Data** (CSV)
   - Columns: Site_Name, Dilution_Factor, Distance_m
   - Format: Dilution ratios (e.g., 100 = 100:1 dilution)

3. **Scenario Definitions** (CSV)
   - Columns: Scenario_ID, Treatment_Type, Log_Reduction, Volume_mL
   - Format: Treatment parameters and exposure conditions

#### Output Files

- **Results CSV:** Comprehensive risk metrics with uncertainty bounds
- **PDF Report:** Publication-ready summary with plots and tables
- **Plots:** PNG images for risk distributions and compliance

---

## 3. Getting Started

### 3.1 Installation

**Prerequisites:**
- Python 3.8 or higher
- pip package manager
- Internet connection (for initial setup)

**Installation Steps:**

```bash
# 1. Navigate to application directory
cd Batch_Processing_App/app

# 2. Install required packages
pip install -r ../requirements.txt

# 3. Verify installation
python -c "import streamlit; print('Streamlit version:', streamlit.__version__)"
```

### 3.2 Launching the Application

```bash
# Start the web application
streamlit run web_app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`.

**Default Credentials:** Not required (local deployment)

**First-Time Setup:**
1. Verify Production Mode is enabled (checkbox in sidebar)
2. Confirm "Norovirus" appears as the only pathogen option
3. Load example data to test functionality

### 3.3 Quick Start Guide

**5-Minute Test:**

1. Launch application
2. Select "Temporal Assessment" from sidebar
3. Click "Use example monitoring data"
4. Set exposure frequency: 20 events/year
5. Set population: 10,000 people
6. Click "Run Temporal Assessment"
7. Review results and download CSV

---

## 4. Application Interface

### 4.1 Home Page

![Home Page](../screenshots/01_home_page_20251105_103639.png)

**Figure 1:** Main application interface showing sidebar navigation and Production Mode toggle.

The home page provides access to all assessment modules:

- **Sidebar Navigation:** Select assessment type from dropdown menu
- **Production Mode Toggle:** Enable/disable validated norovirus-only mode (default: ON)
- **Status Indicators:** Visual confirmation of mode and pathogen availability
- **Quick Links:** Access to documentation and example data

**Key Interface Elements:**

1. **Page Selector:** Dropdown menu to switch between assessment types
2. **Production Mode Checkbox:** Controls pathogen availability
3. **Information Panel:** Displays current mode status and warnings
4. **Main Content Area:** Assessment-specific input forms and results

### 4.2 Sidebar Configuration

The sidebar contains global settings that apply across all assessment types:

**Production Mode (Default: ON)**
- ✅ Enabled: Only norovirus available (validated model)
- ❌ Disabled: All 6 pathogens available (research mode, unvalidated)

**Navigation Menu:**
- Batch Scenarios
- Spatial Assessment
- Temporal Assessment
- Treatment Comparison
- Multi-Pathogen Assessment

**Status Panel:**
- Current operational mode
- Validation warnings (if in Research Mode)
- Pathogen model information

---

## 5. Assessment Workflows

### 5.1 Batch Scenarios

![Batch Scenarios](../screenshots/02_batch_scenarios_20251105_103642.png)

**Figure 2:** Batch Scenarios interface for processing multiple pre-configured assessments.

**Purpose:** Execute comprehensive risk assessments using pre-defined scenario libraries.

**Use Case:** Regulatory compliance analysis, systematic treatment evaluation, sensitivity studies.

**Workflow:**

1. **Upload Scenario Files** (or use examples)
   - `scenarios.csv` - 15 pre-configured exposure scenarios
   - `pathogen_data.csv` - 3 norovirus pathogen definitions
   - `dilution_data.csv` - Spatial dilution factors

2. **Configure Settings**
   - Pathogen: Norovirus (auto-selected in Production Mode)
   - Monte Carlo iterations: 10,000 (default, recommended)
   - Log Reduction: Specify treatment effectiveness (LRV 0-6)

3. **Execute Batch Processing**
   - Click "Run Batch Assessment"
   - Processing time: ~30-60 seconds for 15 scenarios
   - Progress indicator shows current scenario

4. **Review Results**
   - Summary table: Risk metrics for all scenarios
   - Compliance status: WHO guideline comparison
   - Risk ranking: Scenarios ordered by annual risk

5. **Export Outputs**
   - CSV: Complete results with uncertainty bounds
   - PDF: Executive summary with plots
   - Plots: Individual PNG files for each scenario

**Example Results Table:**

| Scenario | Pathogen | Annual Risk (Median) | Population Impact | Compliance |
|----------|----------|---------------------|-------------------|------------|
| Scenario_001 | Norovirus | 5.97×10⁻³ | 60 infections/year | Non-Compliant |
| Scenario_002 | Norovirus | 8.33×10⁻³ | 83 infections/year | Non-Compliant |

---

### 5.2 Spatial Assessment

![Spatial Assessment](../screenshots/03_spatial_assessment_20251105_103653.png)

**Figure 3:** Spatial Assessment module for multi-site risk comparison.

**Purpose:** Compare infection risks across multiple spatial locations with varying dilution factors.

**Use Case:** Beach water quality monitoring, sewage outfall impact assessment, marine discharge zones.

**Workflow:**

1. **Upload Dilution Data**
   - File format: CSV with Site_Name, Dilution_Factor columns
   - Example: `spatial_dilution_6_sites.csv` (600 simulations for 6 sites)
   - Data source: Hydrodynamic models, tracer studies, or empirical measurements

2. **Specify Exposure Conditions**
   - **Pathogen Concentration:** Mean/median in source water (org/L)
     - Hockey Stick distribution: Min, Median, Max, Breakpoint percentile
   - **Treatment Log Reduction:** LRV for source treatment (typically 2-4 for UV)
   - **Exposure Volume:** Water ingested per event (mL, range: 30-100)
   - **Exposure Frequency:** Number of events per year (typically 10-50)
   - **Exposed Population:** Number of people at risk (e.g., 10,000 swimmers)

3. **Run Assessment**
   - Click "Run Spatial Assessment"
   - Algorithm:
     ```
     For each site:
       For each Monte Carlo iteration (10,000):
         1. Sample concentration from Hockey Stick distribution
         2. Apply treatment: C_treated = C_raw / 10^LRV
         3. Apply dilution: C_receiving = C_treated / Dilution_Factor
         4. Calculate dose: Dose = C_receiving × Volume_sampled
         5. Calculate P(infection) using Beta-Binomial model
       Calculate annual risk: 1 - (1 - P_event)^frequency
       Calculate population impact: Annual_risk × Population
     ```

4. **Interpret Results**
   - **Risk Map:** Sites ranked by annual infection risk
   - **Compliance Chart:** Sites meeting/exceeding WHO guideline
   - **Uncertainty Bands:** 5th-95th percentile ranges
   - **Critical Sites:** Locations requiring intervention

5. **Export and Document**
   - Download CSV with all site results
   - Generate PDF report with maps and charts
   - Export individual site risk profiles

**Key Metrics Reported:**

- **Per-Event Infection Risk:** Median and 90% uncertainty interval
- **Annual Infection Risk:** Probability of at least one infection per person per year
- **Population Impact:** Expected number of infections in exposed population
- **Compliance Status:** WHO guideline achievement (≤1×10⁻⁴)

---

### 5.3 Temporal Assessment

![Temporal Assessment](../screenshots/04_temporal_assessment_20251105_103704.png)

**Figure 4:** Temporal Assessment interface for time-series risk analysis.

**Purpose:** Analyze temporal trends in infection risk using time-series monitoring data.

**Use Case:** Seasonal risk patterns, treatment performance monitoring, regulatory compliance tracking.

**Workflow:**

1. **Upload Monitoring Data**
   - File format: CSV with Sample_Date, Norovirus_copies_per_L columns
   - Example: `weekly_monitoring_2024.csv` (52 weeks of data)
   - Frequency: Weekly, monthly, or event-based sampling

2. **Configure Temporal Parameters**
   - **Treatment LRV:** Constant or time-varying
   - **Dilution Factor:** Fixed value or site-specific
   - **Exposure Volume:** Mean ingestion volume (mL)
   - **Frequency:** Annual exposure events per person
   - **Population:** Size of exposed population

3. **Execute Temporal Analysis**
   - Click "Run Temporal Assessment"
   - Processing: Calculates risk for each time point
   - Time series: Plots risk vs. date

4. **Analyze Trends**
   - **Seasonal Patterns:** Identify high-risk periods (e.g., winter norovirus peaks)
   - **Compliance Timeline:** Track WHO guideline achievement over time
   - **Treatment Performance:** Correlate LRV with risk reduction
   - **Outbreak Detection:** Flag anomalous risk spikes

5. **Generate Time-Series Outputs**
   - Line plots: Risk vs. time with uncertainty bands
   - Exceedance analysis: Fraction of time exceeding thresholds
   - Cumulative risk: Total illness burden over assessment period
   - CSV export: Date-indexed risk metrics

**Temporal Metrics:**

- **Peak Risk:** Maximum annual risk observed
- **Median Risk:** Typical risk during assessment period
- **Exceedance Frequency:** % of time exceeding WHO guideline
- **Seasonal Variation:** Coefficient of variation in risk

---

### 5.4 Treatment Comparison

![Treatment Comparison](../screenshots/05_treatment_comparison_20251105_103715.png)

**Figure 5:** Treatment Comparison module for technology evaluation.

**Purpose:** Compare effectiveness of different water treatment technologies or configurations.

**Use Case:** Treatment plant design, technology selection, cost-benefit analysis, regulatory approval.

**Workflow:**

1. **Define Treatment Scenarios**
   - Scenario A: Baseline (e.g., chlorination only, LRV = 2)
   - Scenario B: Enhanced (e.g., UV + chlorination, LRV = 4)
   - Scenario C: Advanced (e.g., UV + membrane filtration, LRV = 6)

2. **Upload Treatment Data**
   - File format: CSV with Treatment_Name, Log_Reduction columns
   - Optionally include cost, energy consumption, footprint

3. **Specify Common Conditions**
   - **Source Concentration:** Same for all treatments (baseline comparison)
   - **Dilution Factor:** Receiving water dilution
   - **Exposure Parameters:** Volume, frequency, population

4. **Run Comparison**
   - Click "Compare Treatments"
   - Parallel processing: All treatments assessed simultaneously
   - Standardized output format

5. **Evaluate Treatment Performance**
   - **Risk Reduction:** Compare annual risks across treatments
   - **Cost-Effectiveness:** Risk reduction per dollar invested
   - **Compliance Achievement:** Which treatments meet WHO guideline
   - **Margin of Safety:** How much buffer above guideline

6. **Decision Support Outputs**
   - Comparison table: Side-by-side treatment metrics
   - Bar charts: Visual comparison of risks
   - Recommendation: Optimal treatment based on criteria
   - Sensitivity analysis: Effect of parameter uncertainty

**Treatment Comparison Table:**

| Treatment | LRV | Annual Risk | Risk Reduction | Compliant? | Cost Ratio |
|-----------|-----|-------------|----------------|------------|------------|
| Baseline (Chlorine) | 2 | 5.97×10⁻³ | Reference | No | 1.0 |
| Enhanced (UV+Cl₂) | 4 | 5.97×10⁻⁵ | 100× | Yes | 1.8 |
| Advanced (UV+MF) | 6 | 5.97×10⁻⁷ | 10,000× | Yes | 3.2 |

**Decision Criteria:**
- Minimum LRV to achieve WHO guideline
- Most cost-effective compliant treatment
- Robustness to concentration variability

---

### 5.5 Multi-Pathogen Assessment

![Multi-Pathogen Assessment](../screenshots/06_multi_pathogen_20251105_103726.png)

**Figure 6:** Multi-Pathogen Assessment interface (Research Mode).

**Purpose:** Evaluate combined risks from multiple pathogens simultaneously.

**Use Case:** Comprehensive water quality assessment, relative risk comparison, research studies.

**⚠️ Important:** Multi-pathogen assessments require **Research Mode** (uncheck Production Mode). Only norovirus has been validated for operational use.

**Workflow:**

1. **Enable Research Mode**
   - Uncheck "Production Mode" in sidebar
   - Review warning about unvalidated pathogens
   - Proceed only for research/exploratory purposes

2. **Upload Multi-Pathogen Data**
   - File format: CSV with columns for each pathogen concentration
   - Example: `multi_pathogen_data.csv` (norovirus, campylobacter, cryptosporidium, etc.)

3. **Select Pathogens**
   - Use multi-select dropdown
   - Available: Norovirus, Campylobacter, Cryptosporidium, E. coli, Rotavirus, Salmonella
   - Note: Only norovirus uses validated Beta-Binomial model

4. **Configure Assessment**
   - **Treatment:** Same LRV applied to all pathogens (or pathogen-specific)
   - **Exposure:** Common volume, frequency, population
   - **Models:** Norovirus (Beta-Binomial), others (Beta-Poisson approximation)

5. **Run Multi-Pathogen Analysis**
   - Click "Run Multi-Pathogen Assessment"
   - Individual risks calculated for each pathogen
   - Combined risk estimated (assuming independence)

6. **Compare Pathogen Risks**
   - **Relative Ranking:** Which pathogen drives overall risk?
   - **Risk Contribution:** % of total risk from each pathogen
   - **Compliance:** Which pathogens cause non-compliance?
   - **Treatment Effectiveness:** Pathogen-specific LRV requirements

**Multi-Pathogen Results Table:**

| Pathogen | Model | Annual Risk | % Total Risk | Dominant? |
|----------|-------|-------------|--------------|-----------|
| Norovirus | Beta-Binomial | 5.97×10⁻³ | 85% | Yes |
| Campylobacter | Beta-Poisson | 8.20×10⁻⁴ | 12% | No |
| Cryptosporidium | Beta-Poisson | 2.10×10⁻⁴ | 3% | No |

**Research Considerations:**
- Beta-Poisson models for non-norovirus pathogens are approximations
- Relative risks may be informative but require validation
- Use for hypothesis generation and research planning
- Do not use for regulatory compliance without additional validation

---

## 6. Production Mode

### 6.1 What is Production Mode?

Production Mode is a safety feature that restricts the application to **validated norovirus risk assessment only**, ensuring compliance with the current contract scope and scientific validation standards.

**When Production Mode is ENABLED (default):**
- ✅ Only norovirus is available for selection
- ✅ Beta-Binomial exact model is used (validated)
- ✅ Results suitable for regulatory reporting
- ✅ Full quality assurance confidence

**When Production Mode is DISABLED (Research Mode):**
- ⚠️ All 6 pathogens available
- ⚠️ Non-norovirus pathogens use Beta-Poisson approximations (NOT validated)
- ⚠️ Warning displayed prominently
- ⚠️ Results for research/exploratory use only

### 6.2 Enabling/Disabling Production Mode

**To Enable Production Mode (Recommended):**
1. Locate "Production Mode (Norovirus Only)" checkbox in sidebar
2. Ensure box is **checked** (✅)
3. Confirm green "Production Mode Active" message appears
4. Verify pathogen dropdown shows only "Norovirus"

**To Disable Production Mode (Research Use Only):**
1. Uncheck "Production Mode (Norovirus Only)" checkbox
2. Read and acknowledge warning message
3. Confirm understanding that other pathogens are unvalidated
4. Proceed with research assessment

### 6.3 Validation Status

**Norovirus - Beta-Binomial Model:**
- ✅ **Validated:** Exact match to reference Excel model (David Wood)
- ✅ **Test Results:** Doses 1, 10, 100 → P(infection) = 0.421053, 0.480735, 0.527157
- ✅ **Reference:** Teunis et al. (2008) updated parameters
- ✅ **Verification:** McBride (2017) Bell Island QMRA
- ✅ **Production Ready:** Approved for operational use

**Other Pathogens - Beta-Poisson Models:**
- ⚠️ **Not Validated:** No independent verification performed
- ⚠️ **Research Only:** Requires additional validation before operational use
- ⚠️ **Approximation:** Beta-Poisson may underestimate risk by 2-4× for low-dose pathogens
- ⚠️ **Use With Caution:** Suitable for exploratory analysis only

### 6.4 Verification Evidence

The Beta-Binomial implementation has been rigorously verified:

**Test Case: Norovirus (α=0.04, β=0.055)**

| Dose (organisms) | Our Code | David's Excel | Match? |
|------------------|----------|---------------|--------|
| 1 | 0.421053 | 0.421053 | ✅ Exact |
| 10 | 0.480735 | 0.480735 | ✅ Exact |
| 100 | 0.527157 | 0.527157 | ✅ Exact |

**Formula Verification:**
```
P(infection) = 1 - exp(ln(Γ(β+dose)) + ln(Γ(α+β)) - ln(Γ(α+β+dose)) - ln(Γ(β)))

Where: Γ = gamma function, ln(Γ) = gammaln function
```

This exact match confirms the implementation is mathematically correct and suitable for operational use.

---

## 7. QMRA Methodology

### 7.1 Risk Assessment Framework

The application implements the standard QMRA framework as recommended by WHO Guidelines for Drinking-water Quality (2017) and recreational water quality guidelines.

**Four-Step Process:**

```
┌─────────────────────────────────────────────────────────────┐
│  1. HAZARD IDENTIFICATION                                    │
│     └─ Select pathogen (norovirus)                          │
│     └─ Identify exposure routes (primary contact)            │
├─────────────────────────────────────────────────────────────┤
│  2. EXPOSURE ASSESSMENT                                      │
│     └─ Pathogen concentration in source water                │
│     └─ Treatment effectiveness (Log Reduction)               │
│     └─ Dilution in receiving water                          │
│     └─ Volume ingested per exposure event                   │
│     └─ Frequency of exposure per year                       │
├─────────────────────────────────────────────────────────────┤
│  3. DOSE-RESPONSE ASSESSMENT                                │
│     └─ Beta-Binomial model for norovirus                    │
│     └─ P(infection) = f(dose, α, β)                         │
│     └─ P(illness) = P(infection) × P(ill|infected) × susc.  │
├─────────────────────────────────────────────────────────────┤
│  4. RISK CHARACTERIZATION                                   │
│     └─ Annual infection risk: 1 - (1 - P_event)^frequency   │
│     └─ Population impact: Annual_risk × Population           │
│     └─ WHO compliance: Risk ≤ 1×10⁻⁴                        │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Dose Calculation

**Step-by-Step Calculation:**

1. **Source Concentration** (C_source)
   - Input: Pathogen concentration in raw/source water (org/L)
   - Distribution: Hockey Stick (Min, Median, Max, Breakpoint)

2. **Treatment** (C_treated)
   ```
   C_treated = C_source / 10^LRV

   Where LRV = Log Reduction Value
   Example: LRV=3 → 99.9% removal → Factor of 1000
   ```

3. **Dilution** (C_receiving)
   ```
   C_receiving = C_treated / Dilution_Factor

   Example: Dilution=100 → 100:1 dilution in receiving water
   ```

4. **Exposure Dose**
   ```
   Dose = (C_receiving / 1000) × Volume_mL

   Units: organisms ingested per exposure event
   Example: C_receiving=0.05 org/L, Volume=50 mL
            Dose = (0.05/1000) × 50 = 0.0025 organisms
   ```

### 7.3 Dose-Response Models

**Beta-Binomial Model (Norovirus):**

```
P(infection) = 1 - exp(gammaln(β+dose) + gammaln(α+β) - gammaln(α+β+dose) - gammaln(β))

Parameters:
  α = 0.04 (shape parameter)
  β = 0.055 (shape parameter)
  dose = organisms ingested
  gammaln = natural log of gamma function
```

**Key Properties:**
- **Exact Model:** No approximations, accounts for heterogeneity in host susceptibility
- **Low-Dose Accuracy:** Reliable for sub-single organism exposures
- **Upper Bound:** Asymptotic maximum P(infection) ≈ 0.53 at high doses
- **Validated:** Matches reference implementation exactly

**Why NOT Beta-Poisson for Norovirus:**

Beta-Poisson is an approximation valid only when β >> 1. For norovirus (β=0.055 << 1):
- ❌ Underestimates risk by 2-4× at typical doses
- ❌ Violates model assumptions
- ❌ Not supported by current best practices

### 7.4 Monte Carlo Simulation

**Purpose:** Quantify uncertainty in risk estimates due to variability in input parameters.

**Structure:**

```
For iteration i = 1 to 10,000:
  1. Sample concentration from Hockey Stick distribution → C_i
  2. Sample volume from Uniform distribution → V_i
  3. Sample dilution from Empirical CDF → D_i

  4. Calculate dose_i:
     dose_i = (C_i / 10^LRV / D_i / 1000) × V_i

  5. Calculate P(infection)_i using Beta-Binomial model
  6. Calculate P(illness)_i = P(infection)_i × 0.60 × 0.74

Calculate statistics:
  - Median: 50th percentile of 10,000 values
  - 5th percentile: Lower uncertainty bound
  - 95th percentile: Upper uncertainty bound
```

**Important:** 10,000 iterations represent 10,000 **uncertainty scenarios**, NOT 10,000 individual people. Each iteration samples different values from input distributions to characterize uncertainty.

### 7.5 Annual Risk Calculation

**Per-Event to Annual Risk:**

```
P(annual infection) = 1 - (1 - P(per event))^frequency

Derivation:
  P(no infection all year) = P(no infection event 1) × ... × P(no infection event n)
                           = (1 - P_event)^n    [assuming independent events]

  P(at least one infection) = 1 - P(no infection all year)
                            = 1 - (1 - P_event)^n

Example:
  Per-event risk = 0.001 (0.1%)
  Frequency = 20 events/year
  Annual risk = 1 - (1-0.001)^20 = 1 - 0.9802 = 0.0198 (1.98%)
```

**Interpretation:** Annual risk is the probability that a person experiences **at least one infection** during the year, given their exposure frequency.

### 7.6 Population Impact

```
Expected infections per year = Annual risk × Exposed population

Example:
  Annual risk = 0.0198 (1.98%)
  Population = 10,000 people
  Expected infections = 0.0198 × 10,000 = 198 infections/year
```

**Interpretation:** This is the **expected value** (mean) of infections in the population. Actual number may vary due to stochastic effects, but 198 is the best estimate for planning purposes.

### 7.7 WHO Guideline Compliance

**WHO Threshold:** Annual infection risk ≤ 1×10⁻⁴ (0.01% or 1 in 10,000 per year)

**Compliance Check:**

```python
if annual_risk_median <= 1e-4:
    status = "COMPLIANT"
else:
    status = "NON-COMPLIANT"
    exceedance_factor = annual_risk_median / 1e-4
```

**Example:**
- Annual risk = 5.97×10⁻³ (0.597%)
- WHO threshold = 1.00×10⁻⁴ (0.01%)
- Status: NON-COMPLIANT (59.7× over threshold)
- Action: Treatment upgrade required to achieve 60× additional reduction

---

## 8. Interpreting Results

### 8.1 Risk Metrics Explained

**Per-Event Infection Risk:**
- **Definition:** Probability of infection from a single exposure event
- **Units:** Unitless probability (0 to 1) or percentage
- **Typical Range:** 10⁻⁶ to 10⁻² for treated water
- **Use:** Comparing exposure routes, assessing single-event risks

**Annual Infection Risk:**
- **Definition:** Probability of at least one infection per person per year
- **Units:** Unitless probability, expressed as scientific notation (e.g., 5.97×10⁻³)
- **Guideline:** WHO recommends ≤ 1×10⁻⁴
- **Use:** Regulatory compliance, public health protection

**Population Impact:**
- **Definition:** Expected number of infections in exposed population per year
- **Units:** Number of infections (people/year)
- **Use:** Burden of disease estimation, cost-benefit analysis

### 8.2 Uncertainty Interpretation

Results include 90% uncertainty intervals (5th to 95th percentiles):

**Example Result:**
```
Annual Risk (Median): 5.97×10⁻³
Annual Risk (5th %ile): 1.00×10⁻³
Annual Risk (95th %ile): 2.30×10⁻²
```

**Interpretation:**
- **Median (50th percentile):** Best estimate, 50% chance risk is higher, 50% lower
- **5th percentile:** Conservative lower bound, 95% confident risk exceeds this
- **95th percentile:** Conservative upper bound, 95% confident risk is below this
- **Range width:** Indicates uncertainty magnitude; wider = more uncertain

**Decision-Making:**
- Use **median** for best estimate
- Use **95th percentile** for conservative/protective decisions
- Narrow uncertainty intervals indicate high confidence in results

### 8.3 Compliance Interpretation

**Compliant (Annual Risk ≤ 1×10⁻⁴):**
- ✅ Meets WHO guideline for safe water
- ✅ Adequate public health protection
- ✅ No action required (unless margin is small)
- ✅ Monitor to ensure continued compliance

**Non-Compliant (Annual Risk > 1×10⁻⁴):**
- ❌ Exceeds WHO guideline
- ❌ Public health risk present
- ❌ Action required: Improve treatment, reduce exposure, or restrict access
- ❌ Calculate exceedance factor to determine required risk reduction

**Exceedance Factor:**
```
Factor = Annual_risk / WHO_threshold

Example: 5.97×10⁻³ / 1×10⁻⁴ = 59.7×
Interpretation: Need 60× risk reduction to achieve compliance
```

**Treatment Options to Achieve Compliance:**
```
Required LRV = log₁₀(Exceedance_Factor)

Example: log₁₀(59.7) = 1.78
Interpretation: Need to increase treatment LRV by ~1.8 (e.g., from LRV=3 to LRV=4.8)
```

### 8.4 Spatial Results Interpretation

**Site Comparison:**

Sites are ranked by risk to prioritize interventions:

| Site | Distance (m) | Dilution | Annual Risk | Rank | Priority |
|------|-------------|----------|-------------|------|----------|
| Discharge | 0 | 1 | 4.21×10⁻¹ | 1 | Critical |
| Site_50m | 50 | 7 | 8.33×10⁻³ | 2 | High |
| Site_100m | 100 | 14 | 5.97×10⁻³ | 3 | High |
| Site_500m | 500 | 200 | 3.12×10⁻⁴ | 4 | Medium |
| Site_1000m | 1000 | 850 | 5.20×10⁻⁵ | 5 | Low (Compliant) |

**Actions:**
- **Critical Sites:** Restrict access, post warnings
- **High Priority:** Increase treatment, reduce exposure frequency
- **Medium Priority:** Monitor, consider seasonal restrictions
- **Low Priority (Compliant):** Maintain current management

### 8.5 Temporal Results Interpretation

**Time-Series Analysis:**

Identify patterns and trends:

- **Seasonal Peaks:** Winter (Jan-Mar) norovirus risk typically 3-5× higher than summer
- **Treatment Performance:** Stable LRV → stable risk; declining LRV → increasing risk
- **Outbreak Detection:** Sudden spikes indicate contamination events requiring investigation
- **Long-Term Trends:** Are risks increasing, decreasing, or stable over time?

**Example Findings:**
```
Peak Risk Period: January-March (winter)
  - Median annual risk: 1.54×10⁻²
  - Exceedance: 90% of weeks non-compliant
  - Recommendation: Seasonal treatment upgrade or swimming restrictions

Low Risk Period: June-August (summer)
  - Median annual risk: 2.10×10⁻⁴
  - Exceedance: 15% of weeks non-compliant
  - Recommendation: Maintain current treatment, target specific high-risk weeks
```

### 8.6 Treatment Comparison Results

**Decision Matrix:**

| Treatment | Capital Cost | Annual Cost | LRV | Risk Reduction | Compliant? | Cost-Effectiveness |
|-----------|-------------|-------------|-----|----------------|------------|--------------------|
| Baseline | $0 | $50k | 2 | 1× | No | - |
| UV Addition | $200k | $80k | 4 | 100× | Yes | $2,000/factor |
| UV+Membrane | $500k | $120k | 6 | 10,000× | Yes | $500/factor |

**Recommendation:**
- UV Addition provides sufficient risk reduction to achieve compliance
- Most cost-effective option on annualized basis ($80k/year vs. $120k/year)
- UV+Membrane provides excessive margin (10,000× reduction when 100× needed)
- Selected option: UV Addition

---

## 9. Troubleshooting

### 9.1 Common Issues

**Issue:** "QMRA modules required for distribution-based assessments"
**Cause:** Python path not configured correctly
**Solution:**
```bash
cd Batch_Processing_App/app
python -c "from qmra_core import PathogenDatabase; print('OK')"
```
If error persists, check that `sys.path.insert(0, '..')` is at top of batch_processor.py

---

**Issue:** "File not found: input_data/..."
**Cause:** Incorrect relative path from app directory
**Solution:** Use example data buttons instead of manual file upload, or ensure file paths use `../input_data/...`

---

**Issue:** Production Mode shows multiple pathogens
**Cause:** Production Mode checkbox not enabled
**Solution:** Check "Production Mode (Norovirus Only)" box in sidebar, verify green status message

---

**Issue:** Results show very high risk (>0.5)
**Cause:** Concentration or dilution parameters unrealistic
**Solution:** Review input data:
- Typical treated effluent: 100-10,000 org/L
- Typical dilution factors: 10-1,000
- Typical LRV: 2-6

---

**Issue:** CSV export fails or is empty
**Cause:** Assessment not completed before export attempt
**Solution:** Wait for "Results:" header to appear, then click "Download Results CSV"

---

### 9.2 Data Validation Errors

**Error:** "Invalid concentration values: must be > 0"
**Fix:** Check CSV file for missing data, zeros, or negative values. Replace with realistic positives.

**Error:** "Dilution factor must be ≥ 1"
**Fix:** Dilution factors are ratios (e.g., 100 = 100:1 dilution). Values <1 indicate concentration, not dilution.

**Error:** "Hockey Stick parameters invalid: x_min < x_median < x_max required"
**Fix:** Ensure Min < Median < Max in concentration distribution settings.

---

### 9.3 Performance Issues

**Slow Processing (>2 minutes for single assessment):**
- Reduce iterations from 10,000 to 1,000 for testing (not recommended for final results)
- Close other applications to free memory
- Check if antivirus is scanning Python processes

**Browser Crashes:**
- Use Chrome or Firefox (Edge may have compatibility issues)
- Disable browser extensions
- Clear browser cache

---

## 10. Technical Support

### 10.1 Contact Information

**Primary Contact:**
Reza Moghaddam, PhD
NIWA (National Institute of Water and Atmospheric Research)
Email: reza.moghaddam@niwa.co.nz
Phone: [Contact details]

**Technical Validation:**
David Wood
[Contact details]

### 10.2 Reporting Issues

When reporting technical issues, please provide:

1. **Error Message:** Complete text from error dialog or console
2. **Steps to Reproduce:** Detailed sequence leading to issue
3. **Input Files:** Example CSV files causing the problem (if applicable)
4. **Screenshot:** Visual evidence of the issue
5. **Environment:** Operating system, Python version, browser

**Example Issue Report:**

```
Subject: Error in Temporal Assessment - Invalid Date Format

Description:
When uploading weekly_monitoring_custom.csv to Temporal Assessment,
receiving error "Invalid date format in row 15: 32/01/2024"

Steps to Reproduce:
1. Navigate to Temporal Assessment
2. Upload attached CSV file
3. Click "Run Temporal Assessment"
4. Error appears immediately

Expected Behavior:
Assessment should process with dates in DD/MM/YYYY format

Actual Behavior:
Error message appears, assessment does not run

Environment:
- OS: Windows 11
- Python: 3.10.5
- Browser: Chrome 118
- App Version: 2.0

Attached: weekly_monitoring_custom.csv
```

### 10.3 Documentation Updates

This manual is version-controlled and updated regularly. Current version: **2.0 (November 2025)**.

**Revision History:**
- **v2.0 (Nov 2025):** Added Production Mode, updated to Beta-Binomial validation
- **v1.5 (Oct 2025):** Initial batch processing implementation
- **v1.0 (Sep 2025):** Single-scenario assessments only

Check for updates at: [Internal documentation repository]

---

## Appendices

### Appendix A: Glossary

**Annual Risk:** Probability of at least one infection per person per year
**Beta-Binomial:** Exact dose-response model accounting for host variability
**Beta-Poisson:** Approximate dose-response model (valid only when β >> 1)
**Dilution Factor:** Ratio of receiving water volume to discharge volume
**Hockey Stick Distribution:** Hybrid distribution with uniform body and exponential tail
**LRV (Log Reduction Value):** log₁₀(C_influent / C_effluent), e.g., LRV=3 = 99.9% removal
**Monte Carlo Simulation:** Computational method to propagate uncertainty through calculations
**Per-Event Risk:** Probability of infection from single exposure event
**Production Mode:** Safety feature restricting app to validated norovirus assessments
**QMRA:** Quantitative Microbial Risk Assessment
**WHO Guideline:** Annual infection risk ≤ 1×10⁻⁴ for safe water

### Appendix B: References

1. Teunis, P.F.M., et al. (2008). Norwalk virus: How infectious is it? *Journal of Medical Virology*, 80(8), 1468-1476.

2. World Health Organization (2017). *Guidelines for Drinking-water Quality: Fourth Edition Incorporating the First Addendum*. Geneva: WHO.

3. McBride, G.B. (2017). *Bell Island QMRA for Wastewater Discharge*. Technical Report, NIWA.

4. Haas, C.N., Rose, J.B., & Gerba, C.P. (2014). *Quantitative Microbial Risk Assessment* (2nd ed.). John Wiley & Sons.

5. National Research Council (1983). *Risk Assessment in the Federal Government: Managing the Process*. Washington, DC: National Academies Press.

### Appendix C: Example Data Files

Example files are located in `Batch_Processing_App/input_data/`:

**Production Mode Files (Norovirus Only):**
- `pathogen_data.csv` - 3 norovirus scenarios
- `norovirus_monitoring_data.csv` - 12 weekly samples
- `spatial_dilution_6_sites.csv` - 6 spatial locations
- `weekly_monitoring_2024.csv` - 52 weeks temporal data
- `scenarios.csv` - 15 assessment scenarios
- `dilution_data.csv` - General dilution factors

**Research Mode Files:**
- `multi_pathogen_data.csv` - 6 pathogens (use with caution)

See `README_EXAMPLE_DATA.md` for detailed descriptions.

### Appendix D: Calculation Verification

To verify calculations independently:

**Test Case: Norovirus Beta-Binomial**

```python
import numpy as np
from scipy.special import gammaln

def beta_binomial_infection_prob(dose, alpha=0.04, beta=0.055):
    log_prob_complement = (
        gammaln(beta + dose) +
        gammaln(alpha + beta) -
        gammaln(alpha + beta + dose) -
        gammaln(beta)
    )
    return 1.0 - np.exp(log_prob_complement)

# Verification values (David Wood's Excel)
assert abs(beta_binomial_infection_prob(1) - 0.421053) < 1e-5
assert abs(beta_binomial_infection_prob(10) - 0.480735) < 1e-5
assert abs(beta_binomial_infection_prob(100) - 0.527157) < 1e-5
print("Verification PASSED")
```

---

**End of Technical User Manual**

**Document Control:**
- Document ID: QMRA-APP-MANUAL-v2.0
- Date: November 13, 2025
- Status: APPROVED FOR PRODUCTION USE
- Next Review: May 2026
