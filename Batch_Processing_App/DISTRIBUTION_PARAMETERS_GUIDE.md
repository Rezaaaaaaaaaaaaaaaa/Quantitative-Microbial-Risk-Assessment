# Custom Distribution Parameters Guide

**Version:** 2.0
**Date:** October 2025
**Enhancement:** Scenario-Specific Uncertainty Distributions

---

## Overview

The batch processing system now supports **custom uncertainty distributions** for each scenario, allowing you to specify parameter variability based on data quality, environmental conditions, and confidence levels.

### What Changed?

**Before (v1.0):**
- All scenarios used the same fixed uncertainty (CV = 0.5 for concentration, ±50% for volume)
- No way to distinguish high-quality data from uncertain estimates

**After (v2.0):**
- Each scenario can have custom uncertainty parameters
- Reflects real-world data quality differences
- More realistic risk assessments with appropriate confidence intervals

---

## New CSV Columns

### Required Columns (same as before)
- `Scenario_ID`, `Scenario_Name`, `Pathogen`, `Exposure_Route`
- `Effluent_Conc`, `Treatment_LRV`, `Dilution_Factor`
- `Volume_mL`, `Frequency_Year`, `Population`

### New Distribution Parameter Columns

| Column | Type | Range | Description |
|--------|------|-------|-------------|
| **Effluent_Conc_CV** | Float | 0.2-1.0 | Coefficient of variation for effluent concentration |
| **Treatment_LRV_Uncertainty** | Float | 0.0-0.8 | Uncertainty in treatment effectiveness (log units) |
| **Dilution_Factor_CV** | Float | 0.1-0.9 | Coefficient of variation for dilution |
| **Volume_Min** | Float | >0 | Minimum ingestion volume (mL) |
| **Volume_Max** | Float | >Volume_Min | Maximum ingestion volume (mL) |

---

## Parameter Guidelines

### 1. Effluent_Conc_CV (Concentration Uncertainty)

**Interpretation:** Standard deviation as fraction of mean

| CV Value | Data Quality | Typical Scenario |
|----------|--------------|------------------|
| 0.2-0.3 | Excellent | Daily monitoring, robust lab QA/QC |
| 0.4-0.5 | Good | Weekly monitoring, standard methods |
| 0.6-0.7 | Moderate | Monthly monitoring, some gaps |
| 0.8-0.9 | Poor | Infrequent data, high variability |
| >0.9 | Very poor | Single grab sample, worst-case estimate |

**Example:**
```csv
# Beach with excellent monitoring program
Effluent_Conc,Effluent_Conc_CV
1000000,0.3

# Emergency bypass with limited data
Effluent_Conc,Effluent_Conc_CV
1500000,0.9
```

### 2. Treatment_LRV_Uncertainty (Treatment Reliability)

**Interpretation:** ±Uncertainty in log reduction value

| Uncertainty | Treatment Reliability | Example |
|-------------|----------------------|---------|
| 0.0-0.2 | Very reliable | MBR with continuous monitoring |
| 0.3-0.4 | Reliable | UV with regular maintenance |
| 0.5-0.6 | Moderate | Chlorination with variable dosing |
| 0.7+ | Unreliable | Poorly maintained, bypassing |

**Example:**
```csv
# Well-maintained UV system
Treatment_LRV,Treatment_LRV_Uncertainty
8.0,0.3

# Bypass scenario (no treatment)
Treatment_LRV,Treatment_LRV_Uncertainty
0.0,0.0
```

### 3. Dilution_Factor_CV (Environmental Variability)

**Interpretation:** Variability in dilution due to tides, currents, seasons

| CV Value | Conditions | Location Type |
|----------|-----------|---------------|
| 0.2-0.3 | Stable | Open coast, strong currents |
| 0.4-0.5 | Moderate | Tidal influence |
| 0.6-0.8 | Variable | Enclosed bay, seasonal changes |
| 0.9+ | Highly variable | Small harbor, stagnant zones |

**Example:**
```csv
# Open ocean outfall
Dilution_Factor,Dilution_Factor_CV
500,0.2

# Small enclosed bay
Dilution_Factor,Dilution_Factor_CV
25,0.8
```

### 4. Volume_Min and Volume_Max (Behavioral Range)

**Interpretation:** Range of ingestion volumes based on activity

| Activity | Typical Min-Max (mL) | Notes |
|----------|---------------------|-------|
| Swimming (winter) | 20-50 | Less splashing, shorter duration |
| Swimming (summer) | 40-100 | Active play, longer duration |
| Surfing | 50-150 | High water contact |
| Shellfish consumption | 80-200 | Meal portion variability |

**Example:**
```csv
# Summer beach
Volume_mL,Volume_Min,Volume_Max
50,35,75

# Shellfish harvesting
Volume_mL,Volume_Min,Volume_Max
100,80,150
```

---

## How Uncertainties are Combined

The system automatically combines uncertainties using **uncertainty propagation**:

### Total Concentration Uncertainty

```
CV_total = √(CV_effluent² + CV_treatment² + CV_dilution²)
```

**Example:**
- Effluent CV = 0.4 (good monitoring)
- Treatment uncertainty = 0.3 log (reliable UV)
- Dilution CV = 0.3 (stable conditions)

```
CV_total = √(0.4² + 0.3² + 0.3²) = √(0.16 + 0.09 + 0.09) = 0.58
```

This combined CV is used in the **lognormal distribution** for concentration during Monte Carlo simulation.

---

## Example Scenarios

### Scenario 1: High-Quality Monitoring

```csv
Scenario_ID: S001
Scenario_Name: Beach_A_Summer_Well_Monitored
Effluent_Conc: 1000000
Effluent_Conc_CV: 0.3          # Daily sampling
Treatment_LRV: 8.0
Treatment_LRV_Uncertainty: 0.3  # Reliable UV
Dilution_Factor: 100
Dilution_Factor_CV: 0.2        # Stable currents
Volume_mL: 50
Volume_Min: 40
Volume_Max: 70
```

**Expected Result:**
- Narrow confidence interval (95th/5th ≈ 1.5x)
- High confidence in risk estimate

### Scenario 2: High Uncertainty (Bypass Event)

```csv
Scenario_ID: S010
Scenario_Name: Emergency_Bypass_Worst_Case
Effluent_Conc: 1500000
Effluent_Conc_CV: 0.9          # Single sample
Treatment_LRV: 0.0
Treatment_LRV_Uncertainty: 0.0  # No treatment
Dilution_Factor: 50
Dilution_Factor_CV: 0.7        # Poor mixing
Volume_mL: 50
Volume_Min: 30
Volume_Max: 100
```

**Expected Result:**
- Wide confidence interval (95th/5th ≈ 3-4x)
- Conservative decision-making recommended

---

## Interpreting Results

### Risk Metrics in Output CSV

| Column | Meaning |
|--------|---------|
| `Annual_Risk_Median` | Most likely risk (50th percentile) |
| `Annual_Risk_5th` | Lower bound (optimistic scenario) |
| `Annual_Risk_95th` | Upper bound (conservative scenario) |

### Uncertainty Ratio

```
Uncertainty Ratio = Annual_Risk_95th / Annual_Risk_5th
```

| Ratio | Interpretation | Action |
|-------|---------------|--------|
| 1.2-1.5x | Low uncertainty | High confidence in decision |
| 1.5-2.5x | Moderate uncertainty | Standard risk management |
| 2.5-4.0x | High uncertainty | Conservative approach recommended |
| >4.0x | Very high uncertainty | Additional monitoring needed |

---

## Best Practices

### 1. Setting CV Values

- **Base on actual data:** Calculate CV from monitoring records
- **Be realistic:** Don't underestimate uncertainty
- **Document assumptions:** Note data sources in CSV "Notes" column

### 2. Scenario Design

- **High-priority scenarios:** Use lower CV (better data)
- **Worst-case scenarios:** Use higher CV (acknowledge uncertainty)
- **Seasonal variations:** Adjust volume ranges and dilution CV

### 3. Decision-Making

- **Low uncertainty scenarios:** Use median risk for decisions
- **High uncertainty scenarios:** Use 95th percentile (conservative)
- **Risk near threshold:** Consider confidence interval width

---

## Backward Compatibility

The system is **fully backward compatible**. If distribution columns are missing, it uses default values:

```python
Effluent_Conc_CV = 0.5          # Default
Treatment_LRV_Uncertainty = 0.2  # Default
Dilution_Factor_CV = 0.3         # Default
Volume_Min = Volume_mL * 0.5     # Default
Volume_Max = Volume_mL * 1.5     # Default
```

Old CSV files will work without modification but use generic uncertainty.

---

## Testing Your Distributions

Use the test script to verify custom distributions:

```bash
python test_custom_distributions.py
```

This compares low-uncertainty vs high-uncertainty scenarios and verifies that higher CV values produce wider risk ranges.

---

## References

- WHO (2016). Quantitative Microbial Risk Assessment - Uncertainty Analysis
- U.S. EPA (2019). Exposure Factors Handbook
- Haas et al. (2014). QMRA 2nd Edition - Chapter 8: Uncertainty

---

## Support

For questions about setting distribution parameters:
1. Review your monitoring data statistics
2. Consult similar published QMRA studies
3. Use conservative values when uncertain

**Remember:** It's better to acknowledge uncertainty than to pretend you have more confidence than the data supports!

---

**NIWA Earth Sciences New Zealand**
*Batch Processing Tool v2.0*
