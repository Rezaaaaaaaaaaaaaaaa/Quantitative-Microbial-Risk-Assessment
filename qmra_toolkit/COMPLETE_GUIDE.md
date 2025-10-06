# NIWA QMRA Toolkit - Complete Getting Started Guide

**Version 2.0 - October 2025**

This comprehensive guide covers everything you need to install, use, and master the NIWA QMRA Assessment Toolkit.

---

## 📦 What's Included

### 1. **Two User Interfaces**
- **Desktop GUI** - Traditional application with tkinter
- **Web App** - Modern browser-based interface with Streamlit

### 2. **Comprehensive Documentation**
- **User Manual** (47 pages) - Complete methodology and workflows
- **Web App Guide** - Browser application documentation
- **Quick Start Guides** - Built into both interfaces
- **Troubleshooting** - Common issues and solutions

### 3. **Example Projects**
- Beach Swimming Assessment
- Drinking Water Safety
- Wastewater Treatment Comparison
- Shellfish Harvesting Risk

### 4. **Automated Installation**
- One-click setup script
- Automatic dependency installation
- Directory structure creation

---

## 🚀 Quick Installation (3 Steps)

### Step 1: Download/Clone Repository
```bash
# If using Git
git clone <repository-url>
cd qmra_toolkit

# Or download and extract ZIP file
```

### Step 2: Run Installation Script

**Windows:**
```
Double-click: INSTALL.bat
```

**Mac/Linux:**
```bash
python3 install.py
```

### Step 3: Verify Installation
The installer will automatically:
- ✅ Check Python version (3.8+ required)
- ✅ Install core dependencies (numpy, scipy, matplotlib, pandas)
- ✅ Install GUI dependencies (tkinter)
- ✅ Install web dependencies (streamlit, plotly)
- ✅ Install optional features (PDF/Word generation)
- ✅ Create directory structure
- ✅ Verify all components
- ✅ Create launcher scripts

---

## 🎯 Choosing Your Interface

### Use Desktop GUI When:
- ✓ Working offline
- ✓ Prefer traditional desktop applications
- ✓ Need quick local analysis
- ✓ Want familiar Windows/Mac interface

**Launch:**
```
Windows: Double-click Launch_QMRA_GUI.bat
Mac/Linux: ./launch_gui.sh
Or: python launch_enhanced_gui.py
```

### Use Web App When:
- ✓ Want modern, interactive visualizations
- ✓ Need mobile/tablet access
- ✓ Deploying to cloud
- ✓ Sharing with remote team
- ✓ Prefer browser-based tools

**Launch:**
```
Windows: Double-click Launch_Web_App.bat
Mac/Linux: ./launch_web.sh
Or: streamlit run web_app.py
```

---

## 📚 Learning Path

### Level 1: Beginner (30 minutes)

1. **Read Quick Start**
   - Desktop GUI: Help → Quick Start Guide
   - Web App: Navigate to Help page

2. **Try Demo Mode**
   - Web App: Click "🎮 Demo Mode" button
   - Automatically loads beach swimming example
   - Pre-calculated results ready to explore

3. **Explore Interface**
   - Navigate all tabs/pages
   - View pre-calculated results
   - Check visualizations
   - Review compliance status

### Level 2: Intermediate (1-2 hours)

1. **Load Example Project**
   - File → Open Project
   - Select: `examples/projects/beach_swimming_assessment.json`
   - Study the pre-filled parameters

2. **Run Your First Assessment**
   - Review pathogen settings (Norovirus)
   - Check exposure parameters
   - Click "Run Assessment"
   - Analyze results

3. **Modify Parameters**
   - Change concentration (try 500 or 2000)
   - Adjust frequency (try 10 or 15)
   - Re-run and compare results

4. **Generate Outputs**
   - Create visualizations
   - Generate report (PDF/Word)
   - Export results to CSV

### Level 3: Advanced (2-4 hours)

1. **Try Different Scenarios**
   - Drinking Water Safety example
   - Compare Cryptosporidium vs Norovirus
   - Understand regulatory compliance

2. **Multi-Pathogen Assessment**
   - Load: `wastewater_treatment_comparison.json`
   - Study multi-pathogen setup
   - Compare treatment scenarios
   - Analyze cost-benefit

3. **Complex Assessment**
   - Load: `shellfish_consumption_risk.json`
   - Understand bioaccumulation
   - Explore seasonal variations
   - Review management options

4. **Create Your Own Project**
   - Set up from scratch
   - Use your monitoring data
   - Apply to your location
   - Generate professional report

---

## 🎓 Key Concepts

### QMRA Framework (4 Steps)

1. **Hazard Identification**
   - Select pathogen (Norovirus, Campylobacter, Cryptosporidium, etc.)
   - Choose primary concern for your scenario

2. **Exposure Assessment**
   - Define route (swimming, drinking, shellfish)
   - Set concentration (from monitoring data)
   - Determine volume ingested/contacted
   - Specify frequency of exposure

3. **Dose-Response**
   - Automatic based on pathogen selection
   - Uses validated models from literature
   - Exponential or Beta-Poisson models

4. **Risk Characterization**
   - Monte Carlo simulation (10,000 iterations)
   - Infection risk, illness risk, annual risk
   - Population impact calculation
   - Uncertainty quantification

### Understanding Results

**Infection Risk (Pinf):** Probability per exposure
- Example: 0.05 = 5% chance per swim

**Illness Risk (Pill):** Symptomatic infection probability
- Example: 0.035 = 3.5% chance of illness per exposure

**Annual Risk (Pannual):** Risk over one year
- Example: 0.30 = 30% chance of ≥1 infection/year

**Population Impact:** Expected cases
- Example: 30,000 cases in 100,000 people

### Regulatory Benchmarks

**NZ Drinking Water:** ≤ 10⁻⁶ DALY/person/year
**WHO Guidelines:** ≤ 10⁻⁶ DALY/person/year
**Recreational Water:** ~10⁻³ illness risk (context-dependent)

### Compliance Status

- ✅ **COMPLIANT** - Risk ≤ benchmark
- ⚠️ **MARGINAL** - Risk slightly above benchmark
- ❌ **NON-COMPLIANT** - Risk significantly exceeds benchmark

---

## 💡 Pro Tips

### Data Quality
1. Use recent monitoring data (<3 months when possible)
2. Take multiple samples for Monte Carlo input
3. Use 95th percentile for conservative estimates
4. Document all data sources

### Parameter Selection
1. Click 📊 for typical concentration ranges
2. Check LRV guidelines for treatment types
3. Use Concentration Helper in GUI
4. Validate against published studies

### Results Interpretation
1. Report median AND 95th percentile
2. Include confidence intervals
3. Compare to regulatory benchmarks
4. Assess practical significance

### Report Generation
1. Use Executive Summary for decision-makers
2. Use Technical Report for peer review
3. Include uncertainty analysis
4. Add literature references

---

## 🆘 Troubleshooting

### Installation Issues

**Problem:** Python version too old
**Solution:** Install Python 3.8+ from python.org

**Problem:** pip install fails
**Solution:** Update pip: `python -m pip install --upgrade pip`

**Problem:** tkinter not found (Linux)
**Solution:** `sudo apt-get install python3-tk` (Ubuntu/Debian)

### Application Issues

**Problem:** Results seem unrealistic
**Solutions:**
- Check units (copies/L not /100mL)
- Verify volume in mL not L
- Confirm LRV applied correctly
- Use Concentration Helper

**Problem:** Simulation too slow
**Solutions:**
- Reduce iterations to 1,000 for testing
- Close other applications
- Disable auto-plotting

**Problem:** Can't generate report
**Solutions:**
- Run assessment first
- Install: `pip install reportlab python-docx`
- Try different format (PDF vs Word)

### Web App Issues

**Problem:** streamlit command not found
**Solution:** `pip install streamlit`

**Problem:** Port already in use
**Solution:** `streamlit run web_app.py --server.port 8502`

**Problem:** Can't access from other device
**Solution:** `streamlit run web_app.py --server.address 0.0.0.0`

---

## 📁 File Structure Reference

```
qmra_toolkit/
│
├── docs/
│   ├── USER_MANUAL.md          # 47-page comprehensive manual
│   └── USER_MANUAL.pdf          # PDF version (after generation)
│
├── examples/
│   └── projects/
│       ├── beach_swimming_assessment.json
│       ├── drinking_water_safety.json
│       ├── wastewater_treatment_comparison.json
│       ├── shellfish_consumption_risk.json
│       └── README.md            # Example projects guide
│
├── src/
│   ├── enhanced_qmra_gui.py     # Desktop GUI (enhanced with help)
│   ├── pathogen_database.py
│   ├── exposure_assessment.py
│   └── risk_characterization.py
│
├── web_app.py                   # Streamlit web application
├── launch_enhanced_gui.py       # GUI launcher
├── install.py                   # Installation script
│
├── Launch_QMRA_GUI.bat         # Windows GUI launcher
├── Launch_Web_App.bat          # Windows web launcher
├── INSTALL.bat                 # Windows installer
│
├── WEB_APP_README.md           # Web app documentation
├── WHATS_NEW.md                # Release notes
├── COMPLETE_GUIDE.md           # This file
├── README.md                   # Main project README
│
├── requirements.txt            # Core dependencies
└── requirements_web.txt        # Web app dependencies
```

---

## 🔧 Advanced Configuration

### Custom Pathogen Models

Add to pathogen database:
1. Navigate to Pathogen Database tab
2. Click "Add Custom Pathogen"
3. Enter dose-response parameters
4. Provide literature reference

### Batch Processing

Run multiple scenarios:
```bash
python src/qmra_toolkit.py batch --config scenarios.json
```

### Cloud Deployment (Web App)

**Streamlit Cloud (Free):**
1. Push to GitHub
2. Visit share.streamlit.io
3. Connect repository
4. Deploy

**Other Platforms:**
- Heroku: `heroku create && git push heroku main`
- AWS EC2/Elastic Beanstalk
- Azure App Service
- Google Cloud Run

---

## 📊 Workflow Examples

### Scenario 1: Beach Safety Assessment

1. **Project Setup**
   - Name: "Mission Bay Beach Summer 2025"
   - Population: 50,000 visitors

2. **Parameters**
   - Pathogen: Norovirus
   - Route: Primary Contact
   - Concentration: 1,000 copies/L
   - Volume: 100 mL
   - Frequency: 7 events/year

3. **Run & Analyze**
   - Monte Carlo: 10,000 iterations
   - Review annual risk
   - Check compliance

4. **Outputs**
   - Risk distribution plot
   - Compliance dashboard
   - Executive summary report

### Scenario 2: Treatment Upgrade Decision

1. **Current System**
   - Secondary treatment
   - LRV: 1.5 log

2. **Proposed System**
   - Tertiary + UV
   - LRV: 3.5 log

3. **Compare**
   - Run both scenarios
   - Calculate risk reduction
   - Estimate cases prevented

4. **Decision Support**
   - Cost per case avoided
   - Compliance improvement
   - Public health benefit

---

## 🎯 Success Checklist

Before finalizing any assessment:

- [ ] **Data Quality**
  - [ ] Recent monitoring data used
  - [ ] Multiple samples for variability
  - [ ] Sources documented

- [ ] **Parameters**
  - [ ] Units verified (copies/L, mL, events/year)
  - [ ] Values within typical ranges
  - [ ] LRVs appropriate for treatment type

- [ ] **Analysis**
  - [ ] Sufficient iterations (≥10,000)
  - [ ] Uncertainty included
  - [ ] Sensitivity checked

- [ ] **Results**
  - [ ] Median and percentiles reported
  - [ ] Compared to benchmarks
  - [ ] Practical significance assessed

- [ ] **Documentation**
  - [ ] Assumptions listed
  - [ ] Limitations noted
  - [ ] References included

- [ ] **QA/QC**
  - [ ] Peer reviewed
  - [ ] Results benchmarked
  - [ ] Sanity checked

---

## 📞 Getting Help

### Built-in Help

**Desktop GUI:**
- Help → User Manual (F1)
- Help → Quick Start Guide
- Help → Troubleshooting
- Help → Online Resources

**Web App:**
- Help page with 4 tabs:
  - Quick Start
  - User Manual
  - Troubleshooting
  - About

### Documentation

1. **USER_MANUAL.md** - Complete 47-page guide
2. **WEB_APP_README.md** - Web app specific
3. **WHATS_NEW.md** - Latest features
4. **examples/projects/README.md** - Example guide

### Support Channels

- **NIWA QMRA Team** - Primary support
- **GitHub Issues** - Bug reports, feature requests
- **Email** - [Contact information]

### Online Resources

- US EPA QMRA Wiki: https://qmrawiki.org/
- WHO Water Safety: https://www.who.int/water_sanitation_health/
- NZ Ministry of Health: https://www.health.govt.nz/

---

## 🏆 Best Practices

### Professional Assessment

1. **Always document:**
   - Data sources and dates
   - All assumptions
   - Known limitations
   - QA/QC steps

2. **Use conservative estimates:**
   - 95th percentile concentrations
   - Upper bound exposure volumes
   - Protective LRV values

3. **Include uncertainty:**
   - Monte Carlo distributions
   - Confidence intervals
   - Sensitivity analysis

4. **Validate results:**
   - Compare to literature
   - Benchmark against similar studies
   - Peer review process

### Report Quality

1. **Executive Summary:**
   - Decision-focused
   - Key findings first
   - Visual summaries

2. **Technical Report:**
   - Full methodology
   - Detailed results
   - Peer-review ready

3. **Regulatory Submission:**
   - Compliance-focused
   - All data in appendices
   - Meet specific requirements

---

## 🚀 Next Steps

### Immediate (Today):
1. Run installation: `INSTALL.bat` or `python install.py`
2. Launch GUI or Web App
3. Try Demo Mode (web app)
4. Load beach swimming example

### Short-term (This Week):
1. Complete all 4 example projects
2. Read relevant USER_MANUAL sections
3. Create first custom assessment
4. Generate professional report

### Long-term (This Month):
1. Apply to real projects
2. Develop project templates
3. Train team members
4. Establish QA procedures

---

## 📈 Version History

**v2.0 (October 2025)** - Current
- ✅ Comprehensive 47-page User Manual
- ✅ Enhanced GUI with Help menu
- ✅ Browser-based Web Application
- ✅ 4 detailed example projects
- ✅ Automated installation script
- ✅ Interactive Plotly visualizations
- ✅ Demo mode for quick testing
- ✅ PDF manual generation
- ✅ Cloud deployment ready

**v1.0 (September 2025)**
- Initial release
- Core QMRA functionality
- Basic GUI
- Command-line interface

---

## 📝 License & Citation

**© 2025 NIWA (National Institute of Water & Atmospheric Research Ltd)**

This software is provided for professional QMRA assessments.

**Citation:**
```
Moghaddam, R., Wood, D., & Hughes, A. (2025).
NIWA QMRA Assessment Toolkit (Version 2.0) [Computer software].
NIWA Earth Sciences, New Zealand.
```

---

## 🎉 You're Ready!

You now have everything needed to:
- ✅ Install the toolkit
- ✅ Run professional QMRA assessments
- ✅ Generate regulatory reports
- ✅ Support decision-making
- ✅ Ensure public health protection

**Start with:**
```
python install.py
```

Then choose your interface and begin your QMRA journey!

---

**Questions? Issues? Suggestions?**

Contact the NIWA QMRA Team or check the comprehensive User Manual.

**Happy Assessing! 🧬💧🏖️**
