# QMRA Toolkit Project Structure

## Directory Layout

```
qmra_toolkit/
│
├── src/                           # Source code modules
│   ├── __init__.py               # Package initialization (v2.0)
│   │
│   ├── Core Modules (Original)
│   ├── dose_response.py          # Basic dose-response models
│   ├── exposure_assessment.py    # Exposure calculations
│   ├── monte_carlo.py           # Basic Monte Carlo simulation
│   ├── pathogen_database.py     # Original pathogen data
│   ├── risk_characterization.py # Risk calculations
│   ├── dilution_model.py        # Dilution calculations
│   ├── report_generator.py      # Report generation
│   │
│   ├── Enhanced Modules (v2.0 - from R package)
│   ├── dose_response_advanced.py     # 11 comprehensive DR models
│   ├── monte_carlo_advanced.py       # Advanced MC framework
│   ├── pathogen_database_advanced.py # Extended pathogen database
│   ├── qmra_integration.py          # High-level integration
│   │
│   ├── Utilities
│   ├── validation.py             # Input validation
│   ├── error_handling.py        # Error management
│   │
│   ├── User Interfaces
│   ├── qmra_toolkit.py          # CLI interface
│   ├── qmra_gui.py              # Basic GUI
│   └── enhanced_qmra_gui.py     # Enhanced GUI
│
├── tests/                        # Test suite
│   ├── Core Tests
│   ├── test_dose_response.py
│   ├── test_exposure_assessment.py
│   ├── test_monte_carlo.py
│   ├── test_pathogen_database.py
│   ├── test_risk_characterization.py
│   ├── test_dilution_model.py
│   ├── test_report_generator.py
│   │
│   ├── Enhanced Tests (v2.0)
│   ├── test_dose_response_advanced.py
│   ├── test_monte_carlo_advanced.py
│   ├── test_pathogen_database_advanced.py
│   │
│   ├── Utility Tests
│   ├── test_validation.py
│   ├── test_error_handling.py
│   │
│   └── run_all_tests.py         # Test runner
│
├── data/                         # Data files
│   ├── pathogens.json           # Pathogen parameters
│   ├── treatment_efficacy.json  # Treatment data
│   └── exposure_parameters.json # Exposure scenarios
│
├── config/                       # Configuration files
│   ├── default_config.yaml      # Default settings
│   └── logging_config.yaml      # Logging configuration
│
├── examples/                     # Example scripts
│   ├── simple_assessment.py     # Basic example
│   └── niwa_qmra_example.py    # Professional NIWA standard example
│
├── docs/                         # Documentation
│   ├── API_Documentation.md     # API reference
│   ├── example reports/          # Sample NIWA reports
│   └── images/                   # Documentation images
│
├── templates/                    # Report templates
│   └── qmra_report_template.docx
│
├── Launch Scripts
├── launch_gui.py                # Basic GUI launcher
├── launch_enhanced_gui.py       # Enhanced GUI launcher
├── Launch_QMRA_GUI.bat         # Windows batch file
├── Launch_Enhanced_QMRA_GUI.bat # Windows batch file (enhanced)
│
├── Configuration Files
├── treatment_config.yaml        # Treatment configurations
├── wastewater_treatment.yaml    # Wastewater scenarios
│
├── Documentation
├── README.md                    # Main documentation
├── PROJECT_STRUCTURE.md        # This file
├── ENHANCED_FEATURES.md        # v2.0 features documentation
│
└── requirements.txt             # Python dependencies
```

## Module Dependencies

### Core Workflow
1. **Input** → `validation.py` → `error_handling.py`
2. **Pathogen Data** → `pathogen_database_advanced.py`
3. **Exposure** → `exposure_assessment.py` + `dilution_model.py`
4. **Dose-Response** → `dose_response_advanced.py`
5. **Monte Carlo** → `monte_carlo_advanced.py`
6. **Risk** → `risk_characterization.py`
7. **Integration** → `qmra_integration.py`
8. **Output** → `report_generator.py`

### Enhanced Features (v2.0)
- **Advanced Models**: 11 dose-response models vs. 2 original
- **Extended Database**: 14+ pathogens vs. 5 original
- **Professional Standards**: NIWA report-quality outputs
- **Multi-site Support**: Compare risks across locations
- **Treatment Scenarios**: Comprehensive treatment evaluation

## Key Files by Function

### Assessment Execution
- `src/qmra_integration.py` - Main assessment orchestrator
- `src/qmra_toolkit.py` - CLI interface
- `examples/niwa_qmra_example.py` - Professional example

### Data & Configuration
- `data/pathogens.json` - Pathogen parameters
- `config/default_config.yaml` - System settings
- `treatment_config.yaml` - Treatment scenarios

### Testing
- `tests/run_all_tests.py` - Run all tests
- `tests/test_*_advanced.py` - Enhanced module tests

### Documentation
- `README.md` - Getting started
- `ENHANCED_FEATURES.md` - v2.0 features
- `docs/API_Documentation.md` - API reference

## Usage Patterns

### Basic Assessment (CLI)
```bash
python src/qmra_toolkit.py assess --pathogen norovirus --treatment secondary
```

### Enhanced Assessment (Python)
```python
from src import QMRAAssessment, QMRAScenario
qmra = QMRAAssessment()
results = qmra.run_assessment(scenario, nsim=10000)
```

### GUI Interface
```bash
python launch_enhanced_gui.py
```

## Version History
- **v1.0**: Original toolkit with basic QMRA functionality
- **v2.0**: Enhanced with Charlotte Jones-Todd's R package features
  - 11 dose-response models
  - Advanced Monte Carlo
  - Extended pathogen database
  - Professional NIWA standards