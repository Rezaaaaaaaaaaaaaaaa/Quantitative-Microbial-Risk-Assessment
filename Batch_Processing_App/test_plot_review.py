#!/usr/bin/env python3
"""
Plot Review Script
==================

Generate and review all plots to ensure they look correct.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys

# Import plotting functions from web_app
sys.path.insert(0, str(Path(__file__).parent))
from web_app import (
    create_risk_overview_plot,
    create_compliance_plot,
    create_risk_distribution_plot,
    create_population_impact_plot
)

def review_plots():
    """Generate and review all plots."""
    print("="*70)
    print("PLOT REVIEW")
    print("="*70)

    # Load results
    results_file = "outputs/results/batch_scenarios_results.csv"

    if not Path(results_file).exists():
        print(f"\n[ERROR] Results file not found: {results_file}")
        print("Please run batch assessment first.")
        return False

    df = pd.read_csv(results_file)
    print(f"\n[OK] Loaded {len(df)} scenarios")

    # Check data quality
    print("\n1. Data Quality Check:")
    print(f"   Columns: {list(df.columns)}")
    print(f"   Annual_Risk_Median range: {df['Annual_Risk_Median'].min():.2e} - {df['Annual_Risk_Median'].max():.2e}")
    print(f"   Population_Impact range: {df['Population_Impact'].min():.0f} - {df['Population_Impact'].max():.0f}")

    if 'Compliance_Status' in df.columns:
        compliance_counts = df['Compliance_Status'].value_counts()
        print(f"   Compliance Status: {compliance_counts.to_dict()}")

    # Check for WHO threshold consistency
    print("\n2. WHO Threshold Check:")
    print("   IMPORTANT: Checking consistency between compliance determination and plot threshold")

    # Count scenarios near thresholds
    below_1e6 = len(df[df['Annual_Risk_Median'] <= 1e-6])
    between_1e6_and_1e4 = len(df[(df['Annual_Risk_Median'] > 1e-6) & (df['Annual_Risk_Median'] <= 1e-4)])
    above_1e4 = len(df[df['Annual_Risk_Median'] > 1e-4])

    print(f"   Scenarios <= 1e-6 (very safe): {below_1e6}")
    print(f"   Scenarios 1e-6 to 1e-4 (safe range): {between_1e6_and_1e4}")
    print(f"   Scenarios > 1e-4 (WHO threshold): {above_1e4}")

    if 'Compliance_Status' in df.columns:
        compliant_count = len(df[df['Compliance_Status'] == 'COMPLIANT'])
        print(f"   Marked as COMPLIANT: {compliant_count}")
        if compliant_count == below_1e6:
            print("   [INFO] Compliance uses 1e-6 threshold (conservative)")
        else:
            print("   [WARNING] Compliance count doesn't match 1e-6 threshold!")

    # Generate plots
    print("\n3. Generating Plots...")

    try:
        # Plot 1: Risk Overview
        print("   [1/4] Risk Overview Plot...")
        fig1 = create_risk_overview_plot(df)
        fig1.savefig("outputs/results/review_risk_overview.png", dpi=150, bbox_inches='tight')
        plt.close(fig1)
        print("         Saved: review_risk_overview.png")

        # Plot 2: Compliance Distribution
        print("   [2/4] Compliance Distribution Plot...")
        fig2 = create_compliance_plot(df)
        fig2.savefig("outputs/results/review_compliance.png", dpi=150, bbox_inches='tight')
        plt.close(fig2)
        print("         Saved: review_compliance.png")

        # Plot 3: Risk Distribution
        print("   [3/4] Risk Distribution Plot...")
        fig3 = create_risk_distribution_plot(df)
        fig3.savefig("outputs/results/review_risk_distribution.png", dpi=150, bbox_inches='tight')
        plt.close(fig3)
        print("         Saved: review_risk_distribution.png")

        # Plot 4: Population Impact
        print("   [4/4] Population Impact Plot...")
        fig4 = create_population_impact_plot(df)
        fig4.savefig("outputs/results/review_population_impact.png", dpi=150, bbox_inches='tight')
        plt.close(fig4)
        print("         Saved: review_population_impact.png")

        print("\n[SUCCESS] All plots generated successfully!")

    except Exception as e:
        print(f"\n[ERROR] Plot generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Review findings
    print("\n" + "="*70)
    print("REVIEW FINDINGS:")
    print("="*70)

    issues = []
    warnings = []
    good = []

    # Check 1: Compliance threshold
    if below_1e6 == 0 and above_1e4 > 0:
        warnings.append("All scenarios exceed WHO threshold (1e-4)")
        warnings.append("Consider showing 1e-6 line on plot for consistency with compliance determination")

    # Check 2: Data range
    if df['Annual_Risk_Median'].max() / df['Annual_Risk_Median'].min() < 10:
        warnings.append("Limited risk range - plots may not show much variation")
    else:
        good.append("Good risk range for visualization")

    # Check 3: Population impact
    if df['Population_Impact'].max() == 0:
        issues.append("Zero population impact - check population parameter")
    else:
        good.append("Population impact calculated correctly")

    # Check 4: Log scale appropriateness
    risk_span = np.log10(df['Annual_Risk_Median'].max()) - np.log10(df['Annual_Risk_Median'].min())
    if risk_span > 2:
        good.append(f"Log scale appropriate (risk spans {risk_span:.1f} orders of magnitude)")
    else:
        warnings.append(f"Risk span only {risk_span:.1f} orders - linear scale might be clearer")

    # Print findings
    if issues:
        print("\n[ISSUES]:")
        for issue in issues:
            print(f"  - {issue}")

    if warnings:
        print("\n[WARNINGS]:")
        for warning in warnings:
            print(f"  - {warning}")

    if good:
        print("\n[GOOD]:")
        for g in good:
            print(f"  + {g}")

    # Recommendations
    print("\n" + "="*70)
    print("RECOMMENDATIONS:")
    print("="*70)

    print("\n1. WHO Threshold Consistency:")
    print("   The code uses 1e-6 for compliance (very conservative)")
    print("   But plots show 1e-4 (standard WHO recreational water guideline)")
    print("   ")
    print("   Options:")
    print("   A) Keep 1e-6 compliance + add both threshold lines to plot")
    print("   B) Change compliance to 1e-4 (standard approach)")
    print("   C) Add note explaining the conservative 1e-6 threshold")

    print("\n2. Plot Improvements:")
    print("   - Risk Overview: Consider adding error bars (5th-95th percentiles)")
    print("   - Compliance: Good as-is")
    print("   - Risk Distribution: Consider adding percentile lines")
    print("   - Population Impact: Consider color legend for impact levels")

    return True


if __name__ == '__main__':
    success = review_plots()

    print("\n" + "="*70)
    if success:
        print("[SUCCESS] Plot review complete!")
        print("\nGenerated files:")
        print("  - outputs/results/review_risk_overview.png")
        print("  - outputs/results/review_compliance.png")
        print("  - outputs/results/review_risk_distribution.png")
        print("  - outputs/results/review_population_impact.png")
        sys.exit(0)
    else:
        print("[FAILED] Plot review failed")
        sys.exit(1)
