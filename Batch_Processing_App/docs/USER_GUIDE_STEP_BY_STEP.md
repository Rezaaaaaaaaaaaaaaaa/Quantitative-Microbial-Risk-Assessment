# QMRA Web App - Step-by-Step User Guide

## Quick Start: Running Your First Norovirus Risk Assessment

---

## STEP 1: Launch the Web Application

**Open Terminal/Command Prompt:**

```bash
# Navigate to the app folder
cd "Batch_Processing_App/app"

# Launch the Streamlit app
streamlit run web_app.py
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.x:8501
```

**Result:** Your web browser will automatically open to `http://localhost:8501`

---

## STEP 2: Configure Production Mode (Sidebar)

**What you see on the left sidebar:**

```
┌─────────────────────────────────────┐
│ 🔧 Configuration                    │
│                                     │
│ ☑ Production Mode (Norovirus Only) │ ← This should be CHECKED ✅
│                                     │
│ ✅ Production Mode Active           │
│ Norovirus dose-response validated   │
│ with Beta-Binomial model (exact).   │
│ Other pathogens require additional  │
│ validation.                         │
└─────────────────────────────────────┘
```

**Action:**
- ✅ **Keep the checkbox CHECKED** for production use (norovirus only)
- ⚠️ Uncheck only if you need research mode (all pathogens with warnings)

---

## STEP 3: Select Assessment Type

**In the sidebar, scroll down to "Assessment Mode":**

```
┌─────────────────────────────────────┐
│ Assessment Mode                     │
│                                     │
│ Select batch processing type:       │
│ ┌─────────────────────────────────┐ │
│ │ ▼ Spatial Assessment            │ │ ← Example selection
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘

Options:
• Batch Scenarios (library approach with 3 CSV files)
• Spatial Assessment (multiple sites, one pathogen)
• Temporal Assessment (time series data)
• Treatment Comparison (compare treatment options)
• Multi-Pathogen Assessment (compare pathogens)
```

**Choose based on your need:**
- **Spatial** → Different locations (dilution varies by site)
- **Temporal** → Over time (concentration varies by date)
- **Treatment** → Compare treatment technologies
- **Multi-Pathogen** → Compare different pathogens (production mode = norovirus only)
- **Batch Scenarios** → Full library approach with CSVs

---

## EXAMPLE A: Spatial Assessment (Step-by-Step)

### STEP 4A: Configure Input Data

**Main panel shows:**

```
🗺️ Spatial Risk Assessment
Evaluate risk across multiple sites with different dilution factors

┌─────────────────────────────────────┐
│ Input Parameters                    │
│                                     │
│ ☑ Use example dilution data        │ ← Check this for demo
│   (6 sites)                         │
│                                     │
│ Or upload your own CSV:             │
│ [Browse files...]                   │
└─────────────────────────────────────┘
```

**Action:**
- ✅ Check "Use example dilution data" for your first test
- Later: Upload your own CSV with columns: `Location, Dilution_Factor`

---

### STEP 5A: Select Pathogen

```
┌─────────────────────────────────────┐
│ Pathogen:                           │
│ ┌─────────────────────────────────┐ │
│ │ ▼ norovirus                     │ │ ← Only option in Production Mode ✅
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

**What you see:**
- **Production Mode ON:** Only "norovirus" available ✅
- **Research Mode:** 6 pathogens listed

---

### STEP 6A: Enter Assessment Parameters

```
┌─────────────────────────────────────────────────────┐
│ Effluent concentration (org/L):                     │
│ ┌─────────────────────────────────┐                 │
│ │ 1.00e+06                        │ ← Default 1 million org/L
│ └─────────────────────────────────┘                 │
│                                                     │
│ Treatment LRV:                                      │
│ ┌─────────────────────────────────┐                 │
│ │ 3.0                             │ ← Default 3-log reduction
│ └─────────────────────────────────┘                 │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Volume (mL):                                        │
│ ┌─────────────────────────────────┐                 │
│ │ 50.0                            │ ← Ingestion volume
│ └─────────────────────────────────┘                 │
│                                                     │
│ Frequency (events/year):                            │
│ ┌─────────────────────────────────┐                 │
│ │ 20                              │ ← Exposure frequency
│ └─────────────────────────────────┘                 │
│                                                     │
│ Population:                                         │
│ ┌─────────────────────────────────┐                 │
│ │ 10000                           │ ← Exposed population
│ └─────────────────────────────────┘                 │
└─────────────────────────────────────────────────────┘

Monte Carlo iterations:
┌─────────────────────────────────────────────────────┐
│ ▁▁▁▁▁▁▁▁▁▁█▁▁▁▁▁▁▁▁▁                                │
│      10000                                          │ ← Slide to adjust
│ (1000 to 50000)                                     │
└─────────────────────────────────────────────────────┘
```

**Typical Values:**
- **Concentration:** 1e6 org/L (raw wastewater)
- **Treatment LRV:** 3.0 (typical wastewater treatment)
- **Volume:** 50 mL (swimming ingestion)
- **Frequency:** 20 events/year (recreational swimming)
- **Population:** 10,000 people
- **Iterations:** 10,000 (recommended for stable results)

---

### STEP 7A: Run the Assessment

```
┌─────────────────────────────────────┐
│ [🚀 Run Spatial Assessment]         │ ← Click this button
└─────────────────────────────────────┘
```

**What happens:**
```
Processing...
⏳ Running Monte Carlo simulation (10,000 iterations)
⏳ Calculating infection probabilities (Beta-Binomial)
⏳ Computing annual risks
⏳ Generating results...

✅ Assessment complete!
```

**Processing time:** ~10-30 seconds depending on iterations

---

### STEP 8A: View Results

**Results appear below the button:**

```
📊 Risk Assessment Results

Summary Statistics:
┌──────────────┬──────────────────┬──────────────────┐
│ Site         │ Annual Risk      │ Status           │
├──────────────┼──────────────────┼──────────────────┤
│ Site_A       │ 1.38e-02 (1.38%) │ NON-COMPLIANT ⚠️ │
│ Site_B       │ 5.21e-03 (0.52%) │ NON-COMPLIANT ⚠️ │
│ Site_C       │ 2.14e-04 (0.02%) │ NON-COMPLIANT ⚠️ │
│ Site_D       │ 8.32e-05 (0.01%) │ COMPLIANT ✅     │
│ Site_E       │ 3.45e-05 (0.00%) │ COMPLIANT ✅     │
│ Site_F       │ 1.23e-05 (0.00%) │ COMPLIANT ✅     │
└──────────────┴──────────────────┴──────────────────┘

WHO Guideline: Annual risk < 1e-4 (0.01%)

[📊 View Plot]  [📥 Download CSV]  [📄 Generate PDF Report]
```

**Plot shows:**
- Horizontal bar chart of annual risks by site
- Color-coded: Green (compliant), Red (non-compliant)
- WHO threshold line at 1e-4

---

### STEP 9A: Download Results

**Click the download buttons:**

```
[📥 Download CSV]
```

**Downloads:** `spatial_results_20251113_143022.csv`

**CSV Format:**
```csv
Location,Dilution,Pinf_Median,Annual_Risk_Median,Annual_Risk_5th,Annual_Risk_95th,
Population_Impact,Compliance_Status

Site_A,10,0.004780,0.01382,0.00545,0.03324,138,NON-COMPLIANT
Site_B,25,0.001912,0.00521,0.00219,0.01456,52,NON-COMPLIANT
...
```

**PDF Report includes:**
- Assessment parameters
- Risk calculations
- Plots and charts
- WHO compliance summary
- References (Beta-Binomial, Teunis et al.)

---

## EXAMPLE B: Temporal Assessment (Time Series)

### STEP 4B: Upload Monitoring Data

```
📅 Temporal Risk Assessment
Analyze risk over time using monitoring data

┌─────────────────────────────────────┐
│ ☑ Use example monitoring data       │
│   (52 weeks, 2024)                  │
│                                     │
│ Or upload CSV with:                 │
│ • Sample_Date                       │
│ • Concentration_org_per_L           │
│                                     │
│ [Browse files...]                   │
└─────────────────────────────────────┘
```

**Your CSV should look like:**
```csv
Sample_Date,Concentration_org_per_L
1/7/2024,1992
1/14/2024,1199
1/21/2024,2248
...
```

### STEP 5B: Configure and Run

Same as Spatial Assessment:
1. Select pathogen: **norovirus** (Production Mode)
2. Enter treatment LRV: **3.0**
3. Enter dilution: **100**
4. Enter volume: **50 mL**
5. Enter frequency: **20 events/year**
6. Enter population: **10,000**
7. Set iterations: **10,000**
8. Click **[🚀 Run Temporal Assessment]**

### STEP 6B: View Time Series Results

```
📊 Temporal Risk Results

Time Series Plot:
[Shows line chart of risk over time with WHO threshold]

Summary:
• Samples analyzed: 52
• Median annual risk: 1.23e-03 (0.123%)
• 95th percentile: 3.45e-03 (0.345%)
• Weeks non-compliant: 48 out of 52 (92%)

[📥 Download Results]  [📄 Generate Report]
```

**CSV Output:**
```csv
Sample_Date,Raw_Concentration,Post_Treatment_Conc,Receiving_Water_Conc,
Infection_Risk_Median,Annual_Risk_Median,Compliance_Status

1/7/2024,1992,1.992,0.01992,0.000692,0.01375,NON-COMPLIANT
1/14/2024,1199,1.199,0.01199,0.000418,0.00833,NON-COMPLIANT
...
```

---

## EXAMPLE C: Batch Scenarios (Library Approach)

### STEP 4C: Upload 3 CSV Files

**Tab 1: Input Data**

```
Upload your data files:

┌─────────────────────────────────────┐
│ 1. Dilution Data                    │
│    (Time, Location, Dilution)       │
│    [Browse...]                      │
│    ✓ 1,250 records uploaded         │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 2. Pathogen Data                    │
│    (Hockey Stick parameters)        │
│    [Browse...]                      │
│    ✓ 3 pathogens uploaded           │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 3. Scenarios                        │
│    (All assessment parameters)      │
│    [Browse...]                      │
│    ✓ 15 scenarios uploaded          │
└─────────────────────────────────────┘
```

**Required File Formats:**

**dilution_data.csv:**
```csv
Time,Location,Dilution_Factor
2024-01-01,Site_A,100
2024-01-01,Site_B,250
...
```

**pathogen_data.csv:**
```csv
Pathogen_ID,Pathogen_Name,Pathogen_Type,Min_Concentration,Median_Concentration,Max_Concentration,P_Breakpoint
PATH001,Norovirus GII,norovirus,100,1000,10000,0.95
```

**scenarios.csv:**
```csv
Scenario_ID,Scenario_Name,Pathogen_ID,Location,Exposure_Route,Treatment_LRV,
Ingestion_Volume_mL,Exposure_Frequency_per_Year,Exposed_Population,Monte_Carlo_Iterations

SCEN001,Beach Swimming A,PATH001,Site_A,primary_contact,0,50,20,10000,10000
SCEN002,Beach Swimming B,PATH001,Site_B,primary_contact,0,50,20,10000,10000
...
```

### STEP 5C: Run Batch Processing

**Tab 2: Run Assessment**

```
Settings:
┌─────────────────────────────────────┐
│ Output filename:                    │
│ batch_results_20251113_143022       │
└─────────────────────────────────────┘

Monte Carlo iterations: 10,000

[🚀 Run Batch Assessment]
```

**Progress:**
```
Processing scenarios...
✓ Scenario 1/15: Beach Swimming A (SCEN001)
  Risk: 1.38e-02 NON-COMPLIANT
✓ Scenario 2/15: Beach Swimming B (SCEN002)
  Risk: 5.21e-03 NON-COMPLIANT
...
✓ All 15 scenarios complete!

[📊 View Results]  [📥 Download All]
```

---

## Understanding the Results

### Key Output Columns:

**Pinf_Median:**
- Per-event infection probability (median across 10,000 iterations)
- Example: 0.000692 = 0.0692% chance per swimming event

**Annual_Risk_Median:**
- Annual infection risk accounting for repeated exposures
- Formula: `1 - (1 - Pinf)^frequency`
- Example: 0.01375 = 1.375% chance per year

**Annual_Risk_5th / 95th:**
- Uncertainty bounds (5th and 95th percentiles)
- Shows range of possible risks

**Population_Impact:**
- Expected number of infections per year
- Formula: `Annual_Risk × Population`
- Example: 0.01375 × 10,000 = 138 infections/year

**Compliance_Status:**
- **COMPLIANT:** Annual risk ≤ 1e-4 (0.01%) ✅
- **NON-COMPLIANT:** Annual risk > 1e-4 ⚠️

---

## Tips for Production Use

### ✅ Best Practices:

1. **Always use Production Mode** (norovirus only, Beta-Binomial validated)
2. **Use 10,000 iterations** for stable, reproducible results
3. **Check example data first** before uploading custom files
4. **Download CSV** for further analysis in Excel/R/Python
5. **Generate PDF report** for documentation and compliance

### ⚠️ Common Mistakes:

1. **Wrong units:**
   - Concentration: org/L (not org/mL)
   - Volume: mL (not L)

2. **Incorrect LRV:**
   - Raw discharge: LRV = 0
   - Primary treatment: LRV = 1-2
   - Secondary treatment: LRV = 2-3
   - Tertiary/UV: LRV = 3-5

3. **Misunderstanding iterations:**
   - 10,000 iterations ≠ 10,000 people
   - Iterations = uncertainty scenarios
   - Population = exposed people (separate parameter)

---

## Validation: How to Verify It's Working Correctly

### Test Case (should match David's Excel):

**Input:**
- Pathogen: norovirus
- Raw concentration: 1,000 org/L
- Treatment LRV: 0 (no treatment)
- Dilution: 1 (no dilution)
- Volume: 1 L = 1,000 mL
- Single exposure (frequency = 1)

**Expected Result:**
- Dose: 1,000 organisms
- P(infection): 0.527157 (52.7%) ← Should match David's Excel ✅

**How to test:**
1. Select Spatial Assessment
2. Enter parameters above
3. Check if Pinf_Median ≈ 0.527 (may vary slightly due to MC sampling)

---

## Troubleshooting

### App won't start:
```bash
# Check Python version
python --version  # Should be 3.8+

# Install dependencies
pip install -r requirements.txt

# Try again
streamlit run web_app.py
```

### "File not found" error:
- Make sure you're in the `Batch_Processing_App/app` directory
- Check that `web_app.py` exists in current folder

### Wrong pathogen appears:
- Check Production Mode checkbox in sidebar
- Should be ON (✅) for norovirus-only

### Results seem wrong:
- Verify input units (org/L, mL, not other units)
- Check LRV value is reasonable (0-5 typical)
- Compare simple test case to David's Excel

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│ QMRA WEB APP - QUICK START                         │
├─────────────────────────────────────────────────────┤
│ 1. Launch: streamlit run web_app.py                │
│ 2. Check: Production Mode ON ✅                     │
│ 3. Select: Assessment type (Spatial/Temporal/etc)  │
│ 4. Choose: Pathogen = norovirus                    │
│ 5. Enter: Parameters (conc, LRV, volume, etc)      │
│ 6. Set: Iterations = 10,000                        │
│ 7. Click: Run Assessment button                    │
│ 8. View: Results table and plots                   │
│ 9. Download: CSV + PDF report                      │
│                                                     │
│ WHO Guideline: Annual risk < 1e-4 (0.01%)          │
│ Model: Beta-Binomial (α=0.04, β=0.055)             │
│ Validated: Matches David's Excel exactly ✅         │
└─────────────────────────────────────────────────────┘
```

---

**Need Help?**
- Documentation: See CALCULATION_FLOW.md for mathematical details
- Validation: See CRITICAL_ASSESSMENT_REPORT.md for verification
- Production Mode: See PRODUCTION_MODE_GUIDE.md

**Last Updated:** November 13, 2025
**Version:** 1.0 (Production Mode enabled)
