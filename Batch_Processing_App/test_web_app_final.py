#!/usr/bin/env python3
"""
Final test of web app backend with correct parameter names.

Author: NIWA Earth Sciences New Zealand
Date: October 2025
"""

from batch_processor import BatchProcessor
from pathlib import Path

def test_web_app_backend():
    """Test the backend processing that web app uses."""

    print("="*80)
    print("TESTING WEB APP BACKEND - FINAL TEST")
    print("="*80)

    # Use the same file paths the web app would use
    dilution_file = "input_data/dilution_data.csv"
    pathogen_file = "input_data/pathogen_data.csv"
    scenario_file = "input_data/scenarios.csv"

    # Verify files exist
    for file_path in [dilution_file, pathogen_file, scenario_file]:
        if not Path(file_path).exists():
            print(f"ERROR: File not found: {file_path}")
            return False
        print(f"[OK] Found: {file_path}")

    print("\nInitializing BatchProcessor...")
    processor = BatchProcessor(output_dir='outputs/results')

    print("Running batch scenarios (matching web app call)...")
    try:
        # This matches the web_app.py call exactly
        results = processor.run_batch_scenarios_from_libraries(
            scenarios_file=scenario_file,
            dilution_data_file=dilution_file,
            pathogen_data_file=pathogen_file,
            output_dir='outputs/web_app_final_test'
        )

        print("\n" + "="*80)
        print("SUCCESS - Backend Processing Complete")
        print("="*80)
        print(f"\nProcessed {len(results)} scenarios")
        print(f"Compliant: {len(results[results['Compliance_Status'] == 'COMPLIANT'])}")
        print(f"Non-compliant: {len(results[results['Compliance_Status'] == 'NON-COMPLIANT'])}")

        print("\nTop 3 scenarios by risk:")
        top3 = results.nlargest(3, 'Annual_Risk_Median')[['Scenario_ID', 'Scenario_Name', 'Annual_Risk_Median', 'Compliance_Status']]
        for idx, row in top3.iterrows():
            print(f"  {row['Scenario_ID']}: {row['Scenario_Name']}")
            print(f"    Risk: {row['Annual_Risk_Median']:.2e} - {row['Compliance_Status']}")

        print("\nResults saved to: outputs/web_app_final_test/batch_scenarios_results.csv")

        return True

    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_web_app_backend()

    if success:
        print("\n" + "="*80)
        print("[SUCCESS] Web app backend is ready!")
        print("="*80)
        print("\nTo run the full web app:")
        print("  streamlit run web_app.py")
    else:
        print("\n" + "="*80)
        print("[FAILED] Test failed - please check errors above")
        print("="*80)
