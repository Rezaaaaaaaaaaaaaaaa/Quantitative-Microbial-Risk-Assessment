# Automated Screenshot Capture & Report Generation

This guide explains how to automatically capture screenshots of the QMRA web application and insert them into the professional Word report.

---

## Overview

Two Python scripts automate the screenshot workflow:

1. **`capture_app_screenshots.py`** - Captures screenshots of all app pages
2. **`insert_screenshots_to_word.py`** - Inserts screenshots into Word document

Combined, they create a professional report with embedded app interface screenshots.

---

## Prerequisites

### Install Required Packages

```bash
pip install selenium webdriver-manager python-docx
```

**Packages:**
- `selenium` - Browser automation
- `webdriver-manager` - Automatic ChromeDriver management
- `python-docx` - Word document manipulation

### System Requirements

- Google Chrome browser installed
- Streamlit app running on `http://localhost:8502`
- Python 3.8+

---

## Step-by-Step Instructions

### Step 1: Start the Streamlit App

In one terminal, launch the web application:

```bash
streamlit run web_app.py
```

The app will open in your browser at `http://localhost:8502`. Leave this running.

### Step 2: Capture Screenshots

In another terminal, run the screenshot capture script:

```bash
python capture_app_screenshots.py
```

**What happens:**
- Script waits 5 seconds (gives you time to verify app is running)
- Opens Chrome browser (may open new window)
- Navigates to each page of the app
- Captures full-page screenshots
- Saves images to `screenshots/` directory
- Creates `manifest.json` with metadata
- Creates `index.html` preview (optional)

**Output:**
```
screenshots/
├── 01_home_page_YYYYMMDD_HHMMSS.png
├── 02_batch_scenarios_YYYYMMDD_HHMMSS.png
├── 03_spatial_assessment_YYYYMMDD_HHMMSS.png
├── 04_temporal_assessment_YYYYMMDD_HHMMSS.png
├── 05_treatment_comparison_YYYYMMDD_HHMMSS.png
├── 06_multi_pathogen_YYYYMMDD_HHMMSS.png
├── manifest.json
└── index.html
```

**Expected time:** 2-3 minutes (includes browser startup and load times)

### Step 3: Insert into Word Document

Once screenshots are captured, insert them into the report:

```bash
python insert_screenshots_to_word.py
```

**What happens:**
- Reads manifest.json
- Opens `QMRA_Application_Overview.docx`
- Adds new "Appendix: Application Screenshots" page
- Inserts all 6 screenshots with captions and descriptions
- Saves as `QMRA_Application_Overview_with_screenshots.docx`

**Output:**
```
QMRA_Application_Overview_with_screenshots.docx  (2-3 MB with images)
```

---

## What Gets Captured

| # | Page | What It Shows |
|----|------|---------------|
| 1 | Home Page | Main interface and sidebar navigation |
| 2 | Batch Scenarios | Pre-configured scenario selection and data preview |
| 3 | Spatial Assessment | Multi-site risk mapping interface |
| 4 | Temporal Assessment | Time-series analysis interface |
| 5 | Treatment Comparison | Treatment technology comparison interface |
| 6 | Multi-Pathogen | Multi-pathogen evaluation interface |

Each screenshot includes:
- Full page layout
- All UI elements (input fields, buttons, dropdowns)
- Sidebar navigation
- Current state of interface

---

## Output Files

### Screenshot Images
- **Format:** PNG (high quality, full page)
- **Resolution:** 1920×1080 minimum (native browser window size)
- **Location:** `screenshots/` directory
- **Naming:** `NN_page_name_YYYYMMDD_HHMMSS.png`

### Metadata Files

**`manifest.json`**
```json
{
  "captured_at": "2025-11-05T14:30:00",
  "app_url": "http://localhost:8502",
  "total_screenshots": 6,
  "screenshots": [
    {
      "filename": "01_home_page_20251105_143000.png",
      "page": "home_page",
      "description": "Main application interface...",
      "timestamp": "20251105_143000"
    }
  ]
}
```

**`index.html`**
- Viewable preview of all screenshots in browser
- Useful for quick review before inserting into Word

### Word Document

**`QMRA_Application_Overview_with_screenshots.docx`**
- Original 8-section report
- New 9th section: "Appendix: Application Screenshots"
- 6 high-quality embedded images
- Figure captions and descriptions
- Professional formatting with blue theme
- Ready to print or share

---

## Troubleshooting

### Issue: "Manifest not found"
**Solution:** Run `capture_app_screenshots.py` first to create screenshots

### Issue: Chrome browser doesn't open
**Solution:**
- Verify Chrome is installed: `chrome --version`
- Check no other Chrome instances are running
- Run script with administrator privileges

### Issue: App doesn't load in browser
**Solution:**
- Verify Streamlit is running: `streamlit run web_app.py`
- Check URL: http://localhost:8502
- Wait 10+ seconds for app to fully load
- Clear browser cache and refresh

### Issue: Images blurry or cut off
**Solution:**
- Ensure Chrome window is maximized
- Run script with larger monitor/resolution
- Manually resize Chrome window before running script

### Issue: Word document becomes very large (>10 MB)
**Solution:**
- This is normal with embedded images (images ~500 KB each)
- To reduce size: right-click image → Compress Picture
- Or save as PDF instead of DOCX

---

## Advanced Options

### Custom App URL

Edit `capture_app_screenshots.py`:
```python
# Change this line:
capturer = AppScreenshotCapture(
    app_url='http://localhost:8502',  # <-- Your URL here
    output_dir='screenshots'
)
```

### Custom Output Directory

```bash
# Create script and modify:
capturer = AppScreenshotCapture(
    app_url='http://localhost:8502',
    output_dir='my_screenshots'  # <-- Different directory
)
```

### Selective Screenshots

Modify `capturer.run_all()` in the script:
```python
# Capture only specific pages:
capturer.capture_home_page()
capturer.capture_batch_scenarios()
# Skip others...
capturer.create_index_html()
capturer.create_manifest()
```

### Custom Word Document

To insert screenshots into a different Word file:
```bash
python insert_screenshots_to_word.py --doc my_report.docx
```

(Note: Script currently hardcoded; modify for this feature)

---

## Best Practices

### Before Capturing Screenshots

1. **Restart the app** to ensure clean state
2. **Clear browser cache** for fresh rendering
3. **Maximize browser window** for better visibility
4. **Disable notifications** in Chrome to avoid UI clutter
5. **Check internet connection** (not needed for localhost but good practice)

### After Capturing Screenshots

1. **Review `index.html`** before inserting into Word
2. **Check manifest.json** for correct filenames
3. **Verify all 6 images** were captured
4. **Look at images** to ensure they're readable

### Before Sharing Report

1. **Review the Word document** in full-screen view
2. **Check image quality** (not pixelated or blurry)
3. **Verify captions** are accurate
4. **Print to PDF** for final distribution
5. **Compress images** if file size is an issue

---

## Workflow Summary

```
Terminal 1                          Terminal 2
─────────────────────────────────────────────────────────────
$ streamlit run web_app.py    →    App loads at localhost:8502

[App running...]              →    $ python capture_app_screenshots.py

[Screenshots being captured...]     [6 screenshots saved]

[App still running...]         →    $ python insert_screenshots_to_word.py

                                    [Word doc updated with screenshots]
                                    [QMRA_Application_Overview_with_screenshots.docx created]

DONE! Report is ready to share.
```

---

## Example Output

### File Tree After Execution

```
Batch_Processing_App/
├── web_app.py                              (the app)
├── capture_app_screenshots.py              (screenshot script)
├── insert_screenshots_to_word.py           (word insertion script)
├── QMRA_Application_Overview.docx          (original report)
├── QMRA_Application_Overview_with_screenshots.docx  (new report with images)
│
└── screenshots/                            (auto-created)
    ├── 01_home_page_20251105_143000.png
    ├── 02_batch_scenarios_20251105_143015.png
    ├── 03_spatial_assessment_20251105_143030.png
    ├── 04_temporal_assessment_20251105_143045.png
    ├── 05_treatment_comparison_20251105_143100.png
    ├── 06_multi_pathogen_20251105_143115.png
    ├── manifest.json                      (metadata)
    └── index.html                         (preview)
```

---

## Performance Notes

- **Screenshot capture time:** ~30 seconds per page (includes navigation + rendering)
- **Total capture time:** 2-3 minutes for all 6 pages
- **Word insertion time:** 10-30 seconds
- **Total workflow:** 3-4 minutes from start to finish

---

## Support & Tips

### If You Need Different Screenshots
1. Edit `capture_app_screenshots.py`
2. Add custom `navigate_and_capture()` calls
3. Specify custom selectors and wait conditions
4. Re-run script to capture new images

### If You Want to Update Report Later
1. Run `capture_app_screenshots.py` again (overwrites images)
2. Run `insert_screenshots_to_word.py` (creates new Word file)
3. Compare old and new versions

### If Images Look Wrong
- **Blurry:** Chrome window was too small
- **Cut off:** Waited too long between navigation and capture
- **Wrong page:** Navigation selector didn't match current Streamlit version

---

## Next Steps

1. ✓ Install packages: `pip install selenium webdriver-manager python-docx`
2. ✓ Run app: `streamlit run web_app.py`
3. ✓ Capture screenshots: `python capture_app_screenshots.py`
4. ✓ Insert into Word: `python insert_screenshots_to_word.py`
5. ✓ Review: `QMRA_Application_Overview_with_screenshots.docx`
6. ✓ Share: Send the Word document to stakeholders!

---

**Created for NIWA Earth Sciences - QMRA Batch Processing Application**
**Version 1.2.0 | November 2025**
