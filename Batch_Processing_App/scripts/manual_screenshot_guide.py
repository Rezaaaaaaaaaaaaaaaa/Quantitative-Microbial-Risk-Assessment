#!/usr/bin/env python3
"""
Manual Screenshot Capture Guide for QMRA App
=============================================

Interactive guide for capturing professional screenshots
with step-by-step instructions.
"""

import time
import os
from pathlib import Path

def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Print formatted header."""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def print_step(step_num, total_steps, title):
    """Print step header."""
    print(f"\n{'='*80}")
    print(f"STEP {step_num}/{total_steps}: {title}")
    print(f"{'='*80}\n")

def wait_for_user():
    """Wait for user to press Enter."""
    input("\n>>> Press ENTER when ready to continue...")

def main():
    """Main interactive guide."""

    clear_screen()
    print_header("QMRA APP - PROFESSIONAL SCREENSHOT CAPTURE GUIDE")

    print("This interactive guide will help you capture professional screenshots")
    print("of the QMRA application for documentation.")
    print()
    print("REQUIREMENTS:")
    print("  1. QMRA app running at http://localhost:8501")
    print("  2. Windows Snipping Tool (Win + Shift + S)")
    print("  3. Image editor (Paint, etc.) to save screenshots")
    print()
    print("You will capture 18 screenshots covering:")
    print("  - Each assessment mode (6 modes)")
    print("  - Top, middle, and bottom sections of each page")
    print()

    wait_for_user()

    screenshots_dir = Path("../screenshots_manual")
    screenshots_dir.mkdir(exist_ok=True)

    print(f"\nScreenshots will be saved to: {screenshots_dir.absolute()}")
    print()

    # Define all screenshots to capture
    screenshot_plan = [
        {
            'mode': 'Home Page',
            'file_prefix': '01_home',
            'instructions': [
                ('Top', 'Capture the main title, sidebar with Production Mode checkbox, and assessment mode selector'),
                ('Middle', 'Scroll down and capture the welcome message and feature descriptions'),
                ('Bottom', 'Scroll to bottom and capture any remaining content or footer')
            ],
            'setup_steps': [
                '1. Open http://localhost:8501 in your browser',
                '2. Ensure Production Mode is CHECKED',
                '3. Make sure the sidebar is visible'
            ]
        },
        {
            'mode': 'Batch Scenarios',
            'file_prefix': '02_batch_scenarios',
            'instructions': [
                ('Top', 'Select "Batch Scenarios" from dropdown. Capture title and top configuration options'),
                ('Middle', 'Scroll down to capture the data preview tables (pathogen_data, scenarios, master_scenarios)'),
                ('Bottom', 'Scroll to bottom to capture Run Assessment button and results section')
            ],
            'setup_steps': [
                '1. Select "Batch Scenarios" from the Assessment Mode dropdown',
                '2. Check "Use example data" checkbox',
                '3. Wait for data tables to load'
            ]
        },
        {
            'mode': 'Spatial Assessment',
            'file_prefix': '03_spatial',
            'instructions': [
                ('Top', 'Capture the Spatial Assessment title, pathogen selector, and exposure route options'),
                ('Middle', 'Scroll down to capture dilution data upload area and parameter configuration'),
                ('Bottom', 'Scroll to bottom to capture Run Assessment button and example data preview')
            ],
            'setup_steps': [
                '1. Select "Spatial Assessment" from dropdown',
                '2. Choose "norovirus" as pathogen',
                '3. Select "Shellfish Consumption" as exposure route',
                '4. Check "Use example dilution data"'
            ]
        },
        {
            'mode': 'Temporal Assessment',
            'file_prefix': '04_temporal',
            'instructions': [
                ('Top', 'Capture Temporal Assessment title, pathogen/exposure route selectors'),
                ('Middle', 'Scroll down to capture temporal data upload section and parameters'),
                ('Bottom', 'Scroll to bottom for Run Assessment button and data preview')
            ],
            'setup_steps': [
                '1. Select "Temporal Assessment" from dropdown',
                '2. Choose "norovirus" and "Shellfish Consumption"',
                '3. Note the date range options'
            ]
        },
        {
            'mode': 'Treatment Comparison',
            'file_prefix': '05_treatment',
            'instructions': [
                ('Top', 'Capture Treatment Comparison title and scenario configuration section'),
                ('Middle', 'Scroll down to capture treatment LRV input fields for multiple scenarios'),
                ('Bottom', 'Scroll to bottom for additional parameters and Run Comparison button')
            ],
            'setup_steps': [
                '1. Select "Treatment Comparison" from dropdown',
                '2. Choose "norovirus" and exposure route',
                '3. Note the treatment scenario input fields'
            ]
        },
        {
            'mode': 'Multi-Pathogen Assessment',
            'file_prefix': '06_multipathogen',
            'instructions': [
                ('Top', 'Capture Multi-Pathogen title and pathogen multi-select box'),
                ('Middle', 'Scroll down to capture exposure route and configuration parameters'),
                ('Bottom', 'Scroll to bottom for Run Assessment button')
            ],
            'setup_steps': [
                '1. Select "Multi-Pathogen Assessment" from dropdown',
                '2. Note: In Production Mode, only norovirus will be available',
                '3. Select exposure route'
            ]
        }
    ]

    total_screenshots = sum(len(item['instructions']) for item in screenshot_plan)
    screenshot_count = 0

    for mode_idx, mode_info in enumerate(screenshot_plan, 1):
        clear_screen()
        print_header(f"MODE {mode_idx}/6: {mode_info['mode']}")

        print("SETUP STEPS:")
        for setup_step in mode_info['setup_steps']:
            print(f"  {setup_step}")
        print()

        wait_for_user()

        for section_idx, (section, instruction) in enumerate(mode_info['instructions'], 1):
            screenshot_count += 1

            print_step(screenshot_count, total_screenshots,
                      f"{mode_info['mode']} - {section} Section")

            print("INSTRUCTIONS:")
            print(f"  {instruction}")
            print()

            filename = f"{mode_info['file_prefix']}_{section.lower()}.png"
            filepath = screenshots_dir / filename

            print("CAPTURE STEPS:")
            print("  1. Press Win + Shift + S (opens Snipping Tool)")
            print("  2. Select the area to capture")
            print("  3. Open Paint (or image editor)")
            print("  4. Paste (Ctrl + V)")
            print(f"  5. Save as: {filename}")
            print(f"  6. Location: {screenshots_dir.absolute()}")
            print()

            print(f"[{screenshot_count}/{total_screenshots}] Filename: {filename}")

            wait_for_user()

    # Summary
    clear_screen()
    print_header("SCREENSHOT CAPTURE COMPLETE!")

    print(f"Total screenshots captured: {total_screenshots}")
    print(f"Location: {screenshots_dir.absolute()}")
    print()
    print("CHECKLIST:")
    for mode_info in screenshot_plan:
        for section, _ in mode_info['instructions']:
            filename = f"{mode_info['file_prefix']}_{section.lower()}.png"
            filepath = screenshots_dir / filename
            status = "[OK]" if filepath.exists() else "[  ]"
            print(f"  {status} {filename}")
    print()
    print("Next steps:")
    print("  1. Review all screenshots for quality and completeness")
    print("  2. Retake any that are unclear or missing content")
    print("  3. Run the Word document generator to create the user guide")
    print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScreenshot capture cancelled by user.")
    except Exception as e:
        print(f"\nERROR: {e}")
