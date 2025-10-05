# NIWA QMRA Toolkit API Documentation

## Overview

The NIWA Quantitative Microbial Risk Assessment (QMRA) Toolkit is a comprehensive Python-based solution for conducting quantitative microbial risk assessments.

## Modules

- [pathogen_database](pathogen_database.md): Pathogen Database Module for QMRA Toolkit

This module provides access to pathogen-specific parameters including dose-response
relationships, illness ratios, and environmental data for quantitative microbial
risk assessment
- [dose_response](dose_response.md): Dose-Response Module for QMRA Toolkit

This module implements dose-response models for calculating infection probabilities
from pathogen exposure doses, including Beta-Poisson and exponential models
- [exposure_assessment](exposure_assessment.md): Exposure Assessment Module for QMRA Toolkit

This module provides exposure assessment capabilities for different pathways
including primary contact (recreational water) and shellfish consumption
- [monte_carlo](monte_carlo.md): Monte Carlo Simulation Engine for QMRA Toolkit

This module provides Monte Carlo simulation capabilities for uncertainty analysis
in quantitative microbial risk assessment, replacing @Risk functionality
- [risk_characterization](risk_characterization.md): Risk Characterization Module for QMRA Toolkit

This module integrates exposure assessment and dose-response models to calculate
health risks including infection probability, illness probability, and DALYs
- [dilution_model](dilution_model.md): Dilution Modelling Integration Module for QMRA Toolkit

This module provides dilution modelling capabilities and integration with
engineer-provided log reduction values (LRVs), which is NIWA's key differentiator
- [report_generator](report_generator.md): Report Generator Module for QMRA Toolkit

This module generates standardized reports for regulatory compliance,
replacing @Risk reporting functionality with automated Python-based reports
- [validation](validation.md): Validation utilities for QMRA Toolkit

This module provides comprehensive validation functions for input parameters,
configuration files, and data integrity checks
- [error_handling](error_handling.md): Error handling utilities for QMRA Toolkit

This module provides comprehensive error handling, logging, and user-friendly
error messages for the QMRA toolkit
- [qmra_toolkit](qmra_toolkit.md): QMRA Assessment Toolkit - Main Application

Command-line interface for the Quantitative Microbial Risk Assessment toolkit
