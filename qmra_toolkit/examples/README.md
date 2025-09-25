# QMRA Toolkit Examples

This directory contains example scripts demonstrating advanced usage of the QMRA Assessment Toolkit.

## Available Examples

### 1. Multi-Pathogen Risk Comparison (`pathogen_comparison.py`)
Compares risk levels across different pathogens under identical exposure conditions.

**Usage:**
```bash
python pathogen_comparison.py
```

**What it demonstrates:**
- Automatic model selection for different pathogens
- Risk ranking and comparative analysis  
- Population-level risk calculations
- Regulatory compliance assessment across pathogens

### 2. Treatment Scenario Comparison (`scenario_comparison.py`)
Evaluates the effectiveness of different treatment levels on risk reduction.

**Usage:**
```bash
python scenario_comparison.py
```

**What it demonstrates:**
- Treatment barrier modeling with log reduction values
- Risk reduction analysis across treatment scenarios
- Cost-benefit evaluation of treatment investments

## Running Examples

1. **Navigate to the examples directory:**
   ```bash
   cd qmra_toolkit/examples
   ```

2. **Run any example script:**
   ```bash
   python pathogen_comparison.py
   python scenario_comparison.py
   ```

## Customizing Examples

All examples use the same basic pattern:

1. **Import required modules**
2. **Configure exposure parameters**  
3. **Run assessments with different scenarios**
4. **Compare and analyze results**
5. **Export results to JSON for further analysis**

You can modify the exposure parameters, pathogen concentrations, or add additional scenarios to suit your specific analysis needs.

## Integration with Main Toolkit

These examples demonstrate the Python API usage. For command-line usage, see the main toolkit documentation:

```bash
python ../src/qmra_toolkit.py --help
```