#!/usr/bin/env python3
"""
QMRA Batch Processing Module
============================

Handles batch processing of QMRA assessments for:
- Multi-site spatial analysis
- Temporal/seasonal analysis
- Treatment scenario comparison
- Multi-pathogen assessment
- Master batch scenario execution

Author: NIWA Earth Sciences New Zealand
Date: October 2025
"""

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import yaml
import json
from datetime import datetime
import warnings

# Import QMRA core modules from local qmra_core package
try:
    from qmra_core import (
        PathogenDatabase,
        create_dose_response_model,
        MonteCarloSimulator,
        create_lognormal_distribution,
        create_uniform_distribution
    )
    QMRA_MODULES_AVAILABLE = True
except ImportError as e:
    warnings.warn(f"QMRA core modules not found ({e}). Using simplified calculations.")
    QMRA_MODULES_AVAILABLE = False


class BatchProcessor:
    """Main batch processing engine for QMRA assessments."""

    def __init__(self, output_dir='outputs/results'):
        """Initialize batch processor."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        if QMRA_MODULES_AVAILABLE:
            self.pathogen_db = PathogenDatabase()
        else:
            self.pathogen_db = None

        self.results_cache = []

    def run_spatial_assessment(self, dilution_file, pathogen, effluent_concentration,
                               exposure_route='primary_contact', volume_ml=50,
                               frequency_per_year=20, population=10000,
                               treatment_lrv=0, iterations=10000, output_file=None):
        """
        Run risk assessment at multiple spatial locations.

        Args:
            dilution_file: CSV file with Site_Name, Distance_m, Dilution_Factor columns
            pathogen: Pathogen name (e.g., 'norovirus')
            effluent_concentration: Pathogen concentration in effluent (copies/L)
            exposure_route: 'primary_contact' or 'shellfish_consumption'
            volume_ml: Ingestion volume per exposure (mL)
            frequency_per_year: Exposure events per year
            population: Exposed population size
            treatment_lrv: Log reduction from treatment
            iterations: Monte Carlo iterations
            output_file: Output CSV file path

        Returns:
            DataFrame with spatial risk results
        """
        print(f"\n{'='*80}")
        print("SPATIAL RISK ASSESSMENT")
        print(f"{'='*80}")
        print(f"Pathogen: {pathogen}")
        print(f"Effluent concentration: {effluent_concentration:,.0f} copies/L")
        print(f"Treatment LRV: {treatment_lrv}")

        # Load dilution data
        dilution_df = pd.read_csv(dilution_file)
        print(f"\nLoaded {len(dilution_df)} dilution data points")

        # Get unique sites
        sites = dilution_df.groupby('Site_Name').agg({
            'Distance_m': 'first',
            'Dilution_Factor': 'median'
        }).reset_index()

        print(f"Processing {len(sites)} sites...")

        results = []

        for idx, site in sites.iterrows():
            site_name = site['Site_Name']
            distance = site['Distance_m']
            dilution_factor = site['Dilution_Factor']

            # Apply treatment
            post_treatment_conc = effluent_concentration / (10 ** treatment_lrv)

            # Apply dilution
            receiving_water_conc = post_treatment_conc / dilution_factor

            # Run QMRA assessment
            result = self._run_single_assessment(
                pathogen=pathogen,
                concentration=receiving_water_conc,
                exposure_route=exposure_route,
                volume_ml=volume_ml,
                frequency_per_year=frequency_per_year,
                population=population,
                iterations=iterations
            )

            # Compile results
            results.append({
                'Site_Name': site_name,
                'Distance_m': distance,
                'Dilution_Factor': dilution_factor,
                'Effluent_Conc': effluent_concentration,
                'Post_Treatment_Conc': post_treatment_conc,
                'Receiving_Water_Conc': receiving_water_conc,
                'Infection_Risk_Median': result['pinf_median'],
                'Infection_Risk_5th': result['pinf_5th'],
                'Infection_Risk_95th': result['pinf_95th'],
                'Illness_Risk_Median': result['pill_median'],
                'Annual_Risk_Median': result['annual_risk_median'],
                'Annual_Risk_5th': result['annual_5th'],
                'Annual_Risk_95th': result['annual_95th'],
                'Population_Impact': result['population_impact'],
                'Compliance_Status': 'COMPLIANT' if result['annual_risk_median'] <= 1e-4 else 'NON-COMPLIANT'
            })

            print(f"  {site_name:20s} {distance:6.0f}m  Dilution: {dilution_factor:8.1f}x  Risk: {result['annual_risk_median']:.2e}  {results[-1]['Compliance_Status']}")

        results_df = pd.DataFrame(results)

        # Save results
        if output_file:
            output_path = self.output_dir / output_file
            results_df.to_csv(output_path, index=False)
            print(f"\nResults saved to: {output_path}")

        return results_df

    def run_temporal_assessment(self, monitoring_file, pathogen,
                                concentration_column=None,
                                exposure_route='primary_contact',
                                treatment_lrv=0, dilution_factor=100,
                                volume_ml=50, frequency_per_year=20,
                                population=10000, iterations=10000,
                                output_file=None):
        """
        Run risk assessment for time-series monitoring data.

        Args:
            monitoring_file: CSV file with temporal pathogen concentration data
            pathogen: Pathogen name
            concentration_column: Column name with concentrations (auto-detected if None)
            exposure_route: Exposure route
            treatment_lrv: Additional treatment LRV to apply
            dilution_factor: Dilution in receiving water
            volume_ml, frequency_per_year, population: Exposure parameters
            iterations: Monte Carlo iterations
            output_file: Output CSV file

        Returns:
            DataFrame with temporal risk results
        """
        print(f"\n{'='*80}")
        print("TEMPORAL RISK ASSESSMENT")
        print(f"{'='*80}")
        print(f"Pathogen: {pathogen}")

        # Load monitoring data
        monitoring_df = pd.read_csv(monitoring_file)
        print(f"Loaded {len(monitoring_df)} monitoring samples")

        # Auto-detect concentration column if not provided
        if concentration_column is None:
            possible_columns = [col for col in monitoring_df.columns if pathogen.lower() in col.lower()]
            if possible_columns:
                concentration_column = possible_columns[0]
                print(f"Using concentration column: {concentration_column}")
            else:
                raise ValueError(f"Could not find concentration column for {pathogen}")

        results = []

        for idx, row in monitoring_df.iterrows():
            sample_date = row.get('Sample_Date', row.get('Date', idx))
            raw_concentration = row[concentration_column]

            # Apply treatment
            post_treatment_conc = raw_concentration / (10 ** treatment_lrv)

            # Apply dilution
            receiving_water_conc = post_treatment_conc / dilution_factor

            # Run QMRA
            result = self._run_single_assessment(
                pathogen=pathogen,
                concentration=receiving_water_conc,
                exposure_route=exposure_route,
                volume_ml=volume_ml,
                frequency_per_year=frequency_per_year,
                population=population,
                iterations=iterations
            )

            results.append({
                'Sample_Date': sample_date,
                'Raw_Concentration': raw_concentration,
                'Post_Treatment_Conc': post_treatment_conc,
                'Receiving_Water_Conc': receiving_water_conc,
                'Infection_Risk_Median': result['pinf_median'],
                'Annual_Risk_Median': result['annual_risk_median'],
                'Annual_Risk_5th': result['annual_5th'],
                'Annual_Risk_95th': result['annual_95th'],
                'Population_Impact': result['population_impact'],
                'Compliance_Status': 'COMPLIANT' if result['annual_risk_median'] <= 1e-4 else 'NON-COMPLIANT'
            })

            if (idx + 1) % 10 == 0:
                print(f"  Processed {idx + 1}/{len(monitoring_df)} samples...")

        results_df = pd.DataFrame(results)

        # Save results
        if output_file:
            output_path = self.output_dir / output_file
            results_df.to_csv(output_path, index=False)
            print(f"\nResults saved to: {output_path}")

        return results_df

    def run_treatment_comparison(self, treatment_files, pathogen,
                                 raw_concentration, dilution_factor=100,
                                 exposure_route='primary_contact',
                                 volume_ml=50, frequency_per_year=20,
                                 population=10000, iterations=10000,
                                 output_file=None):
        """
        Compare multiple treatment scenarios.

        Args:
            treatment_files: List of YAML files with treatment configurations
            pathogen: Pathogen name
            raw_concentration: Raw effluent concentration
            dilution_factor: Dilution in receiving water
            exposure_route, volume_ml, frequency_per_year, population: Exposure parameters
            iterations: Monte Carlo iterations
            output_file: Output file path

        Returns:
            DataFrame with treatment comparison results
        """
        print(f"\n{'='*80}")
        print("TREATMENT SCENARIO COMPARISON")
        print(f"{'='*80}")
        print(f"Pathogen: {pathogen}")
        print(f"Raw concentration: {raw_concentration:,.0f} copies/L")

        results = []

        for treatment_file in treatment_files:
            # Load treatment configuration
            with open(treatment_file, 'r') as f:
                treatment_config = yaml.safe_load(f)

            scenario_name = treatment_config['scenario_name']
            total_lrv = treatment_config['total_log_reduction']

            print(f"\nProcessing: {scenario_name} (LRV: {total_lrv})")

            # Apply treatment
            post_treatment_conc = raw_concentration / (10 ** total_lrv)

            # Apply dilution
            receiving_water_conc = post_treatment_conc / dilution_factor

            # Run QMRA
            result = self._run_single_assessment(
                pathogen=pathogen,
                concentration=receiving_water_conc,
                exposure_route=exposure_route,
                volume_ml=volume_ml,
                frequency_per_year=frequency_per_year,
                population=population,
                iterations=iterations
            )

            results.append({
                'Treatment_Scenario': scenario_name,
                'Total_LRV': total_lrv,
                'Number_of_Barriers': len(treatment_config['treatment_barriers']),
                'Raw_Concentration': raw_concentration,
                'Post_Treatment_Conc': post_treatment_conc,
                'Receiving_Water_Conc': receiving_water_conc,
                'Infection_Risk_Median': result['pinf_median'],
                'Annual_Risk_Median': result['annual_risk_median'],
                'Annual_Risk_95th': result['annual_95th'],
                'Population_Impact': result['population_impact'],
                'Compliance_Status': 'COMPLIANT' if result['annual_risk_median'] <= 1e-4 else 'NON-COMPLIANT',
                'Risk_Reduction_vs_Raw': raw_concentration / receiving_water_conc
            })

            print(f"  Annual Risk: {result['annual_risk_median']:.2e}  {results[-1]['Compliance_Status']}")

        results_df = pd.DataFrame(results)

        # Save results
        if output_file:
            output_path = self.output_dir / output_file
            results_df.to_csv(output_path, index=False)
            print(f"\nResults saved to: {output_path}")

        return results_df

    def run_multi_pathogen_assessment(self, concentration_file, pathogens,
                                      exposure_route='primary_contact',
                                      treatment_lrv=0, dilution_factor=100,
                                      volume_ml=50, frequency_per_year=20,
                                      population=10000, iterations=10000,
                                      output_file=None):
        """
        Run assessment for multiple pathogens.

        Args:
            concentration_file: CSV with concentrations for multiple pathogens
            pathogens: List of pathogen names to assess
            exposure_route, treatment_lrv, dilution_factor: Assessment parameters
            volume_ml, frequency_per_year, population: Exposure parameters
            iterations: Monte Carlo iterations
            output_file: Output file path

        Returns:
            DataFrame with multi-pathogen comparison results
        """
        print(f"\n{'='*80}")
        print("MULTI-PATHOGEN RISK ASSESSMENT")
        print(f"{'='*80}")
        print(f"Pathogens: {', '.join(pathogens)}")

        # Load concentration data
        conc_df = pd.read_csv(concentration_file)
        print(f"Loaded {len(conc_df)} samples")

        results = []

        for pathogen in pathogens:
            # Find concentration column
            conc_columns = [col for col in conc_df.columns if pathogen.lower() in col.lower()]
            if not conc_columns:
                print(f"  WARNING: No concentration column found for {pathogen}, skipping")
                continue

            conc_column = conc_columns[0]
            mean_concentration = conc_df[conc_column].mean()

            print(f"\n{pathogen.title()}:")
            print(f"  Mean concentration: {mean_concentration:,.1f} copies/L")

            # Apply treatment and dilution
            post_treatment_conc = mean_concentration / (10 ** treatment_lrv)
            receiving_water_conc = post_treatment_conc / dilution_factor

            # Run QMRA
            result = self._run_single_assessment(
                pathogen=pathogen,
                concentration=receiving_water_conc,
                exposure_route=exposure_route,
                volume_ml=volume_ml,
                frequency_per_year=frequency_per_year,
                population=population,
                iterations=iterations
            )

            results.append({
                'Pathogen': pathogen,
                'Mean_Concentration': mean_concentration,
                'Post_Treatment_Conc': post_treatment_conc,
                'Receiving_Water_Conc': receiving_water_conc,
                'Infection_Risk_Median': result['pinf_median'],
                'Annual_Risk_Median': result['annual_risk_median'],
                'Annual_Risk_5th': result['annual_5th'],
                'Annual_Risk_95th': result['annual_95th'],
                'Population_Impact': result['population_impact'],
                'Compliance_Status': 'COMPLIANT' if result['annual_risk_median'] <= 1e-4 else 'NON-COMPLIANT'
            })

            print(f"  Annual Risk: {result['annual_risk_median']:.2e}  {results[-1]['Compliance_Status']}")

        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values('Annual_Risk_Median', ascending=False)

        # Save results
        if output_file:
            output_path = self.output_dir / output_file
            results_df.to_csv(output_path, index=False)
            print(f"\nResults saved to: {output_path}")

        print(f"\nPathogen Risk Ranking:")
        for idx, row in results_df.iterrows():
            print(f"  {idx+1}. {row['Pathogen']:20s} {row['Annual_Risk_Median']:.2e}")

        return results_df

    def run_batch_scenarios(self, scenario_file, output_dir=None):
        """
        Run batch scenarios from master CSV file.

        Args:
            scenario_file: CSV file with complete scenario definitions
            output_dir: Directory for output files

        Returns:
            DataFrame with all scenario results
        """
        print(f"\n{'='*80}")
        print("BATCH SCENARIO EXECUTION")
        print(f"{'='*80}")

        # Load scenarios
        scenarios_df = pd.read_csv(scenario_file)
        print(f"Loaded {len(scenarios_df)} scenarios")

        if output_dir:
            output_path = Path(output_dir)
        else:
            output_path = self.output_dir
        output_path.mkdir(parents=True, exist_ok=True)

        results = []

        for idx, scenario in scenarios_df.iterrows():
            scenario_id = scenario['Scenario_ID']
            scenario_name = scenario['Scenario_Name']

            print(f"\n[{idx+1}/{len(scenarios_df)}] Processing: {scenario_id} - {scenario_name}")

            # Apply treatment and dilution
            # Note: Treatment and dilution uncertainty handled in concentration uncertainty
            post_treatment_conc = scenario['Effluent_Conc'] / (10 ** scenario['Treatment_LRV'])
            receiving_water_conc = post_treatment_conc / scenario['Dilution_Factor']

            # Read distribution parameters (with backwards compatibility)
            effluent_conc_cv = scenario.get('Effluent_Conc_CV', 0.5)
            treatment_lrv_uncertainty = scenario.get('Treatment_LRV_Uncertainty', 0.2)
            dilution_factor_cv = scenario.get('Dilution_Factor_CV', 0.3)
            volume_min = scenario.get('Volume_Min', None)
            volume_max = scenario.get('Volume_Max', None)

            # Combine uncertainties: effluent + treatment + dilution
            # Using uncertainty propagation: CV_total = sqrt(CV1^2 + CV2^2 + CV3^2)
            total_concentration_cv = np.sqrt(
                effluent_conc_cv**2 +
                (treatment_lrv_uncertainty * np.log(10))**2 +  # Convert LRV uncertainty to relative
                dilution_factor_cv**2
            )

            # Run QMRA with custom distributions
            result = self._run_single_assessment(
                pathogen=scenario['Pathogen'],
                concentration=receiving_water_conc,
                exposure_route=scenario['Exposure_Route'],
                volume_ml=scenario['Volume_mL'],
                frequency_per_year=scenario['Frequency_Year'],
                population=scenario['Population'],
                iterations=scenario.get('Monte_Carlo_Iterations', 10000),
                concentration_cv=total_concentration_cv,
                volume_min=volume_min,
                volume_max=volume_max,
                dilution_cv=dilution_factor_cv,
                treatment_uncertainty=treatment_lrv_uncertainty
            )

            results.append({
                'Scenario_ID': scenario_id,
                'Scenario_Name': scenario_name,
                'Pathogen': scenario['Pathogen'],
                'Exposure_Route': scenario['Exposure_Route'],
                'Effluent_Conc': scenario['Effluent_Conc'],
                'Treatment_LRV': scenario['Treatment_LRV'],
                'Dilution_Factor': scenario['Dilution_Factor'],
                'Receiving_Water_Conc': receiving_water_conc,
                'Volume_mL': scenario['Volume_mL'],
                'Frequency_Year': scenario['Frequency_Year'],
                'Population': scenario['Population'],
                'Infection_Risk_Median': result['pinf_median'],
                'Annual_Risk_Median': result['annual_risk_median'],
                'Annual_Risk_5th': result['annual_5th'],
                'Annual_Risk_95th': result['annual_95th'],
                'Population_Impact': result['population_impact'],
                'Compliance_Status': 'COMPLIANT' if result['annual_risk_median'] <= 1e-4 else 'NON-COMPLIANT',
                'Priority': scenario.get('Priority', 'Medium')
            })

            print(f"  Risk: {result['annual_risk_median']:.2e}  {results[-1]['Compliance_Status']}")

        results_df = pd.DataFrame(results)

        # Save combined results
        output_file = output_path / 'batch_scenarios_results.csv'
        results_df.to_csv(output_file, index=False)
        print(f"\n{'='*80}")
        print(f"All results saved to: {output_file}")
        print(f"{'='*80}")

        # Summary statistics
        total_scenarios = len(results_df)
        compliant = len(results_df[results_df['Compliance_Status'] == 'COMPLIANT'])
        high_priority_non_compliant = len(results_df[
            (results_df['Priority'] == 'High') &
            (results_df['Compliance_Status'] == 'NON-COMPLIANT')
        ])

        print(f"\nBatch Summary:")
        print(f"  Total scenarios: {total_scenarios}")
        print(f"  Compliant: {compliant} ({100*compliant/total_scenarios:.1f}%)")
        print(f"  Non-compliant: {total_scenarios - compliant} ({100*(total_scenarios-compliant)/total_scenarios:.1f}%)")
        print(f"  High priority non-compliant: {high_priority_non_compliant}")

        return results_df

    def _run_single_assessment(self, pathogen, concentration, exposure_route,
                               volume_ml, frequency_per_year, population,
                               iterations=10000, concentration_cv=0.5,
                               volume_min=None, volume_max=None,
                               dilution_cv=0.3, treatment_uncertainty=0.2):
        """
        Run a single QMRA assessment.

        Internal method used by all batch processors.

        Args:
            pathogen: Pathogen name
            concentration: Mean concentration in receiving water
            exposure_route: Exposure route
            volume_ml: Mean ingestion volume
            frequency_per_year: Exposure frequency
            population: Exposed population
            iterations: Monte Carlo iterations
            concentration_cv: Coefficient of variation for concentration (default 0.5)
            volume_min: Minimum volume (default: volume_ml * 0.5)
            volume_max: Maximum volume (default: volume_ml * 1.5)
            dilution_cv: Coefficient of variation for dilution (default 0.3)
            treatment_uncertainty: Uncertainty in treatment LRV (default 0.2)
        """
        if QMRA_MODULES_AVAILABLE:
            return self._run_full_qmra(pathogen, concentration, exposure_route,
                                      volume_ml, frequency_per_year, population, iterations,
                                      concentration_cv, volume_min, volume_max,
                                      dilution_cv, treatment_uncertainty)
        else:
            return self._run_simplified_qmra(pathogen, concentration, exposure_route,
                                            volume_ml, frequency_per_year, population, iterations,
                                            concentration_cv, volume_min, volume_max)

    def _run_full_qmra(self, pathogen, concentration, exposure_route,
                       volume_ml, frequency_per_year, population, iterations,
                       concentration_cv=0.5, volume_min=None, volume_max=None,
                       dilution_cv=0.3, treatment_uncertainty=0.2):
        """
        Run full QMRA with proper modules using custom distributions.

        Args:
            concentration_cv: Coefficient of variation for concentration
            volume_min: Minimum ingestion volume
            volume_max: Maximum ingestion volume
            dilution_cv: Not used directly here (applied upstream)
            treatment_uncertainty: Not used directly here (applied upstream)
        """
        # Get pathogen parameters
        pathogen_info = self.pathogen_db.get_pathogen_info(pathogen)
        default_model_type = self.pathogen_db.get_default_model_type(pathogen)
        dr_params = self.pathogen_db.get_dose_response_parameters(pathogen, default_model_type)
        health_data = self.pathogen_db.get_health_impact_data(pathogen)

        # Create dose-response model
        dr_model = create_dose_response_model(default_model_type, dr_params)

        # Monte Carlo simulation
        mc_simulator = MonteCarloSimulator(random_seed=42)

        # Add concentration distribution with custom CV
        # CV relates to std for lognormal: std = sqrt(log(1 + CV^2))
        log_std = np.sqrt(np.log(1 + concentration_cv**2))
        conc_dist = create_lognormal_distribution(
            mean=np.log(max(concentration, 1e-10)),
            std=log_std,
            name="concentration"
        )
        mc_simulator.add_distribution("concentration", conc_dist)

        # Add volume distribution with custom min/max
        if volume_min is None:
            volume_min = volume_ml * 0.5
        if volume_max is None:
            volume_max = volume_ml * 1.5

        vol_dist = create_uniform_distribution(
            min_val=volume_min,
            max_val=volume_max,
            name="volume"
        )
        mc_simulator.add_distribution("volume", vol_dist)

        # QMRA model
        def qmra_model(samples):
            conc = samples["concentration"]
            vol = samples["volume"]
            dose = (conc * vol) / 1000.0
            return dr_model.calculate_infection_probability(dose)

        # Run simulation
        infection_results = mc_simulator.run_simulation(
            qmra_model,
            n_iterations=iterations,
            variable_name="infection_probability"
        )

        # Calculate risks
        pinf_samples = infection_results.samples
        pill_inf_ratio = health_data["illness_to_infection_ratio"]
        pill_samples = pinf_samples * pill_inf_ratio
        annual_samples = 1 - np.power(1 - pinf_samples, frequency_per_year)

        return {
            'pinf_median': float(np.median(pinf_samples)),
            'pinf_mean': float(np.mean(pinf_samples)),
            'pinf_5th': float(np.percentile(pinf_samples, 5)),
            'pinf_95th': float(np.percentile(pinf_samples, 95)),
            'pill_median': float(np.median(pill_samples)),
            'annual_risk_median': float(np.median(annual_samples)),
            'annual_mean': float(np.mean(annual_samples)),
            'annual_5th': float(np.percentile(annual_samples, 5)),
            'annual_95th': float(np.percentile(annual_samples, 95)),
            'population_impact': int(population * np.median(annual_samples))
        }

    def _run_simplified_qmra(self, pathogen, concentration, exposure_route,
                            volume_ml, frequency_per_year, population, iterations,
                            concentration_cv=0.5, volume_min=None, volume_max=None):
        """
        Run simplified QMRA when modules unavailable.

        Args:
            concentration_cv: Coefficient of variation for concentration
            volume_min: Minimum ingestion volume
            volume_max: Maximum ingestion volume
        """
        # Simplified dose-response parameters
        dr_params = {
            'norovirus': {'alpha': 0.04, 'model': 'exponential', 'pill_inf': 0.7},
            'campylobacter': {'alpha': 0.145, 'beta': 7.59, 'model': 'beta_poisson', 'pill_inf': 0.33},
            'cryptosporidium': {'r': 0.0042, 'model': 'exponential', 'pill_inf': 0.39},
            'e_coli': {'alpha': 0.49, 'beta': 5.99e4, 'model': 'beta_poisson', 'pill_inf': 0.5},
            'salmonella': {'alpha': 0.33, 'beta': 2.49e3, 'model': 'beta_poisson', 'pill_inf': 0.5},
            'rotavirus': {'alpha': 0.26, 'beta': 0.42, 'model': 'beta_poisson', 'pill_inf': 0.5}
        }

        params = dr_params.get(pathogen, {'alpha': 0.1, 'model': 'exponential', 'pill_inf': 0.5})

        # Set volume range
        if volume_min is None:
            volume_min = volume_ml * 0.5
        if volume_max is None:
            volume_max = volume_ml * 1.5

        # Simple Monte Carlo with custom distributions
        np.random.seed(42)

        # Sample concentrations with custom CV
        log_std = np.sqrt(np.log(1 + concentration_cv**2))
        conc_samples = np.random.lognormal(np.log(max(concentration, 1e-10)), log_std, iterations)

        # Sample volumes uniformly
        vol_samples = np.random.uniform(volume_min, volume_max, iterations)

        # Calculate doses
        dose_samples = (conc_samples * vol_samples) / 1000.0

        # Dose-response
        if params['model'] == 'exponential':
            pinf_samples = 1 - np.exp(-params['alpha'] * dose_samples)
        else:  # beta_poisson
            pinf_samples = 1 - np.power(1 + dose_samples / params['beta'], -params['alpha'])

        pill_samples = pinf_samples * params['pill_inf']
        annual_samples = 1 - (1 - pinf_samples) ** frequency_per_year

        return {
            'pinf_median': float(np.median(pinf_samples)),
            'pinf_mean': float(np.mean(pinf_samples)),
            'pinf_5th': float(np.percentile(pinf_samples, 5)),
            'pinf_95th': float(np.percentile(pinf_samples, 95)),
            'pill_median': float(np.median(pill_samples)),
            'annual_risk_median': float(np.median(annual_samples)),
            'annual_mean': float(np.mean(annual_samples)),
            'annual_5th': float(np.percentile(annual_samples, 5)),
            'annual_95th': float(np.percentile(annual_samples, 95)),
            'population_impact': int(population * np.median(annual_samples))
        }


if __name__ == '__main__':
    print("QMRA Batch Processor Module")
    print("Use run_batch_assessment.py for command-line interface")
