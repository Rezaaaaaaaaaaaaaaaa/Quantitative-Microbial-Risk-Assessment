# Quick Start Guide: Best Way to Use Empirical Distributions

## TL;DR - The Simplest Recommendation

**Just run**: `python SIMPLE_EXAMPLE.py`

That's it! This shows you exactly how to use the distributions.

## The Best Implementation (Copy-Paste Ready)

```python
from batch_processor import BatchProcessor
import pandas as pd

# Step 1: Calculate pathogen parameters from YOUR monitoring data
monitoring = pd.read_csv('input_data/pathogen_concentrations/multi_pathogen_data.csv')
p_min = monitoring['Norovirus_copies_per_L'].min()
p_median = monitoring['Norovirus_copies_per_L'].median()
p_max = monitoring['Norovirus_copies_per_L'].max()

# Step 2: Run assessment (THIS IS THE RECOMMENDED WAY)
processor = BatchProcessor()
results = processor.run_spatial_assessment(
    dilution_file='input_data/dilution_data/spatial_dilution_6_sites.csv',
    pathogen='norovirus',
    use_ecdf_dilution=True,      # ← Uses all 100 simulations (not just median)
    use_hockey_pathogen=True,     # ← Uses monitoring data distribution
    pathogen_min=p_min,
    pathogen_median=p_median,
    pathogen_max=p_max,
    treatment_lrv=3.0,
    iterations=10000
)

# Step 3: Done! Review results
print(results[['Site_Name', 'Annual_Risk_Median', 'Compliance_Status']])
```

## What These Two Flags Do

### `use_ecdf_dilution=True` (ALWAYS USE THIS)
- **What it does**: Uses all 100 hydrodynamic simulations
- **What you had before**: Only used median (threw away 99% of data)
- **Benefit**: Captures full range of dilution variability
- **When to use**: ALWAYS (if you have hydrodynamic data)
- **Downside**: None

### `use_hockey_pathogen=True` (USE IF CV > 0.5)
- **What it does**: Models pathogen concentration as distribution (min/median/max)
- **What you had before**: Used single fixed concentration
- **Benefit**: Represents high-concentration events better
- **When to use**: When monitoring data shows high variability (CV > 0.5)
- **Downside**: Requires monitoring data with min/median/max

## Decision Matrix

```
Your Data Situation                          → Recommended Settings
─────────────────────────────────────────────────────────────────────
✓ Have hydrodynamic modeling (100 sims)     → use_ecdf_dilution=True
✓ Have monitoring with CV > 0.5              → use_hockey_pathogen=True

Example: You have both                       → use_ecdf_dilution=True
                                               use_hockey_pathogen=True
                                               ← THIS IS THE BEST OPTION

Only have median dilution                    → use_ecdf_dilution=False
Only have single pathogen measurement        → use_hockey_pathogen=False
                                               (provide effluent_concentration)
```

## What Changed in Your Data

### Before (Your Current Workflow):
```python
# Old way - only uses median
results = processor.run_spatial_assessment(
    dilution_file='spatial_dilution_6_sites.csv',
    pathogen='norovirus',
    effluent_concentration=1000000,  # Single fixed value
    # Behind the scenes: uses median of 100 simulations
    # Result: Wastes 99% of hydrodynamic data
)
```

### After (New Recommended Way):
```python
# New way - uses ALL data
results = processor.run_spatial_assessment(
    dilution_file='spatial_dilution_6_sites.csv',
    pathogen='norovirus',
    use_ecdf_dilution=True,      # Uses all 100 simulations
    use_hockey_pathogen=True,     # Uses min/median/max from monitoring
    pathogen_min=200,
    pathogen_median=772,
    pathogen_max=3484,
    # Result: Uses 100% of your data, better uncertainty estimates
)
```

## Input Files - No Changes Needed!

Your existing files work perfectly:

✓ `spatial_dilution_6_sites.csv` - Already has 100 simulations per site
✓ `multi_pathogen_data.csv` - Already has monitoring data
✓ No file format changes required!

The ONLY thing that changes is **how** you call the function (two new parameters).

## Common Questions

### Q: Do I need to change my CSV files?
**A**: No! Your existing files work perfectly.

### Q: What if I don't have monitoring data?
**A**: Use `use_hockey_pathogen=False` and provide `effluent_concentration` like before.

### Q: What if I only have median dilution?
**A**: Use `use_ecdf_dilution=False` and it works like before.

### Q: Is this backward compatible?
**A**: Yes! Your old code still works exactly the same way.

### Q: Which approach should I use?
**A**:
- **Best**: `use_ecdf_dilution=True` + `use_hockey_pathogen=True` (both)
- **Good**: `use_ecdf_dilution=True` + `use_hockey_pathogen=False` (ECDF only)
- **Legacy**: `use_ecdf_dilution=False` + `use_hockey_pathogen=False` (old way)

### Q: How do I know if Hockey Stick is appropriate?
**A**: Calculate CV from monitoring data. If CV > 0.5, use Hockey Stick.

```python
monitoring = pd.read_csv('monitoring_file.csv')
data = monitoring['Pathogen_Column']
cv = data.std() / data.mean()

if cv > 0.5:
    print("Use Hockey Stick (high variability)")
    use_hockey = True
else:
    print("Fixed concentration OK (low variability)")
    use_hockey = False
```

## Three-Step Migration Path

### Step 1: Start with ECDF Dilution Only (5 minutes)
```python
# Just add one parameter to your existing code
results = processor.run_spatial_assessment(
    # ... your existing parameters ...
    use_ecdf_dilution=True,  # ← Add this line
)
```
**Benefit**: Immediately uses all 100 simulations instead of median.

### Step 2: Calculate Pathogen Parameters (10 minutes)
```python
# One-time calculation
monitoring = pd.read_csv('your_monitoring_file.csv')
p_min = monitoring['Pathogen_Column'].min()
p_median = monitoring['Pathogen_Column'].median()
p_max = monitoring['Pathogen_Column'].max()
print(f"Parameters: min={p_min}, median={p_median}, max={p_max}")
# Save these for future use
```

### Step 3: Add Hockey Stick (2 minutes)
```python
# Add Hockey Stick using calculated parameters
results = processor.run_spatial_assessment(
    # ... your existing parameters ...
    use_ecdf_dilution=True,
    use_hockey_pathogen=True,  # ← Add this
    pathogen_min=p_min,         # ← Add these three
    pathogen_median=p_median,
    pathogen_max=p_max,
)
```

**Total time**: ~20 minutes to fully upgrade your workflow!

## Examples to Run

We've created ready-to-run examples:

1. **`SIMPLE_EXAMPLE.py`** - Start here! Shows the recommended approach
2. **`test_distributions.py`** - Comprehensive comparison of all 4 methods
3. **`demo_ecdf_vs_median.py`** - Visual demonstration of ECDF impact

Run any of these:
```bash
python SIMPLE_EXAMPLE.py           # ← Start here
python test_distributions.py       # More detailed comparison
python demo_ecdf_vs_median.py      # Visual demonstration
```

## Summary: What to Do Now

1. **Run the simple example**: `python SIMPLE_EXAMPLE.py`
2. **Calculate your pathogen parameters** from monitoring data
3. **Use this code** in your workflow:

```python
# This is all you need!
processor = BatchProcessor()
results = processor.run_spatial_assessment(
    dilution_file='your_dilution_file.csv',
    pathogen='your_pathogen',
    use_ecdf_dilution=True,      # ← Always True if you have hydro data
    use_hockey_pathogen=True,     # ← True if CV > 0.5
    pathogen_min=...,             # ← From monitoring data
    pathogen_median=...,
    pathogen_max=...,
    treatment_lrv=3.0,
    iterations=10000
)
```

That's it! Questions? Check `BEST_PRACTICES_GUIDE.md` for more details.
