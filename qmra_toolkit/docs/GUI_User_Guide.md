# QMRA Toolkit - GUI User Guide

## Overview

The QMRA Assessment Toolkit includes a user-friendly graphical interface that makes quantitative microbial risk assessment accessible to users without programming experience. The GUI provides all the functionality of the command-line tool in an intuitive, point-and-click interface.

## Features

- **Easy-to-use tabbed interface** - Organized workflow with separate tabs for assessment, results, and pathogen information
- **Form-based input** - Simple forms for entering assessment parameters
- **Real-time validation** - Input validation with helpful error messages
- **Interactive pathogen database** - Browse and explore pathogen information
- **Automated report generation** - Generate professional Word reports with one click
- **Results visualization** - Clear display of risk assessment results
- **Save/load functionality** - Save results as JSON files for later analysis

## Launching the GUI

### Windows
1. **Double-click method**: Double-click `Launch_QMRA_GUI.bat`
2. **Command-line method**:
   ```bash
   cd qmra_toolkit
   Launch_QMRA_GUI.bat
   ```

### Mac/Linux
```bash
cd qmra_toolkit
python launch_gui.py
```

## User Interface Tour

### Main Window

The GUI consists of three main tabs:

1. **Risk Assessment** - Input parameters and run assessments
2. **Results** - View detailed assessment results
3. **Pathogen Database** - Browse pathogen information

### Risk Assessment Tab

**Input Parameters:**

- **Pathogen**: Select from available pathogens (norovirus, campylobacter, cryptosporidium)
- **Exposure Route**: Choose exposure pathway:
  - Primary Contact (recreational water)
  - Shellfish Consumption
- **Concentration**: Pathogen concentration (organisms per 100mL)
- **Volume/Consumption**:
  - For primary contact: Volume ingested per event (mL)
  - For shellfish: Mass consumed per serving (g)
- **Frequency**: Number of exposure events per year
- **Population Size**: Population for risk scaling calculations
- **Monte Carlo Iterations**: Number of simulation iterations (minimum 1000, recommended 10000)

**Action Buttons:**

- **Run Assessment**: Execute the risk assessment
- **Generate Report**: Create a professional Word report (enabled after assessment)
- **Save Results**: Save results to JSON file (enabled after assessment)

### Results Tab

Displays comprehensive assessment results including:

- **Assessment Parameters**: Summary of input values used
- **Risk Metrics**:
  - Infection Probability
  - Illness Probability
  - Annual Risk
  - DALYs (Disability Adjusted Life Years)
- **Statistical Analysis**: Mean, median, and 95th percentile values
- **Population Risk**: Expected cases per year
- **Regulatory Compliance**: Pass/fail status against standard thresholds

### Pathogen Database Tab

Interactive pathogen information browser:

- **Pathogen Selection**: Dropdown to select pathogen
- **Detailed Information**: Complete pathogen data including:
  - Pathogen type (virus, bacteria, protozoa)
  - Dose-response model parameters
  - Health impact data
  - Valid exposure routes
  - Environmental survival data
  - Typical concentrations in different matrices

## Step-by-Step Assessment Guide

### Basic Assessment Workflow

1. **Launch the GUI**
   - Double-click `Launch_QMRA_GUI.bat` (Windows) or run `python launch_gui.py`

2. **Select Assessment Parameters**
   - Choose your pathogen from the dropdown
   - Select the appropriate exposure route
   - Enter pathogen concentration (e.g., 10.0 org/100mL)
   - Set exposure volume and frequency
   - Specify population size
   - Set Monte Carlo iterations (10,000 recommended)

3. **Run the Assessment**
   - Click "Run Assessment"
   - Progress bar will show assessment is running
   - Results will automatically appear in the Results tab

4. **Review Results**
   - Switch to Results tab to view comprehensive output
   - Check regulatory compliance status
   - Review statistical summaries

5. **Generate Reports** (Optional)
   - Click "Generate Report" to create a Word document
   - Choose save location and filename
   - Professional report will be generated automatically

6. **Save Results** (Optional)
   - Click "Save Results" to export data as JSON
   - Results can be imported for further analysis

### Example: Beach Safety Assessment

Let's assess norovirus risk from swimming at a beach:

1. **Parameters**:
   - Pathogen: norovirus
   - Exposure Route: primary_contact
   - Concentration: 10.0 org/100mL (typical beach water)
   - Volume: 50.0 mL (water ingested per swim)
   - Frequency: 10 events/year (seasonal swimming)
   - Population: 10,000 (local community)

2. **Expected Results**:
   - Single event infection risk: ~16%
   - Annual risk: ~84%
   - Expected cases: ~8,400 per year
   - Regulatory status: FAIL (exceeds acceptable thresholds)

3. **Interpretation**:
   - High risk scenario requiring treatment or advisories
   - Consider source control or public health interventions

## Troubleshooting

### Common Issues

**GUI won't start:**
- Check Python installation (`python --version`)
- Install dependencies (`pip install -r requirements.txt`)
- Check error messages in console

**Assessment fails:**
- Verify all input fields are filled
- Check that numeric values are positive
- Ensure Monte Carlo iterations ≥ 1000

**Report generation fails:**
- Check file permissions in save directory
- Ensure sufficient disk space
- Verify python-docx package is installed

**Slow performance:**
- Reduce Monte Carlo iterations for faster results
- Close other applications to free memory
- Use smaller population sizes for initial testing

### Error Messages

**"Please select a pathogen"**: Choose a pathogen from the dropdown

**"Concentration must be positive"**: Enter a value greater than 0

**"Monte Carlo iterations should be at least 1000"**: Increase iteration count for reliable results

**"Assessment failed"**: Check console for detailed error message

## Advanced Features

### Batch Processing

While the GUI is designed for single assessments, you can:

1. Save results as JSON files
2. Use the command-line tool or Python API for batch processing
3. Import results back into GUI for visualization

### Custom Scenarios

The GUI supports various exposure scenarios:

**Recreational Water**:
- Beach swimming: 10-100 org/100mL, 50mL, 10-20 events/year
- River recreation: 100-1000 org/100mL, 50mL, 5-15 events/year

**Shellfish Consumption**:
- Raw oysters: 1000-10000 org/100g, 150g, 12-24 servings/year
- Cooked shellfish: 10-100 org/100g, 150g, 6-12 servings/year

### Integration with Other Tools

GUI results can be:
- Exported to Excel for further analysis
- Integrated with GIS systems using JSON exports
- Combined with epidemiological data
- Used in risk management decision frameworks

## Best Practices

### Input Validation
- Always use realistic concentration ranges
- Consider seasonal variations in pathogen levels
- Account for population demographics
- Use appropriate exposure frequencies

### Result Interpretation
- Compare results against regulatory thresholds
- Consider uncertainty ranges (95th percentiles)
- Account for population vulnerability
- Document assumptions and limitations

### Quality Assurance
- Run test cases with known results
- Compare GUI outputs with command-line tool
- Review generated reports before submission
- Maintain assessment documentation

## Getting Help

If you need assistance:

1. **Built-in Help**: Hover over controls for tooltips
2. **Documentation**: Review the complete user guide
3. **Examples**: Use the provided example scenarios
4. **Support**: Contact the NIWA QMRA team

## Updates and Maintenance

The GUI automatically uses the latest pathogen database and models. To update:

1. Download the latest toolkit version
2. Replace existing files
3. Re-run `pip install -r requirements.txt`
4. Test with known scenarios

---

*QMRA Assessment Toolkit GUI v1.0*
*© NIWA Earth Sciences New Zealand*
*Strategic Investment Programme 2025-2026*