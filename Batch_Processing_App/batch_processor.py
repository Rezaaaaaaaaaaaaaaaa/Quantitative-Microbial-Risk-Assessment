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
        create_uniform_distribution,
        create_empirical_cdf_from_data,
        create_hockey_stick_distribution,
        calculate_empirical_cdf
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

    def run_spatial_assessment(self, dilution_file, pathogen, effluent_concentration=None,
                               exposure_route='primary_contact', volume_ml=50,
                               frequency_per_year=20, population=10000,
                               treatment_lrv=0, iterations=10000, output_file=None,
                               use_ecdf_dilution=True, use_hockey_pathogen=False,
                               pathogen_min=None, pathogen_median=None, pathogen_max=None):
        """
        Run risk assessment at multiple spatial locations with empirical distributions.

        Args:
            dilution_file: CSV file with Site_Name, Distance_m, Dilution_Factor columns
            pathogen: Pathogen name (e.g., 'norovirus')
            effluent_concentration: Fixed pathogen concentration (copies/L) - ignored if use_hockey_pathogen=True
            exposure_route: 'primary_contact' or 'shellfish_consumption'
            volume_ml: Ingestion volume per exposure (mL)
            frequency_per_year: Exposure events per year
            population: Exposed population size
            treatment_lrv: Log reduction from treatment
            iterations: Monte Carlo iterations
            output_file: Output CSV file path
            use_ecdf_dilution: Use full ECDF of dilution data (True) or median only (False)
            use_hockey_pathogen: Use Hockey Stick distribution for pathogen concentration
            pathogen_min: Minimum pathogen concentration (required if use_hockey_pathogen=True)
            pathogen_median: Median pathogen concentration (required if use_hockey_pathogen=True)
            pathogen_max: Maximum pathogen concentration (required if use_hockey_pathogen=True)

        Returns:
            DataFrame with spatial risk results
        """
        print(f"\n{'='*80}")
        print("SPATIAL RISK ASSESSMENT")
        print(f"{'='*80}")
        print(f"Pathogen: {pathogen}")

        # Validate Hockey Stick parameters if needed
        if use_hockey_pathogen:
            if None in [pathogen_min, pathogen_median, pathogen_max]:
                raise ValueError("When use_hockey_pathogen=True, must provide pathogen_min, pathogen_median, pathogen_max")
            print(f"Pathogen concentration: Hockey Stick (min={pathogen_min:.0e}, median={pathogen_median:.0e}, max={pathogen_max:.0e})")
        else:
            if effluent_concentration is None:
                raise ValueError("Must provide effluent_concentration when use_hockey_pathogen=False")
            print(f"Effluent concentration: {effluent_concentration:,.0f} copies/L")

        print(f"Treatment LRV: {treatment_lrv}")
        print(f"Using ECDF for dilution: {use_ecdf_dilution}")

        # Load dilution data
        dilution_df = pd.read_csv(dilution_file)
        print(f"\nLoaded {len(dilution_df)} dilution data points")

        # Get unique sites
        site_names = dilution_df['Site_Name'].unique()
        print(f"Processing {len(site_names)} sites...")

        results = []

        for site_name in site_names:
            # Get all dilution data for this site
            site_data = dilution_df[dilution_df['Site_Name'] == site_name]
            distance = site_data['Distance_m'].iloc[0]
            dilution_values = site_data['Dilution_Factor'].values

            if use_ecdf_dilution:
                print(f"\n  {site_name}: Using ECDF with {len(dilution_values)} simulations")
            else:
                dilution_median = np.median(dilution_values)
                print(f"\n  {site_name}: Using median dilution: {dilution_median:.2f}x")

            # Run QMRA assessment with distributions
            result = self._run_spatial_assessment_with_distributions(
                pathogen=pathogen,
                dilution_values=dilution_values,
                use_ecdf_dilution=use_ecdf_dilution,
                effluent_concentration=effluent_concentration,
                use_hockey_pathogen=use_hockey_pathogen,
                pathogen_min=pathogen_min,
                pathogen_median=pathogen_median,
                pathogen_max=pathogen_max,
                treatment_lrv=treatment_lrv,
                exposure_route=exposure_route,
                volume_ml=volume_ml,
                frequency_per_year=frequency_per_year,
                population=population,
                iterations=iterations
            )

            # Compile results
            dilution_summary = f"{len(dilution_values)} ECDF" if use_ecdf_dilution else f"{np.median(dilution_values):.2f}x"
            results.append({
                'Site_Name': site_name,
                'Distance_m': distance,
                'Dilution_Factor_Median': np.median(dilution_values),
                'Dilution_Factor_Min': np.min(dilution_values),
                'Dilution_Factor_Max': np.max(dilution_values),
                'Dilution_Method': 'ECDF' if use_ecdf_dilution else 'Median',
                'Pathogen_Method': 'Hockey_Stick' if use_hockey_pathogen else 'Fixed',
                'Effluent_Conc_Input': pathogen_median if use_hockey_pathogen else effluent_concentration,
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

            print(f"    Risk: {result['annual_risk_median']:.2e} (5th: {result['annual_5th']:.2e}, 95th: {result['annual_95th']:.2e}) {results[-1]['Compliance_Status']}")

        results_df = pd.DataFrame(results)

        # Save results
        if output_file:
            output_path = self.output_dir / output_file
            results_df.to_csv(output_path, index=False)
            print(f"\nResults saved to: {output_path}")

        return results_df

    def _run_spatial_assessment_with_distributions(self, pathogen, dilution_values,
                                                    use_ecdf_dilution, effluent_concentration,
                                                    use_hockey_pathogen, pathogen_min, pathogen_median,
                                                    pathogen_max, treatment_lrv, exposure_route,
                                                    volume_ml, frequency_per_year, population, iterations):
        """
        Internal method to run spatial assessment with empirical distributions.

        Uses ECDF for dilution and/or Hockey Stick for pathogen concentration.
        """
        if not QMRA_MODULES_AVAILABLE:
            raise RuntimeError("QMRA modules required for distribution-based assessments")

        # Get pathogen parameters
        pathogen_info = self.pathogen_db.get_pathogen_info(pathogen)
        default_model_type = self.pathogen_db.get_default_model_type(pathogen)
        dr_params = self.pathogen_db.get_dose_response_parameters(pathogen, default_model_type)
        health_data = self.pathogen_db.get_health_impact_data(pathogen)

        # Create dose-response model
        dr_model = create_dose_response_model(default_model_type, dr_params)

        # Setup Monte Carlo simulator
        mc_simulator = MonteCarloSimulator(random_seed=42)

        # Add pathogen concentration distribution
        if use_hockey_pathogen:
            pathogen_dist = create_hockey_stick_distribution(
                x_min=pathogen_min,
                x_median=pathogen_median,
                x_max=pathogen_max,
                name="pathogen_concentration"
            )
            mc_simulator.add_distribution("pathogen_concentration", pathogen_dist)
        else:
            # Use lognormal with moderate uncertainty for fixed concentration
            log_std = np.sqrt(np.log(1 + 0.5**2))  # CV = 0.5
            conc_dist = create_lognormal_distribution(
                mean=np.log(max(effluent_concentration, 1e-10)),
                std=log_std,
                name="pathogen_concentration"
            )
            mc_simulator.add_distribution("pathogen_concentration", conc_dist)

        # Add dilution distribution
        if use_ecdf_dilution:
            dilution_dist = create_empirical_cdf_from_data(
                dilution_values,
                name="dilution_factor"
            )
            mc_simulator.add_distribution("dilution_factor", dilution_dist)
        else:
            # Use single median value as fixed
            median_dilution = np.median(dilution_values)
            # Create narrow distribution around median
            dilution_dist = create_lognormal_distribution(
                mean=np.log(median_dilution),
                std=0.01,  # Very narrow
                name="dilution_factor"
            )
            mc_simulator.add_distribution("dilution_factor", dilution_dist)

        # Add ingestion volume distribution
        volume_dist = create_uniform_distribution(
            min_val=volume_ml * 0.7,
            max_val=volume_ml * 1.3,
            name="ingestion_volume"
        )
        mc_simulator.add_distribution("ingestion_volume", volume_dist)

        # Define QMRA model
        def qmra_model(samples):
            """Calculate infection risk from sampled variables."""
            pathogen_conc = samples["pathogen_concentration"]
            dilution = samples["dilution_factor"]
            volume = samples["ingestion_volume"]

            # Apply treatment
            post_treatment = pathogen_conc / (10 ** treatment_lrv)

            # Apply dilution
            exposure_conc = post_treatment / dilution

            # Calculate dose (organisms ingested)
            # Convert: exposure_conc is in organisms/L, volume is in mL
            dose = exposure_conc * (volume / 1000.0)  # Convert mL to L

            # Calculate infection probability
            infection_prob = dr_model.calculate_infection_probability(dose)

            return infection_prob

        # Run simulation
        mc_results = mc_simulator.run_simulation(qmra_model, n_iterations=iterations,
                                                 variable_name="infection_probability")

        # Calculate illness probability
        pill_median = mc_results.statistics['median'] * health_data['illness_to_infection_ratio']
        pill_5th = mc_results.percentiles['5%'] * health_data['illness_to_infection_ratio']
        pill_95th = mc_results.percentiles['95%'] * health_data['illness_to_infection_ratio']

        # Calculate annual risk
        pinf_per_event = mc_results.statistics['median']
        annual_risk_median = 1 - (1 - pinf_per_event) ** frequency_per_year
        annual_5th = 1 - (1 - mc_results.percentiles['5%']) ** frequency_per_year
        annual_95th = 1 - (1 - mc_results.percentiles['95%']) ** frequency_per_year

        # Population impact
        population_impact = annual_risk_median * population

        return {
            'pinf_median': mc_results.statistics['median'],
            'pinf_5th': mc_results.percentiles['5%'],
            'pinf_95th': mc_results.percentiles['95%'],
            'pill_median': pill_median,
            'pill_5th': pill_5th,
            'pill_95th': pill_95th,
            'annual_risk_median': annual_risk_median,
            'annual_5th': annual_5th,
            'annual_95th': annual_95th,
            'population_impact': population_impact
        }

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

    def run_batch_scenarios_from_libraries(self, scenarios_file, dilution_data_file,
                                           pathogen_data_file, output_dir=None):
        """
        Run batch scenarios using simplified three-file approach.

        Files:
        - dilution_data.csv: Time, Location, Dilution_Factor (raw data from hydrodynamic models)
        - pathogen_data.csv: Pathogen_ID, Pathogen_Name, Pathogen_Type,
                             Min_Concentration, Median_Concentration, Max_Concentration, P_Breakpoint
                             (Hockey Stick distribution parameters: X0, X50, X100, P)
        - scenarios.csv: All scenario parameters (references Location and Pathogen_ID)

        Args:
            scenarios_file: CSV with scenario definitions
            dilution_data_file: CSV with dilution time-series data
            pathogen_data_file: CSV with pathogen Hockey Stick parameters
            output_dir: Directory for output files

        Returns:
            DataFrame with all scenario results
        """
        print(f"\n{'='*80}")
        print("BATCH SCENARIO EXECUTION (Simplified Approach)")
        print(f"{'='*80}")

        # Load data files
        print("\nLoading data files...")
        dilution_data = pd.read_csv(dilution_data_file)
        pathogen_data = pd.read_csv(pathogen_data_file)
        scenarios_df = pd.read_csv(scenarios_file)

        print(f"  Dilution data: {len(dilution_data)} records")
        print(f"  Pathogen data: {len(pathogen_data)} entries")
        print(f"  Scenarios: {len(scenarios_df)}")

        # Show unique locations in dilution data
        unique_locations = dilution_data['Location'].unique()
        print(f"  Unique locations: {', '.join(unique_locations)}")

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

            # Look up pathogen data by Pathogen_ID
            pathogen_id = scenario['Pathogen_ID']
            pathogen_row = pathogen_data[pathogen_data['Pathogen_ID'] == pathogen_id]

            if len(pathogen_row) == 0:
                raise ValueError(f"Pathogen ID '{pathogen_id}' not found in pathogen data")

            pathogen_row = pathogen_row.iloc[0]
            pathogen_type = pathogen_row['Pathogen_Type']

            # Get Hockey Stick parameters for pathogen
            pathogen_min = pathogen_row['Min_Concentration']
            pathogen_median = pathogen_row['Median_Concentration']
            pathogen_max = pathogen_row['Max_Concentration']
            pathogen_p = pathogen_row.get('P_Breakpoint', 0.95)  # Default to 0.95 if not specified

            print(f"    Pathogen: {pathogen_type} (Hockey Stick: X0={pathogen_min:.0e}, X50={pathogen_median:.0e}, X100={pathogen_max:.0e}, P={pathogen_p:.2f})")

            # Look up dilution data by Location
            location = scenario['Location']
            location_dilution = dilution_data[dilution_data['Location'] == location]

            if len(location_dilution) == 0:
                raise ValueError(f"Location '{location}' not found in dilution data")

            # Get all dilution values for this location (for ECDF)
            dilution_values = location_dilution['Dilution_Factor'].values
            dilution_median = np.median(dilution_values)

            print(f"    Location: {location} ({len(dilution_values)} dilution records, median={dilution_median:.1f}x)")

            # Run QMRA with empirical distributions
            result = self._run_assessment_with_distributions(
                pathogen=pathogen_type,
                dilution_values=dilution_values,
                pathogen_min=pathogen_min,
                pathogen_median=pathogen_median,
                pathogen_max=pathogen_max,
                pathogen_p=pathogen_p,
                treatment_lrv=scenario['Treatment_LRV'],
                treatment_lrv_uncertainty=scenario.get('Treatment_LRV_Uncertainty', 0.2),
                exposure_route=scenario['Exposure_Route'],
                volume_ml=scenario['Ingestion_Volume_mL'],
                volume_min=scenario.get('Volume_Min_mL', None),
                volume_max=scenario.get('Volume_Max_mL', None),
                frequency_per_year=scenario['Exposure_Frequency_per_Year'],
                population=scenario['Exposed_Population'],
                iterations=scenario.get('Monte_Carlo_Iterations', 10000)
            )

            results.append({
                'Scenario_ID': scenario_id,
                'Scenario_Name': scenario_name,
                'Pathogen_ID': pathogen_id,
                'Pathogen': pathogen_type,
                'Location': location,
                'Dilution_Median': dilution_median,
                'Dilution_Min': np.min(dilution_values),
                'Dilution_Max': np.max(dilution_values),
                'Dilution_Records': len(dilution_values),
                'Pathogen_Conc_Median': pathogen_median,
                'Exposure_Route': scenario['Exposure_Route'],
                'Treatment_LRV': scenario['Treatment_LRV'],
                'Volume_mL': scenario['Ingestion_Volume_mL'],
                'Frequency_Year': scenario['Exposure_Frequency_per_Year'],
                'Population': scenario['Exposed_Population'],
                'Infection_Risk_Median': result['pinf_median'],
                'Annual_Risk_Median': result['annual_risk_median'],
                'Annual_Risk_5th': result['annual_5th'],
                'Annual_Risk_95th': result['annual_95th'],
                'Population_Impact': result['population_impact'],
                'Compliance_Status': 'COMPLIANT' if result['annual_risk_median'] <= 1e-4 else 'NON-COMPLIANT',
                'Priority': scenario.get('Priority', 'Medium')
            })

            print(f"    Risk: {result['annual_risk_median']:.2e}  {results[-1]['Compliance_Status']}")

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

        print(f"\nBatch Summary:")
        print(f"  Total scenarios: {total_scenarios}")
        print(f"  Compliant: {compliant} ({100*compliant/total_scenarios:.1f}%)")
        print(f"  Non-compliant: {total_scenarios - compliant} ({100*(total_scenarios-compliant)/total_scenarios:.1f}%)")

        return results_df

    def _run_assessment_with_distributions(self, pathogen, dilution_values,
                                            pathogen_min, pathogen_median, pathogen_max,
                                            pathogen_p=0.95,
                                            treatment_lrv=0, treatment_lrv_uncertainty=0.2,
                                            exposure_route='primary_contact', volume_ml=50, volume_min=None, volume_max=None,
                                            frequency_per_year=20, population=10000, iterations=10000):
        """
        Run QMRA with empirical dilution ECDF and Hockey Stick pathogen distribution.

        Args:
            pathogen: Pathogen name
            dilution_values: Array of dilution factors for ECDF
            pathogen_min: Min pathogen concentration (X₀)
            pathogen_median: Median pathogen concentration (X₅₀)
            pathogen_max: Max pathogen concentration (X₁₀₀)
            pathogen_p: Breakpoint percentile for hockey stick (default 0.95)
            treatment_lrv: Log reduction value (default 0)
            treatment_lrv_uncertainty: Uncertainty in treatment (default 0.2)
            exposure_route: Exposure route (default 'primary_contact')
            volume_ml: Mean ingestion volume (default 50 mL)
            volume_min: Minimum volume (default None = 0.7 * volume_ml)
            volume_max: Maximum volume (default None = 1.3 * volume_ml)
            frequency_per_year: Exposure frequency (default 20)
            population: Exposed population (default 10000)
            iterations: Monte Carlo iterations (default 10000)

        Returns:
            Dictionary with risk results
        """
        if not QMRA_MODULES_AVAILABLE:
            raise RuntimeError("QMRA modules required for distribution-based assessments")

        # Get pathogen parameters
        pathogen_info = self.pathogen_db.get_pathogen_info(pathogen)
        default_model_type = self.pathogen_db.get_default_model_type(pathogen)
        dr_params = self.pathogen_db.get_dose_response_parameters(pathogen, default_model_type)
        health_data = self.pathogen_db.get_health_impact_data(pathogen)

        # Create dose-response model
        dr_model = create_dose_response_model(default_model_type, dr_params)

        # Setup Monte Carlo simulator
        mc_simulator = MonteCarloSimulator(random_seed=42)

        # Add pathogen concentration as Hockey Stick distribution
        pathogen_dist = create_hockey_stick_distribution(
            x_min=pathogen_min,
            x_median=pathogen_median,
            x_max=pathogen_max,
            P=pathogen_p,
            name="pathogen_concentration"
        )
        mc_simulator.add_distribution("pathogen_concentration", pathogen_dist)

        # Add dilution as ECDF from data
        dilution_dist = create_empirical_cdf_from_data(
            dilution_values,
            name="dilution_factor"
        )
        mc_simulator.add_distribution("dilution_factor", dilution_dist)

        # Add ingestion volume distribution
        if volume_min is None:
            volume_min = volume_ml * 0.7
        if volume_max is None:
            volume_max = volume_ml * 1.3

        volume_dist = create_uniform_distribution(
            min_val=volume_min,
            max_val=volume_max,
            name="ingestion_volume"
        )
        mc_simulator.add_distribution("ingestion_volume", volume_dist)

        # Define QMRA model
        def qmra_model(samples):
            """Calculate infection risk from sampled variables."""
            pathogen_conc = samples["pathogen_concentration"]
            dilution = samples["dilution_factor"]
            volume = samples["ingestion_volume"]

            # Apply treatment
            post_treatment = pathogen_conc / (10 ** treatment_lrv)

            # Apply dilution
            exposure_conc = post_treatment / dilution

            # Calculate dose (organisms ingested)
            dose = exposure_conc * (volume / 1000.0)  # Convert mL to L

            # Calculate infection probability
            infection_prob = dr_model.calculate_infection_probability(dose)

            return infection_prob

        # Run simulation
        mc_results = mc_simulator.run_simulation(qmra_model, n_iterations=iterations,
                                                 variable_name="infection_probability")

        # Calculate illness probability
        pill_median = mc_results.statistics['median'] * health_data['illness_to_infection_ratio']

        # Calculate annual risk
        pinf_per_event = mc_results.statistics['median']
        annual_risk_median = 1 - (1 - pinf_per_event) ** frequency_per_year
        annual_5th = 1 - (1 - mc_results.percentiles['5%']) ** frequency_per_year
        annual_95th = 1 - (1 - mc_results.percentiles['95%']) ** frequency_per_year

        # Population impact
        population_impact = annual_risk_median * population

        return {
            'pinf_median': mc_results.statistics['median'],
            'pinf_5th': mc_results.percentiles['5%'],
            'pinf_95th': mc_results.percentiles['95%'],
            'pill_median': pill_median,
            'annual_risk_median': annual_risk_median,
            'annual_5th': annual_5th,
            'annual_95th': annual_95th,
            'population_impact': int(population_impact)
        }

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
