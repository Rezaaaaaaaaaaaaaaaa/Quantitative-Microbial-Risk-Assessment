@echo off
REM Compile LaTeX Demo Document
REM Requires LaTeX distribution (e.g., MiKTeX, TeX Live)

echo.
echo ========================================
echo Compiling QMRA Demo Document
echo ========================================
echo.

REM Check if pdflatex is available
where pdflatex >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: pdflatex not found!
    echo Please install MiKTeX or TeX Live
    echo Download from: https://miktex.org/download
    pause
    exit /b 1
)

echo Compiling LaTeX document (Pass 1/3)...
pdflatex -interaction=nonstopmode QMRA_Batch_Demo.tex

echo.
echo Compiling LaTeX document (Pass 2/3 - Table of Contents)...
pdflatex -interaction=nonstopmode QMRA_Batch_Demo.tex

echo.
echo Compiling LaTeX document (Pass 3/3 - References)...
pdflatex -interaction=nonstopmode QMRA_Batch_Demo.tex

echo.
echo ========================================
echo Compilation Complete!
echo ========================================
echo.
echo Output: QMRA_Batch_Demo.pdf
echo.

REM Clean up auxiliary files
echo Cleaning up auxiliary files...
del QMRA_Batch_Demo.aux QMRA_Batch_Demo.log QMRA_Batch_Demo.out QMRA_Batch_Demo.toc 2>nul

echo.
echo Opening PDF...
start QMRA_Batch_Demo.pdf

pause
