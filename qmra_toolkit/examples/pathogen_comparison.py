"""
Multi-pathogen Risk Comparison Example
Compare risks from different pathogens under identical exposure conditions
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pathogen_database import PathogenDatabase
from exposure_assessment import create_exposure_assessment, ExposureRoute
from risk_characterization import RiskCharacterization
import numpy as np
import json

# Initialize components
pathogen_db = PathogenDatabase()
risk_calc = RiskCharacterization(pathogen_db)

# Standard exposure scenario
exposure_params = {
    "water_ingestion_volume": 50.0,  # mL per swimming event
    "exposure_frequency": 10         # events per year
}

concentration = 10.0  # organisms per 100mL
population = 100000

print("=" * 80)
print("MULTI-PATHOGEN RISK COMPARISON")
print("Identical Exposure Conditions:")
print(f"  Concentration: {concentration} organisms/100mL")
print(f"  Volume ingested: {exposure_params['water_ingestion_volume']} mL per event")
print(f"  Frequency: {exposure_params['exposure_frequency']} events/year")
print(f"  Population: {population:,}")
print("=" * 80)

pathogens = pathogen_db.get_available_pathogens()
results_summary = []

for pathogen_name in pathogens:
    print(f"\n{pathogen_name.upper()}:")
    print("-" * 40)

    try:
        # Set up exposure assessment
        exposure_model = create_exposure_assessment(ExposureRoute.PRIMARY_CONTACT, exposure_params)
        exposure_model.set_pathogen_concentration(concentration)

        # Run comprehensive assessment
        results = risk_calc.run_comprehensive_assessment(
            pathogen_name=pathogen_name,
            exposure_assessment=exposure_model,
            population_size=population,
            n_samples=5000
        )

        # Extract key metrics
        infection_prob = results['infection_probability'].statistics['mean']
        illness_prob = results['illness_probability'].statistics['mean']
        annual_risk = results['annual_risk'].statistics['mean']
        dalys = results['dalys'].statistics['mean']
        expected_cases = results['annual_risk'].population_risks['expected_cases_per_year']

        # Get model information
        default_model = pathogen_db.get_default_model_type(pathogen_name)
        pathogen_info = pathogen_db.get_pathogen_info(pathogen_name)
        pathogen_type = pathogen_info.get('pathogen_type', 'unknown')

        print(f"  Pathogen Type: {pathogen_type}")
        print(f"  Dose-Response Model: {default_model}")
        print(f"  Single Event Infection Risk: {infection_prob:.2e}")
        print(f"  Single Event Illness Risk: {illness_prob:.2e}")
        print(f"  Annual Risk: {annual_risk:.2e}")
        print(f"  DALYs per person: {dalys:.2e}")
        print(f"  Expected annual cases: {expected_cases:.0f}")

        # Regulatory compliance
        compliant = "PASS" if annual_risk < 1e-3 else "FAIL"
        print(f"  Regulatory Status: {compliant}")

        results_summary.append({
            "pathogen": pathogen_name,
            "pathogen_type": pathogen_type,
            "model_type": default_model,
            "single_event_infection_risk": infection_prob,
            "single_event_illness_risk": illness_prob,
            "annual_risk": annual_risk,
            "dalys_per_person": dalys,
            "expected_annual_cases": expected_cases,
            "regulatory_compliant": compliant == "PASS"
        })

    except Exception as e:
        print(f"  ERROR: {str(e)}")
        continue

# Rank by risk level
results_summary.sort(key=lambda x: x['annual_risk'], reverse=True)

print("\n" + "=" * 100)
print("RISK RANKING (Highest to Lowest Annual Risk)")
print("=" * 100)
print(f"{'Rank':<4} {'Pathogen':<15} {'Type':<10} {'Model':<12} {'Annual Risk':<15} {'Cases/Year':<12} {'Status':<10}")
print("-" * 100)

for i, r in enumerate(results_summary, 1):
    status = "PASS" if r['regulatory_compliant'] else "FAIL"
    print(f"{i:<4} {r['pathogen']:<15} {r['pathogen_type']:<10} {r['model_type']:<12} "
          f"{r['annual_risk']:<15.2e} {r['expected_annual_cases']:<12.0f} {status:<10}")

# Calculate risk ratios
if len(results_summary) > 1:
    baseline = results_summary[-1]['annual_risk']  # Lowest risk as baseline
    print(f"\nRISK RATIOS (relative to {results_summary[-1]['pathogen']}):")
    print("-" * 60)
    for r in results_summary:
        ratio = r['annual_risk'] / baseline
        print(f"  {r['pathogen']:<15}: {ratio:.1f}x higher risk")

# Model comparison
print(f"\nDOSE-RESPONSE MODELS USED:")
print("-" * 40)
for r in results_summary:
    print(f"  {r['pathogen']:<15}: {r['model_type']}")

# Save results
with open('pathogen_comparison_results.json', 'w') as f:
    json.dump(results_summary, f, indent=2, default=str)

print(f"\nResults saved to pathogen_comparison_results.json")
print(f"Comparison complete for {len(results_summary)} pathogens")