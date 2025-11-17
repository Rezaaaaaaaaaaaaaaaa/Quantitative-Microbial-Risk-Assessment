@echo off
REM Automated Screenshot Capture for QMRA App
REM ==========================================
REM This script will:
REM 1. Start the Streamlit app
REM 2. Wait for it to load
REM 3. Capture screenshots
REM 4. Stop the app

echo ========================================
echo QMRA APP SCREENSHOT AUTOMATION
echo ========================================
echo.

REM Check if we're in the correct directory
if not exist "app\web_app.py" (
    echo ERROR: Must run from Batch_Processing_App directory!
    echo Current directory: %CD%
    echo.
    echo Please navigate to:
    echo   cd "Batch_Processing_App"
    echo.
    pause
    exit /b 1
)

echo [1/4] Starting Streamlit app...
echo.
cd app
start /B python -m streamlit run web_app.py --server.headless=true --server.port=8501 > nul 2>&1

echo [2/4] Waiting 15 seconds for app to fully load...
timeout /t 15 /nobreak > nul

echo.
echo [3/4] Capturing screenshots...
echo.
cd ..\scripts
python capture_app_screenshots.py

echo.
echo [4/4] Stopping Streamlit app...
taskkill /F /IM streamlit.exe > nul 2>&1
taskkill /F /FI "WINDOWTITLE eq streamlit*" > nul 2>&1

echo.
echo ========================================
echo SCREENSHOT CAPTURE COMPLETE!
echo ========================================
echo.
echo Screenshots saved to: screenshots\
echo.
echo You can now update the documentation with these new images.
echo.
pause
