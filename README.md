# Quantitative Microbial Risk Assessment Project

This repository contains the NIWA QMRA Assessment Toolkit and associated project documentation.

## Project Structure

```
.
├── qmra_toolkit/              # Main QMRA Assessment Toolkit
│   ├── src/                   # Core toolkit modules
│   ├── data/                  # Pathogen database and parameters
│   ├── tests/                 # Comprehensive test suite
│   ├── examples/              # Usage examples and demos
│   ├── docs/                  # Technical documentation
│   └── README.md              # Toolkit documentation
├── project_documentation/     # Strategic Investment Proposal and reviews
├── data/                      # Additional project data
└── docs/                      # General project documentation
```

## Quick Start

1. **Navigate to the toolkit directory:**
   ```bash
   cd qmra_toolkit
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run a basic assessment:**
   ```bash
   python src/qmra_toolkit.py assess --pathogen norovirus --exposure-route primary_contact --concentration 10.0 --volume 50.0 --frequency 10 --population 10000 --report
   ```

4. **Explore examples:**
   ```bash
   cd examples
   python pathogen_comparison.py
   ```

## Documentation

- **[Toolkit README](qmra_toolkit/README.md)** - Complete toolkit documentation
- **[User Guide](qmra_toolkit/docs/user_guide.md)** - Detailed usage instructions
- **[Examples Documentation](qmra_toolkit/examples/README.md)** - Example scripts and demos

## Project Background

This toolkit was developed as part of NIWA's Strategic Investment Programme to replace @Risk Excel functionality with automated, reproducible Python workflows for regulatory compliance QMRA assessments.

**Key Objectives:**
- ✅ Replace @Risk Excel dependency with native Python
- ✅ Reduce project delivery time by 60-70%
- ✅ Eliminate manual, error-prone processes
- ✅ Integrate NIWA's dilution modeling expertise
- ✅ Support regulatory compliance market expansion

**Development Team:**
- **Reza Moghaddam** - Lead Developer (150 hours)
- **David Wood** - Model Review & Support (40 hours)
- **Andrew Hughes** - Project Manager

## Key Features

- 🦠 **Comprehensive Pathogen Database** - Validated dose-response models
- 💧 **Multiple Exposure Routes** - Primary contact, shellfish consumption, drinking water
- 🔬 **Dilution Modeling Integration** - NIWA's key differentiator with engineer-provided LRVs
- 📊 **Monte Carlo Simulation** - Advanced uncertainty analysis replacing @Risk
- 📋 **Automated Reporting** - Generate regulatory compliance reports in Word format
- ⚡ **Command-Line Interface** - Easy-to-use CLI for common workflows

## Benefits Over @Risk

| Feature | @Risk | QMRA Toolkit |
|---------|-------|--------------|
| **Platform** | Excel-dependent | Native Python |
| **Security** | Firewall conflicts | No external dependencies |
| **Automation** | Manual processes | Fully automated |
| **Reproducibility** | Limited | Complete version control |
| **Cost** | Commercial license | Open source |
| **Integration** | Limited | NIWA dilution modeling |

## Support

For technical support, feature requests, or bug reports, contact the NIWA QMRA team.

---

*Developed by NIWA Earth Sciences New Zealand*
*Strategic Investment Programme 2025-2026*