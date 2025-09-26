#!/usr/bin/env python3
"""
Enhanced QMRA Toolkit GUI Launcher
Launch the professional QMRA Assessment Toolkit with enhanced graphical interface
"""

import sys
import os
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def check_dependencies():
    """Check if required dependencies are available."""
    missing = []

    try:
        import tkinter
    except ImportError:
        missing.append("tkinter")

    try:
        import matplotlib
    except ImportError:
        missing.append("matplotlib")

    try:
        import numpy
    except ImportError:
        missing.append("numpy")

    return missing

def main():
    """Main launcher function."""
    print("=" * 60)
    print("   NIWA QMRA Assessment Toolkit - Professional Edition")
    print("=" * 60)
    print()

    # Check dependencies
    missing_deps = check_dependencies()
    if missing_deps:
        print("[ERROR] Missing required dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print()
        print("To install missing dependencies:")
        print("   pip install matplotlib numpy")
        print()
        input("Press Enter to exit...")
        return

    print("[OK] All dependencies available")
    print("[STARTING] Enhanced QMRA GUI...")
    print()

    try:
        from enhanced_qmra_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"[ERROR] Error importing Enhanced GUI: {e}")
        print()
        print("Falling back to basic GUI...")
        try:
            from qmra_gui import main as basic_gui_main
            basic_gui_main()
        except ImportError:
            print("[ERROR] Basic GUI also unavailable")
            print("Please check QMRA toolkit installation")
    except Exception as e:
        print(f"[ERROR] Error starting Enhanced GUI: {e}")
        print()
        print("Please check the error log and try again")

if __name__ == "__main__":
    main()