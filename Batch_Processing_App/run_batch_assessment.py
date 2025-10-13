#!/usr/bin/env python3
"""
QMRA Batch Processing Application - Command Line Interface
==========================================================

Standalone application for running batch QMRA assessments.

Usage:
    python run_batch_assessment.py --help
    python run_batch_assessment.py spatial
    python run_batch_assessment.py temporal
    python run_batch_assessment.py treatment
    python run_batch_assessment.py multi-pathogen
    python run_batch_assessment.py batch

Author: NIWA Earth Sciences New Zealand
Date: October 2025
"""

import argparse
import sys
from pathlib import Path
from batch_processor import BatchProcessor


def spatial_assessment(args):
    """Run spatial risk assessment."""
    print("\n" + "="*80)
    print("SPATIAL RISK ASSESSMENT")
    print("="*80)

    processor = BatchProcessor(output_dir='outputs/results')

    results = processor.run_spatial_assessment(
        dilution_file=args.dilution_file,
        pathogen=args.pathogen,
        effluent_concentration=args.concentration,
        exposure_route=args.exposure_route,
        volume_ml=args.volume,
        frequency_per_year=args.frequency,
        population=args.population,
        treatment_lrv=args.treatment_lrv,
        iterations=args.iterations,
        output_file=args.output
    )

    print(f"\n[SUCCESS] Assessment complete! Results saved to outputs/results/{args.output}")
    return results


def temporal_assessment(args):
    """Run temporal risk assessment."""
    print("\n" + "="*80)
    print("TEMPORAL RISK ASSESSMENT")
    print("="*80)

    processor = BatchProcessor(output_dir='outputs/results')

    results = processor.run_temporal_assessment(
        monitoring_file=args.monitoring_file,
        pathogen=args.pathogen,
        concentration_column=args.concentration_column,
        exposure_route=args.exposure_route,
        treatment_lrv=args.treatment_lrv,
        dilution_factor=args.dilution,
        volume_ml=args.volume,
        frequency_per_year=args.frequency,
        population=args.population,
        iterations=args.iterations,
        output_file=args.output
    )

    print(f"\n[SUCCESS] Assessment complete! Results saved to outputs/results/{args.output}")
    return results


def treatment_comparison(args):
    """Run treatment scenario comparison."""
    print("\n" + "="*80)
    print("TREATMENT SCENARIO COMPARISON")
    print("="*80)

    processor = BatchProcessor(output_dir='outputs/results')

    # Get treatment files
    treatment_dir = Path('input_data/treatment_scenarios')
    if args.treatment_files:
        treatment_files = args.treatment_files
    else:
        # Use all YAML files in treatment scenarios directory
        treatment_files = list(treatment_dir.glob('*.yaml'))

    print(f"Found {len(treatment_files)} treatment scenarios")

    results = processor.run_treatment_comparison(
        treatment_files=treatment_files,
        pathogen=args.pathogen,
        raw_concentration=args.concentration,
        dilution_factor=args.dilution,
        exposure_route=args.exposure_route,
        volume_ml=args.volume,
        frequency_per_year=args.frequency,
        population=args.population,
        iterations=args.iterations,
        output_file=args.output
    )

    print(f"\n[SUCCESS] Comparison complete! Results saved to outputs/results/{args.output}")
    return results


def multi_pathogen_assessment(args):
    """Run multi-pathogen assessment."""
    print("\n" + "="*80)
    print("MULTI-PATHOGEN RISK ASSESSMENT")
    print("="*80)

    processor = BatchProcessor(output_dir='outputs/results')

    pathogens = args.pathogens.split(',')

    results = processor.run_multi_pathogen_assessment(
        concentration_file=args.concentration_file,
        pathogens=pathogens,
        exposure_route=args.exposure_route,
        treatment_lrv=args.treatment_lrv,
        dilution_factor=args.dilution,
        volume_ml=args.volume,
        frequency_per_year=args.frequency,
        population=args.population,
        iterations=args.iterations,
        output_file=args.output
    )

    print(f"\n[SUCCESS] Assessment complete! Results saved to outputs/results/{args.output}")
    return results


def batch_scenarios(args):
    """Run batch scenarios from master file."""
    print("\n" + "="*80)
    print("BATCH SCENARIO EXECUTION")
    print("="*80)

    processor = BatchProcessor(output_dir='outputs/results')

    results = processor.run_batch_scenarios(
        scenario_file=args.scenario_file,
        output_dir='outputs/results'
    )

    print(f"\n[SUCCESS] All scenarios complete!")
    print(f"Results saved to outputs/results/batch_scenarios_results.csv")
    return results


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description='QMRA Batch Processing Application',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Spatial assessment
  python run_batch_assessment.py spatial --dilution-file input_data/dilution_data/spatial_dilution_6_sites.csv

  # Temporal assessment
  python run_batch_assessment.py temporal --monitoring-file input_data/pathogen_concentrations/weekly_monitoring_2024.csv

  # Treatment comparison
  python run_batch_assessment.py treatment

  # Multi-pathogen assessment
  python run_batch_assessment.py multi-pathogen --pathogens norovirus,campylobacter,cryptosporidium

  # Batch scenarios
  python run_batch_assessment.py batch --scenario-file input_data/batch_scenarios/master_batch_scenarios.csv
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Assessment type')

    # Spatial assessment
    spatial_parser = subparsers.add_parser('spatial', help='Multi-site spatial assessment')
    spatial_parser.add_argument('--dilution-file', default='input_data/dilution_data/spatial_dilution_6_sites.csv',
                               help='CSV file with dilution data')
    spatial_parser.add_argument('--pathogen', default='norovirus', help='Pathogen name')
    spatial_parser.add_argument('--concentration', type=float, default=1e6, help='Effluent concentration')
    spatial_parser.add_argument('--exposure-route', default='primary_contact')
    spatial_parser.add_argument('--volume', type=float, default=50, help='Ingestion volume (mL)')
    spatial_parser.add_argument('--frequency', type=int, default=20, help='Events per year')
    spatial_parser.add_argument('--population', type=int, default=10000, help='Population size')
    spatial_parser.add_argument('--treatment-lrv', type=float, default=3.0, help='Treatment LRV')
    spatial_parser.add_argument('--iterations', type=int, default=10000, help='Monte Carlo iterations')
    spatial_parser.add_argument('--output', default='spatial_risk_results.csv', help='Output file')
    spatial_parser.set_defaults(func=spatial_assessment)

    # Temporal assessment
    temporal_parser = subparsers.add_parser('temporal', help='Temporal/seasonal assessment')
    temporal_parser.add_argument('--monitoring-file', default='input_data/pathogen_concentrations/weekly_monitoring_2024.csv',
                                help='CSV file with monitoring data')
    temporal_parser.add_argument('--pathogen', default='norovirus', help='Pathogen name')
    temporal_parser.add_argument('--concentration-column', default=None, help='Concentration column (auto-detected if None)')
    temporal_parser.add_argument('--exposure-route', default='primary_contact')
    temporal_parser.add_argument('--treatment-lrv', type=float, default=3.0, help='Treatment LRV')
    temporal_parser.add_argument('--dilution', type=float, default=100, help='Dilution factor')
    temporal_parser.add_argument('--volume', type=float, default=50, help='Ingestion volume (mL)')
    temporal_parser.add_argument('--frequency', type=int, default=20, help='Events per year')
    temporal_parser.add_argument('--population', type=int, default=10000, help='Population size')
    temporal_parser.add_argument('--iterations', type=int, default=10000, help='Monte Carlo iterations')
    temporal_parser.add_argument('--output', default='temporal_risk_results.csv', help='Output file')
    temporal_parser.set_defaults(func=temporal_assessment)

    # Treatment comparison
    treatment_parser = subparsers.add_parser('treatment', help='Treatment scenario comparison')
    treatment_parser.add_argument('--treatment-files', nargs='+', help='YAML treatment files (uses all if not specified)')
    treatment_parser.add_argument('--pathogen', default='norovirus', help='Pathogen name')
    treatment_parser.add_argument('--concentration', type=float, default=1e6, help='Raw concentration')
    treatment_parser.add_argument('--dilution', type=float, default=100, help='Dilution factor')
    treatment_parser.add_argument('--exposure-route', default='primary_contact')
    treatment_parser.add_argument('--volume', type=float, default=50, help='Ingestion volume (mL)')
    treatment_parser.add_argument('--frequency', type=int, default=20, help='Events per year')
    treatment_parser.add_argument('--population', type=int, default=10000, help='Population size')
    treatment_parser.add_argument('--iterations', type=int, default=10000, help='Monte Carlo iterations')
    treatment_parser.add_argument('--output', default='treatment_comparison_results.csv', help='Output file')
    treatment_parser.set_defaults(func=treatment_comparison)

    # Multi-pathogen assessment
    multipathogen_parser = subparsers.add_parser('multi-pathogen', help='Multi-pathogen assessment')
    multipathogen_parser.add_argument('--concentration-file', default='input_data/pathogen_concentrations/multi_pathogen_data.csv',
                                     help='CSV file with pathogen concentrations')
    multipathogen_parser.add_argument('--pathogens', default='norovirus,campylobacter,cryptosporidium',
                                     help='Comma-separated list of pathogens')
    multipathogen_parser.add_argument('--exposure-route', default='primary_contact')
    multipathogen_parser.add_argument('--treatment-lrv', type=float, default=3.0, help='Treatment LRV')
    multipathogen_parser.add_argument('--dilution', type=float, default=100, help='Dilution factor')
    multipathogen_parser.add_argument('--volume', type=float, default=50, help='Ingestion volume (mL)')
    multipathogen_parser.add_argument('--frequency', type=int, default=20, help='Events per year')
    multipathogen_parser.add_argument('--population', type=int, default=10000, help='Population size')
    multipathogen_parser.add_argument('--iterations', type=int, default=10000, help='Monte Carlo iterations')
    multipathogen_parser.add_argument('--output', default='multi_pathogen_results.csv', help='Output file')
    multipathogen_parser.set_defaults(func=multi_pathogen_assessment)

    # Batch scenarios
    batch_parser = subparsers.add_parser('batch', help='Run batch scenarios from master file')
    batch_parser.add_argument('--scenario-file', default='input_data/batch_scenarios/master_batch_scenarios.csv',
                             help='CSV file with scenario definitions')
    batch_parser.set_defaults(func=batch_scenarios)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        args.func(args)
        return 0
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
