# Report Generator Module

Report Generator Module for QMRA Toolkit

This module generates standardized reports for regulatory compliance,
replacing @Risk reporting functionality with automated Python-based reports.

## Classes

### ReportGenerator

Generate comprehensive QMRA reports for regulatory compliance.

## Functions

### generate_summary_table(risk_results: Dict[str, risk_characterization.RiskResult]) -> pandas.core.frame.DataFrame

Generate summary table from risk results.

Args:
    risk_results: Dictionary of risk results

Returns:
    DataFrame with summary statistics

