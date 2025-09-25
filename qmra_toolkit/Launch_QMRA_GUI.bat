@echo off
REM Launch QMRA Toolkit GUI
echo Starting QMRA Assessment Toolkit GUI...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Launch the GUI
python launch_gui.py

REM Keep window open if there was an error
if %errorlevel% neq 0 (
    echo.
    echo GUI exited with error code %errorlevel%
    pause
)