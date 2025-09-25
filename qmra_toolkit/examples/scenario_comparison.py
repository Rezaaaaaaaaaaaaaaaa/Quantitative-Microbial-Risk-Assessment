"""
Scenario Comparison Example
Compare multiple treatment and exposure scenarios
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pathogen_database import PathogenDatabase
from exposure_assessment import create_exposure_assessment, ExposureRoute
from dilution_model import DilutionModel, TreatmentBarrier, TreatmentType
from risk_characterization import RiskCharacterization
import json

# Initialize components
pathogen_db = PathogenDatabase()
risk_calc = RiskCharacterization(pathogen_db)

# Define scenarios to compare
scenarios = [
    {
        "name": "No Treatment",
        "pathogen": "norovirus",
        "initial_concentration": 1000.0,  # organisms/100mL
        "treatment_lrv": 0.0,
        "exposure_volume": 50.0,  # mL
        "exposure_frequency": 10,  # times/year
        "population": 10000
    },
    {
        "name": "Basic Treatment (2-log)",
        "pathogen": "norovirus",
        "initial_concentration": 1000.0,
        "treatment_lrv": 2.0,
        "exposure_volume": 50.0,
        "exposure_frequency": 10,
        "population": 10000
    },
    {
        "name": "Advanced Treatment (4-log)",
        "pathogen": "norovirus",
        "initial_concentration": 1000.0,
        "treatment_lrv": 4.0,
        "exposure_volume": 50.0,
        "exposure_frequency": 10,
        "population": 10000
    },
    {
        "name": "Best Practice (6-log)",
        "pathogen": "norovirus",
        "initial_concentration": 1000.0,
        "treatment_lrv": 6.0,
        "exposure_volume": 50.0,
        "exposure_frequency": 10,
        "population": 10000
    }
]

print("=" * 80)
print("SCENARIO COMPARISON: Treatment Effectiveness")
print("=" * 80)

results_summary = []

for scenario in scenarios:
    print(f"\n{scenario['name']}:")
    print("-" * 40)

    # Apply treatment
    dilution_model = DilutionModel()
    if scenario['treatment_lrv'] > 0:
        dilution_model.add_treatment_barrier(TreatmentBarrier(
            name=f"{scenario['treatment_lrv']}-log treatment",
            treatment_type=TreatmentType.UV,
            log_reduction_value=scenario['treatment_lrv'],
            variability=0.2
        ))

    # Calculate treated concentration
    treated_conc = scenario['initial_concentration'] * (10 ** -scenario['treatment_lrv'])

    # Set up exposure
    exposure_model = create_exposure_assessment(
        ExposureRoute.PRIMARY_CONTACT,
        {
            "water_ingestion_volume": scenario['exposure_volume'],
            "exposure_frequency": scenario['exposure_frequency']
        }
    )
    exposure_model.set_pathogen_concentration(treated_conc)

    # Run risk assessment
    results = risk_calc.run_comprehensive_assessment(
        pathogen_name=scenario['pathogen'],
        exposure_assessment=exposure_model,
        population_size=scenario['population'],
        n_samples=1000
    )

    # Extract key metrics
    annual_risk = results['annual_risk'].statistics['mean']
    expected_cases = results['annual_risk'].population_risks['expected_cases_per_year']

    # Check compliance
    compliant = "PASS" if annual_risk < 1e-3 else "FAIL"

    print(f"  Initial concentration: {scenario['initial_concentration']:.1f} org/100mL")
    print(f"  Treatment LRV: {scenario['treatment_lrv']:.1f} log")
    print(f"  Final concentration: {treated_conc:.2e} org/100mL")
    print(f"  Annual risk: {annual_risk:.2e}")
    print(f"  Expected cases/year: {expected_cases:.1f}")
    print(f"  Regulatory compliance (1e-3): {compliant}")

    results_summary.append({
        "scenario": scenario['name'],
        "treatment_lrv": scenario['treatment_lrv'],
        "annual_risk": annual_risk,
        "expected_cases": expected_cases,
        "compliant": compliant
    })

# Summary table
print("\n" + "=" * 80)
print("SUMMARY TABLE")
print("=" * 80)
print(f"{'Scenario':<25} {'LRV':<8} {'Annual Risk':<15} {'Cases/Year':<12} {'Status':<10}")
print("-" * 80)
for r in results_summary:
    print(f"{r['scenario']:<25} {r['treatment_lrv']:<8.1f} {r['annual_risk']:<15.2e} {r['expected_cases']:<12.1f} {r['compliant']:<10}")

# Save results
with open('scenario_comparison_results.json', 'w') as f:
    json.dump(results_summary, f, indent=2, default=str)
print("\nResults saved to scenario_comparison_results.json")