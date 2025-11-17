# QMRA Batch Processing - Library-Based Input Data Structure

## Overview

The library-based approach separates reusable data into three distinct files for better organization and maintainability:

1. **dilution_library.csv** - Reusable dilution scenarios
2. **pathogen_library.csv** - Reusable pathogen concentration scenarios
3. **master_scenarios.csv** - Scenario definitions that reference libraries by ID

## File Descriptions

### 1. Dilution Library (`dilution_library.csv`)

Contains reusable dilution scenarios that can be referenced by multiple scenarios.

**Required Columns:**
- `Dilution_ID` (string): Unique identifier (e.g., DIL001, DIL002)
- `Dilution_Name` (string): Descriptive name
- `Dilution_Type` (string): Type of dilution data
  - `fixed`: Single dilution value
  - `lognormal`: Dilution with uncertainty distribution
  - `ecdf`: Empirical CDF from hydrodynamic modeling data
- `Dilution_Value` (number): Dilution factor for fixed/lognormal types
- `Dilution_Min` (number): Minimum for lognormal (optional)
- `Dilution_Max` (number): Maximum for lognormal (optional)
- `Dilution_Data_File` (string): CSV file path for ECDF type
- `Notes` (string): Description/metadata

**Example:**
```csv
Dilution_ID,Dilution_Name,Dilution_Type,Dilution_Value,Dilution_Min,Dilution_Max,Dilution_Data_File,Notes
DIL001,Typical_Beach_100x,fixed,100,,,,"Standard 100x dilution"
DIL002,Variable_Beach_75x,lognormal,75,25,150,,"Variable conditions CV=0.4"
DIL003,Spatial_ECDF,ecdf,,,,spatial_dilution_6_sites.csv,"ECDF from model"
```

### 2. Pathogen Library (`pathogen_library.csv`)

Contains reusable pathogen concentration scenarios.

**Required Columns:**
- `Pathogen_ID` (string): Unique identifier (e.g., PATH001, PATH002)
- `Pathogen_Name` (string): Descriptive name
- `Pathogen_Type` (string): Pathogen organism type
  - Valid values: `norovirus`, `campylobacter`, `cryptosporidium`, `e_coli`, `rotavirus`, `salmonella`
- `Effluent_Conc` (number): Effluent concentration (copies/L or MPN/L) for fixed/lognormal
- `Effluent_Conc_Min` (number): Minimum for hockey_stick distribution
- `Effluent_Conc_Median` (number): Median for hockey_stick distribution
- `Effluent_Conc_Max` (number): Maximum for hockey_stick distribution
- `Effluent_Conc_CV` (number): Coefficient of variation (0-1) for lognormal
- `Distribution_Type` (string): Type of distribution
  - `lognormal`: Log-normal distribution with specified CV
  - `hockey_stick`: Hockey stick distribution (min, median, max)
- `Pathogen_Data_File` (string): CSV file for time series data (optional)
- `Notes` (string): Description/metadata

**Example:**
```csv
Pathogen_ID,Pathogen_Name,Pathogen_Type,Effluent_Conc,Effluent_Conc_Min,Effluent_Conc_Median,Effluent_Conc_Max,Effluent_Conc_CV,Distribution_Type,Pathogen_Data_File,Notes
PATH001,Norovirus_Typical_1M,norovirus,1000000,,,,0.4,lognormal,,"Typical concentration"
PATH002,Norovirus_Hockey_Stick,norovirus,,500000,1000000,2000000,,hockey_stick,,"Variable with Hockey Stick"
PATH003,Campylobacter_500k,campylobacter,500000,,,,0.5,lognormal,,"Typical Campylo"
```

### 3. Master Scenarios (`master_scenarios.csv`)

Defines scenarios by referencing pathogen and dilution libraries.

**Required Columns:**
- `Scenario_ID` (string): Unique scenario identifier (e.g., S001, S002)
- `Scenario_Name` (string): Descriptive name
- `Pathogen_ID` (string): Reference to pathogen_library.csv
- `Dilution_ID` (string): Reference to dilution_library.csv
- `Exposure_Route` (string): Route of exposure
  - Valid values: `primary_contact`, `shellfish_consumption`
- `Treatment_LRV` (number): Log reduction value from treatment (0-10)
- `Treatment_LRV_Uncertainty` (number): Uncertainty in LRV (0-1, typically 0.2-0.5)
- `Ingestion_Volume_mL` (number): Mean ingestion volume in milliliters
- `Volume_Min_mL` (number): Minimum ingestion volume (optional)
- `Volume_Max_mL` (number): Maximum ingestion volume (optional)
- `Exposure_Frequency_per_Year` (number): Number of exposure events per year
- `Exposed_Population` (number): Size of exposed population
- `Monte_Carlo_Iterations` (number): Number of MC iterations (typically 10000)
- `Priority` (string): Scenario priority (High, Medium, Low)
- `Notes` (string): Description/metadata

**Example:**
```csv
Scenario_ID,Scenario_Name,Pathogen_ID,Dilution_ID,Exposure_Route,Treatment_LRV,Treatment_LRV_Uncertainty,Ingestion_Volume_mL,Volume_Min_mL,Volume_Max_mL,Exposure_Frequency_per_Year,Exposed_Population,Monte_Carlo_Iterations,Priority,Notes
S001,Beach_A_Summer,PATH001,DIL001,primary_contact,3,0.3,50,35,75,25,15000,10000,High,"Main tourist beach"
S002,Shellfish_Area_1,PATH001,DIL004,shellfish_consumption,3,0.3,100,80,150,24,5000,10000,High,"Commercial shellfish"
```

## Advantages of This Approach

### 1. **Reusability**
Define dilution and pathogen data once, use in multiple scenarios:
- Same pathogen concentration can be tested with different dilutions
- Same dilution can be tested with different pathogens
- Easy to create scenario matrices

### 2. **Maintainability**
Update data in one place:
- Change a pathogen concentration → affects all scenarios using that pathogen
- Update dilution factor → affects all relevant scenarios
- Centralized data management

### 3. **Clarity**
Separate concerns:
- **Libraries** = Reusable data definitions
- **Scenarios** = Specific combinations and parameters
- Clear which data comes from where

### 4. **Consistency**
- Ensures consistent data across related scenarios
- Reduces copy-paste errors
- Easier quality control

### 5. **Straightforward Column Names**
- Intuitive naming: `Ingestion_Volume_mL` instead of `Volume_mL`
- Clear units in column names: `_mL`, `_per_Year`, etc.
- Self-documenting structure

## Usage Example

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
```

### Command Line:
```bash
cd Batch_Processing_App
python test_library_approach.py
```

## Data Preparation Workflow

1. **Create Dilution Library**
   - Define all dilution scenarios you'll use
   - Assign unique IDs (DIL001, DIL002, ...)
   - Specify type (fixed, lognormal, ecdf)

2. **Create Pathogen Library**
   - Define all pathogen concentration scenarios
   - Assign unique IDs (PATH001, PATH002, ...)
   - Specify distribution type

3. **Create Master Scenarios**
   - Reference pathogen and dilution by ID
   - Specify treatment, exposure, and population parameters
   - Each scenario is a unique combination

4. **Run Batch Processing**
   - Use `run_batch_scenarios_from_libraries()` method
   - Results include traceable IDs back to source data

## Tips for Data Entry

### Excel Workflow:
1. Create three separate sheets in Excel
2. Name them: dilution_library, pathogen_library, master_scenarios
3. Use data validation for:
   - Dilution_Type: dropdown (fixed, lognormal, ecdf)
   - Distribution_Type: dropdown (lognormal, hockey_stick)
   - Pathogen_Type: dropdown (norovirus, campylobacter, etc.)
   - Exposure_Route: dropdown (primary_contact, shellfish_consumption)
4. Save each sheet as CSV

### Validation:
- Ensure all IDs referenced in master_scenarios exist in libraries
- Check that required columns are not empty
- Verify numeric ranges are sensible
- Test with a small subset first

## Common Patterns

### Pattern 1: Treatment Comparison
Use same pathogen and dilution, vary treatment:
```csv
S001,Treatment_None,PATH001,DIL001,primary_contact,0,...
S002,Treatment_Secondary,PATH001,DIL001,primary_contact,3,...
S003,Treatment_UV,PATH001,DIL001,primary_contact,8,...
```

### Pattern 2: Spatial Analysis
Use same pathogen and treatment, vary dilution:
```csv
S001,Site_A,PATH001,DIL001,primary_contact,3,...
S002,Site_B,PATH001,DIL002,primary_contact,3,...
S003,Site_C,PATH001,DIL003,primary_contact,3,...
```

### Pattern 3: Multi-Pathogen
Use same dilution and treatment, vary pathogen:
```csv
S001,Norovirus,PATH001,DIL001,primary_contact,3,...
S002,Campylobacter,PATH003,DIL001,primary_contact,3,...
S003,Cryptosporidium,PATH004,DIL001,primary_contact,3,...
```

## Files Included

- `dilution_library.csv` - Example dilution library with 10 entries
- `pathogen_library.csv` - Example pathogen library with 10 entries
- `master_scenarios.csv` - Example scenarios referencing libraries (15 scenarios)
- `README_LIBRARY_APPROACH.md` - This documentation file

## Support

For questions or issues with the library-based approach:
1. Check that all IDs in master_scenarios exist in the libraries
2. Verify column names match exactly (case-sensitive)
3. Ensure CSV files are properly formatted (UTF-8 encoding, comma-separated)
4. Run `test_library_approach.py` to verify setup

---

**NIWA Earth Sciences New Zealand**
*Quantitative Microbial Risk Assessment Tool*
Version 2.0 | October 2025
