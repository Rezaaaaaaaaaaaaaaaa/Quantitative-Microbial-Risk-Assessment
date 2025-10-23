#!/usr/bin/env python3
"""
Test script for library-based batch processing.

This demonstrates the new approach with separate files for:
- Dilution data library
- Pathogen data library
- Master scenarios (referencing libraries by ID)

Author: NIWA Earth Sciences New Zealand
Date: October 2025
"""

from batch_processor import BatchProcessor
from pathlib import Path

def main():
    """Test the library-based batch processing."""

    print("="*80)
    print("QMRA BATCH PROCESSING - LIBRARY-BASED APPROACH TEST")
    print("="*80)

    # Define file paths
    input_dir = Path("input_data")

    dilution_library = input_dir / "dilution_library.csv"
    pathogen_library = input_dir / "pathogen_library.csv"
    master_scenarios = input_dir / "master_scenarios.csv"

    # Check files exist
    for file_path in [dilution_library, pathogen_library, master_scenarios]:
        if not file_path.exists():
            print(f"ERROR: Required file not found: {file_path}")
            return
        else:
            print(f"[OK] Found: {file_path}")

    print("\n")

    # Create batch processor
    processor = BatchProcessor(output_dir='outputs/library_test')

    # Run batch scenarios using library approach
    try:
        results = processor.run_batch_scenarios_from_libraries(
            scenarios_file=str(master_scenarios),
            dilution_library_file=str(dilution_library),
            pathogen_library_file=str(pathogen_library),
            output_dir='outputs/library_test'
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
        print("ADVANTAGES OF LIBRARY-BASED APPROACH:")
        print("="*80)
        print("""
1. REUSABILITY: Define dilution and pathogen data once, use in multiple scenarios
2. MAINTAINABILITY: Update pathogen/dilution data in one place
3. CLARITY: Separate concerns - data libraries vs. scenario parameters
4. CONSISTENCY: Ensures consistent data across related scenarios
5. FLEXIBILITY: Easy to add new scenarios by referencing existing libraries
6. READABILITY: Clear column names and straightforward structure
        """)

    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
