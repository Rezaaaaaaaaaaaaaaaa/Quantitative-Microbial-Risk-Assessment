# Simple QMRA Batch Processing Guide

## Overview

This batch processor automatically uses empirical distributions for QMRA:
- **ECDF** (Empirical Cumulative Distribution Function) for dilution data
- **Hockey Stick** distribution for pathogen concentrations

**No flags needed** - the app automatically creates distributions from your raw data.

---

## Quick Start

### 1. Prepare Your Dilution Data

Create a CSV with **multiple time points per location**:

```csv
DateTime,Site_Name,Distance_m,Dilution_Factor
2024-01-15 00:00,Discharge,0,0.82
2024-01-15 01:00,Discharge,0,0.87
2024-01-15 02:00,Discharge,0,1.14
...
2024-01-15 00:00,Site_50m,50,4.13
2024-01-15 01:00,Site_50m,50,7.01
2024-01-15 02:00,Site_50m,50,6.35
...
```

**Required columns**:
- `DateTime`: Date and time of each measurement
- `Site_Name`: Location identifier
- `Distance_m`: Distance from discharge point (meters)
- `Dilution_Factor`: Dilution value from hydrodynamic model

**Key point**: Multiple rows per site capture temporal variability. The app creates an ECDF from all time points.

### 2. Prepare Your Scenario File

Create a CSV with pathogen parameters:

```csv
Scenario_ID,Scenario_Name,Pathogen,Pathogen_Min,Pathogen_Median,Pathogen_Max,Dilution_File,Treatment_LRV,Exposure_Route,Volume_mL,Frequency_Year,Population,Iterations
S001,Summer_Beach,norovirus,200,1026,3484,example_dilution_timeseries.csv,3.0,primary_contact,50,25,15000,10000
S002,Winter_Beach,norovirus,500,2000,5000,example_dilution_timeseries.csv,3.0,primary_contact,30,8,2000,10000
```

**New columns** (compared to legacy format):
- `Pathogen_Min`: Minimum observed concentration (copies/L)
- `Pathogen_Median`: Median observed concentration (copies/L)
- `Pathogen_Max`: Maximum observed concentration (copies/L)

**How to get these values**: Calculate from your monitoring data
```python
import pandas as pd
data = pd.read_csv('monitoring_data.csv')
pathogen_min = data['Pathogen_Column'].min()
pathogen_median = data['Pathogen_Column'].median()
pathogen_max = data['Pathogen_Column'].max()
```

### 3. Run the Batch Processor

```bash
python run_simple_qmra.py
```

That's it! The app automatically:
1. Loads your dilution time series
2. Creates ECDF for each site (from all time points)
3. Creates Hockey Stick distribution (from min/median/max)
4. Runs QMRA for all scenarios
5. Saves results to `outputs/simple_batch/`

---

## What's Different from Legacy Approach?

### Old Approach
```python
# Used only median dilution (wasted 99% of hydrodynamic data)
# Used single fixed pathogen concentration
results = processor.run_spatial_assessment(
    dilution_file='spatial_dilution.csv',
    pathogen='norovirus',
    effluent_concentration=1000  # Single fixed value
)
```

### New Approach
```python
# Uses ALL time points for dilution (100% of data)
# Uses distribution for pathogen (captures high-concentration events)
results = processor.run_spatial_assessment(
    dilution_file='dilution_timeseries.csv',
    pathogen='norovirus',
    use_ecdf_dilution=True,        # Auto-enabled
    use_hockey_pathogen=True,       # Auto-enabled
    pathogen_min=200,
    pathogen_median=1026,
    pathogen_max=3484
)
```

**Impact**: More realistic risk estimates, especially at high percentiles (e.g., 95th percentile).

---

## Understanding the Results

The processor generates several output files:

### Individual Scenario Results
- `S001_results.csv` - Results for scenario S001
- `S002_results.csv` - Results for scenario S002
- etc.

### Combined Results
- `all_scenarios_combined.csv` - All scenarios and sites in one file

### Key Output Columns

| Column | Description |
|--------|-------------|
| `Site_Name` | Location identifier |
| `Distance_m` | Distance from discharge |
| `Dilution_Method` | Method used (ECDF or Median) |
| `Pathogen_Method` | Method used (Hockey_Stick or Fixed) |
| `Annual_Risk_Median` | Median annual infection risk |
| `Annual_Risk_95th` | 95th percentile annual risk |
| `Compliance_Status` | COMPLIANT or NON-COMPLIANT (vs WHO guideline: 1/1000) |
| `Population_Impact` | Expected annual infections in population |

### Example Results

From the test run:

```
Scenario: Summer_Beach_Main (S001)
Pathogen: Norovirus (min=200, median=1026, max=3484)
Treatment: 3.0 LRV

Site          Distance  Median Risk  95th Risk    Status
----------------------------------------------------------------
Discharge     0m        3.23e-01     4.98e-01     NON-COMPLIANT
Site_50m      50m       7.05e-02     1.50e-01     NON-COMPLIANT
Site_100m     100m      3.82e-02     9.05e-02     NON-COMPLIANT
Site_250m     250m      1.24e-02     2.62e-02     NON-COMPLIANT
```

---

## File Organization

```
Batch_Processing_App/
├── input_data/
│   ├── dilution_data/
│   │   └── example_dilution_timeseries.csv    # Your raw dilution data
│   └── batch_scenarios/
│       └── simple_scenarios.csv                # Your scenario definitions
├── outputs/
│   └── simple_batch/
│       ├── S001_results.csv                    # Individual results
│       ├── S002_results.csv
│       └── all_scenarios_combined.csv          # Combined results
└── run_simple_qmra.py                          # Main script
```

---

## FAQ

### Q: How many time points do I need per site?
**A**: The more the better! Minimum 10-20 time points to capture variability. The example uses 10 hourly measurements.

### Q: Do I need to pre-calculate distributions?
**A**: No! Just provide:
- Raw dilution time series (DateTime column)
- Min/median/max for pathogen
- The app calculates distributions automatically

### Q: What if I only have median dilution?
**A**: The batch processor can fall back to the legacy approach by setting `use_ecdf_dilution=False`. However, using ECDF is recommended if you have hydrodynamic model output.

### Q: How do I calculate pathogen min/median/max?
**A**: From your monitoring data:
```python
import pandas as pd
monitoring = pd.read_csv('pathogen_monitoring.csv')
print(f"Min: {monitoring['Pathogen'].min()}")
print(f"Median: {monitoring['Pathogen'].median()}")
print(f"Max: {monitoring['Pathogen'].max()}")
```

### Q: Why Hockey Stick instead of normal distribution?
**A**: Pathogen concentrations are typically right-skewed with occasional high values. Hockey Stick distribution better represents this pattern, especially for high-percentile risk estimates.

### Q: Can I add more environmental variables?
**A**: Yes! The dilution CSV can include additional columns (Tidal_State, Wind_Speed_ms, Current_Speed_ms, etc.) for documentation. The app uses only DateTime, Site_Name, Distance_m, and Dilution_Factor.

---

## Tips for Production Use

1. **Use sufficient iterations**: 10,000 is recommended for stable results
2. **Include temporal variability**: Capture different tidal states, seasons, and conditions
3. **Document data sources**: Keep notes on where dilution and pathogen data came from
4. **Review compliance carefully**: Non-compliance at 95th percentile may warrant treatment upgrades
5. **Compare approaches**: Run legacy vs. ECDF to understand the difference for your data

---

## Example Session

```bash
# Navigate to the app directory
cd "C:\Users\...\Batch_Processing_App"

# Run the batch processor
python run_simple_qmra.py

# Output:
# ================================================================================
# SIMPLE QMRA BATCH PROCESSOR
# Automatic ECDF (dilution) + Hockey Stick (pathogen)
# ================================================================================
#
# Loaded 3 scenarios from input_data/batch_scenarios/simple_scenarios.csv
#
# [1/3] Processing: S001 - Summer_Beach_Main
# ...
# Results saved to: outputs/simple_batch/S001_results.csv
#
# ================================================================================
# BATCH PROCESSING COMPLETE
# ================================================================================
```

---

## Support

For more detailed information:
- `QUICK_START.md` - Quick reference guide
- `BEST_PRACTICES_GUIDE.md` - Detailed methodology
- `SIMPLE_EXAMPLE.py` - Working code example

For technical questions about distributions, see `Disttribution.pdf`.
