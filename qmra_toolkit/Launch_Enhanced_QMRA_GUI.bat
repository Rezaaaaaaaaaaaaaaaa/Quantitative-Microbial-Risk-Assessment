@echo off
title NIWA QMRA Toolkit - Professional Edition
color 0B

echo.
echo ================================================
echo   NIWA QMRA Assessment Toolkit
echo   Professional Edition with Enhanced GUI
echo ================================================
echo.
echo Starting enhanced professional interface...
echo.

python src/enhanced_qmra_gui.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to start the enhanced GUI
    echo.
    echo Possible solutions:
    echo 1. Install required packages: pip install matplotlib numpy
    echo 2. Check Python installation
    echo 3. Ensure all dependencies are available
    echo.
    pause
) else (
    echo.
    echo Enhanced QMRA GUI closed successfully.
)