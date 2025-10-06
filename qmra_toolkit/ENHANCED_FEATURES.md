# Enhanced QMRA Toolkit - Features Ported from Charlotte's R Package

## Overview
This enhanced version of the QMRA toolkit has been developed by adapting Charlotte Jones-Todd's comprehensive R QMRA package from NIWA. The toolkit now matches professional NIWA QMRA report standards and includes advanced features previously only available in the R implementation.

## New Modules Added

### 1. `dose_response_advanced.py`
**Comprehensive dose-response models ported from R package:**
- **11 different models implemented:**
  - Exponential
  - Fractional Poisson (Messner et al 2014)
  - Beta-Poisson (exact and approximation)
  - Simple Threshold
  - Log-logistic
  - Log-probit
  - Weibull
  - Simple Binomial
  - Beta-binomial
  - Overdispersed exponential
  - Gauss hypergeometric

**Key features:**
- Model selection framework
- N50/ID50 calculation
- Multi-model comparison capability
- Validated against R package outputs

### 2. `monte_carlo_advanced.py`
**Advanced Monte Carlo simulation framework:**
- **Distribution samplers:**
  - Triangular, Uniform, Lognormal, Normal, Gamma, Beta
  - Empirical cumulative distribution (for hydrodynamic data)

- **QMRA-specific simulators:**
  - `ConcentrationQMRA`: Microbe concentration at exposure site
  - `IngestedQMRA`: Volume ingested calculations
  - `MonteCarloQMRA`: Full Monte Carlo QMRA simulation

- **Hydrodynamic dilution processing:**
  - Convert concentration to dilution factors
  - Empirical CDF generation
  - Distribution preparation for Monte Carlo

### 3. `pathogen_database_advanced.py`
**Comprehensive pathogen database from literature:**
- **14 pathogen groups with multiple parameterizations:**
  - Bacteria: Campylobacter, E. coli, Salmonella, Shigella, Vibrio, Legionella, Listeria
  - Parasites: Cryptosporidium, Giardia
  - Viruses: Norovirus, Rotavirus, Adenovirus, Enterovirus, Hepatitis A

- **For each pathogen:**
  - Multiple model parameterizations
  - Literature sources
  - Host and route specifications
  - N50/ID50 values where available

- **Additional data:**
  - Bioaccumulation factors for shellfish
  - Morbidity ratios (infection to illness)

### 4. `qmra_integration.py`
**High-level integration module matching NIWA standards:**
- `QMRAAssessment`: Main assessment class
- `QMRAScenario`: Scenario configuration
- `QMRAResults`: Results container with statistics
- Multi-site assessment capability
- Treatment scenario comparison
- Annual risk calculations

## Comparison with Original Python Toolkit

| Feature | Original Toolkit | Enhanced Toolkit (from R) |
|---------|-----------------|---------------------------|
| Dose-response models | 2 (Beta-Poisson, Exponential) | 11 comprehensive models |
| Monte Carlo | Basic | Advanced with multiple distributions |
| Pathogen database | 5 pathogens | 14+ pathogens with literature params |
| Dilution modeling | Basic | Hydrodynamic with empirical CDF |
| Assessment standards | Basic | NIWA professional standards |
| Validation | Limited | Extensive test coverage |

## Key Improvements from Charlotte's R Package

1. **Scientific Rigor:**
   - More accurate dose-response models
   - Literature-validated parameters
   - Proper uncertainty propagation

2. **Professional Standards:**
   - Matches NIWA report format
   - Comprehensive risk metrics
   - Multi-scenario comparison

3. **Flexibility:**
   - Multiple distribution types
   - Custom exposure scenarios
   - Site-specific assessments

4. **Validation:**
   - 40+ new tests added
   - Validated against R outputs
   - Comprehensive error handling

## Usage Example

```python
from src import QMRAAssessment, QMRAScenario, PathogenDatabase

# Initialize
qmra = QMRAAssessment()
pathogen_db = PathogenDatabase()

# Create scenario
scenario = QMRAScenario(
    name="WWTP Assessment",
    pathogen='norovirus',
    exposure_route='swimming',
    treatment_efficacy={'min': 2, 'max': 3},  # log reduction
    influent_concentration={
        'distribution': 'lognormal',
        'params': {'meanlog': 5, 'sdlog': 1}
    },
    events_per_year=20
)

# Run assessment
results = qmra.run_assessment(scenario, nsim=10000)

# Access results
print(f"Median illness risk: {results.risk_percentiles['illness_median']:.2e}")
print(f"Annual illness risk: {results.risk_percentiles['annual_illness_median']:.2e}")
```

## Testing
All new modules have comprehensive test coverage:
- `test_dose_response_advanced.py`: 10 tests
- `test_monte_carlo_advanced.py`: 14 tests
- `test_pathogen_database_advanced.py`: 16 tests

Run tests with:
```bash
python -m unittest discover tests -p "test_*_advanced.py"
```

## References
- Jones-Todd, C. (2018). QMRA R Package. NIWA. https://git.niwa.local/jonestoddcm/qmra
- Messner, M. J., Berger, P., & Nappier, S. P. (2014). Fractional Poisson—a simple dose‐response model for human norovirus. Risk Analysis, 34(10), 1820-1829.
- Haas, C. N., Rose, J. B., & Gerba, C. P. (2014). Quantitative microbial risk assessment. John Wiley & Sons.
- NIWA (2023). Quantitative Microbial Risk Assessment Reports. New Zealand.

## Future Enhancements
- R-Python interoperability layer (planned)
- GUI interface matching R Shiny apps
- Additional pathogens as literature expands
- Machine learning for parameter estimation

## Credits
- Original R package: Charlotte Jones-Todd (NIWA)
- Python adaptation: QMRA Toolkit Team
- Literature parameters: Various sources cited in pathogen database