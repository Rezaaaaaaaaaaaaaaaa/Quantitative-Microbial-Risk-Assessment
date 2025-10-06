# What's New in QMRA Toolkit v2.0

## October 2025 Release

This release adds comprehensive user documentation and a browser-based web interface to the NIWA QMRA Assessment Toolkit.

---

## 📖 New: Comprehensive User Manual

### Location
`qmra_toolkit/docs/USER_MANUAL.md`

### Contents (47 pages)
1. **Introduction** - Overview and key features
2. **Understanding QMRA** - QMRA methodology explained
3. **Getting Started** - Installation and setup
4. **Interface Overview** - Detailed GUI walkthrough
5. **Step-by-Step Workflows** - Three complete workflow examples
6. **Understanding Results** - Interpreting risk metrics
7. **Advanced Features** - Custom models, batch processing, sensitivity analysis
8. **Troubleshooting** - Common issues and solutions
9. **Best Practices** - Data quality, documentation, validation
10. **References and Resources** - Literature, online resources, training
11. **Appendices** - Pathogen information, glossary

### Key Features
- ✅ Complete context on QMRA methodology
- ✅ NZ regulatory framework explained
- ✅ Three detailed workflow examples
- ✅ Troubleshooting guide with solutions
- ✅ Best practices for professional assessments
- ✅ Pathogen-specific information
- ✅ Comprehensive glossary

---

## 🎯 Enhanced Desktop GUI

### New Help Menu
Access from the menu bar: **Help** → Choose option

#### Help Menu Items:
1. **📖 User Manual** - Opens comprehensive USER_MANUAL.md
2. **🚀 Quick Start Guide** - In-app quick reference (5 steps)
3. **💡 Troubleshooting** - Common issues and solutions
4. **📊 Example Projects** - Opens examples directory
5. **🔗 Online Resources** - Links to QMRA resources
6. **ℹ️ About QMRA Toolkit** - Version and credits

### Keyboard Shortcuts
- `Ctrl+N` - New Project
- `Ctrl+O` - Open Project
- `Ctrl+S` - Save Project
- `F1` - Open User Manual
- `F5` - Refresh Results

### Quick Start Guide (In-App)
Accessible pop-up window with:
- 5-step basic workflow
- Common scenario examples (swimming, drinking water, treatment comparison)
- Understanding results section
- Keyboard shortcuts
- Typical concentration ranges
- LRV guidelines
- Troubleshooting tips

### Troubleshooting Guide (In-App)
Comprehensive troubleshooting window covering:
- Application launch issues
- Unrealistic results
- Slow Monte Carlo simulations
- Report generation problems
- Plot display issues
- Error message explanations
- Data quality checks

---

## 🌐 NEW: Browser-Based Web Application

### What is it?
A modern, browser-based interface using Streamlit that provides all QMRA functionality through a web browser.

### How to Launch

**Option 1: Batch File (Windows)**
```
Double-click: Launch_Web_App.bat
```

**Option 2: Command Line**
```bash
cd qmra_toolkit
streamlit run web_app.py
```

**Option 3: Python**
```python
import subprocess
subprocess.run(['streamlit', 'run', 'web_app.py'])
```

Browser automatically opens to: `http://localhost:8501`

### Installation
```bash
pip install -r requirements_web.txt
```

Required packages:
- streamlit (web framework)
- plotly (interactive visualizations)
- pandas, numpy (data analysis)
- matplotlib, scipy (scientific computing)

### Web App Features

#### 8 Interactive Pages:

1. **🏠 Home**
   - Overview of toolkit capabilities
   - Quick start guide
   - Regulatory context
   - Getting started instructions

2. **📋 Project Setup**
   - Project information entry
   - Population at risk configuration
   - Helpful tips and typical ranges

3. **🧬 Assessment**
   - Pathogen selection with info popups
   - Exposure route configuration
   - Concentration helper with typical ranges
   - Monte Carlo settings
   - Run assessment button

4. **🔬 Treatment Scenarios**
   - Current vs. proposed treatment comparison
   - LRV configuration
   - Dilution factor settings
   - Built-in LRV guidelines

5. **📈 Results**
   - Summary metrics cards
   - Regulatory compliance status
   - Detailed statistics table
   - CSV download option

6. **📊 Visualizations**
   - Interactive Plotly charts:
     * Risk Distribution (histogram with percentiles)
     * Percentile Comparison (grouped bar chart)
     * Population Impact (gauge chart)
     * Compliance Dashboard (compliance gauge)
   - Zoom, pan, hover features
   - Export to PNG/SVG

7. **📄 Reports**
   - Report template selection
   - Customizable options
   - PDF/Word generation (planned)

8. **📖 Help**
   - Quick Start tab
   - User Manual tab
   - Troubleshooting tab
   - About tab

### Web App Advantages

#### 🚀 Accessibility
- No desktop GUI frameworks required
- Access from any device with browser
- Works on Windows, Mac, Linux, tablets
- Mobile-responsive design

#### 📊 Better Visualizations
- Interactive Plotly charts (vs. static matplotlib)
- Zoom, pan, hover, download features
- Real-time updates
- Professional presentation

#### 🌐 Deployment Options
- Local: `streamlit run web_app.py`
- Network: `streamlit run web_app.py --server.address 0.0.0.0`
- Cloud: Deploy to Streamlit Cloud, Heroku, AWS, Azure, GCP

#### 💻 Modern UX
- Clean, card-based interface
- Color-coded status indicators
- Responsive layout
- Real-time feedback

---

## 📚 Documentation Summary

### Files Created

1. **`docs/USER_MANUAL.md`** (47 pages)
   - Complete user documentation
   - QMRA methodology
   - Step-by-step workflows
   - Troubleshooting guide
   - Best practices
   - References

2. **`src/enhanced_qmra_gui.py`** (Updated)
   - Added menu bar
   - File, Edit, Help menus
   - Quick Start Guide dialog
   - Troubleshooting Guide dialog
   - Online Resources window
   - About dialog
   - Keyboard shortcuts

3. **`web_app.py`** (New - 1,000+ lines)
   - Complete Streamlit web application
   - 8 interactive pages
   - Plotly visualizations
   - Session state management
   - Responsive design

4. **`WEB_APP_README.md`** (New)
   - Web app documentation
   - Installation instructions
   - Deployment guide
   - Troubleshooting
   - Comparison: Desktop vs. Web

5. **`Launch_Web_App.bat`** (New)
   - Windows batch file launcher
   - Automatic browser opening
   - User-friendly interface

6. **`requirements_web.txt`** (New)
   - Web app dependencies
   - Streamlit, Plotly, etc.
   - Easy installation

---

## 🎨 Interface Improvements

### Desktop GUI
- Professional menu bar
- In-app help dialogs
- Keyboard shortcuts
- Better user guidance
- Quick access to documentation

### Web App
- Modern card-based layout
- Color-coded status indicators:
  - 🟢 Green = Compliant
  - 🟡 Yellow = Marginal/Warning
  - 🔴 Red = Non-compliant/Error
- Interactive tooltips
- Expandable sections
- Responsive columns

---

## 🚀 Getting Started

### Desktop GUI with Help System

1. **Launch GUI:**
   ```bash
   python launch_enhanced_gui.py
   ```

2. **Access Help:**
   - Click **Help** menu → **User Manual**
   - Or press **F1**
   - Or click **Help** → **Quick Start Guide**

3. **In-App Assistance:**
   - Quick Start Guide: Step-by-step walkthrough
   - Troubleshooting: Solutions to common issues
   - Online Resources: External QMRA links

### Web Application

1. **Install Dependencies:**
   ```bash
   pip install -r requirements_web.txt
   ```

2. **Launch Web App:**
   ```bash
   streamlit run web_app.py
   ```
   Or double-click `Launch_Web_App.bat`

3. **Navigate:**
   - Use sidebar to switch between pages
   - Start with 🏠 Home for overview
   - Follow 📋 → 🧬 → 📈 → 📊 workflow

---

## 📊 Comparison: Desktop vs. Web

| Feature | Desktop GUI | Web App |
|---------|-------------|---------|
| **User Manual** | ✅ Opens from Help menu | ✅ Built-in Help tab |
| **Quick Start** | ✅ In-app dialog | ✅ Integrated in pages |
| **Troubleshooting** | ✅ In-app dialog | ✅ Help tab section |
| **Visualizations** | Matplotlib (static) | Plotly (interactive) |
| **Access** | Local only | Browser, any device |
| **Installation** | Tkinter (included) | pip install streamlit |
| **Deployment** | .exe possible | Cloud-ready |
| **Mobile** | ❌ No | ✅ Yes |

**Recommendation:**
- **Desktop GUI**: For offline work, traditional desktop users
- **Web App**: For modern UX, cloud deployment, mobile access, collaboration

---

## 🎯 Use Cases

### Use Desktop GUI When:
- ✓ Working offline
- ✓ Need .exe deployment
- ✓ Prefer traditional desktop applications
- ✓ No web server requirements

### Use Web App When:
- ✓ Want modern, interactive visualizations
- ✓ Need mobile/tablet access
- ✓ Deploying to cloud
- ✓ Sharing with remote team
- ✓ Prefer browser-based tools

### Use Both:
- ✓ Desktop for offline analysis
- ✓ Web for presentations and sharing
- ✓ Both access same underlying QMRA toolkit

---

## 📝 Next Steps

### For Users:

1. **Read the User Manual**
   - Open from Help menu or `docs/USER_MANUAL.md`
   - Understanding QMRA section explains methodology
   - Step-by-Step Workflows provide examples

2. **Try Both Interfaces**
   - Desktop GUI: `python launch_enhanced_gui.py`
   - Web App: `streamlit run web_app.py`
   - Choose your preferred interface

3. **Run Example Assessments**
   - Follow Quick Start Guide workflows
   - Try swimming safety assessment
   - Try drinking water assessment
   - Compare treatment scenarios

### For Developers:

1. **Customize Web App**
   - Edit `web_app.py` styling
   - Modify default values
   - Add custom visualizations

2. **Deploy to Cloud**
   - Follow WEB_APP_README.md deployment section
   - Streamlit Cloud (easiest)
   - Or Heroku, AWS, Azure, GCP

3. **Extend Functionality**
   - Add new pathogen models
   - Create custom report templates
   - Integrate with databases

---

## 📞 Support

### Documentation
- **User Manual**: `docs/USER_MANUAL.md` (47 pages)
- **Web App Guide**: `WEB_APP_README.md`
- **Quick Start**: Help → Quick Start Guide (in app)
- **Troubleshooting**: Help → Troubleshooting (in app)

### Contact
- NIWA QMRA Team
- GitHub Issues: [Repository]
- Email: [Contact Information]

---

## 🙏 Acknowledgments

**Development Team:**
- Reza Moghaddam - Lead Developer
- David Wood - Model Review & Support
- Andrew Hughes - Project Manager

**NIWA Earth Sciences**
National Institute of Water & Atmospheric Research
New Zealand

---

**Enjoy the enhanced QMRA Toolkit with comprehensive documentation and web interface!** 🚀

© 2025 NIWA
