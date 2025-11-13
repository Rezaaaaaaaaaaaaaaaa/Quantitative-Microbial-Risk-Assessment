# Example Input Data Files

This directory contains example data files for the QMRA Batch Processing App.

## Production Mode Files (Norovirus Only)

These files contain **only norovirus** data and are suitable for production use per the contract scope:

### Main Example Files:
- **pathogen_data.csv** - 3 norovirus pathogen definitions (Summer, Winter, High Load)
- **norovirus_monitoring_data.csv** - 12 samples with norovirus concentrations only
- **weekly_monitoring_2024.csv** - 52 weeks of norovirus monitoring data

### Dilution Data (all production-ready):
- **spatial_dilution_6_sites.csv** - 600 rows of dilution factors for 6 sites
- **dilution_data.csv** - General dilution data

### Scenario Files:
- **scenarios.csv** - 15 assessment scenarios

## Research Mode Files (Multiple Pathogens)

⚠️ **For research use only - require additional validation**

- **multi_pathogen_data.csv** - Contains 6 pathogens (norovirus, campylobacter, cryptosporidium, e_coli, salmonella, rotavirus)
  - Use only with Research Mode enabled in the app
  - Other pathogens besides norovirus have not been validated per contract scope

## File Formats

### pathogen_data.csv
```
Pathogen_ID,Pathogen_Name,Pathogen_Type,Min_Concentration,Median_Concentration,Max_Concentration,P_Breakpoint
PATH001,Norovirus_Summer,norovirus,500000,1000000,2000000,0.95
```

### norovirus_monitoring_data.csv / weekly_monitoring_2024.csv
```
Sample_ID,Sample_Date,Norovirus_copies_per_L,Sample_Volume_L,Laboratory,QC_Flag
```

### spatial_dilution_6_sites.csv
```
Simulation_ID,Site_Name,Distance_m,Dilution_Factor,Tidal_State,Wind_Speed_ms,Current_Speed_ms,Model_Type,Confidence
```

### scenarios.csv
```
Scenario_ID,Scenario_Name,Treatment_Type,Log_Reduction,Dilution_Factor,Volume_mL,Frequency,Population,Description
```

## Usage

1. **Production Mode (Default):**
   - Use pathogen_data.csv (norovirus only)
   - Use norovirus_monitoring_data.csv or weekly_monitoring_2024.csv
   - App automatically restricts to norovirus

2. **Research Mode:**
   - Uncheck "Production Mode" in app sidebar
   - Can use multi_pathogen_data.csv
   - WARNING: Other pathogens require validation

## Validation Status

| Pathogen | Dose-Response Model | Validation Status | Production Ready |
|----------|-------------------|-------------------|------------------|
| Norovirus | Beta-Binomial | ✅ Validated (Teunis 2008) | ✅ YES |
| Campylobacter | Beta-Poisson | ⚠️ Not validated | ❌ NO |
| Cryptosporidium | Beta-Poisson | ⚠️ Not validated | ❌ NO |
| E. coli | Beta-Poisson | ⚠️ Not validated | ❌ NO |
| Salmonella | Beta-Poisson | ⚠️ Not validated | ❌ NO |
| Rotavirus | Beta-Poisson | ⚠️ Not validated | ❌ NO |

---

**Last Updated:** November 13, 2025
**Contract Scope:** Norovirus risk assessment (validated)
