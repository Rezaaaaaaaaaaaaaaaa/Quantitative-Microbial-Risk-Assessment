@echo off
echo ========================================
echo   NIWA QMRA Toolkit - Web Application
echo ========================================
echo.
echo Starting web server...
echo Your browser will open automatically to http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

streamlit run web_app.py

pause
