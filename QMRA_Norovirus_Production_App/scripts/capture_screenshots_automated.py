#!/usr/bin/env python3
"""
Automated Screenshot Capture for QMRA Web App - Streamlit-Aware
================================================================

Properly interacts with Streamlit UI elements to capture comprehensive screenshots.
"""

import time
from pathlib import Path
from datetime import datetime

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
except ImportError:
    print("ERROR: Required packages not found!")
    print("Install with: pip install selenium webdriver-manager")
    exit(1)


class StreamlitScreenshotCapture:
    """Automated screenshot capture for Streamlit apps."""

    def __init__(self, app_url='http://localhost:8501', output_dir='screenshots_final'):
        self.app_url = app_url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Setup Chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-notifications')
        options.add_argument('--window-size=1920,1080')

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()
        time.sleep(1)

        self.screenshots = []
        print(f"[INIT] Output directory: {self.output_dir.absolute()}")

    def wait_for_streamlit(self, timeout=10):
        """Wait for Streamlit to finish loading."""
        try:
            # Wait for the stApp div (main Streamlit container)
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='stApp']"))
            )
            time.sleep(2)  # Extra wait for dynamic content
            return True
        except Exception as e:
            print(f"[WARN] Streamlit not fully loaded: {e}")
            return False

    def find_and_click_dropdown(self, placeholder_text):
        """Find and click a Streamlit selectbox dropdown."""
        try:
            # Find the selectbox by its aria-label or text
            selects = self.driver.find_elements(By.CSS_SELECTOR, "select")

            for select in selects:
                # Click to open dropdown
                select.click()
                time.sleep(0.5)

                # Find option by text
                options = select.find_elements(By.TAG_NAME, "option")
                for option in options:
                    if placeholder_text.lower() in option.text.lower():
                        option.click()
                        time.sleep(2)  # Wait for page to update
                        print(f"[OK] Selected: {placeholder_text}")
                        return True

            print(f"[WARN] Could not find dropdown option: {placeholder_text}")
            return False

        except Exception as e:
            print(f"[ERROR] Failed to interact with dropdown: {e}")
            return False

    def scroll_to_position(self, position):
        """Scroll to specific position in pixels."""
        self.driver.execute_script(f"window.scrollTo({{top: {position}, behavior: 'smooth'}});")
        time.sleep(1.5)

    def get_scroll_positions(self):
        """Calculate scroll positions for top, middle, bottom."""
        total_height = self.driver.execute_script("return document.body.scrollHeight")
        window_height = self.driver.execute_script("return window.innerHeight")

        if total_height <= window_height:
            # Page fits in one screen
            return {'top': 0}

        positions = {
            'top': 0,
            'middle': max(0, (total_height - window_height) // 2),
            'bottom': max(0, total_height - window_height)
        }

        return positions

    def capture_screenshot(self, filename, description=''):
        """Capture and save screenshot."""
        try:
            filepath = self.output_dir / filename
            self.driver.save_screenshot(str(filepath))

            self.screenshots.append({
                'filename': filename,
                'description': description
            })

            print(f"  [CAPTURED] {filename}")
            return filepath
        except Exception as e:
            print(f"  [ERROR] Failed: {e}")
            return None

    def capture_page_sections(self, page_name, file_prefix):
        """Capture top, middle, and bottom sections of current page."""
        print(f"\n[PAGE] {page_name}")

        positions = self.get_scroll_positions()
        captured = []

        for pos_name, pos_value in positions.items():
            self.scroll_to_position(pos_value)
            filename = f"{file_prefix}_{pos_name}.png"
            desc = f"{page_name} - {pos_name.title()} section"

            filepath = self.capture_screenshot(filename, desc)
            if filepath:
                captured.append(filepath)

        return captured

    def ensure_production_mode(self):
        """Ensure Production Mode checkbox is checked."""
        try:
            # Find Production Mode checkbox
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")

            for checkbox in checkboxes:
                # Look for the checkbox in the sidebar
                parent = checkbox.find_element(By.XPATH, "./ancestor::div[@data-testid='stSidebar']")
                if parent:
                    # This is in the sidebar
                    if not checkbox.is_selected():
                        checkbox.click()
                        time.sleep(1)
                        print("[OK] Production Mode enabled")
                    return True

            print("[INFO] Production Mode checkbox not found (may already be set)")
            return True

        except Exception as e:
            print(f"[WARN] Could not verify Production Mode: {e}")
            return True

    def capture_home_page(self):
        """Capture home/welcome page."""
        print("\n" + "="*80)
        print("[1/6] HOME PAGE")
        print("="*80)

        self.driver.get(self.app_url)
        self.wait_for_streamlit()
        self.ensure_production_mode()

        self.capture_page_sections("Home Page", "01_home")

    def capture_batch_scenarios(self):
        """Capture Batch Scenarios page."""
        print("\n" + "="*80)
        print("[2/6] BATCH SCENARIOS")
        print("="*80)

        # Select from dropdown
        if self.find_and_click_dropdown("Batch Scenarios"):
            time.sleep(2)

            # Try to check "Use example data" checkbox
            try:
                checkboxes = self.driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
                for checkbox in checkboxes:
                    label_text = checkbox.find_element(By.XPATH, "./following-sibling::div").text
                    if "example" in label_text.lower():
                        if not checkbox.is_selected():
                            checkbox.click()
                            time.sleep(1)
                        break
            except:
                pass

            self.capture_page_sections("Batch Scenarios", "02_batch")

    def capture_spatial_assessment(self):
        """Capture Spatial Assessment page."""
        print("\n" + "="*80)
        print("[3/6] SPATIAL ASSESSMENT")
        print("="*80)

        if self.find_and_click_dropdown("Spatial Assessment"):
            time.sleep(2)

            # Try to select norovirus and shellfish
            self.find_and_click_dropdown("norovirus")
            time.sleep(1)
            self.find_and_click_dropdown("Shellfish")
            time.sleep(1)

            self.capture_page_sections("Spatial Assessment", "03_spatial")

    def capture_temporal_assessment(self):
        """Capture Temporal Assessment page."""
        print("\n" + "="*80)
        print("[4/6] TEMPORAL ASSESSMENT")
        print("="*80)

        if self.find_and_click_dropdown("Temporal Assessment"):
            time.sleep(2)
            self.find_and_click_dropdown("norovirus")
            time.sleep(1)
            self.find_and_click_dropdown("Shellfish")
            time.sleep(1)

            self.capture_page_sections("Temporal Assessment", "04_temporal")

    def capture_treatment_comparison(self):
        """Capture Treatment Comparison page."""
        print("\n" + "="*80)
        print("[5/6] TREATMENT COMPARISON")
        print("="*80)

        if self.find_and_click_dropdown("Treatment Comparison"):
            time.sleep(2)
            self.find_and_click_dropdown("norovirus")
            time.sleep(1)

            self.capture_page_sections("Treatment Comparison", "05_treatment")

    def capture_multi_pathogen(self):
        """Capture Multi-Pathogen Assessment page."""
        print("\n" + "="*80)
        print("[6/6] MULTI-PATHOGEN ASSESSMENT")
        print("="*80)

        if self.find_and_click_dropdown("Multi-Pathogen Assessment"):
            time.sleep(2)

            self.capture_page_sections("Multi-Pathogen Assessment", "06_multipathogen")

    def create_summary(self):
        """Create summary of captured screenshots."""
        print("\n" + "="*80)
        print("CAPTURE SUMMARY")
        print("="*80)
        print(f"\nTotal screenshots: {len(self.screenshots)}")
        print(f"Location: {self.output_dir.absolute()}\n")

        print("Captured files:")
        for i, shot in enumerate(self.screenshots, 1):
            print(f"  {i:2d}. {shot['filename']}")

        print("\n" + "="*80)
        print("NEXT STEP: Update Word document with these screenshots")
        print("="*80)

    def run_all(self):
        """Capture all screenshots."""
        print("\n" + "="*80)
        print("QMRA APP - AUTOMATED SCREENSHOT CAPTURE")
        print("="*80)
        print(f"App URL: {self.app_url}")
        print(f"Output: {self.output_dir.absolute()}")
        print("\nCapturing 18 screenshots (6 pages × 3 sections each)...")
        print("="*80)

        try:
            self.capture_home_page()
            self.capture_batch_scenarios()
            self.capture_spatial_assessment()
            self.capture_temporal_assessment()
            self.capture_treatment_comparison()
            self.capture_multi_pathogen()

            self.create_summary()

        except Exception as e:
            print(f"\n[ERROR] Capture failed: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print("\n[CLEANUP] Closing browser...")
            self.driver.quit()
            print("[DONE]")


def main():
    """Main entry point."""

    print("\n[CHECK] Verifying Streamlit app is running at http://localhost:8501")
    print("If not running, start it with: streamlit run web_app.py")
    print("\nStarting capture in 5 seconds...\n")

    time.sleep(5)

    # Run capture
    capturer = StreamlitScreenshotCapture(
        app_url='http://localhost:8501',
        output_dir='../screenshots_final'
    )

    capturer.run_all()


if __name__ == '__main__':
    main()
