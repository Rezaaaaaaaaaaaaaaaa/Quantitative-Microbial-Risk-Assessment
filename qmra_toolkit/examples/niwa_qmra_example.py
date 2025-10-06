"""
NIWA QMRA Example
Demonstrates using the enhanced QMRA toolkit to match NIWA report standards
Based on Charlotte Jones-Todd's R package methodology
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.qmra_integration import QMRAAssessment, QMRAScenario
from src.pathogen_database_advanced import PathogenDatabase
from src.monte_carlo_advanced import HydrodynamicDilution

# Set up plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)


def create_example_dilution_data(n_sites=5, n_samples=1000):
    """
    Create example hydrodynamic dilution data for multiple sites
    Similar to the R package's Enterococci_dilution data
    """
    np.random.seed(42)
    dilution_data = {}

    for i in range(n_sites):
        # Create log-normal distributed dilution factors
        # Sites closer to discharge have lower dilution (higher concentration)
        mean_log = 2 + i * 0.5  # Increasing dilution with distance
        sd_log = 0.5
        dilution_data[f'Site_{i+1}'] = np.random.lognormal(mean_log, sd_log, n_samples)

    return dilution_data


def run_niwa_standard_assessment():
    """
    Run QMRA assessment following NIWA standards
    Similar to the New Plymouth WWTP assessment
    """
    print("=" * 80)
    print("NIWA QMRA ASSESSMENT - Enhanced Toolkit Demonstration")
    print("Based on Charlotte Jones-Todd's R QMRA Package")
    print("=" * 80)

    # Initialize components
    qmra = QMRAAssessment()
    pathogen_db = PathogenDatabase()

    # Display available pathogens
    print("\nAvailable Pathogens in Database:")
    print("-" * 40)
    for pathogen in pathogen_db.get_all_pathogens():
        params_list = pathogen_db.get_pathogen(pathogen)
        print(f"  {pathogen.title()}: {len(params_list)} model(s)")

    # Set up assessment parameters
    pathogen_name = 'norovirus'
    print(f"\nSelected Pathogen: {pathogen_name.title()}")

    # Get pathogen parameters
    best_model = pathogen_db.get_best_fit_model(pathogen_name)
    print(f"Best-fit Model: {best_model.model}")
    print(f"Parameters: {best_model.parameters}")
    print(f"Source: {best_model.source}")

    # Create dilution data for multiple sites
    print("\nGenerating Hydrodynamic Dilution Data...")
    dilution_data = create_example_dilution_data(n_sites=5)

    # Treatment scenarios (matching NIWA report)
    treatment_scenarios = {
        'Bypass (No Treatment)': 0,
        'Primary Treatment': {'min': 0.5, 'max': 1.0},
        'Secondary Treatment': {'min': 1.5, 'max': 2.5},
        'Tertiary Treatment': {'min': 2.5, 'max': 3.5},
        'UV Disinfection': {'min': 3.0, 'max': 4.0}
    }

    # Run assessments for each treatment scenario
    results_by_treatment = {}

    for treatment_name, efficacy in treatment_scenarios.items():
        print(f"\n{'-' * 60}")
        print(f"Running Assessment: {treatment_name}")
        print(f"Treatment Efficacy: {efficacy} log reduction")

        # Create scenario
        scenario = QMRAScenario(
            name=f"NIWA QMRA - {treatment_name}",
            pathogen=pathogen_name,
            exposure_route='swimming',
            treatment_efficacy=efficacy,
            influent_concentration={
                'distribution': 'lognormal',
                'params': {'meanlog': 5.0, 'sdlog': 1.0}  # log10 copies/L
            },
            events_per_year=20  # Swimming events per year
        )

        # Run for multiple sites
        site_results = qmra.run_multiple_sites(
            base_scenario=scenario,
            site_dilutions=dilution_data,
            nsim=10000
        )

        results_by_treatment[treatment_name] = site_results

        # Display results summary
        print(f"\nResults Summary for {treatment_name}:")
        print(f"{'Site':<10} {'Median IIR':<15} {'95th %ile IIR':<15} {'Annual IIR':<15}")
        print("-" * 60)

        for site_name, result in site_results.items():
            median_iir = result.risk_percentiles['illness_median']
            p95_iir = result.risk_percentiles['illness_95']
            annual_iir = result.risk_percentiles['annual_illness_median']
            print(f"{site_name:<10} {median_iir:<15.2e} {p95_iir:<15.2e} {annual_iir:<15.2e}")

    # Create comparison table (similar to NIWA report format)
    print("\n" + "=" * 80)
    print("COMPARISON OF TREATMENT SCENARIOS")
    print("=" * 80)

    comparison_data = []
    for treatment_name, site_results in results_by_treatment.items():
        for site_name, result in site_results.items():
            comparison_data.append({
                'Treatment': treatment_name,
                'Site': site_name,
                'Median IIR': result.risk_percentiles['illness_median'],
                '95th %ile IIR': result.risk_percentiles['illness_95'],
                'Annual IIR': result.risk_percentiles['annual_illness_median'],
                'Mean Dose': np.mean(result.monte_carlo_results.doses),
                'Max Dose': np.max(result.monte_carlo_results.doses)
            })

    comparison_df = pd.DataFrame(comparison_data)

    # Calculate risk reduction
    bypass_risks = comparison_df[comparison_df['Treatment'] == 'Bypass (No Treatment)']['Median IIR'].values

    print("\nRisk Reduction Summary by Treatment Level:")
    print("-" * 60)
    for treatment in treatment_scenarios.keys():
        if treatment != 'Bypass (No Treatment)':
            treatment_risks = comparison_df[comparison_df['Treatment'] == treatment]['Median IIR'].values
            reduction = (1 - treatment_risks.mean() / bypass_risks.mean()) * 100
            print(f"{treatment:<25} {reduction:.1f}% reduction")

    # Create visualizations
    create_visualizations(results_by_treatment)

    # Export results
    export_results(comparison_df, pathogen_db)

    print("\n" + "=" * 80)
    print("ASSESSMENT COMPLETE")
    print("=" * 80)

    return results_by_treatment, comparison_df


def create_visualizations(results_by_treatment):
    """Create professional visualizations similar to NIWA reports"""

    print("\nGenerating Visualizations...")

    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))

    # 1. Risk by treatment level
    ax1 = axes[0, 0]
    treatment_names = []
    median_risks = []
    p95_risks = []

    for treatment_name, site_results in results_by_treatment.items():
        treatment_names.append(treatment_name.replace(' Treatment', '').replace('(No Treatment)', ''))
        all_risks = []
        for site_name, result in site_results.items():
            all_risks.append(result.risk_percentiles['illness_median'])
        median_risks.append(np.mean(all_risks))

        all_p95 = []
        for site_name, result in site_results.items():
            all_p95.append(result.risk_percentiles['illness_95'])
        p95_risks.append(np.mean(all_p95))

    x_pos = np.arange(len(treatment_names))
    ax1.bar(x_pos - 0.2, median_risks, 0.4, label='Median IIR', color='steelblue')
    ax1.bar(x_pos + 0.2, p95_risks, 0.4, label='95th %ile IIR', color='coral')
    ax1.set_xlabel('Treatment Level')
    ax1.set_ylabel('Individual Illness Risk (IIR)')
    ax1.set_title('Risk by Treatment Level (All Sites Average)')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(treatment_names, rotation=45, ha='right')
    ax1.legend()
    ax1.set_yscale('log')
    ax1.grid(True, alpha=0.3)

    # 2. Risk by site for secondary treatment
    ax2 = axes[0, 1]
    secondary_results = results_by_treatment.get('Secondary Treatment', {})
    sites = []
    site_risks = []

    for site_name, result in secondary_results.items():
        sites.append(site_name)
        site_risks.append(result.risk_percentiles['illness_median'])

    ax2.bar(sites, site_risks, color='green', alpha=0.7)
    ax2.set_xlabel('Site')
    ax2.set_ylabel('Median IIR')
    ax2.set_title('Risk by Site (Secondary Treatment)')
    ax2.set_yscale('log')
    ax2.grid(True, alpha=0.3)

    # 3. Dose distribution histogram for secondary treatment
    ax3 = axes[1, 0]
    if secondary_results:
        first_site_result = list(secondary_results.values())[0]
        doses = first_site_result.monte_carlo_results.doses.flatten()
        doses_log = np.log10(doses[doses > 0])  # Log transform for visualization

        ax3.hist(doses_log, bins=50, color='purple', alpha=0.7, edgecolor='black')
        ax3.set_xlabel('Log10(Dose) [organisms]')
        ax3.set_ylabel('Frequency')
        ax3.set_title('Dose Distribution (Secondary Treatment, Site 1)')
        ax3.grid(True, alpha=0.3)

    # 4. Annual risk comparison
    ax4 = axes[1, 1]
    treatment_names_short = []
    annual_risks = []

    for treatment_name, site_results in results_by_treatment.items():
        treatment_names_short.append(treatment_name.split(' ')[0])
        all_annual = []
        for site_name, result in site_results.items():
            all_annual.append(result.risk_percentiles['annual_illness_median'])
        annual_risks.append(np.mean(all_annual))

    colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(treatment_names_short)))
    bars = ax4.bar(treatment_names_short, annual_risks, color=colors)
    ax4.set_xlabel('Treatment Level')
    ax4.set_ylabel('Annual Illness Risk')
    ax4.set_title('Annual Risk Comparison (20 events/year)')
    ax4.set_yscale('log')
    ax4.grid(True, alpha=0.3)

    # Add WHO guideline line (example)
    ax4.axhline(y=1e-3, color='red', linestyle='--', label='WHO Guideline')
    ax4.legend()

    plt.tight_layout()

    # Save figure
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    plt.savefig(output_dir / "niwa_qmra_results.png", dpi=300, bbox_inches='tight')
    print(f"Visualizations saved to {output_dir / 'niwa_qmra_results.png'}")

    # plt.show()  # Commented out to avoid hanging in non-interactive mode
    plt.close('all')


def export_results(comparison_df, pathogen_db):
    """Export results to files"""

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Export comparison table
    csv_path = output_dir / "qmra_comparison_results.csv"
    comparison_df.to_csv(csv_path, index=False)
    print(f"\nResults exported to {csv_path}")

    # Export pathogen database
    json_path = output_dir / "pathogen_database.json"
    pathogen_db.export_to_json(str(json_path))
    print(f"Pathogen database exported to {json_path}")

    # Create summary report
    report_path = output_dir / "qmra_summary_report.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("NIWA QMRA ASSESSMENT SUMMARY REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write("Enhanced QMRA Toolkit - Based on Charlotte Jones-Todd's R Package\n\n")

        f.write("KEY FINDINGS:\n")
        f.write("-" * 40 + "\n")

        # Calculate key statistics
        bypass_median = comparison_df[comparison_df['Treatment'] == 'Bypass (No Treatment)']['Median IIR'].mean()
        uv_median = comparison_df[comparison_df['Treatment'] == 'UV Disinfection']['Median IIR'].mean()
        reduction = (1 - uv_median / bypass_median) * 100

        f.write(f"1. Bypass Median IIR: {bypass_median:.2e}\n")
        f.write(f"2. UV Treatment Median IIR: {uv_median:.2e}\n")
        f.write(f"3. Risk Reduction with UV: {reduction:.1f}%\n\n")

        f.write("METHODOLOGY:\n")
        f.write("-" * 40 + "\n")
        f.write("- Pathogen: Norovirus\n")
        f.write("- Model: Fractional Poisson (Messner et al 2014)\n")
        f.write("- Monte Carlo Simulations: 10,000\n")
        f.write("- Exposure Route: Swimming\n")
        f.write("- Events per Year: 20\n\n")

        f.write("TREATMENT SCENARIOS ASSESSED:\n")
        f.write("-" * 40 + "\n")
        f.write("1. Bypass (No Treatment): 0 log reduction\n")
        f.write("2. Primary Treatment: 0.5-1.0 log reduction\n")
        f.write("3. Secondary Treatment: 1.5-2.5 log reduction\n")
        f.write("4. Tertiary Treatment: 2.5-3.5 log reduction\n")
        f.write("5. UV Disinfection: 3.0-4.0 log reduction\n\n")

        f.write("This assessment follows NIWA standards and incorporates:\n")
        f.write("- Comprehensive dose-response models (11 types)\n")
        f.write("- Advanced Monte Carlo framework\n")
        f.write("- Hydrodynamic dilution modeling\n")
        f.write("- Pathogen-specific parameters from literature\n")

    print(f"Summary report saved to {report_path}")


if __name__ == "__main__":
    # Run the NIWA standard assessment
    results, comparison = run_niwa_standard_assessment()

    print("\nEnhanced QMRA toolkit demonstration complete!")
    print("This implementation adapts Charlotte Jones-Todd's R QMRA package")
    print("and matches NIWA professional report standards.")