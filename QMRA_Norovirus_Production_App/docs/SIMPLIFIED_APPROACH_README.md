# QMRA Batch Processing - Simplified Three-File Approach

## ✨ Overview

The QMRA Batch Processing App uses a **simple, straightforward three-file approach**:

1. **`dilution_data.csv`** - Raw dilution data (Time, Location, Dilution_Factor)
2. **`pathogen_data.csv`** - Hockey Stick parameters (Min, Median, Max)
3. **`scenarios.csv`** - All scenario parameters

## 📋 File Formats

### 1. Dilution Data (`dilution_data.csv`)

**3 columns only - Raw data from hydrodynamic models**

| Column | Description | Example |
|--------|-------------|---------|
| `Time` | Date/time of observation | 2024-01-01 |
| `Location` | Site identifier | Site_A |
| `Dilution_Factor` | Dilution value from model | 120 |

**Example:**
```csv
Time,Location,Dilution_Factor
2024-01-01,Site_A,120
2024-01-01,Site_B,85
2024-01-01,Site_C,200
2024-01-02,Site_A,95
2024-01-02,Site_B,110
2024-01-02,Site_C,180
```

**How It Works:**
- All dilution values for a Location are automatically used to create an ECDF
- No need to specify distribution type - always uses full data
- Just export your hydrodynamic model results as-is!

---

### 2. Pathogen Data (`pathogen_data.csv`)

**6 columns - Hockey Stick distribution only**

| Column | Description | Example |
|--------|-------------|---------|
| `Pathogen_ID` | Unique identifier | PATH001 |
| `Pathogen_Name` | Descriptive name | Norovirus_Summer |
| `Pathogen_Type` | Organism type | norovirus |
| `Min_Concentration` | Minimum (copies/L) | 500000 |
| `Median_Concentration` | Median (copies/L) | 1000000 |
| `Max_Concentration` | Maximum (copies/L) | 2000000 |

**Valid Pathogen Types:**
- `norovirus`
- `campylobacter`
- `cryptosporidium`
- `e_coli`
- `rotavirus`
- `salmonella`

**Example:**
```csv
Pathogen_ID,Pathogen_Name,Pathogen_Type,Min_Concentration,Median_Concentration,Max_Concentration
PATH001,Norovirus_Summer,norovirus,500000,1000000,2000000
PATH002,Norovirus_Winter,norovirus,800000,1500000,3000000
PATH003,Campylobacter_Typical,campylobacter,200000,500000,1000000
```

**How To Determine Min/Median/Max:**
- **Median**: Use your best estimate or monitoring data median
- **Min**: Conservative lower bound (e.g., 10th percentile or 0.5× median)
- **Max**: Conservative upper bound (e.g., 90th percentile or 2× median)

---

### 3. Scenarios (`scenarios.csv`)

**All scenario parameters - References Location and Pathogen_ID**

| Column | Description | Example |
|--------|-------------|---------|
| `Scenario_ID` | Unique ID | S001 |
| `Scenario_Name` | Descriptive name | Site_A_Norovirus_Summer |
| `Pathogen_ID` | Reference to pathogen_data.csv | PATH001 |
| `Location` | Reference to dilution_data.csv | Site_A |
| `Exposure_Route` | primary_contact or shellfish_consumption | primary_contact |
| `Treatment_LRV` | Log reduction value (0-10) | 3 |
| `Treatment_LRV_Uncertainty` | Uncertainty in treatment (0-1) | 0.3 |
| `Ingestion_Volume_mL` | Mean volume in mL | 50 |
| `Volume_Min_mL` | Minimum volume | 35 |
| `Volume_Max_mL` | Maximum volume | 75 |
| `Exposure_Frequency_per_Year` | Events per year | 25 |
| `Exposed_Population` | Population size | 15000 |
| `Monte_Carlo_Iterations` | MC iterations | 10000 |
| `Priority` | High, Medium, or Low | High |
| `Notes` | Description | Main beach summer season |

**Example:**
```csv
Scenario_ID,Scenario_Name,Pathogen_ID,Location,Exposure_Route,Treatment_LRV,Treatment_LRV_Uncertainty,Ingestion_Volume_mL,Volume_Min_mL,Volume_Max_mL,Exposure_Frequency_per_Year,Exposed_Population,Monte_Carlo_Iterations,Priority,Notes
S001,Site_A_Norovirus_Summer,PATH001,Site_A,primary_contact,3,0.3,50,35,75,25,15000,10000,High,Main beach summer
S002,Site_B_Norovirus_Summer,PATH001,Site_B,primary_contact,3,0.3,50,35,75,25,8000,10000,High,Secondary beach
S003,Shellfish_Site_C,PATH001,Site_C,shellfish_consumption,3,0.3,100,80,150,24,5000,10000,High,Commercial shellfish
```

---

## 🚀 Quick Start

### Step 1: Prepare Dilution Data
Export your hydrodynamic model results with 3 columns:
```csv
Time,Location,Dilution_Factor
2024-01-01,Site_A,120
2024-01-01,Site_B,85
...
```

### Step 2: Determine Pathogen Parameters
Based on your monitoring data or literature, determine Min/Median/Max:
```csv
Pathogen_ID,Pathogen_Name,Pathogen_Type,Min_Concentration,Median_Concentration,Max_Concentration
PATH001,Norovirus_Summer,norovirus,500000,1000000,2000000
```

### Step 3: Define Scenarios
Create scenarios referencing Location and Pathogen_ID:
```csv
Scenario_ID,Scenario_Name,Pathogen_ID,Location,Exposure_Route,Treatment_LRV,...
S001,Site_A_Summer,PATH001,Site_A,primary_contact,3,...
```

### Step 4: Run Assessment

**Using Python:**
```python
from batch_processor import BatchProcessor

processor = BatchProcessor(output_dir='outputs/results')

results = processor.run_batch_scenarios_from_libraries(
    scenarios_file='input_data/scenarios.csv',
    dilution_data_file='input_data/dilution_data.csv',
    pathogen_data_file='input_data/pathogen_data.csv'
)

print(f"Processed {len(results)} scenarios")
```

**Using Streamlit Web App:**
```bash
streamlit run web_app.py
```
Then:
1. Select "Batch Scenarios"
2. Check "Use example data" or upload your three files
3. Click "Run Batch Assessment"

---

## ✅ Key Advantages

### 1. **Simple Dilution Data**
- Just 3 columns: Time, Location, Dilution_Factor
- No need to specify distribution type
- Automatically uses ECDF from all data for each location
- Export directly from your hydrodynamic model!

### 2. **Straightforward Pathogen Data**
- Only Hockey Stick distribution (user-determined Min/Median/Max)
- No complicated distribution specifications
- Based on your best professional judgment and data

### 3. **Clear Scenarios**
- All parameters in one place
- Intuitive column names with units
- References Location and Pathogen_ID
- Easy to create scenario matrices

### 4. **Empirical Distributions**
- Dilution: Full ECDF from model data
- Pathogen: Hockey Stick (captures uncertainty)
- More realistic than simple parametric distributions

---

## 📊 Example Use Cases

### Use Case 1: Multi-Site Comparison
```csv
# Same pathogen, different locations
S001,Site_A_Norovirus,PATH001,Site_A,...
S002,Site_B_Norovirus,PATH001,Site_B,...
S003,Site_C_Norovirus,PATH001,Site_C,...
```

### Use Case 2: Treatment Scenarios
```csv
# Same location and pathogen, different treatments
S001,No_Treatment,PATH001,Site_A,primary_contact,0,...
S002,Secondary,PATH001,Site_A,primary_contact,3,...
S003,UV_Treatment,PATH001,Site_A,primary_contact,8,...
S004,MBR_Treatment,PATH001,Site_A,primary_contact,9.3,...
```

### Use Case 3: Multi-Pathogen Assessment
```csv
# Same location and treatment, different pathogens
S001,Site_A_Norovirus,PATH001,Site_A,primary_contact,3,...
S002,Site_A_Campylobacter,PATH003,Site_A,primary_contact,3.5,...
S003,Site_A_Cryptosporidium,PATH004,Site_A,primary_contact,2.5,...
```

### Use Case 4: Seasonal Comparison
```csv
# Summer vs Winter pathogen loads
S001,Summer_Scenario,PATH001,Site_A,...  # PATH001 = Norovirus_Summer
S002,Winter_Scenario,PATH002,Site_A,...  # PATH002 = Norovirus_Winter
```

---

## 🔍 How It Works

### Processing Flow:

1. **Load dilution_data.csv**
   - Filter by Location
   - Extract all Dilution_Factor values
   - Create ECDF

2. **Load pathogen_data.csv**
   - Look up by Pathogen_ID
   - Get Min, Median, Max concentrations
   - Create Hockey Stick distribution

3. **Load scenarios.csv**
   - For each scenario:
     - Look up Location → get dilution ECDF
     - Look up Pathogen_ID → get Hockey Stick parameters
     - Run Monte Carlo simulation
     - Calculate risks

4. **Output Results**
   - Comprehensive CSV with all scenario results
   - Compliance status (vs 1e-4 threshold)
   - Risk statistics (median, 5th, 95th percentiles)

---

## 📝 Column Naming Convention

All column names are **self-documenting** with units included:

| Column | Clear Name | Units Included |
|--------|-----------|----------------|
| Volume | `Ingestion_Volume_mL` | Yes (mL) |
| Frequency | `Exposure_Frequency_per_Year` | Yes (per year) |
| Population | `Exposed_Population` | Clear context |
| Treatment | `Treatment_LRV` | Clear (LRV) |

**Why This Matters:**
- No ambiguity about units
- Self-documenting
- Easy for others to understand
- Reduces errors

---

## ✅ Validation Checklist

Before running, verify:

- [ ] All Pathogen_IDs in scenarios.csv exist in pathogen_data.csv
- [ ] All Locations in scenarios.csv exist in dilution_data.csv
- [ ] Pathogen_Type values are valid (norovirus, campylobacter, etc.)
- [ ] Exposure_Route is either primary_contact or shellfish_consumption
- [ ] Min < Median < Max for all pathogen concentrations
- [ ] Treatment_LRV values are reasonable (0-10)
- [ ] All numeric fields are filled (no blanks)
- [ ] CSV files are UTF-8 encoded, comma-separated

---

## 📦 Example Files Included

The `input_data/` folder contains working examples:
- `dilution_data.csv` - 21 records across 3 locations
- `pathogen_data.csv` - 8 pathogen scenarios
- `scenarios.csv` - 15 example scenarios

Use these as templates for your own data!

---

## 🎯 Tips for Excel Users

1. Create three sheets in Excel:
   - `dilution_data`
   - `pathogen_data`
   - `scenarios`

2. Use data validation dropdowns:
   - `Pathogen_Type`: norovirus, campylobacter, cryptosporidium, e_coli, rotavirus, salmonella
   - `Exposure_Route`: primary_contact, shellfish_consumption
   - `Priority`: High, Medium, Low

3. For Location and Pathogen_ID:
   - Use consistent naming (Site_A, PATH001, etc.)
   - Create a reference table to ensure consistency

4. Save each sheet as separate CSV files

5. Always preview in Notepad to check formatting

---

## ❓ FAQ

**Q: Can I use other distributions for pathogens?**
A: No, this simplified approach only uses Hockey Stick. It's straightforward and captures key uncertainty.

**Q: Can I specify a single dilution value instead of ECDF?**
A: Yes! Just have multiple rows with the same Location and Dilution_Factor value.

**Q: What if I don't have monitoring data for pathogen min/max?**
A: Use literature values or conservative assumptions (e.g., min=0.5×median, max=2×median).

**Q: How many dilution records do I need per location?**
A: At least 10-20 for a reasonable ECDF, but more is better.

**Q: Can I have scenarios at the same location with different dilution data?**
A: No - all scenarios at a Location use all dilution data for that Location. Create separate locations if needed.

---

## 📚 Additional Documentation

- `test_simplified_approach.py` - Test script
- Example files in `input_data/`
- Web app help section (📖 File Format Guide)

---

## 🎉 Summary

The simplified approach provides:
- ✅ **3-column dilution data** - straightforward time-series
- ✅ **Hockey Stick pathogen** - user determines min/median/max
- ✅ **Clear scenarios** - all parameters with intuitive names
- ✅ **Automatic ECDF** - no distribution type needed
- ✅ **Empirical distributions** - more realistic assessments

**Ready to use!**

Run test:
```bash
python test_simplified_approach.py
```

Start web app:
```bash
streamlit run web_app.py
```

---

**NIWA Earth Sciences New Zealand**
*Quantitative Microbial Risk Assessment Tool*
Version 2.0 | October 2025
