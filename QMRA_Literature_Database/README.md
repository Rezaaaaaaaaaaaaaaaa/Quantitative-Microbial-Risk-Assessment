# QMRA Literature Database

This folder contains a comprehensive collection of Quantitative Microbial Risk Assessment (QMRA) research papers fetched from PubMed.

## Contents

### EndNote_Files/
- `qmra_comprehensive_2025.ris` - EndNote-compatible file for direct import into reference management software
- Contains 1000 recent peer-reviewed QMRA papers from the last 5 years

### Raw_Data/
- `qmra_comprehensive_2025.json` - Machine-readable JSON format containing all paper metadata
- Includes titles, authors, abstracts, DOIs, keywords, and publication details

### Reports/
- `qmra_comprehensive_2025_summary.txt` - Human-readable summary report
- Contains paper counts by year, organized list with direct PubMed links

## Usage

### For EndNote Users:
1. Open EndNote
2. Go to File > Import > File
3. Select `EndNote_Files/qmra_comprehensive_2025.ris`
4. Choose "Reference Manager (RIS)" as the import option

### Search Coverage:
- **Time Period**: Last 5 years (2020-2025)
- **Total Papers**: 1000
- **Database**: PubMed (peer-reviewed literature)
- **Search Terms**: Comprehensive QMRA terminology including:
  - "Quantitative Microbial Risk Assessment"
  - "QMRA"
  - "Quantitative Microbiological Risk Assessment"
  - MeSH terms for microbial risk assessment
  - Dose-response and exposure assessment terms

### Generated**: 2025-09-26

## Script Information
Generated using `fetch_qmra_papers.py` with the following parameters:
- Years back: 5
- Max results: 1000
- Email: moghaddamr@niwa.co.nz
- Output prefix: qmra_comprehensive_2025