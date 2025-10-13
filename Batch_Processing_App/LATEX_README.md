# LaTeX Demonstration Document

## Overview

**File:** `QMRA_Batch_Demo.tex`

A comprehensive 60+ page technical demonstration document for the QMRA Batch Processing Application, written in LaTeX for professional publication-quality output.

## Document Contents

### Main Sections
1. **Executive Summary** - Key features, application scope, compliance standards
2. **System Architecture** - Components, data flow, technology stack
3. **Installation and Setup** - System requirements, installation steps
4. **Demonstration Scenarios** - 5 complete worked examples:
   - Batch Assessment (15 scenarios)
   - Spatial Assessment (multi-site dilution)
   - Temporal Assessment (seasonal variation)
   - Treatment Comparison (5 technologies)
   - Multi-Pathogen Assessment (6 pathogens)
5. **PDF Report Generation** - Automated reporting features
6. **Mathematical Background** - Dose-response models, risk calculations
7. **Advanced Usage** - Custom data, sensitivity analysis
8. **Troubleshooting** - Common issues and solutions
9. **References** - Scientific literature citations
10. **Appendices** - Parameters, file formats, command reference

### Features
- ✅ Professional formatting with custom styles
- ✅ Color-coded risk classifications
- ✅ Syntax-highlighted code examples
- ✅ Mathematical equations and formulas
- ✅ Tables with comprehensive data
- ✅ Hyperlinked table of contents
- ✅ Headers and footers with branding
- ✅ Publication-ready quality

## Compilation Instructions

### Option 1: Automated Compilation (Windows)

```bash
# Double-click the batch file
compile_latex_demo.bat
```

This will:
1. Check for LaTeX installation
2. Compile document 3 times (for TOC and references)
3. Clean up auxiliary files
4. Open the resulting PDF

### Option 2: Manual Compilation

#### Prerequisites
Install a LaTeX distribution:
- **Windows:** [MiKTeX](https://miktex.org/download) (recommended)
- **macOS:** [MacTeX](https://www.tug.org/mactex/)
- **Linux:** TeX Live (`sudo apt-get install texlive-full`)

#### Compile Commands

```bash
# Navigate to directory
cd Batch_Processing_App

# Compile (run 3 times for complete processing)
pdflatex QMRA_Batch_Demo.tex
pdflatex QMRA_Batch_Demo.tex
pdflatex QMRA_Batch_Demo.tex
```

**Why 3 times?**
- Pass 1: Generate document structure
- Pass 2: Process table of contents
- Pass 3: Resolve cross-references

### Option 3: Online LaTeX Compilation

Upload `QMRA_Batch_Demo.tex` to:
- [Overleaf](https://www.overleaf.com/) (free online LaTeX editor)
- [Papeeria](https://papeeria.com/)

## Required LaTeX Packages

The document uses these packages (auto-installed by MiKTeX):

```latex
inputenc, geometry, graphicx, float, amsmath, amssymb
booktabs, longtable, xcolor, listings, hyperref
fancyhdr, titlesec, caption, subcaption, array
multirow, enumitem
```

## Output

**File:** `QMRA_Batch_Demo.pdf`
**Size:** ~60-70 pages
**Format:** A4, 11pt font
**Quality:** Publication-ready

## Customization

### Change Organization Name

Find and replace:
```latex
NIWA Earth Sciences New Zealand
```

### Change Colors

Modify color definitions:
```latex
\definecolor{niwablue}{rgb}{0.12,0.47,0.71}  % Change RGB values
\definecolor{riskred}{rgb}{0.86,0.21,0.27}
\definecolor{compliantgreen}{rgb}{0.16,0.65,0.27}
```

### Add Your Logo

Replace placeholder image URL:
```latex
\includegraphics[width=0.8\textwidth]{your_logo.png}
```

### Modify Sections

The document is modular - easily add/remove sections by commenting out:
```latex
% \section{Your Custom Section}
```

## Troubleshooting

### "pdflatex: command not found"

**Solution:** Install LaTeX distribution (see Prerequisites above)

### Missing Package Errors

**Solution:** MiKTeX will prompt to install missing packages automatically. Click "Install" when prompted.

### Compilation Errors

**Common fixes:**
```bash
# Clear auxiliary files
del *.aux *.log *.out *.toc

# Recompile from scratch
pdflatex QMRA_Batch_Demo.tex
```

### Special Characters Not Displaying

Ensure UTF-8 encoding:
```latex
\usepackage[utf8]{inputenc}
```

## Converting to Other Formats

### Convert to Word

1. Compile to PDF first
2. Use Pandoc:
```bash
pandoc QMRA_Batch_Demo.tex -o QMRA_Batch_Demo.docx
```

### Convert to HTML

```bash
htlatex QMRA_Batch_Demo.tex
```

## Document Statistics

- **Total Pages:** ~60-70
- **Word Count:** ~15,000 words
- **Figures:** ASCII diagrams
- **Tables:** 20+ comprehensive tables
- **Code Listings:** 15+ Python and Bash examples
- **Equations:** 10+ mathematical formulas
- **References:** 8 scientific citations

## Version History

**Version 1.0 (October 2025)**
- Initial release
- Complete demonstration of all 5 assessment modes
- Mathematical background section
- Advanced usage examples
- Comprehensive appendices

## Notes

- The document references actual results from the batch processing application
- All code examples are functional and tested
- Risk values and statistics are from real demonstration runs
- Tables contain actual data from example scenarios

## Support

For LaTeX-specific issues:
- [LaTeX Stack Exchange](https://tex.stackexchange.com/)
- [Overleaf Documentation](https://www.overleaf.com/learn)
- MiKTeX Documentation

For application-specific content questions:
- See main `README.md` in Batch_Processing_App directory
- Review example data files in `input_data/` directory

---

**Last Updated:** October 2025
**LaTeX Version Required:** LaTeX2e
**Document Class:** article (11pt, A4)
