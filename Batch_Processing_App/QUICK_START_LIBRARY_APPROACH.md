# Quick Start Guide: Library-Based Batch Processing

## What's New?

The batch app now uses **three separate files** for cleaner, more maintainable data input:

```
input_data/
├── dilution_library.csv       ← Reusable dilution scenarios
├── pathogen_library.csv       ← Reusable pathogen concentrations
└── master_scenarios.csv       ← Your scenarios (references above by ID)
```

## Why This Approach?

✅ **Reusability**: Define data once, use in multiple scenarios
✅ **Clear Structure**: Separate data libraries from scenario parameters
✅ **Easy Maintenance**: Update pathogen/dilution data in one place
✅ **Straightforward**: Intuitive column names with units included

## Column Names Reference

### Dilution Library

| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| `Dilution_ID` | Text | Unique ID | DIL001, DIL002 |
| `Dilution_Name` | Text | Descriptive name | "Typical_Beach_100x" |
| `Dilution_Type` | Text | fixed, lognormal, ecdf | fixed |
| `Dilution_Value` | Number | Dilution factor | 100 |
| `Dilution_Min` | Number | Minimum (optional) | 25 |
| `Dilution_Max` | Number | Maximum (optional) | 150 |
| `Dilution_Data_File` | Text | CSV for ECDF (optional) | "spatial_data.csv" |
| `Notes` | Text | Description | "Standard conditions" |

### Pathogen Library

| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| `Pathogen_ID` | Text | Unique ID | PATH001, PATH002 |
| `Pathogen_Name` | Text | Descriptive name | "Norovirus_Typical_1M" |
| `Pathogen_Type` | Text | Organism | norovirus, campylobacter, cryptosporidium, e_coli, rotavirus, salmonella |
| `Effluent_Conc` | Number | Concentration (copies/L) | 1000000 |
| `Effluent_Conc_Min` | Number | Min for hockey_stick | 500000 |
| `Effluent_Conc_Median` | Number | Median for hockey_stick | 1000000 |
| `Effluent_Conc_Max` | Number | Max for hockey_stick | 2000000 |
| `Effluent_Conc_CV` | Number | Coefficient of variation (0-1) | 0.4 |
| `Distribution_Type` | Text | lognormal, hockey_stick | lognormal |
| `Pathogen_Data_File` | Text | Time series file (optional) | "weekly_data.csv" |
| `Notes` | Text | Description | "Summer season data" |

### Master Scenarios

| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| `Scenario_ID` | Text | Unique ID | S001, S002 |
| `Scenario_Name` | Text | Descriptive name | "Beach_A_Summer" |
| `Pathogen_ID` | Text | Reference to pathogen library | PATH001 |
| `Dilution_ID` | Text | Reference to dilution library | DIL001 |
| `Exposure_Route` | Text | primary_contact, shellfish_consumption | primary_contact |
| `Treatment_LRV` | Number | Log reduction value (0-10) | 3 |
| `Treatment_LRV_Uncertainty` | Number | Uncertainty (0-1) | 0.3 |
| `Ingestion_Volume_mL` | Number | Mean volume (mL) | 50 |
| `Volume_Min_mL` | Number | Minimum volume (optional) | 35 |
| `Volume_Max_mL` | Number | Maximum volume (optional) | 75 |
| `Exposure_Frequency_per_Year` | Number | Events per year | 25 |
| `Exposed_Population` | Number | Population size | 15000 |
| `Monte_Carlo_Iterations` | Number | MC iterations | 10000 |
| `Priority` | Text | High, Medium, Low | High |
| `Notes` | Text | Description | "Main tourist beach" |

## Quick Start in 3 Steps

### Step 1: Prepare Your Dilution Library

Create `dilution_library.csv` with your dilution scenarios:

```csv
Dilution_ID,Dilution_Name,Dilution_Type,Dilution_Value,Dilution_Min,Dilution_Max,Dilution_Data_File,Notes
DIL001,Standard_100x,fixed,100,,,,"Standard dilution"
DIL002,Poor_50x,fixed,50,,,,"Poor mixing"
DIL003,Excellent_500x,fixed,500,,,,"Good dilution"
```

### Step 2: Prepare Your Pathogen Library

Create `pathogen_library.csv` with your pathogen concentrations:

```csv
Pathogen_ID,Pathogen_Name,Pathogen_Type,Effluent_Conc,Effluent_Conc_Min,Effluent_Conc_Median,Effluent_Conc_Max,Effluent_Conc_CV,Distribution_Type,Pathogen_Data_File,Notes
PATH001,Norovirus_1M,norovirus,1000000,,,,0.4,lognormal,,"Typical concentration"
PATH002,Campylo_500k,campylobacter,500000,,,,0.5,lognormal,,"Typical Campylobacter"
```

### Step 3: Create Your Scenarios

Create `master_scenarios.csv` referencing the libraries:

```csv
Scenario_ID,Scenario_Name,Pathogen_ID,Dilution_ID,Exposure_Route,Treatment_LRV,Treatment_LRV_Uncertainty,Ingestion_Volume_mL,Volume_Min_mL,Volume_Max_mL,Exposure_Frequency_per_Year,Exposed_Population,Monte_Carlo_Iterations,Priority,Notes
S001,Beach_A_Norovirus,PATH001,DIL001,primary_contact,3,0.3,50,35,75,25,15000,10000,High,"Main beach"
S002,Beach_A_Campylo,PATH002,DIL001,primary_contact,3.5,0.3,50,35,75,25,15000,10000,Medium,"Main beach Campylo"
```

## Running the Analysis

### Python Script:

```python
from batch_processor import BatchProcessor

processor = BatchProcessor(output_dir='outputs/results')

results = processor.run_batch_scenarios_from_libraries(
    scenarios_file='input_data/master_scenarios.csv',
    dilution_library_file='input_data/dilution_library.csv',
    pathogen_library_file='input_data/pathogen_library.csv',
    output_dir='outputs/results'
)

print(f"Processed {len(results)} scenarios")
print(f"Compliant: {len(results[results['Compliance_Status'] == 'COMPLIANT'])}")
```

### Test Script:

```bash
cd Batch_Processing_App
python test_library_approach.py
```

## Common Use Cases

### Case 1: Test Multiple Treatments

Keep pathogen and dilution the same, vary treatment:

```csv
# In dilution_library.csv
DIL001,Beach_Standard,fixed,100,...

# In pathogen_library.csv
PATH001,Norovirus_Typical,norovirus,1000000,...

# In master_scenarios.csv
S001,No_Treatment,PATH001,DIL001,primary_contact,0,...
S002,Secondary_Treatment,PATH001,DIL001,primary_contact,3,...
S003,UV_Treatment,PATH001,DIL001,primary_contact,8,...
S004,MBR_Treatment,PATH001,DIL001,primary_contact,9.3,...
```

### Case 2: Spatial Analysis (Multiple Sites)

Keep pathogen and treatment the same, vary dilution:

```csv
# In dilution_library.csv
DIL001,Site_A_100x,fixed,100,...
DIL002,Site_B_50x,fixed,50,...
DIL003,Site_C_200x,fixed,200,...

# In master_scenarios.csv
S001,Site_A,PATH001,DIL001,primary_contact,3,...
S002,Site_B,PATH001,DIL002,primary_contact,3,...
S003,Site_C,PATH001,DIL003,primary_contact,3,...
```

### Case 3: Multi-Pathogen Comparison

Keep dilution and treatment the same, vary pathogen:

```csv
# In pathogen_library.csv
PATH001,Norovirus,norovirus,1000000,...
PATH002,Campylobacter,campylobacter,500000,...
PATH003,Cryptosporidium,cryptosporidium,50000,...

# In master_scenarios.csv
S001,Norovirus_Test,PATH001,DIL001,primary_contact,3,...
S002,Campylo_Test,PATH002,DIL001,primary_contact,3.5,...
S003,Crypto_Test,PATH003,DIL001,primary_contact,2.5,...
```

## Tips for Excel Users

1. Create three sheets: `dilution_library`, `pathogen_library`, `master_scenarios`
2. Use data validation for dropdown columns:
   - `Dilution_Type`: fixed, lognormal, ecdf
   - `Pathogen_Type`: norovirus, campylobacter, cryptosporidium, e_coli, rotavirus, salmonella
   - `Distribution_Type`: lognormal, hockey_stick
   - `Exposure_Route`: primary_contact, shellfish_consumption
   - `Priority`: High, Medium, Low
3. Save each sheet as separate CSV files
4. Use consistent ID naming (DIL001, PATH001, S001, etc.)

## Validation Checklist

Before running:
- [ ] All Pathogen_IDs in master_scenarios exist in pathogen_library
- [ ] All Dilution_IDs in master_scenarios exist in dilution_library
- [ ] Column names match exactly (case-sensitive)
- [ ] No empty required fields
- [ ] Numeric values in correct ranges
- [ ] CSV files are UTF-8 encoded, comma-separated

## Example Files Provided

The `input_data/` folder contains working examples:
- `dilution_library.csv` - 10 example dilution scenarios
- `pathogen_library.csv` - 10 example pathogen scenarios
- `master_scenarios.csv` - 15 example scenarios

Use these as templates for your own data!

## Need Help?

1. Check `README_LIBRARY_APPROACH.md` for detailed documentation
2. Run `test_library_approach.py` to verify your setup
3. Look at example files in `input_data/` folder
4. Ensure all IDs match between files

---

**NIWA Earth Sciences** | QMRA Batch Processing v2.0 | October 2025
