#!/usr/bin/env python3
"""
Test the simplified three-file approach:
- dilution_data.csv: Time, Location, Dilution_Factor
- pathogen_data.csv: Pathogen_ID, Min, Median, Max (Hockey Stick)
- scenarios.csv: All scenario parameters

Author: NIWA Earth Sciences New Zealand
Date: October 2025
"""

from batch_processor import BatchProcessor
from pathlib import Path

def main():
    """Test the simplified approach."""

    print("="*80)
    print("QMRA BATCH PROCESSING - SIMPLIFIED THREE-FILE APPROACH")
    print("="*80)

    # Define file paths
    input_dir = Path("input_data")

    dilution_file = input_dir / "dilution_data.csv"
    pathogen_file = input_dir / "pathogen_data.csv"
    scenarios_file = input_dir / "scenarios.csv"

    # Check files exist
    for file_path in [dilution_file, pathogen_file, scenarios_file]:
        if not file_path.exists():
            print(f"ERROR: Required file not found: {file_path}")
            return
        else:
            print(f"[OK] Found: {file_path}")

    print("\n")

    # Create batch processor
    processor = BatchProcessor(output_dir='outputs/simplified_test')

    # Run batch scenarios using simplified approach
    try:
        results = processor.run_batch_scenarios_from_libraries(
            scenarios_file=str(scenarios_file),
            dilution_data_file=str(dilution_file),
            pathogen_data_file=str(pathogen_file),
            output_dir='outputs/simplified_test'
        )

        print("\n" + "="*80)
        print("TEST COMPLETE - RESULTS SUMMARY")
        print("="*80)

        # Display summary
        print(f"\nTotal scenarios processed: {len(results)}")
        print(f"Compliant scenarios: {len(results[results['Compliance_Status'] == 'COMPLIANT'])}")
        print(f"Non-compliant scenarios: {len(results[results['Compliance_Status'] == 'NON-COMPLIANT'])}")

        print("\nTop 5 highest risk scenarios:")
        top5 = results.nlargest(5, 'Annual_Risk_Median')[['Scenario_ID', 'Scenario_Name', 'Annual_Risk_Median', 'Compliance_Status']]
        for idx, row in top5.iterrows():
            print(f"  {row['Scenario_ID']}: {row['Scenario_Name']}")
            print(f"    Risk: {row['Annual_Risk_Median']:.2e} - {row['Compliance_Status']}")

        print("\n" + "="*80)
        print("SIMPLIFIED APPROACH BENEFITS:")
        print("="*80)
        print("""
1. DILUTION DATA: Just Time, Location, Dilution_Factor
   - Raw data from hydrodynamic models
   - Automatically uses ECDF

2. PATHOGEN DATA: Only Hockey Stick parameters (Min, Median, Max)
   - User determines these three values
   - Simple and straightforward

3. SCENARIOS: All scenario parameters in one place
   - References Location and Pathogen_ID
   - Clear column names with units
        """)

    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
