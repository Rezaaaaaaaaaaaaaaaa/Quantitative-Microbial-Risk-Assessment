# QMRA Toolkit - Staff Quick Start Guide
**Visual Step-by-Step Instructions for All Staff Levels**
**NIWA Earth Sciences - Version 2025**

---

## 🎯 **Quick Navigation for Staff**

### **📚 NEW STAFF - Start Here**
1. [Understanding QMRA Basics](#understanding-qmra-basics) - What is QMRA and why do we use it?
2. [Your First Assessment](#your-first-assessment) - Simple 5-minute tutorial
3. [Common Scenarios](#common-scenarios) - Typical projects you'll encounter

### **⚡ EXPERIENCED STAFF - Jump To**
1. [Advanced Workflows](#advanced-workflows) - Complex multi-scenario analyses
2. [Troubleshooting](#troubleshooting-guide) - Fix common issues quickly
3. [Quality Assurance](#quality-assurance-checklist) - Ensure professional results

### **👥 MANAGERS & REVIEWERS**
1. [Results Interpretation](#interpreting-results) - Understand output reports
2. [Client Presentation](#client-presentation-guide) - Professional delivery
3. [Regulatory Compliance](#regulatory-framework) - New Zealand guidelines

---

## 🔍 **Understanding QMRA Basics**

### **What is QMRA? (2-minute explanation)**

```
🦠 PATHOGENS in wastewater → 💧 EXPOSURE through recreation → 😷 HEALTH RISK to public

QMRA calculates: "How many people might get sick from swimming in this water?"
```

### **The 4 Simple Questions QMRA Answers:**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ 1. WHAT         │    │ 2. HOW MUCH     │    │ 3. HOW LIKELY   │    │ 4. SO WHAT      │
│ pathogens are   │───▶│ exposure will   │───▶│ is infection    │───▶│ is the overall  │
│ we worried      │    │ people get?     │    │ from that dose? │    │ risk & impact?  │
│ about?          │    │                 │    │                 │    │                 │
│                 │    │ • Swimming      │    │ • Dose-response │    │ • Annual risk   │
│ • Norovirus     │    │ • Shellfish     │    │   models        │    │ • Cases/year    │
│ • Campylobacter │    │ • Contact       │    │ • Probability   │    │ • Compliance    │
│ • Cryptosporidium│    │ • Frequency     │    │   calculation   │    │ • Recommendations│
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 🚀 **Your First Assessment - 5-Minute Tutorial**

### **Step 1: Launch the Toolkit (Choose Your Method)**

#### **🖱️ Method A: GUI Interface (Easiest for beginners)**
```
📂 Navigate to: qmra_toolkit folder
🖱️ Double-click: Launch_QMRA_GUI.bat
⏳ Wait 10 seconds for window to open
🎉 You should see the QMRA GUI interface!
```

#### **💻 Method B: Command Line (For technical staff)**
```bash
# Open command prompt/terminal
cd qmra_toolkit/
python src/qmra_toolkit.py --help

# Quick example run:
python examples/pathogen_comparison.py
```

### **Step 2: Set Up Your First Assessment**

#### **GUI Method - Fill in the Form:**
```
┌─────────────────────────────────────────────────────────────┐
│                    QMRA Assessment Setup                    │
├─────────────────────────────────────────────────────────────┤
│ Pathogen:           [▼ Norovirus        ]  ← Click dropdown │
│ Exposure Route:     [▼ Primary Contact  ]  ← Swimming       │
│ Concentration:      [  10.0            ]  ← org/100mL       │
│ Ingestion Volume:   [  50.0            ]  ← mL per event    │
│ Events per Year:    [  15              ]  ← frequency       │
│ Population:         [  10000           ]  ← people at risk  │
│                                                             │
│ Treatment Scenario: [▼ Tertiary + UV   ]  ← Choose level   │
│ Log Reduction:      [  3.5             ]  ← LRV value      │
│                                                             │
│                    [  RUN ASSESSMENT  ]   ← Click this!    │
└─────────────────────────────────────────────────────────────┘
```

### **Step 3: Understand Your Results**

#### **Results Window Will Show:**
```
╔═══════════════════════════════════════════════════════════╗
║                    ASSESSMENT RESULTS                     ║
╠═══════════════════════════════════════════════════════════╣
║ 📊 ANNUAL RISK:           2.4e-02 (per person per year)  ║
║ 🏥 EXPECTED CASES:        240 cases per year             ║
║ ✅ COMPLIANCE STATUS:     PASS (meets NZ guidelines)      ║
║                                                           ║
║ 📈 UNCERTAINTY RANGE:     1.8e-02 to 3.1e-02            ║
║ 🎯 CONFIDENCE LEVEL:      95% confidence interval        ║
╚═══════════════════════════════════════════════════════════╝
```

#### **What These Numbers Mean:**
- **Annual Risk**: Probability one person gets infected per year
- **Expected Cases**: Total illnesses across your population
- **Compliance**: Does this meet New Zealand health guidelines?
- **Uncertainty**: Range of possible values (accounts for variability)

---

## 📋 **Common Scenarios - Quick Reference Cards**

### **Scenario 1: Wastewater Treatment Upgrade**
```
┌─────────────────────────────────────────────────────────┐
│ 🏭 TREATMENT UPGRADE ASSESSMENT                         │
├─────────────────────────────────────────────────────────┤
│ QUESTION: "Will tertiary treatment reduce risk enough?" │
│                                                         │
│ SETUP:                                                  │
│ • Compare 2 scenarios: Current vs Proposed treatment   │
│ • Same pathogen, exposure, population                  │
│ • Different LRV values                                 │
│                                                         │
│ TYPICAL VALUES:                                         │
│ • Current Secondary: 1.0-2.0 LRV                       │
│ • Proposed Tertiary: 3.5-4.0 LRV                       │
│ • Population: 50,000-500,000                           │
│                                                         │
│ OUTPUT: Risk reduction percentage & cases prevented     │
└─────────────────────────────────────────────────────────┘
```

### **Scenario 2: Recreational Water Standards**
```
┌─────────────────────────────────────────────────────────┐
│ 🏊 RECREATIONAL WATER COMPLIANCE                        │
├─────────────────────────────────────────────────────────┤
│ QUESTION: "Is this beach/lake safe for swimming?"      │
│                                                         │
│ SETUP:                                                  │
│ • Use measured water quality data                      │
│ • Primary contact exposure route                       │
│ • Conservative exposure assumptions                    │
│                                                         │
│ TYPICAL VALUES:                                         │
│ • Pathogen concentration: Measured values              │
│ • Ingestion: 50 mL per swimming event                  │
│ • Frequency: 10-20 events per summer                   │
│                                                         │
│ OUTPUT: Compare to NZ recreational guidelines          │
└─────────────────────────────────────────────────────────┘
```

### **Scenario 3: Emergency Response**
```
┌─────────────────────────────────────────────────────────┐
│ 🚨 EMERGENCY CONTAMINATION EVENT                        │
├─────────────────────────────────────────────────────────┤
│ QUESTION: "How bad is this spill/failure?"             │
│                                                         │
│ SETUP:                                                  │
│ • High pathogen concentrations                         │
│ • Multiple exposure routes affected                    │
│ • Large population potentially exposed                 │
│                                                         │
│ RAPID ASSESSMENT:                                       │
│ • Use worst-case assumptions                           │
│ • Focus on most vulnerable pathogens                   │
│ • Generate quick compliance check                      │
│                                                         │
│ OUTPUT: Immediate risk level & recommended actions     │
└─────────────────────────────────────────────────────────┘
```

---

## ⚡ **Advanced Workflows**

### **Multi-Scenario Batch Processing**

#### **Step 1: Prepare Scenario File**
```yaml
# scenarios.yaml
scenarios:
  - name: "Current Treatment"
    pathogen: "norovirus"
    concentration: 100.0
    treatment_lrv: 1.0

  - name: "Upgraded Treatment"
    pathogen: "norovirus"
    concentration: 100.0
    treatment_lrv: 3.5

  - name: "Best Available Technology"
    pathogen: "norovirus"
    concentration: 100.0
    treatment_lrv: 5.0
```

#### **Step 2: Run Batch Assessment**
```python
# batch_assessment.py
from qmra_toolkit import BatchProcessor

processor = BatchProcessor("scenarios.yaml")
results = processor.run_all_scenarios()
processor.generate_comparison_report(results)
```

### **Custom Pathogen Addition**

#### **When to Add New Pathogens:**
- Client requests specific organism assessment
- New research identifies emerging pathogens
- Regulatory requirements change

#### **Required Information:**
```python
new_pathogen = {
    "name": "Custom Pathogen",
    "pathogen_type": "virus/bacteria/protozoa",
    "dose_response_models": {
        "beta_poisson": {
            "alpha": 0.04,        # Literature value
            "beta": 0.055,        # Literature value
            "source": "Reference",
            "r_squared": 0.85     # Model fit quality
        }
    },
    "illness_to_infection_ratio": 0.7,  # % who get symptoms
    "dalys_per_case": 0.002            # Disability weight
}
```

---

## 🔧 **Troubleshooting Guide**

### **Common Error Messages & Solutions**

#### **Error 1: "Pathogen concentration not specified"**
```
❌ PROBLEM: Missing or incorrect concentration input

✅ SOLUTION:
# Make sure you set concentration BEFORE running assessment
exposure_model.set_pathogen_concentration(final_concentration)

# Check units: Should be organisms per 100mL for recreational water
# Example: 10.0 means 10 organisms per 100mL
```

#### **Error 2: "Monte Carlo simulation failed to converge"**
```
❌ PROBLEM: Statistical instability in simulation

✅ SOLUTIONS:
1. Increase iterations: iterations=50000 (from default 10000)
2. Check input ranges: Ensure realistic concentration values
3. Review exposure parameters: No negative or zero values
4. Restart assessment: Sometimes random seed issues resolve
```

#### **Error 3: "Results seem unrealistically high/low"**
```
❌ PROBLEM: Unexpected risk values

✅ CHECKLIST:
□ Verify units (per L vs per 100mL vs per mL)
□ Check dilution factors (environmental mixing)
□ Confirm LRV values (treatment effectiveness)
□ Review population size (realistic for scenario)
□ Compare to literature values (sanity check)
```

### **Performance Optimization**

#### **Speed Up Assessments:**
```python
# For testing/development - faster runs
mc_simulator = MonteCarloSimulator(iterations=1000)

# For final reports - thorough analysis
mc_simulator = MonteCarloSimulator(iterations=50000)

# For publications - maximum precision
mc_simulator = MonteCarloSimulator(iterations=100000)
```

#### **Memory Management:**
```python
# For large batch jobs
processor.set_memory_limit(8GB)  # Adjust for your system
processor.enable_parallel_processing(cores=4)
```

---

## ✅ **Quality Assurance Checklist**

### **Before Starting Assessment**
```
DATA VERIFICATION:
□ Pathogen concentrations from reliable sources
□ Treatment LRV values confirmed with engineers
□ Population estimates current and realistic
□ Exposure scenarios match actual conditions
□ Regulatory guidelines up-to-date

TECHNICAL SETUP:
□ Toolkit version is current
□ All required dependencies installed
□ Pathogen database contains needed organisms
□ Assessment parameters documented
□ Backup of input data created
```

### **During Assessment**
```
PROCESS CHECK:
□ Monte Carlo iterations sufficient (≥10,000 for reports)
□ Confidence intervals reasonable (not too wide/narrow)
□ Intermediate results make sense
□ No error messages or warnings
□ Progress tracking documented

SANITY CHECKS:
□ Risk values in expected range (10^-6 to 10^-1)
□ Higher concentrations = higher risk
□ Better treatment = lower risk
□ Results consistent with literature
□ Uncertainty appropriately captured
```

### **After Assessment**
```
RESULTS VALIDATION:
□ Independent verification of key calculations
□ Peer review by qualified colleague
□ Comparison to similar published studies
□ Regulatory compliance properly assessed
□ Recommendations clear and actionable

DOCUMENTATION:
□ All assumptions clearly stated
□ Methods and models referenced
□ Uncertainty and limitations discussed
□ Professional figures generated
□ Executive summary prepared
```

---

## 📊 **Interpreting Results**

### **Risk Value Interpretation Guide**

```
ANNUAL RISK RANGES:
1e-8 to 1e-6  │ ████████████████ │ VERY LOW    │ Excellent compliance
1e-6 to 1e-4  │ ████████████░░░░ │ LOW         │ Meets NZ guidelines
1e-4 to 1e-2  │ ████████░░░░░░░░ │ MODERATE    │ May need management
1e-2 to 1e-1  │ ████░░░░░░░░░░░░ │ HIGH        │ Action required
>1e-1         │ ░░░░░░░░░░░░░░░░ │ VERY HIGH   │ Immediate intervention
```

### **Population Impact Assessment**

#### **Calculate Real-World Meaning:**
```python
# Example calculation
annual_risk = 2.4e-02        # Per person per year
population = 100000          # People at risk
expected_cases = annual_risk * population
print(f"Expected cases per year: {expected_cases}")

# Output: Expected cases per year: 2400
# Meaning: About 2400 people might get sick each year
```

### **Regulatory Compliance Interpretation**

#### **New Zealand Guidelines:**
```
DRINKING WATER EQUIVALENT:
• Target: ≤ 1e-6 annual risk
• Acceptable: ≤ 1e-4 annual risk
• Status: "PASS" or "FAIL"

RECREATIONAL WATER:
• Target: ≤ 1e-3 per exposure event
• Typical: 10-20 exposures per year
• Annual equivalent: ≤ 1e-2 to 2e-2

SHELLFISH CONSUMPTION:
• Target: ≤ 1e-4 annual risk
• Frequency: 12-24 meals per year
• Per meal: ≤ 1e-5 to 5e-6 per serving
```

---

## 🎯 **Client Presentation Guide**

### **Executive Summary Structure**
```
1. PROJECT OVERVIEW (1 slide)
   • What was assessed
   • Why it was needed
   • Key question answered

2. METHODOLOGY (1 slide)
   • QMRA 4-step process
   • Professional toolkit used
   • Conservative assumptions

3. KEY FINDINGS (2-3 slides)
   • Current risk levels
   • Proposed improvements
   • Risk reduction achieved

4. REGULATORY COMPLIANCE (1 slide)
   • NZ guideline comparison
   • Compliance status
   • Safety margins

5. RECOMMENDATIONS (1 slide)
   • Primary recommendation
   • Implementation steps
   • Ongoing monitoring

6. QUESTIONS & DISCUSSION
```

### **Key Messages for Different Audiences**

#### **For Engineers & Technical Staff:**
- Specific LRV values and treatment effectiveness
- Monte Carlo simulation details and uncertainty
- Peer-reviewed models and literature references
- Technical implementation requirements

#### **For Managers & Decision Makers:**
- Bottom-line risk numbers and compliance status
- Cost-benefit implications (cases prevented)
- Regulatory requirements and timelines
- Recommended actions and priorities

#### **For Regulators & Health Officials:**
- Compliance with NZ health guidelines
- Conservative assumptions and safety margins
- Peer-review and quality assurance processes
- Professional methodology and references

---

## 📞 **Getting Help**

### **Internal Support Structure**
```
LEVEL 1 - IMMEDIATE HELP:
• Quick questions: Ask experienced colleague
• GUI problems: Restart toolkit, check dependencies
• Basic interpretation: Use this guide

LEVEL 2 - TECHNICAL SUPPORT:
• Complex scenarios: Senior QMRA specialist
• Custom modifications: Toolkit development team
• Quality assurance: Independent peer reviewer

LEVEL 3 - EXPERT CONSULTATION:
• Novel pathogens: External subject matter expert
• Regulatory queries: Legal/regulatory team
• Research questions: Academic collaborators
```

### **Documentation Resources**
```
QUICK REFERENCE:
• This guide: Day-to-day operations
• User manual: Complete technical reference
• FAQ database: Common questions answered

DETAILED DOCUMENTATION:
• Scientific papers: Methodology validation
• Case studies: Real project examples
• Training materials: Skill development
```

### **Professional Development**
```
BEGINNER → INTERMEDIATE:
• Complete 5 practice assessments
• Review 2 published QMRA studies
• Attend QMRA methodology training

INTERMEDIATE → ADVANCED:
• Lead client project independently
• Peer review colleague's work
• Customize toolkit for new scenarios

ADVANCED → EXPERT:
• Develop new pathogen parameters
• Validate new dose-response models
• Train other staff members
```

---

## 🎓 **Training Certification Path**

### **Level 1: Basic Operator (2-4 weeks)**
```
SKILLS REQUIRED:
□ Understand QMRA concepts
□ Use GUI interface confidently
□ Interpret basic results
□ Generate standard reports

ASSESSMENT:
□ Complete 3 tutorial exercises
□ Pass written knowledge test
□ Demonstrate GUI proficiency
□ Present results to supervisor
```

### **Level 2: Technical Specialist (2-3 months)**
```
SKILLS REQUIRED:
□ Command-line toolkit operation
□ Custom scenario development
□ Quality assurance procedures
□ Client communication

ASSESSMENT:
□ Complete independent project
□ Peer review assessment
□ Client presentation
□ Technical documentation
```

### **Level 3: Expert Practitioner (6-12 months)**
```
SKILLS REQUIRED:
□ Toolkit modification and enhancement
□ New pathogen parameter development
□ Regulatory consultation
□ Staff training capability

ASSESSMENT:
□ Lead complex multi-scenario project
□ Develop new methodology component
□ Train Level 1 operators
□ External peer review validation
```

---

**Document Version**: 2.0
**Last Updated**: September 26, 2025
**Next Review**: December 2025
**Target Audience**: All NIWA QMRA staff levels
**Maintainer**: QMRA Toolkit Development Team