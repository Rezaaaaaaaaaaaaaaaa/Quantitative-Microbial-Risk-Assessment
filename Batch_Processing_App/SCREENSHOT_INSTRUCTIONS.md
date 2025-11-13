# Screenshot Capture Instructions

## Automated Method (Recommended)

### Prerequisites
- Python 3.8+ with Streamlit installed
- Selenium and webdriver-manager packages:
  ```bash
  pip install selenium webdriver-manager
  ```
- Chrome browser installed

### Steps

1. **Navigate to Application Directory:**
   ```bash
   cd "C:\Users\moghaddamr\OneDrive - NIWA\Quantitative Microbial Risk Assessment\Batch_Processing_App"
   ```

2. **Run Automated Screenshot Script:**
   ```bash
   capture_screenshots_automated.bat
   ```

3. **Wait for Completion:**
   - Script will start the app
   - Wait 15 seconds for app to load
   - Capture 6 screenshots automatically
   - Stop the app
   - Total time: ~2-3 minutes

4. **Verify Screenshots:**
   - Check `screenshots/` folder
   - Should contain 6 PNG files:
     - 01_home_page_YYYYMMDD_HHMMSS.png
     - 02_batch_scenarios_YYYYMMDD_HHMMSS.png
     - 03_spatial_assessment_YYYYMMDD_HHMMSS.png
     - 04_temporal_assessment_YYYYMMDD_HHMMSS.png
     - 05_treatment_comparison_YYYYMMDD_HHMMSS.png
     - 06_multi_pathogen_YYYYMMDD_HHMMSS.png
   - Plus index.html and manifest.json

---

## Manual Method (If Automated Fails)

### Part 1: Start the App

1. Open Command Prompt / Terminal

2. Navigate to app directory:
   ```bash
   cd "C:\Users\moghaddamr\OneDrive - NIWA\Quantitative Microbial Risk Assessment\Batch_Processing_App\app"
   ```

3. Start Streamlit:
   ```bash
   streamlit run web_app.py
   ```

4. App should open in browser at `http://localhost:8501`

### Part 2: Capture Screenshots

**For each page, follow these steps:**

#### Screenshot 1: Home Page (Production Mode ON)
1. Ensure you're on home page
2. **VERIFY:** Production Mode checkbox is **CHECKED** ✅
3. **VERIFY:** Green "Production Mode Active" message visible
4. **VERIFY:** Pathogen dropdown shows only "Norovirus"
5. Press **Windows Key + Shift + S** (Snipping Tool)
6. Capture entire browser window
7. Save as: `screenshots/01_home_page_production_mode.png`

#### Screenshot 2: Batch Scenarios
1. Select "Batch Scenarios" from sidebar dropdown
2. Click "Use example files" for all three inputs
3. **VERIFY:** Pathogen shows "Norovirus" only
4. Wait for page to fully load
5. Capture screenshot
6. Save as: `screenshots/02_batch_scenarios.png`

#### Screenshot 3: Spatial Assessment
1. Select "Spatial Assessment" from sidebar
2. Click "Use example dilution data"
3. **VERIFY:** Pathogen dropdown shows "Norovirus" only
4. Expand "Advanced Settings" section (optional, shows Hockey Stick parameters)
5. Capture screenshot
6. Save as: `screenshots/03_spatial_assessment.png`

#### Screenshot 4: Temporal Assessment
1. Select "Temporal Assessment" from sidebar
2. Click "Use example monitoring data"
3. **VERIFY:** Pathogen is "Norovirus"
4. Set Frequency: 20 events/year
5. Set Population: 10,000
6. Capture screenshot
7. Save as: `screenshots/04_temporal_assessment.png`

#### Screenshot 5: Treatment Comparison
1. Select "Treatment Comparison" from sidebar
2. Upload or use example treatment scenarios
3. **VERIFY:** Pathogen is "Norovirus"
4. Show multiple treatment rows
5. Capture screenshot
6. Save as: `screenshots/05_treatment_comparison.png`

#### Screenshot 6: Multi-Pathogen (Research Mode)
1. **UNCHECK** "Production Mode" checkbox in sidebar
2. **VERIFY:** Orange warning "Research Mode Active" appears
3. Select "Multi-Pathogen Assessment"
4. **VERIFY:** Pathogen multi-select shows all 6 pathogens
5. **IMPORTANT:** Warning message should be visible
6. Capture screenshot showing warning
7. Save as: `screenshots/06_multi_pathogen_research_mode.png`

#### Screenshot 7 (NEW): Results Example
1. Return to "Temporal Assessment"
2. **RE-ENABLE** Production Mode (checkbox back ON)
3. Click "Run Temporal Assessment"
4. Wait for results to appear
5. Scroll to show results table and compliance status
6. Capture screenshot
7. Save as: `screenshots/07_results_example.png`

#### Screenshot 8 (NEW): Production Mode Status Panel
1. Zoom in on sidebar
2. Capture close-up of:
   - Production Mode checkbox (checked)
   - Green status message
   - Pathogen dropdown (norovirus only)
3. Save as: `screenshots/08_production_mode_detail.png`

### Part 3: Stop the App

1. Return to Command Prompt where Streamlit is running
2. Press **Ctrl + C**
3. Confirm shutdown

---

## Screenshot Quality Guidelines

### Technical Requirements
- **Format:** PNG (lossless)
- **Resolution:** Minimum 1920x1080 browser window
- **Color:** Full color (24-bit RGB)
- **File Size:** Typically 200-500 KB per screenshot

### Content Requirements
- ✅ Entire browser window visible (including URL bar)
- ✅ No personal information in browser (close other tabs)
- ✅ Sidebar fully expanded and visible
- ✅ Main content area not cut off
- ✅ Status messages (Production Mode, warnings) visible
- ✅ No empty/loading states (wait for content to render)

### What to Include
- Navigation sidebar (left)
- Page title and description
- Input forms with example values filled in
- Status indicators (Production Mode panel)
- Dropdown menus showing available options

### What to Avoid
- ❌ Partial screenshots (cut off content)
- ❌ Screenshots of error states (unless documenting errors)
- ❌ Screenshots during page loading
- ❌ Multiple browser tabs visible
- ❌ Personal bookmarks or history visible

---

## Verifying Screenshot Coverage

After capturing, verify you have:

| # | Page | Key Elements Visible | Production Mode | File Name |
|---|------|---------------------|-----------------|-----------|
| 1 | Home | Sidebar navigation, Production Mode ON, norovirus only | ✅ ON | 01_home_page_production_mode.png |
| 2 | Batch Scenarios | Example files loaded, norovirus only | ✅ ON | 02_batch_scenarios.png |
| 3 | Spatial Assessment | Example dilution data, Hockey Stick params | ✅ ON | 03_spatial_assessment.png |
| 4 | Temporal Assessment | Example monitoring data, frequency/population | ✅ ON | 04_temporal_assessment.png |
| 5 | Treatment Comparison | Multiple treatments, norovirus only | ✅ ON | 05_treatment_comparison.png |
| 6 | Multi-Pathogen | Research Mode warning, 6 pathogens visible | ❌ OFF | 06_multi_pathogen_research_mode.png |
| 7 | Results Example | Results table, compliance status, plots | ✅ ON | 07_results_example.png |
| 8 | Production Mode Detail | Close-up of Production Mode panel | ✅ ON | 08_production_mode_detail.png |

**Total Screenshots Needed:** 8

---

## Updating Documentation

After capturing screenshots, update:

1. **TECHNICAL_USER_MANUAL.md** - Replace image paths with new screenshots
2. **USER_GUIDE_STEP_BY_STEP.md** - Update figure references
3. **PRODUCTION_MODE_GUIDE.md** - Add Production Mode detail screenshot

### Find and Replace

Old format:
```markdown
![Home Page](../screenshots/01_home_page_20251105_103639.png)
```

New format:
```markdown
![Home Page](../screenshots/01_home_page_production_mode.png)
```

---

## Troubleshooting

### Issue: Streamlit won't start
**Solution:**
```bash
pip install --upgrade streamlit
streamlit --version
```

### Issue: Selenium can't find Chrome driver
**Solution:**
```bash
pip install --upgrade selenium webdriver-manager
```

### Issue: Screenshots are blank or all the same
**Solution:**
- Increase wait time in script (change `time.sleep(2)` to `time.sleep(5)`)
- Check that app actually loaded in browser before script runs

### Issue: Can't find screenshots folder
**Solution:**
- Screenshots save to: `Batch_Processing_App/screenshots/`
- Check working directory when running script

---

## Contact

For screenshot capture issues, contact:
Reza Moghaddam (reza.moghaddam@niwa.co.nz)

---

**Last Updated:** November 13, 2025
**Next Capture:** After any UI changes or new features added
