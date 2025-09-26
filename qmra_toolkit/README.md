# QMRA Assessment Toolkit

A comprehensive Python-based Quantitative Microbial Risk Assessment toolkit developed by NIWA Earth Sciences New Zealand.

## Overview

This toolkit replaces @Risk Excel functionality with automated, reproducible workflows for regulatory compliance QMRA assessments. It addresses the key issues with @Risk including security conflicts, manual processes, and Excel-based errors.

## Key Features

- 🦠 **Comprehensive Pathogen Database** - Validated dose-response models for key pathogens
- 💧 **Multiple Exposure Routes** - Primary contact, shellfish consumption, drinking water, aerosols
- 🔬 **Dilution Modeling Integration** - NIWA's key differentiator with engineer-provided LRVs
- 📊 **Monte Carlo Simulation** - Advanced uncertainty analysis replacing @Risk
- 📋 **Automated Reporting** - Generate regulatory compliance reports in Word format
- ⚡ **Command-Line Interface** - Easy-to-use CLI for common workflows
- 🖥️ **Graphical User Interface** - User-friendly GUI for non-technical users
- 🧪 **Comprehensive Testing** - Extensive test suite with validation benchmarks

## Quick Start

### Installation

```bash
# Clone or download the toolkit
cd qmra_toolkit

# Install dependencies
pip install -r requirements.txt

# Verify installation
python tests/run_all_tests.py
```

### GUI Applications

Two graphical interfaces available:

#### **🎨 Enhanced Professional GUI** (Recommended)
Modern, professional interface with advanced features:

**Windows:**
```bash
# Double-click Launch_Enhanced_QMRA_GUI.bat or run:
Launch_Enhanced_QMRA_GUI.bat
```

**Cross-platform:**
```bash
python launch_enhanced_gui.py
```

**Features:**
- 8 specialized tabs (Project Setup, Assessment, Scenarios, Results, Plots, Reports, Database, Settings)
- Interactive matplotlib plotting and visualizations
- Professional report generation (PDF/Word formats)
- Multi-pathogen assessment capabilities
- Treatment scenario comparison tools
- NIWA professional styling and branding

#### **📋 Basic GUI** (Legacy)
Simple interface for basic assessments:

**Windows:**
```bash
Launch_QMRA_GUI.bat
```

**Cross-platform:**
```bash
python launch_gui.py
```

### Command-Line Usage

Run a complete QMRA assessment:

```bash
python src/qmra_toolkit.py assess \
  --pathogen norovirus \
  --exposure-route primary_contact \
  --concentration 10.0 \
  --volume 50.0 \
  --frequency 10 \
  --population 10000 \
  --report
```

### Example Output

```
QMRA Assessment Results: Norovirus
============================================================

Infection Probability:
  Mean: 2.45e-03
  Median: 1.89e-03
  95th Percentile: 8.12e-03

Annual Risk:
  Mean: 2.38e-02
  Median: 1.85e-02
  95th Percentile: 7.84e-02
  Expected cases per year: 238.0

Regulatory Compliance:
  acceptable_annual_risk: FAIL
  recreational_water_risk: PASS
```

## Architecture

The toolkit consists of modular components:

```
qmra_toolkit/
├── src/
│   ├── pathogen_database.py      # Pathogen data management
│   ├── dose_response.py          # Dose-response models
│   ├── exposure_assessment.py    # Exposure route modeling
│   ├── dilution_model.py         # Treatment & dilution (NIWA differentiator)
│   ├── monte_carlo.py           # Uncertainty analysis
│   ├── risk_characterization.py # Risk calculation engine
│   ├── report_generator.py      # Automated report generation
│   └── qmra_toolkit.py          # Main CLI application
├── config/
│   └── config.yaml              # Configuration settings
├── data/
│   └── pathogen_parameters.json # Pathogen database
├── tests/
│   └── test_*.py                # Comprehensive test suite
├── docs/
│   └── user_guide.md            # Detailed user guide
└── requirements.txt             # Python dependencies
```

## Supported Pathogens

- **Norovirus** - Beta-Poisson model (Teunis et al. 2008)
- **Campylobacter jejuni** - Beta-Poisson model (Teunis et al. 2005)
- **Cryptosporidium parvum** - Exponential model (Haas et al. 1996)

## Exposure Routes

### Primary Contact (Recreational Water)
- Swimming, surfing, water sports
- Inadvertent water ingestion
- Default: 50 mL per event, 10 events/year

### Shellfish Consumption
- Oysters, mussels, clams
- Bioaccumulation modeling
- Default: 150g per serving, 12 servings/year

### Drinking Water
- Treated and untreated water
- Daily consumption modeling
- Default: 2L per day

## NIWA's Key Differentiator: Dilution Modeling

The toolkit integrates NIWA's specialized dilution modeling capabilities:

- **Engineer-provided Log Reduction Values (LRVs)**
- **Multi-barrier treatment trains**
- **Far-field dilution calculations**
- **Natural die-off processes**
- **Uncertainty quantification in treatment efficacy**

```python
# Example: Wastewater treatment train
from dilution_model import DilutionModel, TreatmentBarrier

model = DilutionModel()
model.add_treatment_barrier(TreatmentBarrier(
    name="UV Disinfection",
    treatment_type=TreatmentType.UV,
    log_reduction_value=3.0,
    variability=0.2
))

# Apply 3-log reduction with uncertainty
results = model.apply_complete_scenario(initial_concentration=1e6)
```

## Command-Line Interface

### Main Commands

```bash
# Complete risk assessment
qmra-toolkit assess [options]

# Dose-response analysis
qmra-toolkit dose-response [options]

# Treatment modeling
qmra-toolkit treatment [options]

# List available pathogens
qmra-toolkit list-pathogens

# Get pathogen information
qmra-toolkit pathogen-info --pathogen norovirus

# Run example
qmra-toolkit example
```

### Options

- `--pathogen` - Pathogen name
- `--exposure-route` - Exposure pathway
- `--concentration` - Pathogen concentration
- `--volume` - Exposure volume
- `--frequency` - Exposure frequency
- `--population` - Population size
- `--iterations` - Monte Carlo iterations
- `--output` - Results output file
- `--report` - Generate Word report

## Python API

For advanced users, the toolkit provides a comprehensive Python API:

```python
from pathogen_database import PathogenDatabase
from exposure_assessment import create_exposure_assessment, ExposureRoute
from risk_characterization import RiskCharacterization

# Initialize components
pathogen_db = PathogenDatabase()
risk_calc = RiskCharacterization(pathogen_db)

# Configure exposure
exposure_model = create_exposure_assessment(
    ExposureRoute.PRIMARY_CONTACT,
    {"water_ingestion_volume": 50.0, "exposure_frequency": 10}
)
exposure_model.set_pathogen_concentration(10.0)

# Run assessment
results = risk_calc.run_comprehensive_assessment(
    pathogen_name="norovirus",
    exposure_assessment=exposure_model,
    population_size=10000
)
```

## Monte Carlo Simulation

Advanced uncertainty analysis with native Python implementation:

- **10+ probability distributions** (Normal, Lognormal, Triangular, etc.)
- **Parameter uncertainty quantification**
- **Sensitivity analysis**
- **Convergence diagnostics**
- **Export capabilities**

```python
from monte_carlo import MonteCarloSimulator, create_lognormal_distribution

mc_sim = MonteCarloSimulator(random_seed=42)
mc_sim.add_distribution("concentration", create_lognormal_distribution(2.0, 1.0))

results = mc_sim.run_simulation(model_function, n_iterations=10000)
```

## Automated Reporting

Generate comprehensive regulatory compliance reports:

- **Executive summary with key findings**
- **Detailed methodology section**
- **Risk assessment results tables**
- **Uncertainty analysis plots**
- **Regulatory compliance evaluation**
- **Professional Word format output**

## Testing and Validation

Comprehensive test suite ensures reliability:

```bash
# Run all tests
python tests/run_all_tests.py

# Run specific test modules
python -m unittest tests.test_pathogen_database
python -m unittest tests.test_dose_response
python -m unittest tests.test_integration
```

### Test Coverage

- ✅ Unit tests for all modules
- ✅ Integration tests for complete workflows
- ✅ Validation against literature benchmarks
- ✅ Error handling and edge cases
- ✅ Performance benchmarking

## Benefits Over @Risk

| Feature | @Risk | QMRA Toolkit |
|---------|-------|--------------|
| **Platform** | Excel-dependent | Native Python |
| **Security** | Firewall conflicts | No external dependencies |
| **Automation** | Manual processes | Fully automated |
| **Reproducibility** | Limited | Complete version control |
| **Extensibility** | Closed system | Open, modular architecture |
| **Cost** | Commercial license | Open source |
| **Integration** | Limited | NIWA dilution modeling |
| **Reporting** | Manual assembly | Automated generation |

## Project Background

This toolkit was developed as part of NIWA's Strategic Investment Programme to:

- Replace problematic @Risk Excel dependency
- Reduce project delivery time by 60-70%
- Eliminate manual, error-prone processes
- Integrate NIWA's dilution modeling expertise
- Build internal technical capabilities
- Support regulatory compliance market expansion

## Development Team

- **Reza Moghaddam** - Lead Developer (150 hours)
- **David Wood** - Model Review & Support (40 hours)
- **Andrew Hughes** - Project Manager

## Documentation

- [User Guide](docs/user_guide.md) - Comprehensive usage documentation
- [API Documentation](src/) - Detailed module documentation
- [Test Results](tests/) - Validation and benchmarking

## Support

For technical support, feature requests, or bug reports, contact the NIWA QMRA team.

## License

© NIWA Earth Sciences New Zealand

---

*Developed by NIWA Earth Sciences New Zealand*
*Strategic Investment Programme 2025-2026*

**Ready to replace @Risk with modern, automated QMRA workflows.**