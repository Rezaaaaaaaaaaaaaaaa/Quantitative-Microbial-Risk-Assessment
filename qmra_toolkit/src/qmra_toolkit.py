#!/usr/bin/env python3
"""
QMRA Assessment Toolkit - Main Application

Command-line interface for the Quantitative Microbial Risk Assessment toolkit.
This replaces @Risk Excel functionality with a comprehensive Python-based solution.
"""

import click
import yaml
import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional
import logging
import sys

# Import QMRA modules
from pathogen_database import PathogenDatabase
from dose_response import create_dose_response_model
from exposure_assessment import create_exposure_assessment, ExposureRoute
from dilution_model import DilutionModel, TreatmentBarrier, DilutionScenario, TreatmentType
from monte_carlo import MonteCarloSimulator, create_normal_distribution, create_lognormal_distribution
from risk_characterization import RiskCharacterization
from report_generator import ReportGenerator


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version='1.0.0')
@click.option('--config', '-c', type=click.Path(exists=True),
              help='Path to configuration file')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, config, verbose):
    """
    QMRA Assessment Toolkit - Quantitative Microbial Risk Assessment

    Developed by NIWA Earth Sciences New Zealand
    Replaces @Risk Excel functionality with Python-based automation.
    """
    ctx.ensure_object(dict)

    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Load configuration
    if config:
        with open(config, 'r') as f:
            ctx.obj['config'] = yaml.safe_load(f)
    else:
        # Load default config
        config_path = Path(__file__).parent.parent / 'config' / 'config.yaml'
        if config_path.exists():
            with open(config_path, 'r') as f:
                ctx.obj['config'] = yaml.safe_load(f)
        else:
            ctx.obj['config'] = {}

    logger.info("QMRA Assessment Toolkit initialized")


@cli.command()
@click.option('--pathogen', '-p', required=True,
              help='Pathogen name (e.g., norovirus, cryptosporidium)')
@click.option('--exposure-route', '-e', required=True,
              type=click.Choice(['primary_contact', 'shellfish_consumption', 'drinking_water', 'aerosol_inhalation']))
@click.option('--concentration', '-c', type=float, required=True,
              help='Pathogen concentration (organisms per unit volume/mass)')
@click.option('--volume', type=float,
              help='Exposure volume (mL for water, grams for food)')
@click.option('--frequency', type=float, default=1,
              help='Exposure frequency (events per year)')
@click.option('--population', type=int,
              help='Population size for population risk calculation')
@click.option('--iterations', '-n', type=int, default=10000,
              help='Number of Monte Carlo iterations')
@click.option('--output', '-o', type=click.Path(),
              help='Output file for results (JSON format)')
@click.option('--report', '-r', is_flag=True,
              help='Generate comprehensive report')
@click.pass_context
def assess(ctx, pathogen, exposure_route, concentration, volume, frequency,
           population, iterations, output, report):
    """
    Run complete QMRA assessment for specified pathogen and exposure scenario.
    """
    logger.info(f"Starting QMRA assessment for {pathogen}")

    try:
        # Initialize components
        pathogen_db = PathogenDatabase()
        risk_calc = RiskCharacterization(pathogen_db)

        # Validate pathogen
        if pathogen not in pathogen_db.get_available_pathogens():
            click.echo(f"Error: Pathogen '{pathogen}' not found in database")
            click.echo(f"Available pathogens: {', '.join(pathogen_db.get_available_pathogens())}")
            sys.exit(1)

        # Set up exposure assessment
        route = ExposureRoute(exposure_route)

        # Default parameters based on route
        if route == ExposureRoute.PRIMARY_CONTACT:
            params = {
                "water_ingestion_volume": volume or 50.0,
                "exposure_frequency": frequency
            }
        elif route == ExposureRoute.SHELLFISH_CONSUMPTION:
            params = {
                "shellfish_consumption": volume or 150.0,
                "consumption_frequency": frequency
            }
        elif route == ExposureRoute.DRINKING_WATER:
            params = {
                "daily_consumption_volume": volume or 2000.0  # mL per day
            }
        else:
            click.echo(f"Error: Exposure route {exposure_route} not fully implemented")
            sys.exit(1)

        exposure_model = create_exposure_assessment(route, params)
        exposure_model.set_pathogen_concentration(concentration)

        # Run comprehensive assessment
        results = risk_calc.run_comprehensive_assessment(
            pathogen_name=pathogen,
            exposure_assessment=exposure_model,
            population_size=population,
            n_samples=iterations
        )

        # Display results
        click.echo("\n" + "="*60)
        click.echo(f"QMRA Assessment Results: {pathogen.title()}")
        click.echo("="*60)

        for metric_name, result in results.items():
            click.echo(f"\n{metric_name.replace('_', ' ').title()}:")
            click.echo(f"  Mean: {result.statistics['mean']:.2e}")
            click.echo(f"  Median: {result.statistics['median']:.2e}")
            click.echo(f"  95th Percentile: {result.statistics['p95']:.2e}")

            if result.population_risks and population:
                expected_cases = result.population_risks['expected_cases_per_year']
                click.echo(f"  Expected cases per year: {expected_cases:.1f}")

        # Check regulatory compliance
        if 'annual_risk' in results:
            annual_result = results['annual_risk']
            compliance = risk_calc.evaluate_regulatory_compliance(annual_result)

            click.echo("\nRegulatory Compliance:")
            for threshold, compliant in compliance.items():
                status = "PASS" if compliant else "FAIL"
                click.echo(f"  {threshold}: {status}")

        # Save results if requested
        if output:
            save_results(results, output)
            click.echo(f"\nResults saved to: {output}")

        # Generate report if requested
        if report:
            report_path = generate_assessment_report(
                pathogen, results, params, concentration, frequency
            )
            click.echo(f"\nComprehensive report generated: {report_path}")

    except Exception as e:
        logger.error(f"Assessment failed: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--pathogen', '-p', required=True, help='Pathogen name')
@click.option('--dose', '-d', type=float, multiple=True, required=True,
              help='Dose values (can specify multiple)')
@click.option('--model', '-m', default='beta_poisson',
              type=click.Choice(['beta_poisson', 'exponential', 'hypergeometric']),
              help='Dose-response model type')
@click.option('--output', '-o', type=click.Path(), help='Output file for results')
def dose_response(pathogen, dose, model, output):
    """
    Calculate dose-response relationships for specified pathogen and doses.
    """
    logger.info(f"Calculating dose-response for {pathogen}")

    try:
        # Initialize database
        pathogen_db = PathogenDatabase()

        # Validate pathogen
        if pathogen not in pathogen_db.get_available_pathogens():
            click.echo(f"Error: Pathogen '{pathogen}' not found in database")
            sys.exit(1)

        # Get dose-response parameters
        dr_params = pathogen_db.get_dose_response_parameters(pathogen, model)
        dr_model = create_dose_response_model(model, dr_params)

        # Calculate probabilities
        doses = np.array(dose)
        probabilities = dr_model.calculate_infection_probability(doses)

        # Display results
        click.echo(f"\nDose-Response Results: {pathogen.title()} ({model})")
        click.echo("-" * 50)
        click.echo(f"{'Dose':<12} {'Probability':<12} {'Risk (1 in N)':<15}")
        click.echo("-" * 50)

        for d, p in zip(doses, probabilities):
            risk_ratio = 1 / p if p > 0 else float('inf')
            click.echo(f"{d:<12.1f} {p:<12.4e} {risk_ratio:<15.0f}")

        if output:
            results = {
                'pathogen': pathogen,
                'model': model,
                'parameters': dr_params,
                'doses': doses.tolist(),
                'probabilities': probabilities.tolist()
            }
            with open(output, 'w') as f:
                json.dump(results, f, indent=2)
            click.echo(f"\nResults saved to: {output}")

    except Exception as e:
        logger.error(f"Dose-response calculation failed: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--initial-concentration', '-c', type=float, required=True,
              help='Initial pathogen concentration (organisms/L)')
@click.option('--treatment-config', '-t', type=click.Path(exists=True),
              help='Treatment train configuration file (YAML)')
@click.option('--dilution-flow', type=float,
              help='Dilution flow rate (m³/s)')
@click.option('--receiving-flow', type=float,
              help='Receiving water flow rate (m³/s)')
@click.option('--output', '-o', type=click.Path(), help='Output file for results')
def treatment(initial_concentration, treatment_config, dilution_flow, receiving_flow, output):
    """
    Model treatment train and dilution effects on pathogen concentrations.
    """
    logger.info("Running treatment and dilution modeling")

    try:
        # Initialize dilution model
        dilution_model = DilutionModel()

        # Load treatment configuration if provided
        if treatment_config:
            with open(treatment_config, 'r') as f:
                config = yaml.safe_load(f)

            for barrier_config in config.get('treatment_barriers', []):
                barrier = TreatmentBarrier(
                    name=barrier_config['name'],
                    treatment_type=TreatmentType(barrier_config['type']),
                    log_reduction_value=barrier_config['lrv'],
                    variability=barrier_config.get('variability'),
                    description=barrier_config.get('description')
                )
                dilution_model.add_treatment_barrier(barrier)

        # Set dilution scenario if flows provided
        if dilution_flow and receiving_flow:
            scenario = DilutionScenario(
                initial_flow=dilution_flow,
                receiving_flow=receiving_flow
            )
            dilution_model.set_dilution_scenario(scenario)

        # Run complete scenario
        results = dilution_model.apply_complete_scenario(initial_concentration)

        # Display results
        click.echo(f"\nTreatment and Dilution Results")
        click.echo("-" * 40)
        click.echo(f"{'Stage':<20} {'Concentration':<15}")
        click.echo("-" * 40)

        for stage, concentration in results.items():
            click.echo(f"{stage.replace('_', ' ').title():<20} {concentration:.2e}")

        # Show treatment summary
        click.echo(f"\n{dilution_model.get_treatment_summary()}")

        if output:
            output_data = {
                'initial_concentration': initial_concentration,
                'results': {k: float(v) for k, v in results.items()},
                'treatment_summary': dilution_model.get_treatment_summary()
            }
            with open(output, 'w') as f:
                json.dump(output_data, f, indent=2)
            click.echo(f"Results saved to: {output}")

    except Exception as e:
        logger.error(f"Treatment modeling failed: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def list_pathogens():
    """List available pathogens in the database."""
    pathogen_db = PathogenDatabase()
    pathogens = pathogen_db.get_available_pathogens()

    click.echo("Available Pathogens:")
    click.echo("-" * 20)
    for pathogen in pathogens:
        pathogen_info = pathogen_db.get_pathogen_info(pathogen)
        pathogen_type = pathogen_info.get('pathogen_type', 'unknown')
        click.echo(f"• {pathogen.title()} ({pathogen_type})")


@cli.command()
@click.option('--pathogen', '-p', required=True, help='Pathogen name')
def pathogen_info(pathogen):
    """Display detailed information about a specific pathogen."""
    try:
        pathogen_db = PathogenDatabase()
        info = pathogen_db.get_pathogen_info(pathogen)

        click.echo(f"\nPathogen Information: {pathogen.title()}")
        click.echo("=" * 50)
        click.echo(f"Type: {info.get('pathogen_type', 'Unknown')}")
        click.echo(f"Illness-to-infection ratio: {info.get('illness_to_infection_ratio', 'N/A')}")
        click.echo(f"DALYs per case: {info.get('dalys_per_case', 'N/A')}")

        # Dose-response models
        click.echo("\nDose-Response Models:")
        for model_name, model_params in info.get('dose_response_models', {}).items():
            click.echo(f"  {model_name.title()}:")
            for param, value in model_params.items():
                if param not in ['source', 'notes']:
                    click.echo(f"    {param}: {value}")
            click.echo(f"    Source: {model_params.get('source', 'N/A')}")

        # Environmental data
        env_data = info.get('environmental_data', {})
        if env_data:
            click.echo("\nEnvironmental Data:")
            click.echo(f"  Survival time: {env_data.get('survival_time_days', 'N/A')} days")

            concentrations = env_data.get('typical_concentrations', {})
            if concentrations:
                click.echo("  Typical concentrations:")
                for matrix, conc in concentrations.items():
                    click.echo(f"    {matrix.replace('_', ' ')}: {conc:.0e}")

    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


def save_results(results: Dict, output_path: str) -> None:
    """Save risk assessment results to JSON file."""
    output_data = {}

    for metric_name, result in results.items():
        output_data[metric_name] = {
            'pathogen': result.pathogen_name,
            'risk_metric': result.risk_metric.value,
            'statistics': result.statistics,
            'population_risks': result.population_risks
        }

    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)


def generate_assessment_report(pathogen: str, results: Dict, params: Dict,
                             concentration: float, frequency: float) -> str:
    """Generate comprehensive assessment report."""
    report_gen = ReportGenerator()

    project_info = {
        'title': f'QMRA Assessment - {pathogen.title()}',
        'pathogen': pathogen,
        'assessment_date': pd.Timestamp.now().strftime('%Y-%m-%d'),
        'generated_by': 'QMRA Assessment Toolkit'
    }

    exposure_params = {
        'pathogen_concentration': f"{concentration:.2e}",
        'exposure_frequency': f"{frequency}/year",
        **params
    }

    filename = f"QMRA_Assessment_{pathogen}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.docx"

    return report_gen.create_regulatory_report(
        project_info=project_info,
        risk_results=results,
        exposure_params=exposure_params,
        output_filename=filename
    )


@cli.command()
def example():
    """Run example QMRA assessment to demonstrate toolkit functionality."""
    click.echo("Running example QMRA assessment...")
    click.echo("Scenario: Norovirus exposure from recreational swimming")

    try:
        # Initialize components
        pathogen_db = PathogenDatabase()
        risk_calc = RiskCharacterization(pathogen_db)

        # Set up primary contact exposure
        params = {
            "water_ingestion_volume": 50.0,  # mL per swimming event
            "exposure_frequency": 10  # events per year
        }

        exposure_model = create_exposure_assessment(
            ExposureRoute.PRIMARY_CONTACT,
            params
        )
        exposure_model.set_pathogen_concentration(10.0)  # organisms per 100mL

        # Run assessment
        results = risk_calc.run_comprehensive_assessment(
            pathogen_name="norovirus",
            exposure_assessment=exposure_model,
            population_size=10000,
            n_samples=5000
        )

        # Display results
        click.echo("\nExample Results:")
        click.echo("-" * 40)

        annual_risk = results['annual_risk']
        click.echo(f"Mean annual infection risk: {annual_risk.statistics['mean']:.2e}")
        click.echo(f"Expected cases per year (10,000 population): {annual_risk.population_risks['expected_cases_per_year']:.1f}")

        # Check compliance
        compliant = annual_risk.statistics['mean'] <= 1e-6
        status = "COMPLIANT" if compliant else "NON-COMPLIANT"
        click.echo(f"Regulatory compliance (1e-6 threshold): {status}")

        click.echo("\nExample completed successfully!")
        click.echo("Use 'qmra-toolkit assess --help' for full assessment options.")

    except Exception as e:
        click.echo(f"Example failed: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()