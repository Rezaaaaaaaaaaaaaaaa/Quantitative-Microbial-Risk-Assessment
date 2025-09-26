# QMRA Toolkit - Interface Mockup Guide

**Complete Walkthrough with ASCII Interface Mockups**
**NIWA Earth Sciences - September 26, 2025**

**Note: This guide contains ASCII text mockups of the interface, not actual screenshots. For real screenshots, the GUI application needs to be launched and screen captures taken manually.**

---

## 🎯 **Visual Quick Start - Your First Assessment in 30 Minutes**

### **STEP 1: Launch the Toolkit**

#### **Option A: GUI Interface (Recommended for Beginners)**

```
┌─────────────────────────────────────────────────────────────────┐
│ Windows Explorer: qmra_toolkit folder                          │
├─────────────────────────────────────────────────────────────────┤
│ 📁 config/           📄 launch_gui.py                         │
│ 📁 data/             📄 Launch_QMRA_GUI.bat  ← DOUBLE-CLICK    │
│ 📁 docs/             📄 README.md                              │
│ 📁 examples/         📄 requirements.txt                       │
│ 📁 src/              📄 treatment_config.yaml                  │
│ 📁 templates/        📄 wastewater_treatment.yaml              │
│ 📁 tests/                                                      │
└─────────────────────────────────────────────────────────────────┘
```

**What to do:**
1. Navigate to the `qmra_toolkit` folder
2. **Double-click** `Launch_QMRA_GUI.bat`
3. Wait for the GUI window to appear (3-5 seconds)

---

### **STEP 2: GUI Interface Overview**

When the GUI launches, you'll see this main window:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ QMRA Assessment Toolkit - NIWA                                  [_][□][X]│
├─────────────────────────────────────────────────────────────────────────┤
│ File   Edit   Assessment   Reports   Help                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─── Project Setup ────────────────┐  ┌─── Assessment Parameters ───┐  │
│  │                                  │  │                             │  │
│  │  Project Name: [________________]│  │  Pathogen: [Norovirus    ▼] │  │
│  │  Assessor: [____________________]│  │  Route: [Primary Contact ▼] │  │
│  │  Date: [2025-09-26______________]│  │  Concentration: [1000000___] │  │
│  │  Client: [______________________]│  │  copies/L                   │  │
│  │                                  │  │                             │  │
│  │  Population at Risk:             │  │  Exposure Volume: [0.1_____] │  │
│  │  [100000________________________]│  │  L per event                │  │
│  │                                  │  │                             │  │
│  └──────────────────────────────────┘  │  Frequency: [7_____________] │  │
│                                         │  events/year                │  │
│  ┌─── Treatment Scenarios ──────────┐  │                             │  │
│  │                                  │  │  Monte Carlo: [10000_______] │  │
│  │  Current Treatment:              │  │  iterations                 │  │
│  │  Type: [Secondary Treatment ____]│  │                             │  │
│  │  LRV Norovirus: [1.0____________]│  └─────────────────────────────┘  │
│  │  LRV Campylobacter: [2.0________]│                                   │
│  │  LRV Cryptosporidium: [1.5______]│  ┌─── Run Assessment ─────────┐   │
│  │                                  │  │                           │   │
│  │  Proposed Treatment:             │  │   [Load Config File]      │   │
│  │  Type: [Tertiary Treatment _____]│  │   [Save Config File]      │   │
│  │  LRV Norovirus: [3.5____________]│  │                           │   │
│  │  LRV Campylobacter: [4.0________]│  │   [▶ RUN ASSESSMENT]      │   │
│  │  LRV Cryptosporidium: [3.0______]│  │                           │   │
│  │                                  │  │   [Generate Report]       │   │
│  └──────────────────────────────────┘  │   [View Results]          │   │
│                                         │                           │   │
│                                         └───────────────────────────┘   │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│ Status: Ready | Progress: [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0%          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Key Interface Elements:**
- **🎯 Project Setup (Top Left)**: Basic project information
- **📊 Assessment Parameters (Top Right)**: Core QMRA settings
- **🔧 Treatment Scenarios (Bottom Left)**: Current vs proposed treatment
- **▶️ Run Assessment (Bottom Right)**: Action buttons
- **📈 Status Bar (Bottom)**: Progress and status messages

---

### **STEP 3: Fill in Your Assessment Parameters**

#### **3.1 Project Setup Section**
```
┌─── Project Setup ─────────────────────────────┐
│                                               │
│  Project Name: [Auckland Council WWTP_______]│ ← Enter descriptive name
│  Assessor: [Your Name Here__________________]│ ← Your name
│  Date: [2025-09-26__________________________]│ ← Auto-filled
│  Client: [Auckland Council__________________]│ ← Client organization
│                                               │
│  Population at Risk:                          │
│  [500000____________________________________]│ ← Number of people exposed
│                                               │
└───────────────────────────────────────────────┘
```

**Visual Cues:**
- **Green border**: Successfully filled field
- **Red border**: Required field missing
- **Yellow background**: Field with validation warning

#### **3.2 Assessment Parameters Section**
```
┌─── Assessment Parameters ─────────────────────┐
│                                               │
│  Pathogen: [Norovirus              ▼]       │ ← Click dropdown
│          [▪ Norovirus                ]        │   Select pathogen
│          [▪ Campylobacter            ]        │
│          [▪ Cryptosporidium          ]        │
│          [▪ E. coli                  ]        │
│                                               │
│  Route: [Primary Contact           ▼]       │ ← Exposure route
│        [▪ Primary Contact            ]        │
│        [▪ Shellfish Consumption      ]        │
│        [▪ Drinking Water             ]        │
│        [▪ Aerosol Inhalation         ]        │
│                                               │
│  Concentration: [1000000________________]    │ ← Pathogen concentration
│  copies/L                                     │   (copies/L or CFU/L)
│                                               │
│  Exposure Volume: [0.1__________________]    │ ← Volume per exposure
│  L per event                                  │   (Liters)
│                                               │
│  Frequency: [7_________________________]    │ ← Events per year
│  events/year                                  │
│                                               │
│  Monte Carlo: [10000___________________]    │ ← Simulation iterations
│  iterations                                   │   (recommended: 10,000)
│                                               │
└───────────────────────────────────────────────┘
```

---

### **STEP 4: Set Up Treatment Scenarios**

#### **4.1 Current Treatment Configuration**
```
┌─── Treatment Scenarios ───────────────────────────┐
│                                                   │
│  Current Treatment:                               │
│  Type: [Secondary Treatment________________]     │ ← Treatment type
│                                                   │
│  Log Reduction Values (LRV):                      │
│  ┌─────────────────────────────────────────────┐  │
│  │  Pathogen          │ LRV    │ Effectiveness │  │
│  ├─────────────────────────────────────────────┤  │
│  │  Norovirus         │ [1.0_] │ 90.0%        │  │ ← 1 log = 90% removal
│  │  Campylobacter     │ [2.0_] │ 99.0%        │  │ ← 2 log = 99% removal
│  │  Cryptosporidium   │ [1.5_] │ 96.8%        │  │ ← 1.5 log = 96.8% removal
│  └─────────────────────────────────────────────┘  │
│                                                   │
│  Proposed Treatment:                              │
│  Type: [Tertiary Treatment_________________]     │ ← Upgraded treatment
│                                                   │
│  ┌─────────────────────────────────────────────┐  │
│  │  Pathogen          │ LRV    │ Effectiveness │  │
│  ├─────────────────────────────────────────────┤  │
│  │  Norovirus         │ [3.5_] │ 99.97%       │  │ ← 3.5 log = 99.97% removal
│  │  Campylobacter     │ [4.0_] │ 99.99%       │  │ ← 4.0 log = 99.99% removal
│  │  Cryptosporidium   │ [3.0_] │ 99.90%       │  │ ← 3.0 log = 99.90% removal
│  └─────────────────────────────────────────────┘  │
│                                                   │
│  Dilution Factor: [100________________________]  │ ← Receiving water dilution
│                                                   │
└───────────────────────────────────────────────────┘
```

**Important Notes:**
- **LRV = Log Reduction Value**: Each log removes 90% of pathogens
- **Higher LRV = Better Treatment**: 3 logs = 99.9% removal
- **Dilution Factor**: How much receiving water dilutes the effluent

---

### **STEP 5: Run the Assessment**

#### **5.1 Pre-Run Validation**
```
┌─── Run Assessment ─────────────────┐
│                                    │
│   [Load Config File]               │ ← Load saved settings
│   [Save Config File]               │ ← Save current settings
│                                    │
│   Validation Status:               │
│   ✅ Project information complete   │ ← All required fields filled
│   ✅ Assessment parameters valid    │ ← Parameters in valid ranges
│   ✅ Treatment scenarios defined    │ ← Both scenarios configured
│   ⚠️  High pathogen concentration   │ ← Warning about assumptions
│                                    │
│   [▶ RUN ASSESSMENT]               │ ← Click to start analysis
│                                    │
│   [Generate Report]                │ ← Available after run
│   [View Results]                   │ ← Available after run
│                                    │
└────────────────────────────────────┘
```

#### **5.2 Assessment Progress**
```
┌─────────────────────────────────────────────────────────────────────────┐
│ QMRA Assessment Toolkit - NIWA                         [_][□][X]        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│              🔄 ASSESSMENT IN PROGRESS                                   │
│                                                                         │
│  Current Step: Monte Carlo Simulation                                   │
│  Iteration: 7,432 of 10,000 (74.3% complete)                          │
│                                                                         │
│  Progress: [████████████████████░░░░░░░░░░] 74%                        │
│                                                                         │
│  ┌─── Current Analysis Status ─────────────────────────────────────┐    │
│  │                                                                 │    │
│  │  ✅ Pathogen database loaded                                    │    │
│  │  ✅ Exposure scenarios configured                               │    │
│  │  ✅ Dose-response models initialized                            │    │
│  │  🔄 Monte Carlo simulation running...                          │    │
│  │  ⏳ Risk characterization pending                               │    │
│  │  ⏳ Report generation pending                                   │    │
│  │                                                                 │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│                    Estimated time remaining: 2 minutes                  │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│ Status: Running Monte Carlo simulation... | Progress: 74%               │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### **STEP 6: View and Interpret Results**

#### **6.1 Results Summary Window**
```
┌─────────────────────────────────────────────────────────────────────────┐
│ Assessment Results - Auckland Council WWTP                    [_][□][X] │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─── Risk Assessment Summary ─────────────────────────────────────┐     │
│  │                                                                 │     │
│  │  Assessment: Auckland Council WWTP Tertiary Treatment          │     │
│  │  Date: September 26, 2025                                      │     │
│  │  Population: 500,000 people                                    │     │
│  │                                                                 │     │
│  │  ┌─────────────────────────────────────────────────────────┐   │     │
│  │  │ PATHOGEN RISK COMPARISON                                │   │     │
│  │  ├─────────────────────────────────────────────────────────┤   │     │
│  │  │                    │ Current  │ Proposed │ Status      │   │     │
│  │  │ Pathogen           │ Risk     │ Risk     │             │   │     │
│  │  ├─────────────────────────────────────────────────────────┤   │     │
│  │  │ 🦠 Norovirus        │ 9.83e-01 │ 5.56e-01 │ ❌ High Risk │   │     │
│  │  │ 🧬 Campylobacter    │ 1.30e-01 │ 1.43e-03 │ 🔶 Moderate  │   │     │
│  │  │ 🔬 Cryptosporidium  │ 3.15e-03 │ 1.22e-05 │ ✅ Low Risk  │   │     │
│  │  └─────────────────────────────────────────────────────────┘   │     │
│  │                                                                 │     │
│  │  PUBLIC HEALTH IMPACT:                                          │     │
│  │  • Norovirus cases prevented: 213,445 per year                 │     │
│  │  • Campylobacter cases prevented: 64,065 per year              │     │
│  │  • Total illness reduction: 277,510 cases per year             │     │
│  │                                                                 │     │
│  └─────────────────────────────────────────────────────────────────┘     │
│                                                                         │
│  ┌─── Regulatory Compliance ───────────────────────────────────────┐     │
│  │                                                                 │     │
│  │  New Zealand Guidelines (Annual Risk ≤ 1e-6):                  │     │
│  │                                                                 │     │
│  │  Current Treatment:                                             │     │
│  │  ❌ NON-COMPLIANT - Risk exceeds guidelines                     │     │
│  │                                                                 │     │
│  │  Proposed Treatment:                                            │     │
│  │  🔶 IMPROVED - Significant risk reduction achieved             │     │
│  │  ⚠️  Norovirus still above compliance threshold                │     │
│  │                                                                 │     │
│  │  Recommendation: Proceed with tertiary treatment upgrade       │     │
│  │                                                                 │     │
│  └─────────────────────────────────────────────────────────────────┘     │
│                                                                         │
│  [📊 View Detailed Plots] [📄 Generate Report] [💾 Export Data] [🔄 New]│
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│ Status: Assessment completed successfully                                │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### **STEP 7: Visual Results and Plots**

#### **7.1 Risk Comparison Plot**
```
┌─────────────────────────────────────────────────────────────────────────┐
│ Risk Analysis Plots                                          [_][□][X] │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─── Pathogen Risk Comparison ─────────────────────────────────────┐   │
│  │                                                                  │   │
│  │  Annual Illness Risk by Pathogen                                 │   │
│  │                                                                  │   │
│  │  1e+0 ┐                                                          │   │
│  │       │  ████                                                    │   │
│  │       │  ████ Current                                            │   │
│  │  1e-1 ┤  ████ ▓▓▓▓                                              │   │
│  │       │  ████ ▓▓▓▓ Proposed                                      │   │
│  │       │  ████ ▓▓▓▓                                              │   │
│  │  1e-2 ┤  ████ ▓▓▓▓ ████                                         │   │
│  │       │  ████ ▓▓▓▓ ████                                         │   │
│  │   ↑   │  ████ ▓▓▓▓ ████ ░░░░                                    │   │
│  │  1e-3 ┤  ████ ▓▓▓▓ ████ ░░░░                                    │   │
│  │   │   │  ████ ▓▓▓▓ ████ ░░░░                                    │   │
│  │  1e-4 ┤  ████ ▓▓▓▓ ████ ░░░░                                    │   │
│  │       │  ████ ▓▓▓▓ ████ ░░░░                                    │   │
│  │  Risk │  ████ ▓▓▓▓ ████ ░░░░                                    │   │
│  │  1e-5 ┤  ████ ▓▓▓▓ ████ ░░░░                                    │   │
│  │       │  ████ ▓▓▓▓ ████ ░░░░                                    │   │
│  │   │   │  ████ ▓▓▓▓ ████ ░░░░                                    │   │
│  │  1e-6 ┼──██████▓▓▓▓████░░░░────── NZ Guideline (1e-6)          │   │
│  │       │                                                          │   │
│  │  1e-7 ┘  Noro  Camp  Crypto                                     │   │
│  │                                                                  │   │
│  │  Legend: ████ Current Treatment  ▓▓▓▓ Proposed Treatment         │   │
│  │                                                                  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─── Treatment Effectiveness ──────────────────────────────────────┐   │
│  │                                                                  │   │
│  │  Cases Prevented Per Year (Population: 500,000)                 │   │
│  │                                                                  │   │
│  │  300,000 ┐                                                      │   │
│  │          │  ████████████████████ 213,445                        │   │
│  │  250,000 ┤  ████████████████████                                │   │
│  │          │  ████████████████████                                │   │
│  │  200,000 ┤  ████████████████████                                │   │
│  │          │  ████████████████████                                │   │
│  │  150,000 ┤  ████████████████████                                │   │
│  │          │  ████████████████████                                │   │
│  │  100,000 ┤  ████████████████████ ██████████ 64,065              │   │
│  │          │  ████████████████████ ██████████                     │   │
│  │   50,000 ┤  ████████████████████ ██████████                     │   │
│  │          │  ████████████████████ ██████████ █ <100               │   │
│  │        0 ┘  Norovirus            Campylobacter Cryptosporidium   │   │
│  │                                                                  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  [💾 Save Plots] [📧 Email Results] [🖨️ Print] [📋 Copy Data]          │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│ Status: Plots generated successfully                                    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### **STEP 8: Generate Professional Report**

#### **8.1 Report Generation Dialog**
```
┌─────────────────────────────────────────────────────────────────────────┐
│ Generate Assessment Report                                     [_][□][X]│
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─── Report Templates ──────────────────────────────────────────────┐  │
│  │                                                                   │  │
│  │  ◉ Executive Summary Report                                       │  │
│  │    • 2-3 page summary for decision-makers                        │  │
│  │    • Key findings and recommendations                             │  │
│  │    • Risk comparison charts                                       │  │
│  │                                                                   │  │
│  │  ○ Technical Assessment Report                                    │  │
│  │    • Detailed 15-20 page technical report                        │  │
│  │    • Complete methodology and calculations                        │  │
│  │    • Peer review ready                                            │  │
│  │                                                                   │  │
│  │  ○ Regulatory Compliance Report                                   │  │
│  │    • Focused on compliance status                                 │  │
│  │    • Regulatory framework alignment                               │  │
│  │    • Submission ready format                                      │  │
│  │                                                                   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌─── Output Options ────────────────────────────────────────────────┐  │
│  │                                                                   │  │
│  │  Report Format:                                                   │  │
│  │  ☑️ PDF (Recommended)    ☑️ Word Document    ☐ HTML               │  │
│  │                                                                   │  │
│  │  Include:                                                         │  │
│  │  ☑️ Risk comparison plots      ☑️ Data tables                     │  │
│  │  ☑️ Uncertainty analysis       ☑️ Methodology section             │  │
│  │  ☑️ Quality assurance info     ☑️ Literature references           │  │
│  │                                                                   │  │
│  │  Output Location:                                                 │  │
│  │  [C:\...\NZ_Consultancy_Project_2025\reports\] [Browse...]       │  │
│  │                                                                   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌─── Report Preview ────────────────────────────────────────────────┐  │
│  │                                                                   │  │
│  │  Estimated report length: 3 pages                                 │  │
│  │  Includes: 2 charts, 1 data table, executive summary              │  │
│  │  Processing time: ~30 seconds                                     │  │
│  │                                                                   │  │
│  │  Report will include:                                             │  │
│  │  • Project overview and parameters                                │  │
│  │  • Risk assessment results                                        │  │
│  │  • Treatment scenario comparison                                  │  │
│  │  • Regulatory compliance status                                   │  │
│  │  • Recommendations and next steps                                 │  │
│  │                                                                   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  [📄 Generate Report] [👁️ Preview] [❌ Cancel]                          │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│ Status: Ready to generate report                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🚨 **Visual Troubleshooting Guide**

### **Common Issue 1: GUI Won't Start**
```
┌─────────────────────────────────────────────────────────────┐
│ Command Prompt Error                               [_][□][X]│
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ C:\...\qmra_toolkit> python launch_gui.py                  │
│                                                             │
│ Error importing GUI modules: No module named 'tkinter'      │
│ Please ensure all dependencies are installed:               │
│ pip install -r requirements.txt                             │
│                                                             │
│ SOLUTION:                                                   │
│ 1. Check Python version: python --version                   │
│    (Should be 3.8 or higher)                               │
│ 2. Install requirements: pip install -r requirements.txt    │
│ 3. Try again: python launch_gui.py                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### **Common Issue 2: Invalid Parameters**
```
┌─────────────────────────────────────────────────────────────┐
│ Parameter Validation Error                         [_][□][X]│
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ⚠️  VALIDATION ERRORS DETECTED                             │
│                                                             │
│  The following parameters need attention:                   │
│                                                             │
│  ❌ Pathogen concentration too high (>1e8)                  │
│     Current: 1e10 copies/L                                 │
│     Typical range: 1e3 - 1e7 copies/L                     │
│     → Check your data source                               │
│                                                             │
│  ❌ LRV values inconsistent                                 │
│     Norovirus LRV > Cryptosporidium LRV                   │
│     → Verify treatment effectiveness data                   │
│                                                             │
│  ⚠️  Population at risk very high                          │
│     Current: 10,000,000 people                            │
│     → Confirm this is correct for your scenario           │
│                                                             │
│  [Fix Parameters] [Continue Anyway] [Load Example]         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 **Understanding Visual Results**

### **Risk Level Color Coding**
```
┌─── Risk Interpretation Legend ────────────────────────────────────┐
│                                                                   │
│  ✅ GREEN (Compliant): Annual risk ≤ 1e-6                        │
│     • Meets New Zealand guidelines                                │
│     • No action required                                          │
│     • Safe for public health                                      │
│                                                                   │
│  🔶 YELLOW (Moderate): 1e-6 < Annual risk ≤ 1e-2                 │
│     • Above guidelines but manageable                             │
│     • Consider treatment improvements                             │
│     • Monitor closely                                             │
│                                                                   │
│  ❌ RED (High Risk): Annual risk > 1e-2                           │
│     • Significant public health concern                           │
│     • Treatment upgrade required                                  │
│     • Not suitable for current use                               │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

### **Treatment Effectiveness Scale**
```
┌─── Log Reduction Value (LRV) Reference ──────────────────────────┐
│                                                                  │
│  LRV 1.0 = 90% removal     ████████░░ 90%                       │
│  LRV 2.0 = 99% removal     █████████░ 99%                       │
│  LRV 3.0 = 99.9% removal   ██████████ 99.9%                     │
│  LRV 4.0 = 99.99% removal  ██████████ 99.99%                    │
│                                                                  │
│  Higher LRV = Better Treatment Performance                       │
│  Typical ranges:                                                 │
│  • Primary treatment: 0.5-1.0 LRV                              │
│  • Secondary treatment: 1.0-2.5 LRV                            │
│  • Tertiary treatment: 2.5-4.0+ LRV                            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📋 **Visual Checklist for Quality Assurance**

### **Before Running Assessment**
```
┌─── Pre-Assessment Checklist ─────────────────────────────────────┐
│                                                                  │
│  □ Project name is descriptive and unique                        │
│  □ Population at risk is realistic (check census data)           │
│  □ Pathogen concentrations from reliable source                  │
│  □ Treatment LRVs match technology specifications                │
│  □ Exposure parameters appropriate for scenario                  │
│  □ Monte Carlo iterations ≥ 10,000                              │
│  □ All required fields show green validation                     │
│                                                                  │
│  ✅ Ready to run assessment                                      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### **After Getting Results**
```
┌─── Post-Assessment Validation ───────────────────────────────────┐
│                                                                  │
│  □ Risk values are reasonable (not exactly 0 or 1)               │
│  □ Proposed treatment shows improvement over current              │
│  □ Results consistent with similar studies                       │
│  □ Confidence intervals make sense                               │
│  □ Plots display without errors                                  │
│  □ Report generation successful                                   │
│                                                                  │
│  ✅ Results validated and ready for reporting                    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

**This visual guide shows you exactly what to expect at each step of using the QMRA toolkit, with detailed interface mockups, troubleshooting screens, and result interpretation guides.**

---

*Visual Step-by-Step Guide with Interface Examples*
*NIWA Earth Sciences QMRA Team - September 26, 2025*