# QMRA Batch Processing App - Installation Guide

**Standalone Quantitative Microbial Risk Assessment Tool**

Version 1.0 | October 2025 | NIWA Earth Sciences New Zealand

---

## Overview

This is a **standalone** QMRA batch processing application that includes all necessary components to run without requiring the parent QMRA toolkit. The application can be copied to any location and will function independently.

---

## System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk Space**: 100 MB for application and dependencies

### Recommended
- **Python**: 3.9 - 3.11
- **RAM**: 16 GB for large batch processing (>1000 scenarios)
- **Internet**: Required for initial package installation only

---

## Quick Installation

### Option 1: Windows Users (Easiest)

1. **Ensure Python is installed:**
   ```bash
   python --version
   ```
   If Python is not installed, download from [python.org](https://www.python.org/downloads/)

2. **Install dependencies:**
   ```bash
   cd Batch_Processing_App
   pip install -r requirements.txt
   ```

3. **Launch the application:**
   - Double-click `launch_web_gui.bat`
   - OR run: `streamlit run web_app.py`

4. **Access the web interface:**
   - Browser will open automatically at `http://localhost:8502`

### Option 2: Mac/Linux Users

1. **Ensure Python is installed:**
   ```bash
   python3 --version
   ```

2. **Install dependencies:**
   ```bash
   cd Batch_Processing_App
   pip3 install -r requirements.txt
   ```

3. **Launch the application:**
   ```bash
   streamlit run web_app.py
   ```

4. **Access the web interface:**
   - Open browser to `http://localhost:8502`

### Option 3: Using Virtual Environment (Recommended for Production)

**Windows:**
```bash
cd Batch_Processing_App
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run web_app.py
```

**Mac/Linux:**
```bash
cd Batch_Processing_App
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run web_app.py
```

---

## Standalone Package Contents

The Batch_Processing_App is **completely self-contained** with the following structure:

```
Batch_Processing_App/
│
├── qmra_core/                    # Standalone QMRA engine (NO external dependencies)
│   ├── __init__.py
│   ├── pathogen_database.py      # Pathogen parameters and dose-response data
│   ├── dose_response.py          # Dose-response models (Beta-Poisson, Exponential)
│   ├── monte_carlo.py            # Monte Carlo simulation engine
│   └── data/
│       └── pathogen_parameters.json   # Pathogen database (6 pathogens)
│
├── web_app.py                    # Streamlit web interface
├── batch_processor.py            # Core batch processing logic
├── pdf_report_generator.py       # PDF report generation
├── launch_web_gui.bat           # Windows launcher
├── requirements.txt              # Python package dependencies
├── README.md                     # User guide
├── INSTALLATION.md              # This file
│
└── input_data/                   # Example datasets
    ├── batch_scenarios/
    ├── pathogen_concentrations/
    ├── dilution_data/
    ├── treatment_scenarios/
    └── exposure_scenarios/
```

### Key Features of Standalone Design

1. **No parent directory dependencies** - All QMRA modules are bundled in `qmra_core/`
2. **Portable** - Copy the entire `Batch_Processing_App/` folder anywhere
3. **Self-contained** - Includes pathogen database and all necessary data files
4. **Independent versioning** - Can be updated separately from main toolkit

---

## Verification

After installation, verify everything is working:

```python
cd Batch_Processing_App
python -c "from qmra_core import PathogenDatabase; print(PathogenDatabase().get_available_pathogens())"
```

Expected output:
```
['norovirus', 'campylobacter', 'cryptosporidium', 'e_coli', 'salmonella', 'rotavirus']
```

---

## Dependencies Explained

All dependencies are standard scientific Python packages:

| Package | Purpose | Size |
|---------|---------|------|
| numpy | Numerical computing | ~15 MB |
| pandas | Data manipulation | ~10 MB |
| scipy | Scientific algorithms | ~20 MB |
| matplotlib | Plotting | ~15 MB |
| streamlit | Web interface | ~30 MB |
| pyyaml | Configuration files | <1 MB |
| openpyxl | Excel export | ~3 MB |
| reportlab | PDF generation | ~5 MB |

**Total installed size:** ~100-150 MB

---

## Troubleshooting

### Issue: `pip: command not found`

**Solution:** Install pip or use `python -m pip` instead:
```bash
python -m pip install -r requirements.txt
```

---

### Issue: `ModuleNotFoundError: No module named 'qmra_core'`

**Solution:** Ensure you're running from the `Batch_Processing_App/` directory:
```bash
cd Batch_Processing_App
python web_app.py
```

---

### Issue: Port 8502 already in use

**Solution:** Use a different port:
```bash
streamlit run web_app.py --server.port 8503
```

---

### Issue: Permission denied on Windows

**Solution:** Run as administrator or use:
```bash
python -m streamlit run web_app.py
```

---

## Distribution

To share this application with colleagues:

1. **Zip the entire folder:**
   ```
   Batch_Processing_App.zip
   ```

2. **Share with instructions:**
   - Extract to any location
   - Install Python 3.8+
   - Run: `pip install -r requirements.txt`
   - Launch: `streamlit run web_app.py`

3. **No other files needed** - The app is fully self-contained!

---

## Updating

To update dependencies:

```bash
pip install --upgrade -r requirements.txt
```

To update the application:
- Replace the `Batch_Processing_App/` folder with the new version
- Rerun `pip install -r requirements.txt`

---

## Uninstalling

To remove the application:

1. Delete the `Batch_Processing_App/` folder
2. (Optional) Remove the virtual environment if created
3. (Optional) Uninstall packages (if not needed elsewhere):
   ```bash
   pip uninstall -r requirements.txt -y
   ```

---

## Support

**For installation issues:**
- Verify Python version: `python --version`
- Check pip: `pip --version`
- Ensure internet connection for initial install

**For application issues:**
- See `README.md` for usage instructions
- Check example files in `input_data/`
- Review error messages in the terminal

---

## Advanced: Docker Deployment (Optional)

For containerized deployment, create a `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY Batch_Processing_App/ /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8502

CMD ["streamlit", "run", "web_app.py", "--server.port=8502", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t qmra-batch .
docker run -p 8502:8502 qmra-batch
```

---

## License & Credits

**Developed by:** NIWA Earth Sciences New Zealand
**Version:** 1.0
**Release Date:** October 2025

This standalone application bundles core QMRA modules for ease of distribution.

For questions or issues, contact NIWA Earth Sciences.

---

**End of Installation Guide**
