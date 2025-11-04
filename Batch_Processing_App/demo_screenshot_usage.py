#!/usr/bin/env python3
"""
QMRA Screenshot Capture - Usage Guide & Demo
==============================================

This script demonstrates how to use the automated screenshot capture system.
It creates mock screenshots and demonstrates the workflow.
"""

import json
from pathlib import Path
from datetime import datetime


def create_demo_manifest():
    """Create example manifest file."""
    manifest = {
        "captured_at": "2025-11-05T10:30:00",
        "app_url": "http://localhost:8502",
        "total_screenshots": 6,
        "screenshots": [
            {
                "filename": "01_home_page_20251105_103000.png",
                "page": "home_page",
                "description": "Main application interface with sidebar navigation showing 5 assessment modes",
                "timestamp": "20251105_103000"
            },
            {
                "filename": "02_batch_scenarios_20251105_103015.png",
                "page": "batch_scenarios",
                "description": "Batch processing interface showing 15 pre-configured scenarios with input data tabs",
                "timestamp": "20251105_103015"
            },
            {
                "filename": "03_spatial_assessment_20251105_103030.png",
                "page": "spatial_assessment",
                "description": "Multi-site risk assessment showing pathogen selection and dilution factor parameters",
                "timestamp": "20251105_103030"
            },
            {
                "filename": "04_temporal_assessment_20251105_103045.png",
                "page": "temporal_assessment",
                "description": "Time-series risk analysis interface with monitoring data upload and temporal parameters",
                "timestamp": "20251105_103045"
            },
            {
                "filename": "05_treatment_comparison_20251105_103100.png",
                "page": "treatment_comparison",
                "description": "Treatment technology comparison showing multiple treatment scenarios and parameters",
                "timestamp": "20251105_103100"
            },
            {
                "filename": "06_multi_pathogen_20251105_103115.png",
                "page": "multi_pathogen",
                "description": "Multi-pathogen assessment interface for simultaneous evaluation of 2-6 pathogens",
                "timestamp": "20251105_103115"
            }
        ]
    }

    return manifest


def print_usage_guide():
    """Print complete usage guide."""
    guide = """
================================================================================
QMRA SCREENSHOT CAPTURE - COMPLETE USAGE GUIDE
================================================================================

STEP 1: INSTALL REQUIRED PACKAGES
──────────────────────────────────
Run once to install dependencies:

    pip install selenium webdriver-manager python-docx

Required packages:
  • selenium          - Browser automation (screenshot capture)
  • webdriver-manager - Automatic ChromeDriver management
  • python-docx       - Word document manipulation


STEP 2: START THE STREAMLIT APP
────────────────────────────────
In Terminal 1, run:

    streamlit run web_app.py

You should see:
  You can now view your Streamlit app in your browser.
  URL: http://localhost:8502

Leave this terminal running.


STEP 3: CAPTURE SCREENSHOTS
─────────────────────────────
In Terminal 2 (new terminal), run:

    python capture_app_screenshots.py

What happens:
  1. Script waits 5 seconds for you to verify app is running
  2. Opens Google Chrome browser
  3. Navigates to http://localhost:8502
  4. Captures 6 pages of the app:
     - Home page
     - Batch Scenarios
     - Spatial Assessment
     - Temporal Assessment
     - Treatment Comparison
     - Multi-Pathogen Assessment
  5. Saves screenshots to screenshots/ directory
  6. Creates manifest.json with metadata
  7. Creates index.html preview file

Expected output:
  [INIT] Screenshot output directory: ...screenshots
  [CAPTURE] Home Page
  [OK] Captured: home_page -> 01_home_page_*.png
  [CAPTURE] Batch Scenarios Page
  [OK] Captured: batch_scenarios -> 02_batch_scenarios_*.png
  ... (and 4 more)
  [OK] Index created: screenshots/index.html
  [OK] Manifest created: screenshots/manifest.json
  [CAPTURE COMPLETE] 6 screenshots

Time: 2-3 minutes


STEP 4: VERIFY SCREENSHOTS
────────────────────────────
Open in browser (optional):

    screenshots/index.html

This shows preview of all 6 screenshots in a web page.


STEP 5: INSERT INTO WORD DOCUMENT
──────────────────────────────────
Still in Terminal 2, run:

    python insert_screenshots_to_word.py

What happens:
  1. Reads screenshots/manifest.json
  2. Opens QMRA_Application_Overview.docx
  3. Adds new "Appendix: Application Screenshots" page
  4. Inserts all 6 screenshots with captions
  5. Saves as QMRA_Application_Overview_with_screenshots.docx

Expected output:
  [LOAD] Found 6 screenshots in manifest
  [LOAD] Opened Word document: QMRA_Application_Overview.docx
  [OK] Inserted image 1/6: Home Page
  [OK] Inserted image 2/6: Batch Scenarios
  ... (and 4 more)
  [OK] Document saved: QMRA_Application_Overview_with_screenshots.docx
  [OK] 6 screenshots inserted

Time: 10-30 seconds


STEP 6: REVIEW & SHARE
──────────────────────
1. Open: QMRA_Application_Overview_with_screenshots.docx
2. Review the new "Appendix: Application Screenshots" section
3. Check that all 6 images are present and clear
4. Optional: Add custom captions or notes
5. Share the document!


================================================================================
TROUBLESHOOTING
================================================================================

Q: "Manifest not found"
A: Run capture_app_screenshots.py first to create screenshots

Q: Chrome browser doesn't open
A: • Verify Chrome is installed: chrome --version
   • Close any existing Chrome windows
   • Run with administrator privileges

Q: "ERR_CONNECTION_REFUSED" error
A: • Verify Streamlit app is running: streamlit run web_app.py
   • Check URL is correct: http://localhost:8502
   • Wait 10+ seconds for app to fully load
   • Clear browser cache and refresh

Q: Images are blurry or cut off
A: • Ensure Chrome window is maximized
   • Use a larger monitor/resolution
   • Manually resize Chrome window before running

Q: Word document is very large (>10 MB)
A: • This is normal with embedded images (~500 KB each)
   • To reduce: right-click image → Compress Picture
   • Or save as PDF instead


================================================================================
WORKFLOW DIAGRAM
================================================================================

Terminal 1                              Terminal 2
─────────────────────────────────────────────────────────────────────────
$ streamlit run web_app.py    →    [App loads at localhost:8502]

[App running on port 8502]     →    $ python capture_app_screenshots.py

[App still running]                [Wait 5 seconds...]
                                   [Chrome opens]
                                   [Navigates to pages]
                                   [Captures 6 screenshots]
                                   [Saves to screenshots/]
                                   [2-3 minutes]

                                   $ python insert_screenshots_to_word.py

                                   [Reads manifest.json]
                                   [Opens Word document]
                                   [Inserts 6 images]
                                   [10-30 seconds]

[Press Ctrl+C to stop]    ←   DONE! Report is ready to share


================================================================================
OUTPUT FILES CREATED
================================================================================

After running both scripts, you'll have:

screenshots/
├── 01_home_page_20251105_103000.png         (High-res app screenshot)
├── 02_batch_scenarios_20251105_103015.png   (High-res app screenshot)
├── 03_spatial_assessment_20251105_103030.png (High-res app screenshot)
├── 04_temporal_assessment_20251105_103045.png (High-res app screenshot)
├── 05_treatment_comparison_20251105_103100.png (High-res app screenshot)
├── 06_multi_pathogen_20251105_103115.png    (High-res app screenshot)
├── manifest.json                             (Metadata about screenshots)
└── index.html                                (Preview of all images)

QMRA_Application_Overview_with_screenshots.docx (Word report with screenshots)


================================================================================
FILE SIZES
================================================================================

Each PNG screenshot:        ~500 KB
All 6 screenshots:          ~3 MB
Word document with images:  ~2-3 MB

(Sizes are typical - actual size depends on screen resolution)


================================================================================
TIPS & BEST PRACTICES
================================================================================

Before capturing:
  [OK] Restart the Streamlit app for clean state
  [OK] Clear browser cache
  [OK] Maximize browser window for better visibility
  [OK] Disable Chrome notifications to avoid UI clutter

After capturing:
  [OK] Review index.html in browser
  [OK] Check manifest.json for correct filenames
  [OK] Look at images to ensure they're readable
  [OK] Verify all 6 images were captured

Before sharing:
  [OK] Review Word document in full-screen view
  [OK] Check image quality (not pixelated)
  [OK] Verify captions are accurate
  [OK] Print to PDF for final distribution


================================================================================
ADVANCED OPTIONS
================================================================================

1. CUSTOM APP URL:
   Edit capture_app_screenshots.py:
     capturer = AppScreenshotCapture(
         app_url='http://your-custom-url:port',  ← Change this
         output_dir='screenshots'
     )

2. CUSTOM OUTPUT DIRECTORY:
   Edit capture_app_screenshots.py:
     capturer = AppScreenshotCapture(
         app_url='http://localhost:8502',
         output_dir='my_custom_screenshots'  ← Change this
     )

3. CAPTURE ONLY SPECIFIC PAGES:
   Edit the run_all() method in capture_app_screenshots.py:
     def run_all(self):
         self.capture_home_page()
         self.capture_batch_scenarios()
         # Comment out or remove others
         self.create_index_html()

4. BATCH PROCESSING:
   Create a batch script to capture multiple times:
     #!/bin/bash
     python capture_app_screenshots.py
     python insert_screenshots_to_word.py
     # optional: git add & commit


================================================================================
NEXT STEPS
================================================================================

1. [OK] Install packages:
     pip install selenium webdriver-manager python-docx

2. [OK] Start the app:
     streamlit run web_app.py

3. [OK] Capture screenshots:
     python capture_app_screenshots.py

4. [OK] Insert into Word:
     python insert_screenshots_to_word.py

5. [OK] Open & review:
     QMRA_Application_Overview_with_screenshots.docx

6. [OK] Share with stakeholders!


================================================================================
QUESTIONS?
================================================================================

See SCREENSHOT_AUTOMATION_README.md for detailed documentation
All scripts have built-in error messages to help troubleshoot
Review example scenarios in input_data/ directory


Created for NIWA Earth Sciences - QMRA Batch Processing Application
Version 1.2.0 | November 2025
================================================================================
"""
    return guide


def print_demo_manifest():
    """Print example manifest."""
    manifest = create_demo_manifest()
    demo_output = f"""
================================================================================
EXAMPLE: What manifest.json looks like
================================================================================

File: screenshots/manifest.json

{json.dumps(manifest, indent=2)}

This file is automatically created by capture_app_screenshots.py
It tracks all screenshots, their descriptions, and timing
It's used by insert_screenshots_to_word.py to insert images into Word document

================================================================================
"""
    return demo_output


def main():
    """Main entry point."""
    print("\n" + "="*80)
    print("QMRA SCREENSHOT CAPTURE - AUTOMATED DOCUMENTATION")
    print("="*80)

    # Print guide
    print(print_usage_guide())

    # Print example manifest
    print(print_demo_manifest())

    # Create sample manifest for reference
    sample_dir = Path('screenshots_example')
    sample_dir.mkdir(exist_ok=True)

    manifest = create_demo_manifest()
    manifest_path = sample_dir / 'manifest_example.json'
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"\nExample manifest saved to: {manifest_path}")
    print("\n" + "="*80)
    print("READY TO RUN!")
    print("="*80)
    print("\nFollow the steps in the guide above to:")
    print("  1. Install packages")
    print("  2. Start Streamlit app")
    print("  3. Capture screenshots")
    print("  4. Insert into Word document")
    print("\n" + "="*80)


if __name__ == '__main__':
    main()
