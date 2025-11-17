#!/usr/bin/env python3
"""
Automated Screenshot Capture for QMRA Web App
==============================================

Captures screenshots of different app pages for documentation/reports.
Requires: selenium, webdriver-manager

Usage:
    1. Start the Streamlit app in another terminal:
       streamlit run web_app.py

    2. Run this script:
       python capture_app_screenshots.py

    3. Screenshots saved to: screenshots/ directory
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
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
except ImportError:
    print("ERROR: Required packages not found!")
    print("Install with: pip install selenium webdriver-manager")
    exit(1)


class AppScreenshotCapture:
    """Captures screenshots of Streamlit app pages."""

    def __init__(self, app_url='http://localhost:8501', output_dir='screenshots'):
        self.app_url = app_url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Setup Chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-notifications')

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

        self.screenshots = []
        print(f"[INIT] Screenshot output directory: {self.output_dir.absolute()}")

    def wait_for_element(self, selector, timeout=10):
        """Wait for element to be present."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            time.sleep(1)  # Extra wait for rendering
            return True
        except:
            return False

    def scroll_to_bottom(self):
        """Scroll to bottom of page."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)

    def capture_screenshot(self, page_name, description=''):
        """Capture and save screenshot."""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{len(self.screenshots)+1:02d}_{page_name}_{timestamp}.png"
            filepath = self.output_dir / filename

            self.driver.save_screenshot(str(filepath))
            self.screenshots.append({
                'filename': filename,
                'page': page_name,
                'description': description,
                'timestamp': timestamp
            })

            print(f"[OK] Captured: {page_name} -> {filename}")
            return filepath
        except Exception as e:
            print(f"[ERROR] Failed to capture {page_name}: {e}")
            return None

    def navigate_and_capture(self, path, page_name, description='', wait_selector=None):
        """Navigate to path and capture screenshot."""
        try:
            self.driver.get(f"{self.app_url}{path}")

            if wait_selector:
                if self.wait_for_element(wait_selector):
                    print(f"[WAIT] Element loaded for {page_name}")
                else:
                    print(f"[WARN] Element not found for {page_name}, proceeding anyway")
            else:
                time.sleep(2)  # Default wait

            self.scroll_to_bottom()
            self.capture_screenshot(page_name, description)

        except Exception as e:
            print(f"[ERROR] Navigation failed for {page_name}: {e}")

    def capture_home_page(self):
        """Capture main landing page."""
        print("\n[CAPTURE] Home Page")
        self.navigate_and_capture(
            '/',
            'home_page',
            'Main application interface with sidebar navigation',
            '[data-testid="stSidebar"]'
        )

    def capture_batch_scenarios(self):
        """Capture Batch Scenarios page."""
        print("\n[CAPTURE] Batch Scenarios Page")
        self.navigate_and_capture(
            '/?page=Batch%20Scenarios',
            'batch_scenarios',
            'Batch processing with 15 pre-configured scenarios',
            '[data-testid="stTabs"]'
        )

    def capture_spatial_assessment(self):
        """Capture Spatial Assessment page."""
        print("\n[CAPTURE] Spatial Assessment Page")
        self.navigate_and_capture(
            '/?page=Spatial%20Assessment',
            'spatial_assessment',
            'Multi-site risk assessment with dilution factors',
            'select'
        )

    def capture_temporal_assessment(self):
        """Capture Temporal Assessment page."""
        print("\n[CAPTURE] Temporal Assessment Page")
        self.navigate_and_capture(
            '/?page=Temporal%20Assessment',
            'temporal_assessment',
            'Time-series risk analysis from monitoring data',
            'select'
        )

    def capture_treatment_comparison(self):
        """Capture Treatment Comparison page."""
        print("\n[CAPTURE] Treatment Comparison Page")
        self.navigate_and_capture(
            '/?page=Treatment%20Comparison',
            'treatment_comparison',
            'Compare multiple treatment technologies',
            'select'
        )

    def capture_multi_pathogen(self):
        """Capture Multi-Pathogen Assessment page."""
        print("\n[CAPTURE] Multi-Pathogen Assessment Page")
        self.navigate_and_capture(
            '/?page=Multi-Pathogen%20Assessment',
            'multi_pathogen',
            'Evaluate multiple pathogens simultaneously',
            '[data-testid="stMultiSelect"]'
        )

    def create_index_html(self):
        """Create HTML index of all screenshots."""
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>QMRA App Screenshots</title>
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
        }
        .screenshot h3 { color: #1f77b4; margin: 0 0 10px 0; }
        .screenshot p { color: #555; margin: 5px 0; }
        .meta { font-size: 0.9em; color: #999; }
    </style>
</head>
<body>
    <h1>QMRA Batch Processing Web Application</h1>
    <p><strong>Screenshots captured:</strong> """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
    <hr/>
"""

        for i, shot in enumerate(self.screenshots, 1):
            html_content += f"""
    <div class="screenshot">
        <h3>{i}. {shot['page'].replace('_', ' ').title()}</h3>
        <p>{shot['description']}</p>
        <img src="{shot['filename']}" alt="{shot['page']}">
        <p class="meta">File: {shot['filename']}</p>
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

    def create_manifest(self):
        """Create JSON manifest of screenshots."""
        import json

        manifest = {
            'captured_at': datetime.now().isoformat(),
            'app_url': self.app_url,
            'total_screenshots': len(self.screenshots),
            'screenshots': self.screenshots
        }

        manifest_path = self.output_dir / 'manifest.json'
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        print(f"[OK] Manifest created: {manifest_path}")

    def run_all(self):
        """Capture all pages."""
        print("\n" + "="*80)
        print("QMRA APP SCREENSHOT CAPTURE")
        print("="*80)
        print(f"App URL: {self.app_url}")
        print(f"Output: {self.output_dir.absolute()}")
        print("="*80)

        try:
            self.driver.get(self.app_url)
            time.sleep(3)  # Wait for app to fully load

            # Capture all pages
            self.capture_home_page()
            self.capture_batch_scenarios()
            self.capture_spatial_assessment()
            self.capture_temporal_assessment()
            self.capture_treatment_comparison()
            self.capture_multi_pathogen()

            # Create index and manifest
            self.create_index_html()
            self.create_manifest()

            print("\n" + "="*80)
            print(f"CAPTURE COMPLETE: {len(self.screenshots)} screenshots")
            print("="*80)
            print(f"\nScreenshots saved to: {self.output_dir.absolute()}")
            print(f"View index: {(self.output_dir / 'index.html').absolute()}")
            print("\nYou can now add these images to your Word document!")

        except Exception as e:
            print(f"[ERROR] Capture failed: {e}")
        finally:
            self.driver.quit()


def main():
    """Main entry point."""

    # Check if app is running
    print("\n[CHECK] Verifying Streamlit app is running...")
    print("Expected URL: http://localhost:8501")
    print("\nIf app is not running, start it in another terminal:")
    print("  cd app")
    print("  streamlit run web_app.py")
    print("\nStarting capture in 5 seconds...\n")

    time.sleep(5)

    # Create capturer and run
    capturer = AppScreenshotCapture(
        app_url='http://localhost:8501',
        output_dir='../screenshots'
    )

    capturer.run_all()


if __name__ == '__main__':
    main()
