API Reference
=============

This section provides detailed documentation for all modules in the QMRA Toolkit.

Core Modules
------------

.. toctree::
   :maxdepth: 2

   pathogen_database
   dose_response
   exposure_assessment
   monte_carlo
   risk_characterization
   dilution_model
   report_generator

Utility Modules
---------------

.. toctree::
   :maxdepth: 2

   validation
   error_handling

Main Application
----------------

.. toctree::
   :maxdepth: 2

   qmra_toolkit

User Interfaces
---------------

.. toctree::
   :maxdepth: 2

   qmra_gui
   enhanced_qmra_gui

Module Overview
===============

Core Assessment Modules
~~~~~~~~~~~~~~~~~~~~~~~~

:mod:`pathogen_database`
    Manages pathogen-specific parameters including dose-response models, illness ratios, and environmental data.

:mod:`dose_response`
    Implements dose-response models (Beta-Poisson, exponential) for calculating infection probabilities.

:mod:`exposure_assessment`
    Provides exposure assessment capabilities for different pathways (primary contact, shellfish consumption, etc.).

:mod:`monte_carlo`
    Monte Carlo simulation engine for uncertainty analysis, replacing @Risk functionality.

:mod:`risk_characterization`
    Integrates dose-response and exposure assessment for comprehensive risk calculations.

:mod:`dilution_model`
    Models treatment barriers and dilution scenarios for wastewater treatment systems.

:mod:`report_generator`
    Generates automated reports in Word format for regulatory compliance.

Support Modules
~~~~~~~~~~~~~~~

:mod:`validation`
    Comprehensive validation functions for input parameters, configuration files, and data integrity.

:mod:`error_handling`
    Error handling utilities providing user-friendly error messages and debugging support.

Application Interfaces
~~~~~~~~~~~~~~~~~~~~~~~

:mod:`qmra_toolkit`
    Command-line interface for the QMRA toolkit with comprehensive CLI commands.

:mod:`qmra_gui`
    Basic graphical user interface for interactive assessments.

:mod:`enhanced_qmra_gui`
    Professional GUI with advanced features and NIWA branding.

Quick Reference
===============

Essential Classes
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Class
     - Module
     - Purpose
   * - PathogenDatabase
     - pathogen_database
     - Access pathogen parameters
   * - BetaPoissonModel
     - dose_response
     - Beta-Poisson dose-response
   * - ExponentialModel
     - dose_response
     - Exponential dose-response
   * - MonteCarloSimulator
     - monte_carlo
     - Uncertainty analysis
   * - RiskCharacterization
     - risk_characterization
     - Complete risk assessment
   * - ReportGenerator
     - report_generator
     - Generate compliance reports

Common Workflow
~~~~~~~~~~~~~~~

1. **Initialize components:**

   .. code-block:: python

      from pathogen_database import PathogenDatabase
      from risk_characterization import RiskCharacterization

      db = PathogenDatabase()
      risk_calc = RiskCharacterization(db)

2. **Set up exposure scenario:**

   .. code-block:: python

      from exposure_assessment import create_exposure_assessment, ExposureRoute

      exposure = create_exposure_assessment(
          ExposureRoute.PRIMARY_CONTACT,
          {"water_ingestion_volume": 50.0, "exposure_frequency": 12}
      )
      exposure.set_pathogen_concentration(100.0)

3. **Run assessment:**

   .. code-block:: python

      results = risk_calc.run_comprehensive_assessment(
          pathogen_name="norovirus",
          exposure_assessment=exposure,
          population_size=10000,
          n_samples=10000
      )

4. **Generate report:**

   .. code-block:: python

      from report_generator import ReportGenerator

      generator = ReportGenerator()
      report_path = generator.generate_assessment_report(
          pathogen="norovirus",
          results=results,
          parameters={"concentration": 100.0, "frequency": 12}
      )