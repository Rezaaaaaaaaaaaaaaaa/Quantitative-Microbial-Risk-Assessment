# QMRA Demo Screenshot Capture Checklist

## Setup
- [ ] Application is running at http://localhost:8501
- [ ] screenshots_example/ folder exists
- [ ] You have a screenshot tool ready (Win+Shift+S)

## Demo 1: Spatial Risk Assessment

### Step 1: Select Mode
- [ ] Navigate to http://localhost:8501
- [ ] In sidebar, select "Spatial Assessment" from dropdown
- [ ] **Capture**: `01_select_spatial_mode.png`
  - Include: Full sidebar showing dropdown
  - Quality check: Dropdown text is clear

### Step 2: Upload Data
- [ ] Click "Browse files" in dilution data section
- [ ] Navigate to: `Batch_Processing_App/input_data/dilution_data/`
- [ ] Select: `spatial_dilution_6_sites.csv`
- [ ] Wait for data preview to appear
- [ ] **Capture**: `02_upload_dilution_data.png`
  - Include: Upload widget + data preview table
  - Quality check: Can see Site_ID, Distance_m, Dilution_Factor columns

### Step 3: Configure Parameters
- [ ] Fill in all parameters in sidebar:
  ```
  Pathogen: Norovirus
  Effluent Concentration: 1540000 (or 1.54e6)
  Treatment LRV: 3.0
  Exposure Route: Primary Contact
  Exposure Volume: 50
  Exposure Frequency: 20
  Population: 10000
  Monte Carlo Iterations: 10000
  ```
- [ ] **Capture**: `03_configure_parameters.png`
  - Include: Full sidebar with all fields visible
  - Quality check: All values are readable

### Step 4: Run Assessment
- [ ] Scroll to bottom of sidebar
- [ ] Click "Run Spatial Assessment" button
- [ ] **Capture**: `04_run_assessment.png`
  - Include: Run button (ideally with processing spinner or success message)
  - Quality check: Button text is clear

### Step 5: View Results
- [ ] Wait for processing to complete
- [ ] Scroll to results table
- [ ] **Capture**: `05_results_table.png`
  - Include: Complete results table showing all sites
  - Quality check: All columns visible (may need wide screenshot)

### Step 6: View Visualizations
- [ ] Click on "Risk Overview" tab
- [ ] **Capture**: `06_visualizations.png`
  - Include: Chart with axes and labels
  - Quality check: Chart is clear and readable

### Step 7: Download Options
- [ ] Scroll to download section
- [ ] Expand "Download Individual Plots" if collapsed
- [ ] **Capture**: `07_download_options.png`
  - Include: All download buttons
  - Quality check: Button text is readable

## Demo 2: Treatment Comparison

### Step 8: Treatment Comparison Mode
- [ ] In sidebar, select "Treatment Comparison" from dropdown
- [ ] Upload current treatment file:
  - Navigate to: `Batch_Processing_App/input_data/treatment_scenarios/`
  - Select: `secondary_treatment.yaml`
- [ ] Upload proposed treatment file:
  - From same directory
  - Select: `advanced_uv_treatment.yaml`
- [ ] **Capture**: `08_treatment_comparison.png`
  - Include: Both file upload sections with files loaded
  - Quality check: File names visible

### Step 9: Comparison Results
- [ ] Configure common parameters (same as Demo 1)
- [ ] Click "Run Treatment Comparison"
- [ ] Wait for results
- [ ] **Capture**: `09_comparison_results.png`
  - Include: Comparison table showing both treatments
  - Quality check: LRV values and risk differences are clear

## Demo 3: Batch Scenarios

### Step 10: Batch Upload
- [ ] In sidebar, select "Batch Scenarios" from dropdown
- [ ] Click "Browse files"
- [ ] Navigate to: `Batch_Processing_App/input_data/batch_scenarios/`
- [ ] Select: `master_batch_scenarios.csv`
- [ ] Wait for preview
- [ ] **Capture**: `10_batch_scenarios.png`
  - Include: Upload widget + scenario preview
  - Quality check: Can see scenario names and parameters

### Step 11: Batch Results
- [ ] Click "Run Batch Assessment"
- [ ] Wait for all scenarios to process
- [ ] Scroll through results table
- [ ] **Capture**: `11_batch_results.png`
  - Include: Results showing multiple scenarios
  - Quality check: Scenario names, risk values, compliance status visible
  - Note: May need to capture in parts if table is very large

## Final Checklist
- [ ] All 11 screenshots captured
- [ ] Files saved to screenshots_example/ folder
- [ ] Filenames match exactly (case-sensitive)
- [ ] All screenshots are clear and readable
- [ ] No browser chrome/toolbars in screenshots (clean capture)
- [ ] File sizes are reasonable (< 2MB each)

## File Verification
Run this command to check all files are present:
```bash
cd "screenshots_example"
ls -1 *.png
```

Expected output:
```
01_select_spatial_mode.png
02_upload_dilution_data.png
03_configure_parameters.png
04_run_assessment.png
05_results_table.png
06_visualizations.png
07_download_options.png
08_treatment_comparison.png
09_comparison_results.png
10_batch_scenarios.png
11_batch_results.png
```

## Next Steps
1. Review all screenshots for quality
2. Open `QMRA_Simple_Demo_NO_TEMPLATE.docx`
3. Replace screenshot placeholders with actual images
4. Copy content to official NIWA template
5. Final review and approval

---
**Date Completed**: _________________
**Captured By**: _________________
**Review By**: _________________
