"""
Clean up Norovirus Production App - Remove unnecessary files
Keep only essential files for production use
"""

import os
import shutil
from pathlib import Path

app_dir = Path(r"c:\Users\moghaddamr\OneDrive - NIWA\Quantitative Microbial Risk Assessment\QMRA_Norovirus_Production_App")

# Files/folders to REMOVE (not needed for production)
to_remove = [
    # Old documentation (keep only essential)
    "docs/BACKEND_VERIFICATION_SUMMARY.md",
    "docs/BEST_PRACTICES_GUIDE.md",
    "docs/COMPLETE_IMPLEMENTATION_SUMMARY.md",
    "docs/DISTRIBUTION_INPUT_FORMAT.md",
    "docs/DISTRIBUTION_PARAMETERS_GUIDE.md",
    "docs/EMAIL_TO_DAVID_AND_ANDREW.txt",
    "docs/FINAL_SUMMARY.md",
    "docs/HOCKEY_STICK_IMPLEMENTATION.md",
    "docs/LIBRARY_APPROACH_SUMMARY.md",
    "docs/PLOT_REVIEW_SUMMARY.md",
    "docs/PRODUCTION_MODE_GUIDE.md",  # No longer needed (always production)
    "docs/QUICK_START.md",  # Superseded by main README
    "docs/QUICK_START_LIBRARY_APPROACH.md",
    "docs/SCREENSHOT_AUTOMATION_README.md",
    "docs/SCREENSHOT_AUTOMATION_SETUP.txt",
    "docs/SIMPLE_WORKFLOW_GUIDE.md",
    "docs/SIMPLIFIED_APPROACH_README.md",
    "docs/USER_GUIDE_STEP_BY_STEP.md",  # Superseded by TECHNICAL_USER_MANUAL
    "docs/QMRA_Application_Overview.docx",
    "docs/QMRA_Application_Overview_with_screenshots.docx",
    "docs/betaBinomial_data.csv",

    # Old screenshots
    "screenshots/",

    # Old test outputs
    "outputs/library_test/",
    "outputs/simple_batch/",
    "outputs/simple_example/",
    "outputs/simplified_test/",
    "outputs/test_distributions/",
    "outputs/web_app_final_test/",
    "outputs/web_app_test/",

    # Development test files (keep only verification)
    "tests/test_custom_distributions.py",
    "tests/test_distributions.py",
    "tests/test_library_approach.py",
    "tests/test_new_features.py",
    "tests/test_pdf_plots.py",
    "tests/test_plot_review.py",
    "tests/test_simplified_approach.py",
    "tests/test_web_app_final.py",
    "tests/test_web_app_library.py",
    "tests/verify_hockey_stick.py",

    # Screenshot/documentation generation scripts
    "scripts/analyze_niwa_template.py",
    "scripts/capture_app_screenshots.py",
    "scripts/capture_app_screenshots_full.py",
    "scripts/capture_screenshots_automated.py",
    "scripts/capture_screenshots_interactive.py",
    "scripts/create_final_user_guide.py",
    "scripts/create_niwa_formatted_guide.py",
    "scripts/create_niwa_formatted_guide_improved.py",
    "scripts/create_professional_doc.py",
    "scripts/create_user_guide_with_screenshots.py",
    "scripts/demo_screenshot_usage.py",
    "scripts/insert_screenshots_to_word.py",
    "scripts/manual_screenshot_guide.py",

    # Old batch scenario files
    "input_data/batch_scenarios/test_custom_dist.csv",
    "input_data/batch_scenarios/scenarios_with_distributions.csv",
    "input_data/batch_scenarios/master_batch_scenarios.csv",

    # Exposure scenario YAMLs (examples, not needed for production)
    "input_data/exposure_scenarios/",

    # Treatment scenario YAMLs (examples, not needed for production)
    "input_data/treatment_scenarios/",

    # Old dilution library
    "input_data/dilution_library.csv",

    # Checkpoints
    ".ipynb_checkpoints/",

    # Old README and screenshot instructions
    "README.md",  # Will replace with README_NOROVIRUS.md
    "SCREENSHOT_INSTRUCTIONS.md",
    "capture_screenshots_automated.bat",
]

print("QMRA Norovirus Production App - Cleanup Script")
print("=" * 60)
print()

removed_count = 0
skipped_count = 0

for item in to_remove:
    item_path = app_dir / item

    if item_path.exists():
        try:
            if item_path.is_dir():
                shutil.rmtree(item_path)
                print(f"[OK] Removed directory: {item}")
            else:
                item_path.unlink()
                print(f"[OK] Removed file: {item}")
            removed_count += 1
        except Exception as e:
            print(f"[ERROR] Error removing {item}: {e}")
    else:
        skipped_count += 1

print()
print("=" * 60)
print(f"Removed: {removed_count} items")
print(f"Skipped (not found): {skipped_count} items")
print()

# Rename README_NOROVIRUS.md to README.md
readme_novo = app_dir / "README_NOROVIRUS.md"
readme_main = app_dir / "README.md"

if readme_novo.exists():
    if readme_main.exists():
        readme_main.unlink()
    readme_novo.rename(readme_main)
    print("[OK] Renamed README_NOROVIRUS.md -> README.md")

print()
print("[COMPLETE] Cleanup complete!")
print()
print("KEPT (Essential files):")
print("  - app/ (core application)")
print("  - qmra_core/ (core modules)")
print("  - input_data/ (norovirus-only data)")
print("  - docs/INSTALLATION.md")
print("  - docs/TECHNICAL_USER_MANUAL.md")
print("  - docs/CALCULATION_FLOW.md")
print("  - tests/test_beta_binomial_validation.py")
print("  - tests/verify_dose_response.py")
print("  - scripts/run_simple_qmra.py")
print("  - scripts/SIMPLE_EXAMPLE.py")
print("  - requirements.txt")
print("  - README.md (norovirus-specific)")
print("  - INPUT_DATA_CLEANUP_SUMMARY.md")
