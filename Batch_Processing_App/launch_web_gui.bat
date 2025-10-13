@echo off
REM QMRA Batch Processing Web Application Launcher
REM ===============================================

echo.
echo ========================================
echo QMRA Batch Processing Web Application
echo ========================================
echo.
echo Starting Streamlit web server...
echo.
echo The application will open in your browser.
echo Press Ctrl+C to stop the server.
echo.

cd /d "%~dp0"
streamlit run web_app.py

pause
