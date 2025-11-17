#!/usr/bin/env python3
"""
Quick test to verify PDF report generation with web app plots works correctly.
"""

import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'app'))

# Import our modules
from pdf_report_generator import QMRAPDFReportGenerator

def create_test_plot():
    """Create a simple test plot."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(['A', 'B', 'C'], [1, 2, 3])
    ax.set_title('Test Plot')
    ax.set_xlabel('Category')
    ax.set_ylabel('Value')
    return fig

def test_pdf_with_plots():
    """Test PDF generation with pre-generated plots."""
    print("Testing PDF generation with web app plots...")

    # Check if we have example results
    results_file = "outputs/results/batch_scenarios_results.csv"

    if not Path(results_file).exists():
        print(f"[ERROR] Test results file not found: {results_file}")
        print("Please run the web app and generate results first.")
        return False

    # Read results
    df = pd.read_csv(results_file)
    print(f"[OK] Loaded results: {len(df)} scenarios")

    # Create test plots (simulating web app plots)
    print("Creating test plots...")
    test_plots = {
        'risk_overview': create_test_plot(),
        'compliance_distribution': create_test_plot(),
        'risk_distribution': create_test_plot(),
        'population_impact': create_test_plot()
    }
    print("[OK] Created 4 test plots")

    # Generate PDF with plots
    output_pdf = "outputs/results/test_report_with_plots.pdf"
    print(f"Generating PDF with plots: {output_pdf}")

    try:
        generator = QMRAPDFReportGenerator()
        generator.generate_report(
            df,
            output_pdf,
            "Test Report with Web App Plots",
            plots=test_plots
        )
        print(f"[SUCCESS] PDF generated successfully: {output_pdf}")

        # Clean up plots
        for fig in test_plots.values():
            plt.close(fig)

        # Verify PDF exists
        if Path(output_pdf).exists():
            size = Path(output_pdf).stat().st_size
            print(f"[OK] PDF file size: {size:,} bytes")
            return True
        else:
            print("[ERROR] PDF file was not created")
            return False

    except Exception as e:
        print(f"[ERROR] Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pdf_without_plots():
    """Test PDF generation without plots (fallback mode)."""
    print("\nTesting PDF generation without plots (fallback mode)...")

    results_file = "outputs/results/batch_scenarios_results.csv"

    if not Path(results_file).exists():
        print(f"[ERROR] Test results file not found: {results_file}")
        return False

    df = pd.read_csv(results_file)
    output_pdf = "outputs/results/test_report_without_plots.pdf"

    try:
        generator = QMRAPDFReportGenerator()
        generator.generate_report(
            df,
            output_pdf,
            "Test Report without Plots",
            plots=None  # No plots provided - should use fallback
        )
        print(f"[SUCCESS] PDF generated successfully (fallback mode): {output_pdf}")

        if Path(output_pdf).exists():
            size = Path(output_pdf).stat().st_size
            print(f"[OK] PDF file size: {size:,} bytes")
            return True
        else:
            print("[ERROR] PDF file was not created")
            return False

    except Exception as e:
        print(f"[ERROR] Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("="*60)
    print("PDF Report Generator Test Suite")
    print("="*60)

    # Test 1: PDF with plots
    test1_passed = test_pdf_with_plots()

    # Test 2: PDF without plots (fallback)
    test2_passed = test_pdf_without_plots()

    # Summary
    print("\n" + "="*60)
    print("Test Summary:")
    print(f"  Test 1 (with plots): {'[PASSED]' if test1_passed else '[FAILED]'}")
    print(f"  Test 2 (fallback):   {'[PASSED]' if test2_passed else '[FAILED]'}")
    print("="*60)

    if test1_passed and test2_passed:
        print("\n[SUCCESS] All tests passed!")
        sys.exit(0)
    else:
        print("\n[WARNING] Some tests failed")
        sys.exit(1)
