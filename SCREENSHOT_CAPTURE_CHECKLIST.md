# QMRA App Screenshot Capture Checklist

## Setup
- [ ] QMRA app is running at http://localhost:8501
- [ ] Browser window is maximized (1920x1080 or larger)
- [ ] Windows Snipping Tool ready (Win + Shift + S)
- [ ] Create folder: `Batch_Processing_App/screenshots_final/`

---

## Screenshots to Capture (18 Total)

### 1. HOME PAGE / WELCOME SCREEN

#### Screenshot 1.1: Home - Top Section
**Filename**: `01_home_top.png`
- [ ] Navigate to: http://localhost:8501
- [ ] Ensure Production Mode checkbox is CHECKED in sidebar
- [ ] Capture:
  - Full sidebar (Production Mode toggle, Assessment Mode dropdown)
  - Main panel title
  - Welcome message
- [ ] Press Win+Shift+S, select area, save

#### Screenshot 1.2: Home - Middle Section
**Filename**: `01_home_middle.png`
- [ ] Scroll down halfway
- [ ] Capture:
  - Feature descriptions
  - Any example content
- [ ] Save screenshot

#### Screenshot 1.3: Home - Bottom Section
**Filename**: `01_home_bottom.png`
- [ ] Scroll to bottom of page
- [ ] Capture:
  - Any remaining content
  - Footer information (if present)
- [ ] Save screenshot

---

### 2. BATCH SCENARIOS ASSESSMENT

#### Screenshot 2.1: Batch Scenarios - Top
**Filename**: `02_batch_top.png`
- [ ] Select "Batch Scenarios" from Assessment Mode dropdown in sidebar
- [ ] Wait for page to load
- [ ] Check "Use example data" if available
- [ ] Capture:
  - Page title "Batch Scenarios Assessment"
  - Top configuration options
  - Data tabs or headers
- [ ] Save screenshot

#### Screenshot 2.2: Batch Scenarios - Middle
**Filename**: `02_batch_middle.png`
- [ ] Scroll down to data preview area
- [ ] Capture:
  - pathogen_data preview table
  - scenarios.csv preview
  - Any visible data rows
- [ ] Save screenshot

#### Screenshot 2.3: Batch Scenarios - Bottom
**Filename**: `02_batch_bottom.png`
- [ ] Scroll to bottom
- [ ] Capture:
  - Run Assessment button
  - Any results area or placeholders
  - Download options (if visible)
- [ ] Save screenshot

---

### 3. SPATIAL RISK ASSESSMENT

#### Screenshot 3.1: Spatial - Top
**Filename**: `03_spatial_top.png`
- [ ] Select "Spatial Assessment" from dropdown
- [ ] Wait for page to load
- [ ] Set:
  - Pathogen: norovirus
  - Exposure Route: Shellfish Consumption
  - Check "Use example dilution data" if available
- [ ] Capture:
  - Page title
  - Pathogen selector
  - Exposure route selector
  - Top of configuration panel
- [ ] Save screenshot

#### Screenshot 3.2: Spatial - Middle
**Filename**: `03_spatial_middle.png`
- [ ] Scroll down
- [ ] Capture:
  - Dilution data upload area
  - Parameter configuration fields (treatment LRV, exposure frequency, etc.)
  - Any data preview
- [ ] Save screenshot

#### Screenshot 3.3: Spatial - Bottom
**Filename**: `03_spatial_bottom.png`
- [ ] Scroll to bottom
- [ ] Capture:
  - Run Spatial Assessment button
  - Any example data shown
  - Results area (if visible without running)
- [ ] Save screenshot

---

### 4. TEMPORAL RISK ASSESSMENT

#### Screenshot 4.1: Temporal - Top
**Filename**: `04_temporal_top.png`
- [ ] Select "Temporal Assessment" from dropdown
- [ ] Set:
  - Pathogen: norovirus
  - Exposure Route: Shellfish Consumption
- [ ] Capture:
  - Page title
  - Pathogen and exposure route selectors
  - Date range options (if visible)
- [ ] Save screenshot

#### Screenshot 4.2: Temporal - Middle
**Filename**: `04_temporal_middle.png`
- [ ] Scroll down
- [ ] Capture:
  - Temporal data upload area
  - CSV format requirements
  - Parameter configuration
- [ ] Save screenshot

#### Screenshot 4.3: Temporal - Bottom
**Filename**: `04_temporal_bottom.png`
- [ ] Scroll to bottom
- [ ] Capture:
  - Run Temporal Assessment button
  - Data preview area
  - Any example shown
- [ ] Save screenshot

---

### 5. TREATMENT COMPARISON

#### Screenshot 5.1: Treatment - Top
**Filename**: `05_treatment_top.png`
- [ ] Select "Treatment Comparison" from dropdown
- [ ] Set:
  - Pathogen: norovirus
  - Exposure Route: Shellfish Consumption
- [ ] Capture:
  - Page title
  - Pathogen/route selectors
  - Treatment scenario configuration section
- [ ] Save screenshot

#### Screenshot 5.2: Treatment - Middle
**Filename**: `05_treatment_middle.png`
- [ ] Scroll down
- [ ] Capture:
  - Treatment LRV input fields for multiple scenarios
  - Scenario name inputs
  - Parameter configuration
- [ ] Save screenshot

#### Screenshot 5.3: Treatment - Bottom
**Filename**: `05_treatment_bottom.png`
- [ ] Scroll to bottom
- [ ] Capture:
  - Additional parameters
  - Run Treatment Comparison button
  - Any preview area
- [ ] Save screenshot

---

### 6. MULTI-PATHOGEN ASSESSMENT

#### Screenshot 6.1: Multi-Pathogen - Top
**Filename**: `06_multipathogen_top.png`
- [ ] Select "Multi-Pathogen Assessment" from dropdown
- [ ] NOTE: In Production Mode, only norovirus will be available
- [ ] Capture:
  - Page title
  - Pathogen multi-select box (showing norovirus only in Production Mode)
  - Exposure route selector
- [ ] Save screenshot

#### Screenshot 6.2: Multi-Pathogen - Middle
**Filename**: `06_multipathogen_middle.png`
- [ ] Scroll down
- [ ] Capture:
  - Configuration parameters
  - Any pathogen-specific settings
- [ ] Save screenshot

#### Screenshot 6.3: Multi-Pathogen - Bottom
**Filename**: `06_multipathogen_bottom.png`
- [ ] Scroll to bottom
- [ ] Capture:
  - Run Multi-Pathogen Assessment button
  - Any results area
- [ ] Save screenshot

---

## Verification Checklist

After capturing all screenshots, verify:

- [ ] All 18 screenshot files exist in `Batch_Processing_App/screenshots_final/`
- [ ] Each screenshot is clear and readable
- [ ] Text is legible (not blurry)
- [ ] No personal information visible (if applicable)
- [ ] Screenshots show the full width of content (no cut-off text)
- [ ] Resolution is at least 1920x1080 or equivalent
- [ ] File sizes are reasonable (200-500 KB each)

---

## File List

When complete, you should have these 18 files:

```
Batch_Processing_App/screenshots_final/
├── 01_home_top.png
├── 01_home_middle.png
├── 01_home_bottom.png
├── 02_batch_top.png
├── 02_batch_middle.png
├── 02_batch_bottom.png
├── 03_spatial_top.png
├── 03_spatial_middle.png
├── 03_spatial_bottom.png
├── 04_temporal_top.png
├── 04_temporal_middle.png
├── 04_temporal_bottom.png
├── 05_treatment_top.png
├── 05_treatment_middle.png
├── 05_treatment_bottom.png
├── 06_multipathogen_top.png
├── 06_multipathogen_middle.png
└── 06_multipathogen_bottom.png
```

---

## Next Steps

1. Review all screenshots for quality
2. Retake any unclear screenshots
3. Run the Word document generator with these screenshots
4. Review final user guide document

---

**Estimated Time**: 15-20 minutes for all 18 screenshots
**Tools Needed**: Windows Snipping Tool (Win + Shift + S), Paint or image editor
