#!/usr/bin/env python3
"""
Enhanced Screenshot Capture for QMRA Web App
=============================================

Captures FULL PAGE screenshots including content below the fold.
Takes multiple screenshots per page by scrolling.

Usage:
    1. Start the Streamlit app: streamlit run web_app.py
    2. Run this script: python capture_app_screenshots_full.py
    3. Screenshots saved to: screenshots_full/ directory
"""

import time
import os
from pathlib import Path
from datetime import datetime

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
except ImportError:
    print("ERROR: Required packages not found!")
    print("Install with: pip install selenium webdriver-manager")
    exit(1)


class EnhancedScreenshotCapture:
    """Captures comprehensive screenshots with scrolling for full page content."""

    def __init__(self, app_url='http://localhost:8501', output_dir='screenshots_full'):
        self.app_url = app_url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Setup Chrome driver with larger window
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-notifications')
        options.add_argument('--window-size=1920,1080')

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

        # Maximize window
        self.driver.maximize_window()
        time.sleep(1)

        self.screenshots = []
        print(f"[INIT] Screenshot output directory: {self.output_dir.absolute()}")

    def wait_for_streamlit(self, timeout=15):
        """Wait for Streamlit to finish loading."""
        try:
            # Wait for main content to be present
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "main"))
            )
            time.sleep(2)  # Extra wait for dynamic content
            return True
        except:
            print("[WARN] Streamlit content not fully loaded")
            return False

    def get_page_height(self):
        """Get total scrollable height of the page."""
        return self.driver.execute_script("return document.body.scrollHeight")

    def scroll_to_position(self, position):
        """Scroll to specific position."""
        self.driver.execute_script(f"window.scrollTo(0, {position});")
        time.sleep(1)  # Wait for content to render

    def capture_screenshot(self, filename, description=''):
        """Capture and save screenshot."""
        try:
            filepath = self.output_dir / filename
            self.driver.save_screenshot(str(filepath))

            self.screenshots.append({
                'filename': filename,
                'description': description,
                'timestamp': datetime.now().strftime('%Y%m%d_%H%M%S')
            })

            print(f"[OK] Captured: {filename}")
            return filepath
        except Exception as e:
            print(f"[ERROR] Failed to capture {filename}: {e}")
            return None

    def capture_full_page(self, page_name, description='', scroll_positions=None):
        """
        Capture multiple screenshots of a page at different scroll positions.

        Args:
            page_name: Base name for the page
            description: Description of the page
            scroll_positions: List of positions like ['top', 'middle', 'bottom']
                            or None to auto-detect
        """
        if scroll_positions is None:
            scroll_positions = ['top', 'middle', 'bottom']

        # Scroll to top first
        self.scroll_to_position(0)
        time.sleep(1)

        page_height = self.get_page_height()
        window_height = self.driver.execute_script("return window.innerHeight")

        print(f"\n[INFO] Page: {page_name}")
        print(f"  Total height: {page_height}px")
        print(f"  Window height: {window_height}px")

        captured = []

        for position_name in scroll_positions:
            if position_name == 'top':
                scroll_pos = 0
            elif position_name == 'middle':
                scroll_pos = max(0, (page_height - window_height) // 2)
            elif position_name == 'bottom':
                scroll_pos = max(0, page_height - window_height)
            else:
                continue

            # Only capture if there's content at this position
            if page_height <= window_height and position_name != 'top':
                print(f"  [SKIP] {position_name} - Page fits in one screen")
                continue

            self.scroll_to_position(scroll_pos)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{page_name}_{position_name}_{timestamp}.png"

            desc = f"{description} - {position_name.title()} section"
            filepath = self.capture_screenshot(filename, desc)

            if filepath:
                captured.append(filepath)

        return captured

    def navigate_to_page(self, path, page_name):
        """Navigate to a specific page and wait for it to load."""
        try:
            url = f"{self.app_url}{path}"
            print(f"\n[NAV] Navigating to: {url}")
            self.driver.get(url)

            # Wait for Streamlit to load
            self.wait_for_streamlit()

            # Scroll to top
            self.scroll_to_position(0)

            return True
        except Exception as e:
            print(f"[ERROR] Navigation failed for {page_name}: {e}")
            return False

    def capture_home_page(self):
        """Capture home/welcome page."""
        print("\n" + "="*80)
        print("[CAPTURE] HOME PAGE")
        print("="*80)

        if self.navigate_to_page('/', 'home_page'):
            self.capture_full_page(
                '01_home_page',
                'Main application interface with sidebar and welcome message'
            )

    def capture_batch_scenarios(self):
        """Capture Batch Scenarios page with all sections."""
        print("\n" + "="*80)
        print("[CAPTURE] BATCH SCENARIOS")
        print("="*80)

        if self.navigate_to_page('/', 'batch_scenarios'):
            # Select Batch Scenarios from dropdown
            try:
                # Wait a bit for page to load
                time.sleep(3)

                # Capture initial view
                self.capture_full_page(
                    '02_batch_scenarios',
                    'Batch Scenarios Assessment - Overview and configuration',
                    ['top', 'middle', 'bottom']
                )

            except Exception as e:
                print(f"[ERROR] Failed to interact with Batch Scenarios: {e}")

    def capture_spatial_assessment(self):
        """Capture Spatial Assessment page."""
        print("\n" + "="*80)
        print("[CAPTURE] SPATIAL ASSESSMENT")
        print("="*80)

        if self.navigate_to_page('/', 'spatial'):
            time.sleep(3)
            self.capture_full_page(
                '03_spatial_assessment',
                'Spatial Risk Assessment - Multi-site evaluation',
                ['top', 'middle', 'bottom']
            )

    def capture_temporal_assessment(self):
        """Capture Temporal Assessment page."""
        print("\n" + "="*80)
        print("[CAPTURE] TEMPORAL ASSESSMENT")
        print("="*80)

        if self.navigate_to_page('/', 'temporal'):
            time.sleep(3)
            self.capture_full_page(
                '04_temporal_assessment',
                'Temporal Risk Assessment - Time series analysis',
                ['top', 'middle', 'bottom']
            )

    def capture_treatment_comparison(self):
        """Capture Treatment Comparison page."""
        print("\n" + "="*80)
        print("[CAPTURE] TREATMENT COMPARISON")
        print("="*80)

        if self.navigate_to_page('/', 'treatment'):
            time.sleep(3)
            self.capture_full_page(
                '05_treatment_comparison',
                'Treatment Comparison - Side-by-side evaluation',
                ['top', 'middle', 'bottom']
            )

    def capture_multi_pathogen(self):
        """Capture Multi-Pathogen Assessment page."""
        print("\n" + "="*80)
        print("[CAPTURE] MULTI-PATHOGEN ASSESSMENT")
        print("="*80)

        if self.navigate_to_page('/', 'multipathogen'):
            time.sleep(3)
            self.capture_full_page(
                '06_multi_pathogen',
                'Multi-Pathogen Assessment - Comparative analysis',
                ['top', 'middle', 'bottom']
            )

    def create_index_html(self):
        """Create HTML index of all screenshots."""
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>QMRA App Screenshots - Full Page</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        h1 { color: #1f77b4; }
        .screenshot {
            background: white;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .screenshot img {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 3px;
            margin: 10px 0;
        }
        .screenshot h3 { color: #1f77b4; margin: 0 0 10px 0; }
        .screenshot p { color: #555; margin: 5px 0; }
        .meta { font-size: 0.9em; color: #999; }
    </style>
</head>
<body>
    <h1>QMRA Batch Processing Web Application - Full Page Screenshots</h1>
    <p><strong>Screenshots captured:</strong> """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
    <p><strong>Total screenshots:</strong> """ + str(len(self.screenshots)) + """</p>
    <hr/>
"""

        for i, shot in enumerate(self.screenshots, 1):
            html_content += f"""
    <div class="screenshot">
        <h3>{i}. {shot['filename']}</h3>
        <p>{shot['description']}</p>
        <img src="{shot['filename']}" alt="{shot['filename']}">
        <p class="meta">File: {shot['filename']} | Captured: {shot['timestamp']}</p>
    </div>
"""

        html_content += """
</body>
</html>
"""

        index_path = self.output_dir / 'index.html'
        with open(index_path, 'w') as f:
            f.write(html_content)

        print(f"\n[OK] Index created: {index_path}")
        return index_path

    def run_all(self):
        """Capture all pages with full content."""
        print("\n" + "="*80)
        print("QMRA APP ENHANCED SCREENSHOT CAPTURE")
        print("Capturing FULL PAGE content with scrolling")
        print("="*80)
        print(f"App URL: {self.app_url}")
        print(f"Output: {self.output_dir.absolute()}")
        print("="*80)

        try:
            # Load app first
            self.driver.get(self.app_url)
            time.sleep(5)  # Wait for initial load

            # Capture all pages
            self.capture_home_page()
            self.capture_batch_scenarios()
            self.capture_spatial_assessment()
            self.capture_temporal_assessment()
            self.capture_treatment_comparison()
            self.capture_multi_pathogen()

            # Create index
            self.create_index_html()

            print("\n" + "="*80)
            print(f"✓ CAPTURE COMPLETE: {len(self.screenshots)} screenshots")
            print("="*80)
            print(f"\nScreenshots saved to: {self.output_dir.absolute()}")
            print(f"View index: {(self.output_dir / 'index.html').absolute()}")

        except Exception as e:
            print(f"[ERROR] Capture failed: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.driver.quit()


def main():
    """Main entry point."""

    print("\n[CHECK] Verifying Streamlit app is running...")
    print("Expected URL: http://localhost:8501")
    print("\nIf app is not running, start it in another terminal:")
    print("  cd Batch_Processing_App/app")
    print("  streamlit run web_app.py")
    print("\nStarting enhanced capture in 5 seconds...\n")

    time.sleep(5)

    # Create capturer and run
    capturer = EnhancedScreenshotCapture(
        app_url='http://localhost:8501',
        output_dir='../screenshots_full'
    )

    capturer.run_all()


if __name__ == '__main__':
    main()
