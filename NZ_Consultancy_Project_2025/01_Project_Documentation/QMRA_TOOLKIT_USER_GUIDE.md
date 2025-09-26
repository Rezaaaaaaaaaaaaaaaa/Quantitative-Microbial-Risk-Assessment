# QMRA Toolkit User Guide - Technical Guidelines
**NIWA Earth Sciences - Quantitative Microbial Risk Assessment Toolkit**
**Version 2025 - Professional Consultancy Edition**

---

## 📖 **Quick Start Guide**

### **🎯 What is QMRA?**
Quantitative Microbial Risk Assessment (QMRA) is a scientific method to:
- **Quantify** public health risks from pathogen exposure
- **Compare** treatment scenarios and compliance options
- **Support** regulatory decision-making with defensible science
- **Protect** public health through evidence-based management

---

## 🏗️ **QMRA Framework - The 4-Step Process**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  1. HAZARD      │    │  2. EXPOSURE    │    │  3. DOSE-       │    │  4. RISK        │
│  IDENTIFICATION │───▶│  ASSESSMENT     │───▶│  RESPONSE       │───▶│  CHARACTERIZ-   │
│                 │    │                 │    │                 │    │  ATION          │
│  • Pathogen     │    │  • Exposure     │    │  • Mathematical │    │  • Risk         │
│    selection    │    │    routes       │    │    models       │    │    calculation  │
│  • Dose-response│    │  • Concentr.    │    │  • Probability  │    │  • Uncertainty  │
│    data         │    │  • Frequency    │    │    of infection │    │  • Population   │
│                 │    │                 │    │                 │    │    impact       │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 🛠️ **Toolkit Architecture**

### **Core Components**
```
┌────────────────────────────────────────────────────────────────┐
│                    QMRA ASSESSMENT TOOLKIT                     │
├────────────────────────────────────────────────────────────────┤
│  📊 GUI Interface     │  🖥️  Command Line    │  📁 Batch Processing │
│  (qmra_gui.py)       │  (qmra_toolkit.py)   │  (custom scripts)    │
├────────────────────────────────────────────────────────────────┤
│                        CORE ENGINES                            │
├────────────────┬───────────────┬────────────────┬──────────────┤
│ 🦠 PATHOGEN    │ 💧 EXPOSURE   │ 🎲 MONTE      │ ⚠️  RISK     │
│ DATABASE       │ ASSESSMENT    │ CARLO         │ CHARACTER-   │
│                │               │               │ IZATION      │
│ • Norovirus    │ • Primary     │ • 10,000      │ • Annual     │
│ • Campylobacter│   contact     │   iterations  │   risk       │
│ • Cryptosporid │ • Shellfish   │ • Uncertainty │ • Population │
│ • Dose-response│ • Drinking H₂O│   analysis    │   impact     │
│   models       │ • Aerosols    │ • Statistics  │ • Compliance │
└────────────────┴───────────────┴────────────────┴──────────────┘
│                        OUTPUTS                                 │
├────────────────┬───────────────┬────────────────┬──────────────┤
│ 📋 REPORTS     │ 📊 PLOTS      │ 📈 TABLES     │ 📄 EXPORT    │
│                │               │               │              │
│ • Executive    │ • Risk        │ • CSV data    │ • Word docs  │
│   summary      │   comparison  │ • Summary     │ • JSON       │
│ • Regulatory   │ • Treatment   │   tables      │ • Excel      │
│   compliance   │   scenarios   │ • Compliance  │ • Figures    │
└────────────────┴───────────────┴────────────────┴──────────────┘
```

---

## 🚀 **Getting Started - 3 Ways to Use the Toolkit**

### **Method 1: GUI Interface (Recommended for New Users)**
```
📂 qmra_toolkit/
├── Launch_QMRA_GUI.bat  ← Double-click this file (Windows)
└── launch_gui.py        ← Run this file (Mac/Linux)

🖱️ WORKFLOW:
1. Double-click Launch_QMRA_GUI.bat
2. Select pathogen from dropdown
3. Enter exposure parameters
4. Choose treatment scenario
5. Click "Run Assessment"
6. View results and save reports
```

### **Method 2: Command Line (For Technical Users)**
```bash
# Navigate to toolkit
cd qmra_toolkit/

# Run pathogen comparison
python examples/pathogen_comparison.py

# Run scenario comparison
python examples/scenario_comparison.py

# Run custom assessment
python src/qmra_toolkit.py --pathogen norovirus --exposure primary_contact
```

### **Method 3: Custom Scripts (For Consultancy Projects)**
```python
# Import toolkit components
from pathogen_database import PathogenDatabase
from exposure_assessment import create_exposure_assessment, ExposureRoute
from risk_characterization import RiskCharacterization

# Set up assessment
pathogen_db = PathogenDatabase()
risk_calc = RiskCharacterization(pathogen_db)

# Define scenario
exposure = create_exposure_assessment(ExposureRoute.PRIMARY_CONTACT, {
    "water_ingestion_volume": 50.0,  # mL per event
    "exposure_frequency": 15         # events per year
})

# Run assessment
results = risk_calc.run_comprehensive_assessment(
    pathogen_name="norovirus",
    exposure_assessment=exposure,
    population_size=500000
)
```

---

## 📊 **Data Flow Diagram**

### **Input → Processing → Output**
```
INPUT DATA                TOOLKIT PROCESSING              OUTPUT DELIVERABLES
┌─────────────────┐      ┌─────────────────────────────┐      ┌─────────────────┐
│ 🦠 Pathogen     │      │                             │      │ 📋 Executive    │
│   parameters    │────▶ │    ┌─────────────────────┐   │────▶ │   Reports       │
│                 │      │    │  MONTE CARLO        │   │      │                 │
│ 💧 Exposure     │      │    │  SIMULATION         │   │      │ 📊 Risk Plots   │
│   scenarios     │────▶ │    │                     │   │────▶ │                 │
│                 │      │    │ • 10,000 iterations │   │      │ 📈 Data Tables  │
│ ⚙️  Treatment   │      │    │ • Statistical       │   │      │                 │
│   parameters    │────▶ │    │   analysis          │   │────▶ │ 📄 Compliance   │
│                 │      │    │ • Uncertainty       │   │      │   Reports       │
│ 🎯 Regulatory   │      │    │   quantification    │   │      │                 │
│   guidelines    │────▶ │    └─────────────────────┘   │────▶ │ 🎨 Professional │
│                 │      │                             │      │   Visualizations │
└─────────────────┘      └─────────────────────────────┘      └─────────────────┘
```

---

## 🔬 **Technical Workflow - Step by Step**

### **Step 1: Project Setup**
```yaml
# Create project_scenario.yaml
project_details:
  client: "Your Client Name"
  project_name: "QMRA Assessment Project"
  location: "Treatment Plant Location"

exposure_scenarios:
  primary_contact:
    water_ingestion_volume: 50.0  # mL per event
    events_per_year: 15          # frequency
    dilution_factor: 100         # environmental dilution

raw_wastewater_concentrations:
  norovirus: 1000000      # copies/L
  campylobacter: 100000   # CFU/L
  cryptosporidium: 1000   # oocysts/L
```

### **Step 2: Treatment Scenario Definition**
```
┌─────────────────────────────────────────────────────────────┐
│                    TREATMENT TRAIN                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  RAW           PRIMARY        SECONDARY       TERTIARY      │
│  WASTEWATER    TREATMENT      TREATMENT      TREATMENT      │
│     │             │             │             │             │
│     │         ┌───────┐     ┌──────────┐  ┌─────────────┐   │
│  1e6 org/L    │Screens│────▶│Activated │─▶│Sand Filter  │   │
│     │         │& Grit │     │ Sludge   │  │+ UV Disinfn │   │
│     └────────▶│Removal│     │+ Clarify │  │             │   │
│               └───────┘     └──────────┘  └─────────────┘   │
│                   │             │             │             │
│               No removal    1-2 LRV      2.5-4.0 LRV       │
│                              reduction    reduction         │
├─────────────────────────────────────────────────────────────┤
│  LRV = Log Reduction Value                                  │
│  1 LRV = 90% removal                                        │
│  2 LRV = 99% removal                                        │
│  3 LRV = 99.9% removal                                      │
└─────────────────────────────────────────────────────────────┘
```

### **Step 3: Risk Assessment Execution**
```python
# AUTOMATED ASSESSMENT FLOW

1. Load Pathogen Database
   ├── Dose-response models (Beta-Poisson, Exponential)
   ├── Illness-to-infection ratios
   └── DALY values per case

2. Calculate Exposure
   ├── Post-treatment concentrations
   ├── Environmental dilution
   ├── Ingestion volumes and frequencies
   └── Monte Carlo uncertainty analysis

3. Apply Dose-Response Models
   ├── Pathogen-specific models
   ├── Probability of infection calculation
   └── Annual risk assessment

4. Risk Characterization
   ├── Population impact assessment
   ├── Regulatory compliance evaluation
   └── Uncertainty quantification

5. Generate Outputs
   ├── Executive reports
   ├── Professional visualizations
   ├── Data tables (CSV/Excel)
   └── Word documents
```

---

## 📋 **Quality Assurance Checklist**

### **✅ Before Running Assessment**
- [ ] **Pathogen data verified** - Check dose-response model sources
- [ ] **Exposure scenarios realistic** - Validate ingestion volumes/frequencies
- [ ] **Treatment data accurate** - Confirm LRV values with engineers
- [ ] **Dilution factors verified** - Environmental modeling completed
- [ ] **Population estimates current** - Use latest census/planning data

### **✅ During Assessment**
- [ ] **Monte Carlo converged** - Check statistical stability
- [ ] **Results reasonable** - Sanity check against literature
- [ ] **Uncertainty captured** - Review confidence intervals
- [ ] **Compliance evaluated** - Check against all relevant guidelines

### **✅ After Assessment**
- [ ] **Technical review completed** - Independent verification
- [ ] **Visualizations clear** - Professional presentation quality
- [ ] **Reports comprehensive** - Executive and technical versions
- [ ] **Data archived** - JSON/CSV results saved
- [ ] **Documentation complete** - Methods and assumptions documented

---

## 🎨 **Visualization Best Practices**

### **Professional Plot Standards**
```
📊 RISK COMPARISON PLOTS
├── Log scale for risk values (essential for wide ranges)
├── Regulatory guideline lines (red dashed for NZ guidelines)
├── Clear pathogen identification (colors, labels)
├── Uncertainty bands (95% confidence intervals)
└── Professional styling (300 DPI, publication quality)

📈 TREATMENT SCENARIO PLOTS
├── Before/after comparisons (current vs proposed)
├── Cases prevented annotations (quantify benefits)
├── LRV effectiveness visualization (bar charts)
└── Cost-benefit context (where applicable)

📋 COMPLIANCE DASHBOARDS
├── Clear PASS/FAIL indicators (traffic light colors)
├── Regulatory threshold lines (visible reference points)
├── Population impact context (cases per year)
└── Executive summary format (decision-maker friendly)
```

---

## 🚨 **Troubleshooting Guide**

### **Common Issues and Solutions**

**Problem**: "Pathogen concentration not specified" warning
```python
# SOLUTION: Always set pathogen concentration before dose calculation
exposure_model = create_exposure_assessment(ExposureRoute.PRIMARY_CONTACT, params)
exposure_model.set_pathogen_concentration(final_concentration)  # ← Add this line
```

**Problem**: High risk values seem unrealistic
```python
# CHECK: Verify units and dilution factors
raw_conc_per_100ml = raw_concentration_per_L / 10  # Convert L to 100mL
final_conc = treated_conc / dilution_factor  # Apply environmental dilution
```

**Problem**: Monte Carlo simulation taking too long
```python
# SOLUTION: Reduce iterations for testing, increase for final analysis
mc_simulator = MonteCarloSimulator(iterations=1000)  # Testing
mc_simulator = MonteCarloSimulator(iterations=10000) # Final analysis
```

**Problem**: GUI not launching
```bash
# CHECK: Python dependencies
pip install -r requirements.txt

# VERIFY: Python version
python --version  # Should be 3.8+

# ALTERNATIVE: Use command line interface
python src/qmra_toolkit.py --help
```

---

## 📚 **Staff Training Resources**

### **Training Materials**
1. **📖 Beginner Guide** - Introduction to QMRA concepts
2. **🎥 Video Tutorials** - Step-by-step toolkit usage
3. **📋 Checklists** - Quality assurance and review protocols
4. **🔬 Case Studies** - Real-world project examples
5. **❓ FAQ Database** - Common questions and solutions

### **Skill Development Path**
```
LEVEL 1: GUI USER                    LEVEL 2: SCRIPT USER              LEVEL 3: DEVELOPER
├── Understanding QMRA concepts       ├── Python scripting skills       ├── Toolkit modification
├── Using GUI interface              ├── Custom scenario development    ├── New pathogen addition
├── Interpreting results             ├── Batch processing              ├── Model enhancement
└── Basic report generation          └── Advanced visualization        └── Peer review capability
```

### **Certification Requirements**
- [ ] **Theoretical Knowledge** - QMRA principles and applications
- [ ] **Practical Skills** - Toolkit operation and troubleshooting
- [ ] **Quality Assurance** - Review and verification procedures
- [ ] **Client Communication** - Results interpretation and presentation

---

## 📞 **Support and Resources**

### **Technical Support**
- **📧 Email**: qmra-support@niwa.co.nz
- **📞 Phone**: +64-X-XXX-XXXX
- **🌐 Documentation**: https://docs.niwa.co.nz/qmra-toolkit
- **🐛 Bug Reports**: https://github.com/niwa/qmra-toolkit/issues

### **Professional Services**
- **🎓 Training Workshops** - On-site staff training
- **🔬 Technical Review** - Independent assessment verification
- **📊 Custom Development** - Specialized analysis requirements
- **🤝 Consulting Support** - Project-specific guidance

---

**Document Version**: 1.0
**Last Updated**: September 26, 2025
**Next Review**: December 2025
**Owner**: NIWA Earth Sciences QMRA Team