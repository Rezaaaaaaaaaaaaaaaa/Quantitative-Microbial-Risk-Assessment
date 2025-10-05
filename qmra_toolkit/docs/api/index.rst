NIWA QMRA Toolkit Documentation
==================================

Welcome to the NIWA Quantitative Microbial Risk Assessment (QMRA) Toolkit documentation.

The QMRA Toolkit is a comprehensive Python-based solution for conducting quantitative microbial risk assessments, developed by NIWA Earth Sciences New Zealand. It replaces @Risk Excel functionality with automated, reproducible Python workflows for regulatory compliance QMRA assessments.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   overview
   installation
   quickstart
   api/modules
   examples
   contributing

Overview
========

The QMRA Toolkit provides:

* 🦠 **Comprehensive Pathogen Database** - Validated dose-response models for multiple pathogens
* 💧 **Multiple Exposure Routes** - Primary contact, shellfish consumption, drinking water, aerosol inhalation
* 🔬 **Dilution Modeling Integration** - NIWA's key differentiator with engineer-provided LRVs
* 📊 **Monte Carlo Simulation** - Advanced uncertainty analysis replacing @Risk
* 📋 **Automated Reporting** - Generate regulatory compliance reports in Word format
* ⚡ **Command-Line Interface** - Easy-to-use CLI for common workflows
* 🖥️ **Graphical User Interface** - Professional GUI for interactive assessments

Key Features
============

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Feature
     - @Risk Excel
     - QMRA Toolkit
   * - Platform
     - Excel-dependent
     - Native Python
   * - Security
     - Firewall conflicts
     - No external dependencies
   * - Automation
     - Manual processes
     - Fully automated
   * - Reproducibility
     - Limited
     - Complete version control
   * - Cost
     - Commercial license
     - Open source
   * - Integration
     - Limited
     - NIWA dilution modeling

Supported Pathogens
===================

The toolkit includes validated dose-response models for:

* **Norovirus** - Beta-Poisson and exponential models
* **Campylobacter jejuni** - Beta-Poisson model
* **Cryptosporidium parvum** - Exponential model

Additional pathogens can be easily added through the extensible pathogen database.

Quick Start
===========

1. **Install the toolkit:**

   .. code-block:: bash

      pip install niwa-qmra-toolkit

2. **Run a basic assessment:**

   .. code-block:: bash

      qmra assess --pathogen norovirus --exposure-route primary_contact \\
                  --concentration 10.0 --volume 50.0 --frequency 10 \\
                  --population 10000 --report

3. **Launch the GUI:**

   .. code-block:: bash

      qmra-enhanced-gui

API Reference
=============

.. toctree::
   :maxdepth: 2

   api/pathogen_database
   api/dose_response
   api/exposure_assessment
   api/monte_carlo
   api/risk_characterization
   api/dilution_model
   api/report_generator
   api/validation
   api/error_handling

Development Team
================

**NIWA Earth Sciences New Zealand**

* **Reza Moghaddam** - Lead Developer (150 hours)
* **David Wood** - Model Review & Support (40 hours)
* **Andrew Hughes** - Project Manager

Strategic Investment Programme 2025-2026

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`