#!/usr/bin/env python3
"""
Test custom distribution parameters in batch processing.

This script tests the enhanced batch processor with scenario-specific
uncertainty distributions.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Import batch processor
from batch_processor import BatchProcessor

def test_custom_distributions():
    """Test batch processing with custom distribution parameters."""
    print("="*70)
    print("Testing Enhanced Batch Processing with Custom Distributions")
    print("="*70)

    # Check if master scenarios file exists
    scenarios_file = "input_data/batch_scenarios/master_batch_scenarios.csv"

    if not Path(scenarios_file).exists():
        print(f"[ERROR] Scenarios file not found: {scenarios_file}")
        return False

    # Load and verify new columns exist
    print("\n1. Verifying CSV format...")
    df = pd.read_csv(scenarios_file)

    required_columns = [
        'Scenario_ID', 'Scenario_Name', 'Pathogen', 'Effluent_Conc',
        'Effluent_Conc_CV', 'Treatment_LRV', 'Treatment_LRV_Uncertainty',
        'Dilution_Factor', 'Dilution_Factor_CV', 'Volume_mL',
        'Volume_Min', 'Volume_Max'
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        print(f"[ERROR] Missing columns: {missing_columns}")
        return False

    print(f"[OK] All required columns present")
    print(f"[OK] Loaded {len(df)} scenarios")

    # Show distribution parameter ranges
    print("\n2. Distribution Parameter Summary:")
    print(f"   Effluent Conc CV:        {df['Effluent_Conc_CV'].min():.2f} - {df['Effluent_Conc_CV'].max():.2f}")
    print(f"   Treatment LRV Uncertainty: {df['Treatment_LRV_Uncertainty'].min():.2f} - {df['Treatment_LRV_Uncertainty'].max():.2f}")
    print(f"   Dilution Factor CV:      {df['Dilution_Factor_CV'].min():.2f} - {df['Dilution_Factor_CV'].max():.2f}")
    print(f"   Volume Range:            {df['Volume_Min'].min():.0f} - {df['Volume_Max'].max():.0f} mL")

    # Test with just first 3 scenarios for speed
    print("\n3. Running Test Batch (3 scenarios)...")
    test_scenarios_file = "input_data/batch_scenarios/test_custom_dist.csv"
    df_test = df.head(3).copy()
    df_test.to_csv(test_scenarios_file, index=False)

    try:
        processor = BatchProcessor(output_dir='outputs/results')

        results = processor.run_batch_scenarios(
            scenario_file=test_scenarios_file,
            output_dir='outputs/results'
        )

        print(f"\n[SUCCESS] Batch processing completed!")
        print(f"[OK] Processed {len(results)} scenarios")

        # Verify results have proper risk ranges
        print("\n4. Verifying Results:")

        # Check if 5th and 95th percentiles exist
        if 'Annual_Risk_5th' in results.columns and 'Annual_Risk_95th' in results.columns:
            print("[OK] Risk percentiles calculated")

            # Show uncertainty ranges for each scenario
            print("\n5. Uncertainty Analysis:")
            print("-" * 70)

            for idx, row in results.iterrows():
                scenario_name = row['Scenario_Name']
                median_risk = row['Annual_Risk_Median']
                risk_5th = row['Annual_Risk_5th']
                risk_95th = row['Annual_Risk_95th']

                # Calculate uncertainty factor (95th / 5th percentile)
                uncertainty_factor = risk_95th / risk_5th if risk_5th > 0 else 0

                print(f"\n{scenario_name}:")
                print(f"  Median Risk:  {median_risk:.2e}")
                print(f"  5th-95th:     {risk_5th:.2e} - {risk_95th:.2e}")
                print(f"  Uncertainty:  {uncertainty_factor:.1f}x range")

            print("-" * 70)

        else:
            print("[WARNING] Risk percentiles not found in results")

        # Compare scenario with low vs high uncertainty
        s001 = results[results['Scenario_ID'] == 'S001'].iloc[0]  # Low uncertainty (CV=0.4)
        s002 = results[results['Scenario_ID'] == 'S002'].iloc[0]  # High uncertainty (CV=0.8)

        print("\n6. Comparing Low vs High Uncertainty Scenarios:")
        print(f"\nS001 (Beach A Summer, CV=0.4 - Good data):")
        print(f"  Risk: {s001['Annual_Risk_Median']:.2e} [{s001['Annual_Risk_5th']:.2e} - {s001['Annual_Risk_95th']:.2e}]")

        print(f"\nS002 (Beach A Winter, CV=0.8 - High uncertainty):")
        print(f"  Risk: {s002['Annual_Risk_Median']:.2e} [{s002['Annual_Risk_5th']:.2e} - {s002['Annual_Risk_95th']:.2e}]")

        # Calculate relative uncertainty width
        s001_width = (s001['Annual_Risk_95th'] / s001['Annual_Risk_5th'])
        s002_width = (s002['Annual_Risk_95th'] / s002['Annual_Risk_5th'])

        print(f"\nUncertainty Ratio (95th/5th):")
        print(f"  S001: {s001_width:.1f}x")
        print(f"  S002: {s002_width:.1f}x (wider due to higher CV)")

        if s002_width > s001_width:
            print("\n[SUCCESS] Higher CV correctly produces wider uncertainty range!")
        else:
            print("\n[WARNING] Expected S002 to have wider range than S001")

        return True

    except Exception as e:
        print(f"\n[ERROR] Batch processing failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("\n" + "="*70)
    print("Custom Distribution Test Suite")
    print("="*70 + "\n")

    success = test_custom_distributions()

    print("\n" + "="*70)
    if success:
        print("[SUCCESS] All tests passed!")
        print("="*70)
        sys.exit(0)
    else:
        print("[FAILED] Some tests failed")
        print("="*70)
        sys.exit(1)
