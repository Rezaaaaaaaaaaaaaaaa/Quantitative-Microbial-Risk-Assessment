"""
New Zealand Treatment Scenarios Comparison
Auckland Council Wastewater Treatment Upgrade Assessment
NIWA Earth Sciences Consultancy - September 2025

Compares current vs proposed treatment scenarios for regulatory compliance.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'qmra_toolkit', 'src'))

from pathogen_database import PathogenDatabase
from exposure_assessment import create_exposure_assessment, ExposureRoute
from dilution_model import DilutionModel, TreatmentBarrier, TreatmentType
from risk_characterization import RiskCharacterization
import json

# Initialize components
pathogen_db = PathogenDatabase()
risk_calc = RiskCharacterization(pathogen_db)

# New Zealand Mangere WWTP scenarios - comparing current vs proposed treatment
scenarios = [
    {
        "name": "Current Secondary Treatment",
        "description": "Activated sludge + clarification (existing)",
        "pathogen": "norovirus",
        "raw_concentration": 1000000,  # copies/L raw wastewater
        "treatment_lrv": 1.0,          # Secondary treatment LRV
        "dilution_factor": 100,        # Manukau Harbour dilution
        "exposure_volume": 50.0,       # mL per swimming event
        "exposure_frequency": 15,      # events/year (Auckland summer)
        "population": 500000
    },
    {
        "name": "Proposed Tertiary Treatment",
        "description": "Secondary + sand filtration + UV disinfection",
        "pathogen": "norovirus",
        "raw_concentration": 1000000,
        "treatment_lrv": 3.5,          # Tertiary + UV LRV
        "dilution_factor": 100,
        "exposure_volume": 50.0,
        "exposure_frequency": 15,
        "population": 500000
    },
    {
        "name": "Current Secondary - Campylobacter",
        "description": "Activated sludge + clarification (bacterial pathogen)",
        "pathogen": "campylobacter",
        "raw_concentration": 100000,   # CFU/L raw wastewater
        "treatment_lrv": 2.0,
        "dilution_factor": 100,
        "exposure_volume": 50.0,
        "exposure_frequency": 15,
        "population": 500000
    },
    {
        "name": "Proposed Tertiary - Campylobacter",
        "description": "Secondary + sand filtration + UV disinfection (bacterial)",
        "pathogen": "campylobacter",
        "raw_concentration": 100000,
        "treatment_lrv": 4.0,
        "dilution_factor": 100,
        "exposure_volume": 50.0,
        "exposure_frequency": 15,
        "population": 500000
    }
]

print("=" * 90)
print("NEW ZEALAND WASTEWATER TREATMENT SCENARIOS COMPARISON")
print("Auckland Council - Mangere WWTP Treatment Upgrade Assessment")
print("NIWA Earth Sciences Consultancy - September 2025")
print("=" * 90)

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

    # Calculate treated concentration after treatment and dilution
    raw_conc_per_100ml = scenario['raw_concentration'] / 10  # Convert L to 100mL
    treated_conc_per_100ml = raw_conc_per_100ml * (10 ** -scenario['treatment_lrv'])
    final_conc = treated_conc_per_100ml / scenario['dilution_factor']

    # Set up exposure
    exposure_model = create_exposure_assessment(
        ExposureRoute.PRIMARY_CONTACT,
        {
            "water_ingestion_volume": scenario['exposure_volume'],
            "exposure_frequency": scenario['exposure_frequency']
        }
    )
    exposure_model.set_pathogen_concentration(final_conc)

    print(f"  Description: {scenario['description']}")
    print(f"  Raw concentration: {scenario['raw_concentration']:.1e} org/L")
    print(f"  Treatment LRV: {scenario['treatment_lrv']} log")
    print(f"  Harbour dilution: {scenario['dilution_factor']}x")
    print(f"  Final concentration: {final_conc:.2e} org/100mL")

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

    # NZ regulatory compliance
    nz_annual_guideline = 1e-6
    compliant_annual = "PASS" if annual_risk <= nz_annual_guideline else "FAIL"
    compliant_recreational = "PASS" if annual_risk <= 1e-3 else "FAIL"

    print(f"  Annual risk: {annual_risk:.2e}")
    print(f"  Expected cases/year: {expected_cases:.1f}")
    print(f"  NZ Annual Guideline (1e-6): {compliant_annual}")
    print(f"  NZ Recreational Guideline (1e-3): {compliant_recreational}")

    results_summary.append({
        "scenario": scenario['name'],
        "description": scenario['description'],
        "pathogen": scenario['pathogen'],
        "treatment_lrv": scenario['treatment_lrv'],
        "final_concentration": final_conc,
        "annual_risk": annual_risk,
        "expected_cases": expected_cases,
        "nz_annual_compliant": compliant_annual == "PASS",
        "nz_recreational_compliant": compliant_recreational == "PASS"
    })

# Summary table
print("\n" + "=" * 100)
print("TREATMENT SCENARIOS SUMMARY")
print("=" * 100)
print(f"{'Scenario':<30} {'Pathogen':<15} {'LRV':<8} {'Annual Risk':<15} {'Cases/Year':<12} {'NZ Compliance':<15}")
print("-" * 100)
for r in results_summary:
    compliance_status = "ANNUAL" if r['nz_annual_compliant'] else ("RECREATIONAL" if r['nz_recreational_compliant'] else "FAIL")
    print(f"{r['scenario']:<30} {r['pathogen']:<15} {r['treatment_lrv']:<8.1f} {r['annual_risk']:<15.2e} {r['expected_cases']:<12.1f} {compliance_status:<15}")

# Calculate risk reduction benefits
print("\n" + "=" * 90)
print("TREATMENT UPGRADE BENEFITS")
print("=" * 90)
norovirus_current = next((r for r in results_summary if 'Current' in r['scenario'] and r['pathogen'] == 'norovirus'), None)
norovirus_proposed = next((r for r in results_summary if 'Proposed' in r['scenario'] and r['pathogen'] == 'norovirus'), None)

if norovirus_current and norovirus_proposed:
    risk_reduction = (norovirus_current['annual_risk'] - norovirus_proposed['annual_risk']) / norovirus_current['annual_risk'] * 100
    cases_prevented = norovirus_current['expected_cases'] - norovirus_proposed['expected_cases']
    log_reduction = scenario['treatment_lrv'] - 1.0  # Tertiary vs Secondary LRV difference

    print(f"Norovirus Risk Reduction: {risk_reduction:.1f}%")
    print(f"Cases Prevented Annually: {cases_prevented:.0f}")
    print(f"Additional Log Reduction: {log_reduction:.1f}")

# Save results
output_file = 'nz_treatment_scenarios_results.json'
with open(output_file, 'w') as f:
    json.dump(results_summary, f, indent=2, default=str)
print(f"\nResults saved to {output_file}")
print(f"New Zealand treatment scenarios assessment complete for {len(results_summary)} scenarios")