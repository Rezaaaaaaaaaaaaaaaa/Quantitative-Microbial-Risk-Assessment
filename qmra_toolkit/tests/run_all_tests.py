#!/usr/bin/env python3
"""
Run all tests for QMRA toolkit with comprehensive reporting.
"""

import unittest
import sys
import os
from pathlib import Path
import time

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

def run_test_suite():
    """Run complete test suite with detailed reporting."""

    print("QMRA Toolkit Test Suite")
    print("=" * 50)

    # Discover and run tests
    test_dir = Path(__file__).parent
    loader = unittest.TestLoader()

    # Load specific test modules
    test_modules = [
        'test_pathogen_database',
        'test_dose_response',
        'test_integration'
    ]

    suite = unittest.TestSuite()

    for module_name in test_modules:
        try:
            module_suite = loader.loadTestsFromName(module_name)
            suite.addTest(module_suite)
            print(f"[OK] Loaded tests from {module_name}")
        except ImportError as e:
            print(f"[FAIL] Failed to load {module_name}: {e}")

    print(f"\nRunning {suite.countTestCases()} tests...")
    print("-" * 50)

    # Run tests with detailed output
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        buffer=True,
        warnings='ignore'
    )

    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()

    # Print summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"Execution time: {end_time - start_time:.2f} seconds")

    # Print detailed failure/error information
    if result.failures:
        print("\nFailures:")
        print("-" * 20)
        for test, traceback in result.failures:
            print(f"FAIL: {test}")
            print(traceback)
            print()

    if result.errors:
        print("\nErrors:")
        print("-" * 20)
        for test, traceback in result.errors:
            print(f"ERROR: {test}")
            print(traceback)
            print()

    if result.skipped:
        print("\nSkipped tests:")
        print("-" * 20)
        for test, reason in result.skipped:
            print(f"SKIP: {test} - {reason}")

    # Return success status
    return len(result.failures) == 0 and len(result.errors) == 0


def validate_installation():
    """Validate that all required modules can be imported."""

    print("Validating QMRA Toolkit Installation")
    print("-" * 40)

    required_modules = [
        'pathogen_database',
        'dose_response',
        'exposure_assessment',
        'dilution_model',
        'monte_carlo',
        'risk_characterization',
        'report_generator',
        'qmra_toolkit'
    ]

    missing_modules = []

    for module_name in required_modules:
        try:
            __import__(module_name)
            print(f"[OK] {module_name}")
        except ImportError as e:
            print(f"[FAIL] {module_name}: {e}")
            missing_modules.append(module_name)

    if missing_modules:
        print(f"\nMissing modules: {', '.join(missing_modules)}")
        return False
    else:
        print("\n[OK] All modules imported successfully")
        return True


def check_dependencies():
    """Check that all required dependencies are available."""

    print("\nChecking Dependencies")
    print("-" * 25)

    required_packages = [
        'numpy',
        'scipy',
        'pandas',
        'matplotlib',
        'docx',
        'yaml',
        'click'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            if package == 'docx':
                import docx
                print(f"[OK] python-docx")
            elif package == 'yaml':
                import yaml
                print(f"[OK] pyyaml")
            else:
                __import__(package)
                print(f"[OK] {package}")
        except ImportError:
            print(f"[FAIL] {package}")
            missing_packages.append(package)

    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    else:
        print("\n[OK] All dependencies available")
        return True


def run_smoke_test():
    """Run a quick smoke test to verify basic functionality."""

    print("\nRunning Smoke Test")
    print("-" * 20)

    try:
        from pathogen_database import PathogenDatabase
        from dose_response import create_dose_response_model
        from risk_characterization import RiskCharacterization

        # Test pathogen database
        db = PathogenDatabase()
        pathogens = db.get_available_pathogens()
        print(f"[OK] Pathogen database loaded ({len(pathogens)} pathogens)")

        if 'norovirus' in pathogens:
            # Test dose-response calculation
            params = db.get_dose_response_parameters('norovirus')
            model = create_dose_response_model('beta_poisson', params)
            prob = model.calculate_infection_probability(10.0)
            print(f"[OK] Dose-response calculation (P = {prob:.4f})")

            # Test risk characterization
            risk_calc = RiskCharacterization(db)
            result = risk_calc.calculate_infection_probability('norovirus', [1, 10, 100])
            print(f"[OK] Risk characterization ({len(result.individual_risks)} results)")

        print("[OK] Smoke test passed")
        return True

    except Exception as e:
        print(f"✗ Smoke test failed: {e}")
        return False


if __name__ == '__main__':
    success = True

    # Check dependencies first
    if not check_dependencies():
        success = False
        print("\nPlease install missing dependencies before running tests.")

    # Validate installation
    if not validate_installation():
        success = False
        print("\nPlease fix import issues before running tests.")

    # Run smoke test
    if not run_smoke_test():
        success = False
        print("\nBasic functionality test failed.")

    # Run full test suite if everything looks good
    if success:
        print("\n" + "=" * 60)
        success = run_test_suite()

    # Final status
    print("\n" + "=" * 60)
    if success:
        print("[PASS] All tests passed! QMRA Toolkit is ready to use.")
        sys.exit(0)
    else:
        print("[FAIL] Some tests failed. Please review the output above.")
        sys.exit(1)