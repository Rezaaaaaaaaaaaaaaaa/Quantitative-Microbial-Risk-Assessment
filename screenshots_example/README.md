# Screenshot Capture Guide for QMRA Demo

This folder will contain screenshots of the QMRA Batch Processing Web Application.

## Required Screenshots

### Demo 1: Spatial Risk Assessment

1. **01_select_spatial_mode.png**
   - Navigate to: http://localhost:8501
   - Show: Main interface with sidebar
   - Highlight: Assessment mode dropdown with "Spatial Assessment" selected
   - Capture: Full screen or main content area

2. **02_upload_dilution_data.png**
   - Show: File upload section
   - Action: Upload spatial_dilution_6_sites.csv
   - Highlight: Data preview table showing Site_ID, Distance, Dilution_Factor
   - Capture: File upload widget + preview

3. **03_configure_parameters.png**
   - Show: Complete sidebar with all parameters filled in:
     * Pathogen: Norovirus
     * Effluent Concentration: 1.54×10⁶
     * Treatment LRV: 3.0
     * Exposure Route: Primary Contact
     * Exposure Volume: 50 mL
     * Frequency: 20 events/year
     * Population: 10,000
     * Iterations: 10,000
   - Capture: Full sidebar configuration

4. **04_run_assessment.png**
   - Show: "Run Spatial Assessment" button
   - Capture: Button area, ideally with processing message or spinner
   - Alternative: Success message after completion

5. **05_results_table.png**
   - Show: Complete results table with all sites
   - Columns visible: Site_ID, Distance, Annual_Risk_Mean, Annual_Risk_Median,
     Annual_Risk_95th, Illness_Risk, Expected_Cases, Compliance_Status
   - Capture: Full results table (may need to scroll/capture in parts)

6. **06_visualizations.png**
   - Show: Visualization tabs area
   - Select: "Risk Overview" tab
   - Display: Bar chart showing risk by site
   - Capture: Chart with axes labels and legend visible

7. **07_download_options.png**
   - Show: Download buttons section
   - Buttons visible:
     * Download Full CSV
     * Download All (ZIP)
     * Generate PDF Report
     * Download Individual Plots (if expanded)
   - Capture: Complete download section

### Demo 2: Treatment Comparison

8. **08_treatment_comparison.png**
   - Navigate to: Treatment Comparison mode
   - Show: File upload sections for both treatments
   - Files uploaded:
     * Current: secondary_treatment.yaml
     * Proposed: advanced_uv_treatment.yaml
   - Capture: Treatment comparison interface

9. **09_comparison_results.png**
   - Show: Side-by-side comparison table
   - Columns: Treatment, LRV, Annual_Risk, Compliance_Status
   - Capture: Comparison results showing difference between treatments

### Demo 3: Batch Scenarios

10. **10_batch_scenarios.png**
    - Navigate to: Batch Scenarios mode
    - Show: File upload widget
    - File: master_batch_scenarios.csv uploaded
    - Display: Preview of scenarios (first few rows)
    - Capture: Upload + preview area

11. **11_batch_results.png**
    - Show: Complete batch results table
    - Display: All 15 scenarios with:
      * Scenario_Name
      * Pathogen
      * Treatment_LRV
      * Annual_Risk
      * Compliance_Status
    - Capture: Full results (may need to capture table in parts if large)

## Screenshot Capture Tips

### Using Windows Snipping Tool (Recommended)
1. Press **Win + Shift + S**
2. Select area to capture
3. Screenshot is copied to clipboard
4. Open Paint or Word, paste, and save to this folder

### Using Full Screenshot
1. Press **PrtScn** (Print Screen)
2. Paste into image editor
3. Crop to relevant area
4. Save to this folder

### Using Browser DevTools
1. Press **F12** to open DevTools
2. Press **Ctrl + Shift + P**
3. Type "screenshot"
4. Select "Capture full size screenshot"
5. Save to this folder

## File Naming
- Use exact filenames as listed above
- PNG format preferred
- Resolution: At least 1920x1080 recommended
- Keep file sizes reasonable (compress if > 2MB)

## Quality Checklist
- [ ] All text is readable
- [ ] Parameter values are clearly visible
- [ ] Charts/plots are sharp and clear
- [ ] No personal/sensitive data visible
- [ ] Proper zoom level (not too zoomed in/out)
- [ ] Browser chrome/bars cropped out (optional)

## After Capturing All Screenshots
1. Verify all 11 screenshots are in this folder
2. Check filenames match exactly
3. Review each screenshot for quality
4. Ready to insert into demo document!
