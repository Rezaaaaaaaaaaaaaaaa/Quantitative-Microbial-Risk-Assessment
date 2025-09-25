#!/usr/bin/env python3
"""
QMRA Toolkit GUI Launcher
Launch the QMRA Assessment Toolkit with a graphical user interface
"""

import sys
import os
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from qmra_gui import main
    print("Starting QMRA Assessment Toolkit GUI...")
    main()
except ImportError as e:
    print(f"Error importing GUI modules: {e}")
    print("Please ensure all dependencies are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Error starting GUI: {e}")
    sys.exit(1)