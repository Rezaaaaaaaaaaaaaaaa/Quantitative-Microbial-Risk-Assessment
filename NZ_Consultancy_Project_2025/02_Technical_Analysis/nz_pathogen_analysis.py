"""
New Zealand Consultancy Project - Pathogen Risk Analysis
Auckland Council Wastewater Treatment Assessment
NIWA Earth Sciences, September 2025

Multi-pathogen risk comparison for Manukau Harbour exposure scenarios.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'qmra_toolkit', 'src'))

from pathogen_database import PathogenDatabase
from exposure_assessment import create_exposure_assessment, ExposureRoute
from risk_characterization import RiskCharacterization
import numpy as np
import json

# Initialize components
pathogen_db = PathogenDatabase()
risk_calc = RiskCharacterization(pathogen_db)

# New Zealand Manukau Harbour exposure scenario (post-tertiary treatment)
exposure_params = {
    "water_ingestion_volume": 50.0,  # mL per swimming event
    "exposure_frequency": 15         # events per year (Auckland summer)
}

# Treated wastewater concentrations after tertiary treatment + UV + dilution
treated_concentrations = {
    'norovirus': 10.0,      # organisms per 100mL (after 3.5 LRV + 100x dilution)
    'campylobacter': 1.0,   # organisms per 100mL (after 4.0 LRV + 100x dilution)
    'cryptosporidium': 0.1  # organisms per 100mL (after 3.0 LRV + 100x dilution)
}

population = 500000  # Greater Auckland recreation population

print("=" * 90)
print("NEW ZEALAND WASTEWATER TREATMENT QMRA - PATHOGEN RISK ANALYSIS")
print("Auckland Council - Mangere WWTP Tertiary Treatment Assessment")
print("NIWA Earth Sciences Consultancy Project - September 2025")
print("=" * 90)
print("EXPOSURE SCENARIO: Manukau Harbour Primary Contact Recreation")
print(f"  Volume ingested: {exposure_params['water_ingestion_volume']} mL per event")
print(f"  Frequency: {exposure_params['exposure_frequency']} events/year")
print(f"  Population at risk: {population:,}")
print("  Treatment: Secondary + Tertiary + UV Disinfection + Harbour Dilution")
print("=" * 90)

pathogens = pathogen_db.get_available_pathogens()
results_summary = []

for pathogen_name in pathogens:
    print(f"\n{pathogen_name.upper()}:")
    print("-" * 40)

    # Use pathogen-specific treated concentration
    concentration = treated_concentrations.get(pathogen_name, 1.0)
    print(f"  Post-treatment concentration: {concentration} organisms/100mL")

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

        # NZ regulatory compliance
        nz_annual_guideline = 1e-6
        nz_recreational_guideline = 1e-3

        compliant_annual = "PASS" if annual_risk <= nz_annual_guideline else "FAIL"
        compliant_event = "PASS" if infection_prob <= nz_recreational_guideline else "FAIL"

        print(f"  NZ Annual Guideline (1e-6): {compliant_annual}")
        print(f"  NZ Event Guideline (1e-3): {compliant_event}")

        results_summary.append({
            "pathogen": pathogen_name,
            "pathogen_type": pathogen_type,
            "model_type": default_model,
            "concentration": concentration,
            "single_event_infection_risk": infection_prob,
            "single_event_illness_risk": illness_prob,
            "annual_risk": annual_risk,
            "dalys_per_person": dalys,
            "expected_annual_cases": expected_cases,
            "nz_annual_compliant": compliant_annual == "PASS",
            "nz_event_compliant": compliant_event == "PASS"
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
    status = "PASS" if r['nz_annual_compliant'] else "FAIL"
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
output_file = 'nz_pathogen_analysis_results.json'
with open(output_file, 'w') as f:
    json.dump(results_summary, f, indent=2, default=str)

print(f"\n" + "=" * 90)
print("NEW ZEALAND CONSULTANCY PROJECT SUMMARY")
print("=" * 90)
print(f"Assessment: Mangere WWTP Tertiary Treatment - Pathogen Risk Analysis")
print(f"Population at Risk: {population:,}")
print(f"Results saved to: {output_file}")
print(f"Analysis complete for {len(results_summary)} pathogens")

# Calculate total risk and cases
total_annual_risk = sum(p['annual_risk'] for p in results_summary)
total_cases = sum(p['expected_annual_cases'] for p in results_summary)
print(f"Combined Annual Risk (all pathogens): {total_annual_risk:.2e}")
print(f"Total Expected Cases/Year: {total_cases:.0f}")

# Compliance summary
annual_compliant = sum(1 for p in results_summary if p['nz_annual_compliant'])
event_compliant = sum(1 for p in results_summary if p['nz_event_compliant'])
print(f"NZ Annual Guideline Compliance: {annual_compliant}/{len(results_summary)} pathogens")
print(f"NZ Event Guideline Compliance: {event_compliant}/{len(results_summary)} pathogens")