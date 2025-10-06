"""
NIWA QMRA Toolkit - Automated Installation Script
Comprehensive setup and verification for both desktop GUI and web application
"""

import subprocess
import sys
import os
from pathlib import Path
import platform

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print formatted header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")

def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")

def print_info(text):
    """Print info message."""
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.ENDC}")

def print_warning(text):
    """Print warning message."""
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def print_error(text):
    """Print error message."""
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def check_python_version():
    """Check if Python version is adequate."""
    print_header("CHECKING PYTHON VERSION")

    version = sys.version_info
    print_info(f"Python version: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error("Python 3.8 or higher is required!")
        print_info("Please upgrade Python: https://www.python.org/downloads/")
        return False

    print_success(f"Python {version.major}.{version.minor} is compatible")
    return True

def install_package(package_name, import_name=None):
    """Install a single package."""
    if import_name is None:
        import_name = package_name

    try:
        __import__(import_name)
        print_success(f"{package_name} is already installed")
        return True
    except ImportError:
        print_info(f"Installing {package_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
            print_success(f"{package_name} installed successfully")
            return True
        except subprocess.CalledProcessError:
            print_error(f"Failed to install {package_name}")
            return False

def install_core_dependencies():
    """Install core QMRA toolkit dependencies."""
    print_header("INSTALLING CORE DEPENDENCIES")

    core_packages = [
        ("numpy", "numpy"),
        ("scipy", "scipy"),
        ("matplotlib", "matplotlib"),
        ("pandas", "pandas"),
    ]

    success = True
    for package, import_name in core_packages:
        if not install_package(package, import_name):
            success = False

    return success

def install_gui_dependencies():
    """Install desktop GUI dependencies."""
    print_header("INSTALLING DESKTOP GUI DEPENDENCIES")

    # Check tkinter (usually comes with Python)
    try:
        import tkinter
        print_success("tkinter is available (comes with Python)")
    except ImportError:
        print_warning("tkinter not found - may need system package")
        if platform.system() == "Linux":
            print_info("On Ubuntu/Debian: sudo apt-get install python3-tk")
            print_info("On Fedora: sudo dnf install python3-tkinter")
        return False

    return True

def install_web_dependencies():
    """Install web application dependencies."""
    print_header("INSTALLING WEB APPLICATION DEPENDENCIES")

    web_packages = [
        ("streamlit", "streamlit"),
        ("plotly", "plotly"),
    ]

    success = True
    for package, import_name in web_packages:
        if not install_package(package, import_name):
            success = False

    return success

def install_optional_dependencies():
    """Install optional dependencies for enhanced features."""
    print_header("INSTALLING OPTIONAL DEPENDENCIES")

    optional_packages = [
        ("reportlab", "reportlab", "PDF report generation"),
        ("python-docx", "docx", "Word document generation"),
        ("openpyxl", "openpyxl", "Excel export support"),
    ]

    for package, import_name, description in optional_packages:
        print_info(f"Installing {package} ({description})...")
        install_package(package, import_name)

def create_directories():
    """Create necessary directories."""
    print_header("CREATING DIRECTORY STRUCTURE")

    base_dir = Path(__file__).parent
    directories = [
        base_dir / "data",
        base_dir / "logs",
        base_dir / "outputs",
        base_dir / "outputs" / "reports",
        base_dir / "outputs" / "plots",
        base_dir / "examples" / "projects",
    ]

    for directory in directories:
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            print_success(f"Created: {directory.relative_to(base_dir)}")
        else:
            print_info(f"Exists: {directory.relative_to(base_dir)}")

def verify_installation():
    """Verify all components are installed correctly."""
    print_header("VERIFYING INSTALLATION")

    # Check core components
    checks = {
        "NumPy": "numpy",
        "SciPy": "scipy",
        "Matplotlib": "matplotlib",
        "Pandas": "pandas",
        "Tkinter": "tkinter",
        "Streamlit": "streamlit",
        "Plotly": "plotly",
    }

    all_good = True
    for name, module in checks.items():
        try:
            __import__(module)
            print_success(f"{name} is ready")
        except ImportError:
            print_warning(f"{name} is not available")
            if module in ["streamlit", "plotly"]:
                print_info(f"  Web app features will not be available")
            else:
                all_good = False

    return all_good

def check_example_files():
    """Check if example files exist."""
    print_header("CHECKING EXAMPLE FILES")

    base_dir = Path(__file__).parent
    examples_dir = base_dir / "examples" / "projects"

    example_files = [
        "beach_swimming_assessment.json",
        "drinking_water_safety.json",
        "wastewater_treatment_comparison.json",
        "shellfish_consumption_risk.json"
    ]

    for example in example_files:
        example_path = examples_dir / example
        if example_path.exists():
            print_success(f"Found: {example}")
        else:
            print_warning(f"Missing: {example}")

def check_documentation():
    """Check if documentation exists."""
    print_header("CHECKING DOCUMENTATION")

    base_dir = Path(__file__).parent
    docs = [
        ("User Manual", base_dir / "docs" / "USER_MANUAL.md"),
        ("Web App Guide", base_dir / "WEB_APP_README.md"),
        ("What's New", base_dir / "WHATS_NEW.md"),
        ("Main README", base_dir / ".." / "README.md"),
    ]

    for name, path in docs:
        if path.exists():
            size_kb = path.stat().st_size / 1024
            print_success(f"{name}: {size_kb:.1f} KB")
        else:
            print_warning(f"{name}: Not found")

def create_launchers():
    """Create launcher scripts."""
    print_header("CREATING LAUNCHER SCRIPTS")

    base_dir = Path(__file__).parent

    # Desktop GUI launcher (Windows)
    if platform.system() == "Windows":
        gui_launcher = base_dir / "Launch_QMRA_GUI.bat"
        if not gui_launcher.exists():
            with open(gui_launcher, 'w') as f:
                f.write("""@echo off
echo ==========================================
echo   NIWA QMRA Toolkit - Desktop GUI
echo ==========================================
echo.
python launch_enhanced_gui.py
pause
""")
            print_success("Created: Launch_QMRA_GUI.bat")

    # Web app launcher (Windows)
    if platform.system() == "Windows":
        web_launcher = base_dir / "Launch_Web_App.bat"
        if web_launcher.exists():
            print_success("Found: Launch_Web_App.bat")
        else:
            print_info("Web launcher will be created separately")

    # Unix launchers
    if platform.system() in ["Linux", "Darwin"]:
        gui_launcher = base_dir / "launch_gui.sh"
        with open(gui_launcher, 'w') as f:
            f.write("""#!/bin/bash
echo "=========================================="
echo "  NIWA QMRA Toolkit - Desktop GUI"
echo "=========================================="
echo ""
python3 launch_enhanced_gui.py
""")
        gui_launcher.chmod(0o755)
        print_success("Created: launch_gui.sh")

        web_launcher = base_dir / "launch_web.sh"
        with open(web_launcher, 'w') as f:
            f.write("""#!/bin/bash
echo "=========================================="
echo "  NIWA QMRA Toolkit - Web Application"
echo "=========================================="
echo ""
streamlit run web_app.py
""")
        web_launcher.chmod(0o755)
        print_success("Created: launch_web.sh")

def print_next_steps():
    """Print next steps for user."""
    print_header("INSTALLATION COMPLETE!")

    print(f"\n{Colors.BOLD}🚀 Quick Start Guide:{Colors.ENDC}\n")

    print(f"{Colors.CYAN}1. Desktop GUI:{Colors.ENDC}")
    if platform.system() == "Windows":
        print(f"   Double-click: Launch_QMRA_GUI.bat")
    else:
        print(f"   Run: ./launch_gui.sh")
    print(f"   Or: python launch_enhanced_gui.py\n")

    print(f"{Colors.CYAN}2. Web Application:{Colors.ENDC}")
    if platform.system() == "Windows":
        print(f"   Double-click: Launch_Web_App.bat")
    else:
        print(f"   Run: ./launch_web.sh")
    print(f"   Or: streamlit run web_app.py\n")

    print(f"{Colors.CYAN}3. Documentation:{Colors.ENDC}")
    print(f"   User Manual: docs/USER_MANUAL.md")
    print(f"   Web Guide: WEB_APP_README.md")
    print(f"   In-App Help: Help menu (GUI) or Help page (Web)\n")

    print(f"{Colors.CYAN}4. Example Projects:{Colors.ENDC}")
    print(f"   Location: examples/projects/")
    print(f"   • Beach Swimming Assessment")
    print(f"   • Drinking Water Safety")
    print(f"   • Wastewater Treatment Comparison")
    print(f"   • Shellfish Harvesting Risk\n")

    print(f"{Colors.BOLD}📚 Learning Path:{Colors.ENDC}")
    print(f"   1. Read Quick Start in USER_MANUAL.md")
    print(f"   2. Load an example project")
    print(f"   3. Run the assessment")
    print(f"   4. Explore results and visualizations")
    print(f"   5. Modify parameters and experiment\n")

    print(f"{Colors.BOLD}💡 Tips:{Colors.ENDC}")
    print(f"   • Press F1 in GUI for instant help")
    print(f"   • Use 📊 button for typical concentration ranges")
    print(f"   • Start with beach swimming example (simplest)")
    print(f"   • Web app has interactive plots (zoom, pan, hover)\n")

    print(f"{Colors.BOLD}🆘 Support:{Colors.ENDC}")
    print(f"   • Help menu in applications")
    print(f"   • Troubleshooting guide in USER_MANUAL.md")
    print(f"   • Contact NIWA QMRA Team\n")

def main():
    """Main installation function."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║         NIWA QMRA ASSESSMENT TOOLKIT                         ║
    ║         Automated Installation & Setup                        ║
    ║         Version 2.0                                          ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    print(Colors.ENDC)

    print_info(f"Platform: {platform.system()} {platform.release()}")
    print_info(f"Python: {sys.executable}")
    print()

    # Run installation steps
    success = True

    if not check_python_version():
        sys.exit(1)

    if not install_core_dependencies():
        print_error("Core dependencies installation failed!")
        success = False

    if not install_gui_dependencies():
        print_warning("GUI dependencies incomplete - desktop GUI may not work")

    if not install_web_dependencies():
        print_warning("Web dependencies incomplete - web app may not work")

    install_optional_dependencies()

    create_directories()

    create_launchers()

    if not verify_installation():
        print_error("Verification failed - some components missing")
        success = False

    check_example_files()

    check_documentation()

    if success:
        print_next_steps()
    else:
        print_error("\nInstallation completed with errors")
        print_info("Some features may not be available")
        print_info("Check error messages above for details")

    print(f"\n{Colors.BOLD}Press Enter to exit...{Colors.ENDC}")
    input()

if __name__ == "__main__":
    main()
