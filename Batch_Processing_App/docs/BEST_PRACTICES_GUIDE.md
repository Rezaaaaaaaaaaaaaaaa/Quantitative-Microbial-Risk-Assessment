# Best Practices Guide: Implementing Empirical Distributions

## Decision Tree: When to Use What

```
Do you have hydrodynamic modeling data (100+ dilution simulations)?
│
├─ YES → Use ECDF for dilution (use_ecdf_dilution=True)
│   │
│   └─ Do you have monitoring data with high variability (CV > 0.5)?
│       │
│       ├─ YES → Use Hockey Stick for pathogen (use_hockey_pathogen=True)
│       │         → BEST: Both distributions
│       │
│       └─ NO → Use fixed pathogen concentration
│                → GOOD: ECDF dilution only
│
└─ NO (only have median dilution) → Use legacy approach
    │
    └─ Do you have monitoring data with high variability?
        │
        ├─ YES → Use Hockey Stick for pathogen only
        │
        └─ NO → Use legacy fixed values
```

## Three Implementation Approaches

### Approach 1: Automated Batch Processing (RECOMMENDED)
**Best for**: Running many scenarios, production workflows

**How it works**:
1. Prepare input CSV with distribution flags
2. Let batch processor auto-calculate everything
3. Review results

**Example**:

```csv
# scenarios_production.csv
Scenario_ID,Pathogen,Dilution_File,Use_ECDF,Use_Hockey,Monitoring_File,Treatment_LRV
S001,norovirus,spatial_dilution_6_sites.csv,TRUE,TRUE,weekly_monitoring_2024.csv,3.0
S002,campylobacter,spatial_dilution_6_sites.csv,TRUE,TRUE,weekly_monitoring_2024.csv,2.5
```

Then run:
```python
from batch_processor import BatchProcessor
processor = BatchProcessor()

# Process all scenarios from CSV
results = processor.run_batch_scenarios_with_distributions(
    scenario_file='scenarios_production.csv'
)
```

### Approach 2: Interactive Single Assessment
**Best for**: Exploring one site, testing parameters, what-if analysis

**How it works**:
1. Load your data interactively
2. Calculate distribution parameters on the fly
3. Run single assessment
4. Adjust and re-run

**Example**:

```python
import pandas as pd
from batch_processor import BatchProcessor

# Load monitoring data and calculate parameters
monitoring = pd.read_csv('input_data/pathogen_concentrations/weekly_monitoring_2024.csv')
pathogen_min = monitoring['Norovirus_copies_per_L'].min()
pathogen_median = monitoring['Norovirus_copies_per_L'].median()
pathogen_max = monitoring['Norovirus_copies_per_L'].max()

print(f"Calculated parameters: min={pathogen_min:.0f}, median={pathogen_median:.0f}, max={pathogen_max:.0f}")

# Run assessment with these parameters
processor = BatchProcessor()
results = processor.run_spatial_assessment(
    dilution_file='input_data/dilution_data/spatial_dilution_6_sites.csv',
    pathogen='norovirus',
    use_ecdf_dilution=True,
    use_hockey_pathogen=True,
    pathogen_min=pathogen_min,
    pathogen_median=pathogen_median,
    pathogen_max=pathogen_max,
    treatment_lrv=3.0,
    iterations=10000
)
```

### Approach 3: Hybrid (CSV + Manual Parameters)
**Best for**: Using standard scenarios but tweaking parameters

**How it works**:
1. Store standard scenarios in CSV
2. Override specific parameters in code
3. Run batch processing

**Example**:

```python
# Read standard scenarios
scenarios = pd.read_csv('scenarios_production.csv')

# Add calculated parameters
for idx, scenario in scenarios.iterrows():
    monitoring = pd.read_csv(scenario['Monitoring_File'])
    pathogen_col = f"{scenario['Pathogen']}_copies_per_L"

    scenarios.loc[idx, 'Pathogen_Min'] = monitoring[pathogen_col].min()
    scenarios.loc[idx, 'Pathogen_Median'] = monitoring[pathogen_col].median()
    scenarios.loc[idx, 'Pathogen_Max'] = monitoring[pathogen_col].max()

# Save updated scenarios
scenarios.to_csv('scenarios_with_params.csv', index=False)

# Run batch processing
processor.run_batch_scenarios('scenarios_with_params.csv')
```

## Recommended: Step-by-Step Workflow

### Step 1: Prepare Your Input Data

You already have these files:
- ✓ `spatial_dilution_6_sites.csv` - 100 simulations per site
- ✓ `weekly_monitoring_2024.csv` - Pathogen monitoring data

### Step 2: Calculate Pathogen Parameters (One-Time Setup)

Create a helper script:

```python
# calculate_pathogen_parameters.py
import pandas as pd
import numpy as np

monitoring = pd.read_csv('input_data/pathogen_concentrations/weekly_monitoring_2024.csv')

pathogens = ['Norovirus', 'Campylobacter', 'Cryptosporidium']
params = []

for pathogen in pathogens:
    col = f'{pathogen}_copies_per_L'

    if col in monitoring.columns:
        data = monitoring[col].dropna()

        # Calculate Hockey Stick parameters
        p_min = data.min()
        p_median = data.median()
        p_max = data.max()

        # Calculate variability
        cv = data.std() / data.mean()

        # Decide if Hockey Stick is appropriate
        use_hockey = cv > 0.5  # High variability

        params.append({
            'Pathogen': pathogen.lower(),
            'Min': p_min,
            'Median': p_median,
            'Max': p_max,
            'CV': cv,
            'Recommended_Distribution': 'Hockey_Stick' if use_hockey else 'Fixed',
            'Sample_Size': len(data)
        })

# Save parameters
params_df = pd.DataFrame(params)
params_df.to_csv('input_data/pathogen_parameters.csv', index=False)
print(params_df)
```

**Run once**:
```bash
python calculate_pathogen_parameters.py
```

**Output** (`pathogen_parameters.csv`):
```csv
Pathogen,Min,Median,Max,CV,Recommended_Distribution,Sample_Size
norovirus,200,1026,3484,0.82,Hockey_Stick,12
campylobacter,3178,26260,73565,0.91,Hockey_Stick,12
cryptosporidium,2.23,6.36,14.35,0.65,Hockey_Stick,12
```

### Step 3: Create Your Scenario Template

Create `my_scenarios.csv`:

```csv
Scenario_ID,Scenario_Name,Pathogen,Site_Selection,Treatment_LRV,Exposure_Route,Volume_mL,Frequency_Year,Population,Use_ECDF,Use_Hockey,Notes
S001,Beach_Main_Summer,norovirus,Site_50m,3.0,primary_contact,50,25,15000,TRUE,TRUE,Main beach summer assessment
S002,Beach_Main_Winter,norovirus,Site_50m,3.0,primary_contact,30,8,2000,TRUE,TRUE,Winter swimmers
S003,Near_Discharge,norovirus,Discharge,2.5,primary_contact,50,20,5000,TRUE,TRUE,Worst case near discharge
S004,Far_Field,norovirus,Site_1000m,3.0,primary_contact,50,25,10000,TRUE,FALSE,Far field - fixed pathogen OK
```

### Step 4: Create a Master Runner Script

```python
# run_qmra_analysis.py
"""
Master script for running QMRA with empirical distributions.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from batch_processor import BatchProcessor

def main():
    print("="*80)
    print("QMRA ANALYSIS WITH EMPIRICAL DISTRIBUTIONS")
    print("="*80)

    # Initialize
    processor = BatchProcessor(output_dir='outputs/production')

    # Load scenario definitions
    scenarios = pd.read_csv('my_scenarios.csv')

    # Load pathogen parameters (pre-calculated)
    pathogen_params = pd.read_csv('input_data/pathogen_parameters.csv')
    pathogen_params = pathogen_params.set_index('Pathogen')

    # Load dilution file (same for all scenarios)
    dilution_file = 'input_data/dilution_data/spatial_dilution_6_sites.csv'

    all_results = []

    for idx, scenario in scenarios.iterrows():
        print(f"\n[{idx+1}/{len(scenarios)}] Processing: {scenario['Scenario_ID']} - {scenario['Scenario_Name']}")

        # Get pathogen parameters
        pathogen = scenario['Pathogen']
        params = pathogen_params.loc[pathogen]

        # Decide on distributions
        use_ecdf = scenario.get('Use_ECDF', True)
        use_hockey = scenario.get('Use_Hockey', True) and params['Recommended_Distribution'] == 'Hockey_Stick'

        print(f"  Dilution: {'ECDF (100 sims)' if use_ecdf else 'Median only'}")
        print(f"  Pathogen: {'Hockey Stick' if use_hockey else 'Fixed'}")

        # Run spatial assessment
        try:
            results = processor.run_spatial_assessment(
                dilution_file=dilution_file,
                pathogen=pathogen,
                exposure_route=scenario['Exposure_Route'],
                volume_ml=scenario['Volume_mL'],
                frequency_per_year=scenario['Frequency_Year'],
                population=scenario['Population'],
                treatment_lrv=scenario['Treatment_LRV'],
                iterations=10000,
                use_ecdf_dilution=use_ecdf,
                use_hockey_pathogen=use_hockey,
                pathogen_min=params['Min'] if use_hockey else None,
                pathogen_median=params['Median'],
                pathogen_max=params['Max'] if use_hockey else None,
                effluent_concentration=params['Median'] if not use_hockey else None,
                output_file=f"{scenario['Scenario_ID']}_results.csv"
            )

            # Filter to requested site if specified
            if scenario.get('Site_Selection'):
                site_name = scenario['Site_Selection']
                results = results[results['Site_Name'] == site_name]

            # Add scenario metadata
            results['Scenario_ID'] = scenario['Scenario_ID']
            results['Scenario_Name'] = scenario['Scenario_Name']

            all_results.append(results)

            # Print summary
            if len(results) > 0:
                for _, site in results.iterrows():
                    print(f"    {site['Site_Name']}: Risk={site['Annual_Risk_Median']:.2e} [{site['Compliance_Status']}]")

        except Exception as e:
            print(f"  ERROR: {e}")
            continue

    # Combine all results
    if all_results:
        combined = pd.concat(all_results, ignore_index=True)
        combined.to_csv('outputs/production/all_scenarios_combined.csv', index=False)

        # Summary report
        print("\n" + "="*80)
        print("SUMMARY REPORT")
        print("="*80)

        summary = combined.groupby(['Scenario_ID', 'Scenario_Name']).agg({
            'Annual_Risk_Median': 'first',
            'Annual_Risk_95th': 'first',
            'Compliance_Status': 'first'
        }).reset_index()

        print(f"\n{len(summary)} scenarios processed:")
        for _, row in summary.iterrows():
            print(f"  {row['Scenario_ID']}: {row['Annual_Risk_Median']:.2e} [{row['Compliance_Status']}]")

        compliant = len(summary[summary['Compliance_Status'] == 'COMPLIANT'])
        print(f"\nCompliance: {compliant}/{len(summary)} ({100*compliant/len(summary):.1f}%)")

        print(f"\nAll results saved to: outputs/production/")

    print("="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
```

### Step 5: Run Your Analysis

```bash
# One-time setup
python calculate_pathogen_parameters.py

# Run analysis
python run_qmra_analysis.py
```

## What Each Approach Gives You

| Approach | Setup Time | Flexibility | Best For |
|----------|-----------|-------------|----------|
| **Automated Batch** | Low (just CSV) | Low | Production, many scenarios |
| **Interactive** | Medium | High | Exploration, testing |
| **Hybrid (RECOMMENDED)** | Medium | High | Most real-world use cases |

## Common Pitfalls to Avoid

### ❌ DON'T: Hard-code pathogen parameters
```python
# Bad - parameters will become outdated
results = processor.run_spatial_assessment(
    pathogen_min=1000,  # Where did this come from?
    pathogen_median=50000,
    pathogen_max=1000000
)
```

### ✅ DO: Calculate from monitoring data
```python
# Good - parameters come from actual data
monitoring = pd.read_csv('weekly_monitoring_2024.csv')
pathogen_min = monitoring['Norovirus_copies_per_L'].min()
pathogen_median = monitoring['Norovirus_copies_per_L'].median()
pathogen_max = monitoring['Norovirus_copies_per_L'].max()
```

### ❌ DON'T: Use Hockey Stick for low-variability data
```python
# Bad - CV < 0.3, Hockey Stick not appropriate
data_cv = 0.25
use_hockey = True  # Wrong!
```

### ✅ DO: Check variability first
```python
# Good - only use Hockey Stick if appropriate
data_cv = data.std() / data.mean()
use_hockey = data_cv > 0.5  # High variability threshold
```

### ❌ DON'T: Mix median dilution with Hockey Stick pathogen
```python
# Bad - inconsistent uncertainty treatment
use_ecdf_dilution = False  # Using median
use_hockey_pathogen = True  # But modeling full pathogen distribution
# This underweights dilution uncertainty!
```

### ✅ DO: Be consistent with uncertainty treatment
```python
# Good - both distributions or neither
use_ecdf_dilution = True
use_hockey_pathogen = True
# OR
use_ecdf_dilution = False
use_hockey_pathogen = False
```

## Quick Reference: Parameter Sources

```python
# Where parameters come from:

# ECDF Dilution:
# - Source: spatial_dilution_6_sites.csv
# - Uses: All 100 simulations per site
# - No calculation needed - just set use_ecdf_dilution=True

# Hockey Stick Pathogen:
# - Source: weekly_monitoring_2024.csv
# - Calculate: min(), median(), max() from monitoring data
# - Check: CV > 0.5 to decide if appropriate

# Fixed Values (Legacy):
# - Source: Literature, expert judgment, single measurement
# - Used when: No time-series data available
```

## Recommended Starting Point

**Start here if unsure**:

```python
from batch_processor import BatchProcessor
import pandas as pd

# 1. Calculate pathogen parameters from your monitoring data
monitoring = pd.read_csv('input_data/pathogen_concentrations/weekly_monitoring_2024.csv')
p_min = monitoring['Norovirus_copies_per_L'].min()
p_median = monitoring['Norovirus_copies_per_L'].median()
p_max = monitoring['Norovirus_copies_per_L'].max()

# 2. Run assessment with both distributions
processor = BatchProcessor()
results = processor.run_spatial_assessment(
    dilution_file='input_data/dilution_data/spatial_dilution_6_sites.csv',
    pathogen='norovirus',
    use_ecdf_dilution=True,      # Use all hydrodynamic data
    use_hockey_pathogen=True,     # Use monitoring data distribution
    pathogen_min=p_min,
    pathogen_median=p_median,
    pathogen_max=p_max,
    treatment_lrv=3.0,
    exposure_route='primary_contact',
    volume_ml=50,
    frequency_per_year=25,
    population=15000,
    iterations=10000,
    output_file='my_first_distributed_assessment.csv'
)

# 3. Review results
print(results[['Site_Name', 'Annual_Risk_Median', 'Compliance_Status']])
```

## Next Steps

1. **Run the one-time setup**: Calculate pathogen parameters
2. **Create your scenario CSV**: Start with 2-3 scenarios
3. **Run the analysis**: Use the master runner script
4. **Compare with legacy results**: See the difference
5. **Adopt for production**: Once validated, make it your standard workflow

Need help with any of these steps? Let me know which approach fits your workflow best!
