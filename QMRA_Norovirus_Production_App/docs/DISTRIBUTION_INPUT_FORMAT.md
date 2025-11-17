# Updated Input Format for Empirical Distributions

## Overview

The batch processor can now use empirical distributions instead of single fixed values:
- **ECDF for dilution data** - Uses the full distribution from hydrodynamic modeling
- **Hockey Stick for pathogen concentrations** - Models right-skewed concentration data

## Current vs. New Approach

### Current Approach (Limited)
```python
# Uses only median dilution
dilution_factor = site['Dilution_Factor']  # Single value: 7.5

# Uses only mean pathogen concentration
effluent_concentration = 1e6  # Single value
```

### New Approach (Full Distributions)
```python
# Samples from ECDF of all 100 hydrodynamic simulations
dilution_samples = sample_ecdf(dilution_data)  # Array of 10,000 samples

# Samples from Hockey Stick distribution
pathogen_samples = sample_hockey_stick(min=1e4, median=1e6, max=1e8)  # Array of 10,000 samples
```

## Input File Formats

### 1. Dilution Data (No Change Needed)

Your existing `spatial_dilution_6_sites.csv` is already perfect for ECDF:

```csv
Simulation_ID,Site_Name,Distance_m,Dilution_Factor,Tidal_State,Wind_Speed_ms
1,Discharge,0,0.818,High,5.799
2,Discharge,0,0.866,Low,6.423
3,Discharge,0,1.141,Low,4.566
...
101,Site_50m,50,4.128,Low,3.601
102,Site_50m,50,7.008,Low,13.110
...
```

**What changes**: Batch processor will use **all values** instead of just median.

### 2. Pathogen Concentration Data (New Format)

#### Option A: Add columns to existing format

**`pathogen_concentrations_with_dist.csv`**:
```csv
Pathogen,Distribution_Type,Min_Concentration,Median_Concentration,Max_Concentration,Percentile
norovirus,hockey_stick,1000,100000,10000000,95
campylobacter,hockey_stick,500,50000,5000000,95
cryptosporidium,hockey_stick,10,5000,500000,95
```

#### Option B: Keep monitoring data, calculate from it

**`weekly_monitoring_2024.csv`** (already exists):
```csv
Sample_ID,Sample_Date,Norovirus_copies_per_L
MP001,6/2/2024,512
MP002,6/9/2024,2204
MP003,6/16/2024,1336
...
```

Then automatically calculate:
```python
min_conc = df['Norovirus_copies_per_L'].min()
median_conc = df['Norovirus_copies_per_L'].median()
max_conc = df['Norovirus_copies_per_L'].max()
```

### 3. Batch Scenarios (Enhanced Format)

**`master_batch_scenarios_v2.csv`**:
```csv
Scenario_ID,Scenario_Name,Pathogen,Use_ECDF_Dilution,Use_Hockey_Pathogen,Pathogen_Min,Pathogen_Median,Pathogen_Max,Dilution_File,Treatment_LRV,Iterations
S001,Beach_A_Summer,norovirus,TRUE,TRUE,1e4,1e6,1e8,spatial_dilution_6_sites.csv,3.0,10000
S002,Beach_A_Winter,norovirus,TRUE,TRUE,5e4,2e6,1e8,spatial_dilution_6_sites.csv,3.0,10000
S003,Beach_B_Summer,norovirus,FALSE,FALSE,800000,,,spatial_dilution_6_sites.csv,3.0,10000
```

**New columns**:
- `Use_ECDF_Dilution`: `TRUE/FALSE` - Whether to sample from full ECDF or use median
- `Use_Hockey_Pathogen`: `TRUE/FALSE` - Whether to use Hockey Stick distribution
- `Pathogen_Min`: Minimum concentration from monitoring data
- `Pathogen_Median`: Median concentration from monitoring data
- `Pathogen_Max`: Maximum concentration from monitoring data

## Backward Compatibility

The system should support both old and new formats:

```python
if 'Use_ECDF_Dilution' in scenario and scenario['Use_ECDF_Dilution']:
    # New: Sample from ECDF
    dilution_dist = create_empirical_cdf_from_data(dilution_data['Dilution_Factor'])
    dilution_samples = mc.sample_distribution("dilution", n_samples)
else:
    # Old: Use median value
    dilution_factor = dilution_data['Dilution_Factor'].median()
    dilution_samples = np.full(n_samples, dilution_factor)

if 'Use_Hockey_Pathogen' in scenario and scenario['Use_Hockey_Pathogen']:
    # New: Sample from Hockey Stick
    pathogen_dist = create_hockey_stick_distribution(
        x_min=scenario['Pathogen_Min'],
        x_median=scenario['Pathogen_Median'],
        x_max=scenario['Pathogen_Max']
    )
    pathogen_samples = mc.sample_distribution("pathogen", n_samples)
else:
    # Old: Use fixed value
    pathogen_conc = scenario['Effluent_Conc']
    pathogen_samples = np.full(n_samples, pathogen_conc)
```

## Example Workflows

### Workflow 1: Using ECDF for Dilution Only

```csv
Scenario_ID: S004
Use_ECDF_Dilution: TRUE
Use_Hockey_Pathogen: FALSE
Effluent_Conc: 1000000
Dilution_File: spatial_dilution_6_sites.csv
```

Result: Samples 10,000 dilution values from the ECDF but uses fixed pathogen concentration.

### Workflow 2: Using Both ECDF and Hockey Stick

```csv
Scenario_ID: S005
Use_ECDF_Dilution: TRUE
Use_Hockey_Pathogen: TRUE
Pathogen_Min: 10000
Pathogen_Median: 1000000
Pathogen_Max: 100000000
Dilution_File: spatial_dilution_6_sites.csv
```

Result: Full distributional analysis using both empirical methods.

### Workflow 3: Traditional Fixed Values (Backward Compatible)

```csv
Scenario_ID: S006
Use_ECDF_Dilution: FALSE
Use_Hockey_Pathogen: FALSE
Effluent_Conc: 800000
Dilution_Factor: 200
```

Result: Works exactly like before - single fixed values.

## Benefits

### Before (Current)
```
Dilution data: 100 simulations → Use only median (7.5)
Pathogen data: 52 weeks monitoring → Use only mean (1.2e6)
```

### After (With Distributions)
```
Dilution data: 100 simulations → Sample from ECDF → Full uncertainty
Pathogen data: 52 weeks monitoring → Calculate min/median/max → Hockey Stick distribution → Full uncertainty
```

## Implementation Priority

### Phase 1: Quick Win (Use existing data better)
1. Add ECDF sampling for dilution in spatial assessment
2. Automatically uses all 100 simulations instead of median
3. **No input file changes needed!**

### Phase 2: Add Hockey Stick support
1. Add new columns to batch scenarios CSV
2. Support `Pathogen_Min`, `Pathogen_Median`, `Pathogen_Max`
3. Maintain backward compatibility

### Phase 3: Advanced features
1. Auto-calculate min/median/max from monitoring data files
2. Generate distribution fit diagnostics
3. Compare results with/without distributions

## Next Steps

Would you like me to:
1. **Update the batch processor code** to support ECDF dilution sampling (Phase 1)?
2. **Create example input files** with the new format?
3. **Add validation** to ensure Hockey Stick parameters make sense (min < median < max)?
4. **Generate comparison plots** showing difference between median-only vs. full ECDF?
