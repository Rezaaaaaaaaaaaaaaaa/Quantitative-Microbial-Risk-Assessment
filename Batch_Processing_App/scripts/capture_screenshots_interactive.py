#!/usr/bin/env python3
"""
Interactive Screenshot Capture for QMRA App
============================================

Guides you through the app while automatically capturing screenshots.
You navigate, the script captures!
"""

import pyautogui
import time
from pathlib import Path

# Safety feature - move mouse to corner to abort
pyautogui.FAILSAFE = True

class InteractiveScreenshotCapture:
    """Interactive screenshot capture with user guidance."""

    def __init__(self, output_dir='screenshots_final'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.screenshots = []

        print(f"\n[INIT] Screenshots will be saved to:")
        print(f"       {self.output_dir.absolute()}\n")

    def wait_for_user(self, message):
        """Wait for user to press Enter."""
        input(f"\n{message}\n>>> Press ENTER when ready...")

    def capture_screenshot(self, filename, description=''):
        """Capture screenshot of entire screen."""
        try:
            filepath = self.output_dir / filename
            screenshot = pyautogui.screenshot()
            screenshot.save(str(filepath))

            self.screenshots.append({
                'filename': filename,
                'description': description
            })

            print(f"  [OK] Captured: {filename}")
            return filepath
        except Exception as e:
            print(f"  [ERROR] Failed to capture {filename}: {e}")
            return None

    def print_header(self, title):
        """Print formatted header."""
        print("\n" + "="*80)
        print(f"  {title}")
        print("="*80 + "\n")

    def print_step(self, step_num, total, title):
        """Print step header."""
        print(f"\n{'='*80}")
        print(f"STEP {step_num}/{total}: {title}")
        print(f"{'='*80}\n")

    def scroll_instruction(self, position):
        """Instructions for scrolling."""
        if position == "top":
            return "Press Home key or scroll to TOP of page"
        elif position == "middle":
            return "Scroll DOWN to MIDDLE of page (about halfway)"
        elif position == "bottom":
            return "Press End key or scroll to BOTTOM of page"

    def capture_page(self, page_name, file_prefix, step_num, total_steps):
        """Capture a page in 3 sections (top, middle, bottom)."""

        sections = [('top', 'TOP'), ('middle', 'MIDDLE'), ('bottom', 'BOTTOM')]

        for idx, (pos_key, pos_name) in enumerate(sections, 1):
            self.print_step(step_num, total_steps,
                          f"{page_name} - {pos_name} Section")

            print(f"ACTION REQUIRED:")
            print(f"  1. {self.scroll_instruction(pos_key)}")
            print(f"  2. Make sure the browser window is in focus")
            print(f"  3. Press ENTER below")
            print()

            filename = f"{file_prefix}_{pos_key}.png"

            self.wait_for_user(f"Ready to capture {pos_name} section")

            # Give user 2 seconds to release Enter key
            print("  Capturing in 2 seconds...")
            time.sleep(2)

            self.capture_screenshot(filename, f"{page_name} - {pos_name}")

            step_num += 1

        return step_num

    def run_interactive_capture(self):
        """Run interactive screenshot capture session."""

        self.print_header("QMRA APP - INTERACTIVE SCREENSHOT CAPTURE")

        print("INSTRUCTIONS:")
        print("  - Open your browser to http://localhost:8501")
        print("  - Keep the browser window MAXIMIZED")
        print("  - Follow the on-screen instructions")
        print("  - The script will capture screenshots automatically")
        print("  - Move mouse to TOP-LEFT corner to abort (FAILSAFE)")
        print()

        self.wait_for_user("Open browser to http://localhost:8501 and maximize window")

        step = 1
        total_steps = 18

        # ===== HOME PAGE =====
        self.print_header("PART 1/6: HOME PAGE")
        print("ACTION: Ensure you're on the home page")
        print("  - Production Mode should be CHECKED in sidebar")
        self.wait_for_user("Ready to capture Home Page")

        step = self.capture_page("Home Page", "01_home", step, total_steps)

        # ===== BATCH SCENARIOS =====
        self.print_header("PART 2/6: BATCH SCENARIOS")
        print("ACTION: Select 'Batch Scenarios' from dropdown")
        print("  1. Find the 'Assessment Mode' dropdown in the sidebar")
        print("  2. Click it and select 'Batch Scenarios'")
        print("  3. Check 'Use example data' if available")
        print("  4. Wait for data to load")
        self.wait_for_user("Batch Scenarios page loaded and ready")

        step = self.capture_page("Batch Scenarios", "02_batch", step, total_steps)

        # ===== SPATIAL ASSESSMENT =====
        self.print_header("PART 3/6: SPATIAL ASSESSMENT")
        print("ACTION: Select 'Spatial Assessment' from dropdown")
        print("  1. Click Assessment Mode dropdown")
        print("  2. Select 'Spatial Assessment'")
        print("  3. Set Pathogen: norovirus")
        print("  4. Set Exposure Route: Shellfish Consumption")
        print("  5. Check 'Use example dilution data' if available")
        self.wait_for_user("Spatial Assessment configured and ready")

        step = self.capture_page("Spatial Assessment", "03_spatial", step, total_steps)

        # ===== TEMPORAL ASSESSMENT =====
        self.print_header("PART 4/6: TEMPORAL ASSESSMENT")
        print("ACTION: Select 'Temporal Assessment' from dropdown")
        print("  1. Click Assessment Mode dropdown")
        print("  2. Select 'Temporal Assessment'")
        print("  3. Set Pathogen: norovirus")
        print("  4. Set Exposure Route: Shellfish Consumption")
        self.wait_for_user("Temporal Assessment configured and ready")

        step = self.capture_page("Temporal Assessment", "04_temporal", step, total_steps)

        # ===== TREATMENT COMPARISON =====
        self.print_header("PART 5/6: TREATMENT COMPARISON")
        print("ACTION: Select 'Treatment Comparison' from dropdown")
        print("  1. Click Assessment Mode dropdown")
        print("  2. Select 'Treatment Comparison'")
        print("  3. Set Pathogen: norovirus")
        print("  4. Set Exposure Route: Shellfish Consumption")
        self.wait_for_user("Treatment Comparison configured and ready")

        step = self.capture_page("Treatment Comparison", "05_treatment", step, total_steps)

        # ===== MULTI-PATHOGEN =====
        self.print_header("PART 6/6: MULTI-PATHOGEN ASSESSMENT")
        print("ACTION: Select 'Multi-Pathogen Assessment' from dropdown")
        print("  1. Click Assessment Mode dropdown")
        print("  2. Select 'Multi-Pathogen Assessment'")
        print("  3. Note: In Production Mode, only norovirus is available")
        self.wait_for_user("Multi-Pathogen Assessment loaded and ready")

        step = self.capture_page("Multi-Pathogen Assessment", "06_multipathogen", step, total_steps)

        # ===== SUMMARY =====
        self.print_header("CAPTURE COMPLETE!")

        print(f"Total screenshots captured: {len(self.screenshots)}")
        print(f"Location: {self.output_dir.absolute()}\n")

        print("Captured files:")
        for i, shot in enumerate(self.screenshots, 1):
            print(f"  {i:2d}. {shot['filename']}")

        print("\n" + "="*80)
        print("NEXT STEP: Update Word document with these screenshots")
        print("="*80 + "\n")


def main():
    """Main entry point."""

    capturer = InteractiveScreenshotCapture(output_dir='../screenshots_final')

    try:
        capturer.run_interactive_capture()
    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Screenshot capture stopped by user.")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
