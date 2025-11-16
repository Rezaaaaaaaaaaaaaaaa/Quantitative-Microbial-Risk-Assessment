#!/usr/bin/env python3
"""
Quick test to verify web app can load and process with library approach.

This doesn't run the Streamlit UI, just tests the backend processing.

Author: NIWA Earth Sciences New Zealand
Date: October 2025
"""

import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'app'))

from batch_processor import BatchProcessor

def test_web_app_backend():
    """Test the backend processing that web app uses."""

    print("="*80)
    print("TESTING WEB APP BACKEND - LIBRARY-BASED APPROACH")
    print("="*80)

    # Use the same file paths the web app would use
    dilution_file = "input_data/dilution_library.csv"
    pathogen_file = "input_data/pathogen_library.csv"
    scenario_file = "input_data/master_scenarios.csv"

    # Verify files exist
    for file_path in [dilution_file, pathogen_file, scenario_file]:
        if not Path(file_path).exists():
            print(f"ERROR: File not found: {file_path}")
            return False
        print(f"[OK] Found: {file_path}")

    print("\nInitializing BatchProcessor...")
    processor = BatchProcessor(output_dir='outputs/results')

    print("Running batch scenarios from libraries...")
    try:
        results = processor.run_batch_scenarios_from_libraries(
            scenarios_file=scenario_file,
            dilution_library_file=dilution_file,
            pathogen_library_file=pathogen_file,
            output_dir='outputs/web_app_test'
        )

        print("\n" + "="*80)
        print("SUCCESS - Backend Processing Complete")
        print("="*80)
        print(f"\nProcessed {len(results)} scenarios")
        print(f"Compliant: {len(results[results['Compliance_Status'] == 'COMPLIANT'])}")
        print(f"Non-compliant: {len(results[results['Compliance_Status'] == 'NON-COMPLIANT'])}")

        print("\nResults saved to: outputs/web_app_test/batch_scenarios_results.csv")

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
        print("[SUCCESS] Web app backend is ready to use with library-based approach!")
        print("="*80)
        print("\nTo run the full web app:")
        print("  streamlit run web_app.py")
    else:
        print("\n" + "="*80)
        print("[FAILED] Test failed - please check errors above")
        print("="*80)
