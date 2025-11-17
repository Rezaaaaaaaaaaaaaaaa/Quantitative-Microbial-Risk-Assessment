#!/usr/bin/env python3
"""
Simple QMRA Batch Processor with Automatic Distribution Handling

This script automatically:
1. Creates ECDF from dilution time series data (multiple measurements per site)
2. Creates Hockey Stick distribution from pathogen min/median/max
3. Runs QMRA for all scenarios

NO FLAGS NEEDED - Everything is automatic!
"""

import pandas as pd
import sys
import os
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'app'))

from batch_processor import BatchProcessor

def main():
    print("="*80)
    print("SIMPLE QMRA BATCH PROCESSOR")
    print("Automatic ECDF (dilution) + Hockey Stick (pathogen)")
    print("="*80)

    # Load scenarios
    scenario_file = 'input_data/batch_scenarios/simple_scenarios.csv'
    scenarios = pd.read_csv(scenario_file)

    print(f"\nLoaded {len(scenarios)} scenarios from {scenario_file}")
    print("\nScenarios:")
    for idx, row in scenarios.iterrows():
        print(f"  {row['Scenario_ID']}: {row['Scenario_Name']}")
        print(f"    Pathogen: {row['Pathogen']} (min={row['Pathogen_Min']:.0f}, "
              f"median={row['Pathogen_Median']:.0f}, max={row['Pathogen_Max']:.0f})")
        print(f"    Dilution: {row['Dilution_File']}")

    # Initialize processor
    processor = BatchProcessor(output_dir='outputs/simple_batch')

    # Process each scenario
    all_results = []

    for idx, scenario in scenarios.iterrows():
        print(f"\n{'='*80}")
        print(f"[{idx+1}/{len(scenarios)}] Processing: {scenario['Scenario_ID']} - {scenario['Scenario_Name']}")
        print(f"{'='*80}")

        dilution_file = f"input_data/dilution_data/{scenario['Dilution_File']}"

        try:
            # Run spatial assessment
            # NO FLAGS - automatically uses ECDF and Hockey Stick!
            results = processor.run_spatial_assessment(
                dilution_file=dilution_file,
                pathogen=scenario['Pathogen'],

                # Pathogen parameters (Hockey Stick created automatically)
                pathogen_min=scenario['Pathogen_Min'],
                pathogen_median=scenario['Pathogen_Median'],
                pathogen_max=scenario['Pathogen_Max'],

                # Standard QMRA parameters
                treatment_lrv=scenario['Treatment_LRV'],
                exposure_route=scenario['Exposure_Route'],
                volume_ml=scenario['Volume_mL'],
                frequency_per_year=scenario['Frequency_Year'],
                population=scenario['Population'],
                iterations=scenario['Iterations'],

                # ECDF created automatically from dilution file!
                use_ecdf_dilution=True,  # Always True
                use_hockey_pathogen=True,  # Always True

                output_file=f"{scenario['Scenario_ID']}_results.csv"
            )

            # Add scenario info to results
            results['Scenario_ID'] = scenario['Scenario_ID']
            results['Scenario_Name'] = scenario['Scenario_Name']
            all_results.append(results)

            # Print summary
            print(f"\nResults Summary:")
            for _, site in results.iterrows():
                print(f"  {site['Site_Name']:<15} Risk: {site['Annual_Risk_Median']:.2e} "
                      f"(95th: {site['Annual_Risk_95th']:.2e}) [{site['Compliance_Status']}]")

        except Exception as e:
            print(f"ERROR processing {scenario['Scenario_ID']}: {e}")
            import traceback
            traceback.print_exc()
            continue

    # Combine all results
    if all_results:
        print(f"\n{'='*80}")
        print("FINAL SUMMARY")
        print(f"{'='*80}")

        combined = pd.concat(all_results, ignore_index=True)
        combined.to_csv('outputs/simple_batch/all_scenarios_combined.csv', index=False)

        # Summary by scenario
        summary = combined.groupby(['Scenario_ID', 'Scenario_Name', 'Site_Name']).agg({
            'Annual_Risk_Median': 'first',
            'Annual_Risk_95th': 'first',
            'Compliance_Status': 'first'
        }).reset_index()

        print(f"\nProcessed {len(scenarios)} scenarios across {len(combined)} site assessments")

        # Count compliance
        compliant = len(combined[combined['Compliance_Status'] == 'COMPLIANT'])
        print(f"\nCompliance: {compliant}/{len(combined)} site-scenarios ({100*compliant/len(combined):.1f}%)")

        # Show non-compliant sites
        non_compliant = combined[combined['Compliance_Status'] == 'NON-COMPLIANT']
        if len(non_compliant) > 0:
            print(f"\nNon-compliant sites:")
            for _, row in non_compliant.iterrows():
                print(f"  {row['Scenario_ID']} - {row['Site_Name']}: {row['Annual_Risk_Median']:.2e}")

        print(f"\nAll results saved to: outputs/simple_batch/")
        print(f"Combined results: outputs/simple_batch/all_scenarios_combined.csv")

    print(f"\n{'='*80}")
    print("BATCH PROCESSING COMPLETE")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
