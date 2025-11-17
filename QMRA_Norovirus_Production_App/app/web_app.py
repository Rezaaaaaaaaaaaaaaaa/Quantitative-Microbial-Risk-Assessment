#!/usr/bin/env python3
"""
QMRA Batch Processing Web Application
=====================================

Streamlit web GUI for running batch QMRA assessments and generating PDF reports.

Usage:
    streamlit run web_app.py

Author: NIWA Earth Sciences New Zealand
Date: October 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import io
from datetime import datetime
import zipfile
import tempfile

# Import our modules
from batch_processor import BatchProcessor
from pdf_report_generator import QMRAPDFReportGenerator

# Page configuration
st.set_page_config(
    page_title="QMRA Norovirus Production",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
    }
    .danger-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Plotting helper functions
def create_risk_overview_plot(df):
    """Create horizontal bar chart of risk by scenario."""
    fig, ax = plt.subplots(figsize=(12, max(6, len(df) * 0.3)))

    # Check if required columns exist
    if 'Annual_Risk_Median' not in df.columns:
        ax.text(0.5, 0.5, 'Annual_Risk_Median column not found',
                ha='center', va='center', fontsize=14)
        plt.tight_layout()
        return fig

    df_sorted = df.sort_values('Annual_Risk_Median', ascending=True)

    # Set colors based on Compliance_Status if available
    if 'Compliance_Status' in df.columns:
        colors = ['#28a745' if s == 'COMPLIANT' else '#dc3545'
                 for s in df_sorted['Compliance_Status']]
    else:
        colors = '#1f77b4'  # Default blue color

    ax.barh(range(len(df_sorted)), df_sorted['Annual_Risk_Median'], color=colors, alpha=0.7)
    ax.set_yticks(range(len(df_sorted)))

    # Use Scenario_Name if available, otherwise use index
    if 'Scenario_Name' in df_sorted.columns:
        ax.set_yticklabels(df_sorted['Scenario_Name'], fontsize=9)
    else:
        ax.set_yticklabels([f"Scenario {i+1}" for i in range(len(df_sorted))], fontsize=9)

    ax.set_xlabel('Annual Infection Risk (Median)', fontsize=12, fontweight='bold')
    ax.set_title('Risk Overview by Scenario', fontsize=14, fontweight='bold', pad=20)
    ax.set_xscale('log')
    ax.axvline(x=1e-4, color='orange', linestyle='--', linewidth=2, label='WHO Threshold (1e-4)')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()
    return fig


def create_compliance_plot(df):
    """Create pie chart of compliance status."""
    fig, ax = plt.subplots(figsize=(8, 8))

    if 'Compliance_Status' not in df.columns:
        ax.text(0.5, 0.5, 'Compliance_Status column not found',
                ha='center', va='center', fontsize=14, transform=ax.transAxes)
        ax.set_title('Compliance Status Distribution', fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        return fig

    compliance_counts = df['Compliance_Status'].value_counts()
    colors_map = {'COMPLIANT': '#28a745', 'NON-COMPLIANT': '#dc3545'}
    colors = [colors_map.get(status, '#6c757d') for status in compliance_counts.index]

    wedges, texts, autotexts = ax.pie(
        compliance_counts.values,
        labels=compliance_counts.index,
        autopct='%1.1f%%',
        colors=colors,
        startangle=90,
        textprops={'fontsize': 12, 'fontweight': 'bold'}
    )

    ax.set_title('Compliance Status Distribution', fontsize=14, fontweight='bold', pad=20)

    # Add count labels
    for i, count in enumerate(compliance_counts.values):
        texts[i].set_text(f"{texts[i].get_text()}\n({count} scenarios)")

    plt.tight_layout()
    return fig


def create_risk_distribution_plot(df):
    """Create histogram of risk distribution."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    if 'Annual_Risk_Median' not in df.columns:
        ax1.text(0.5, 0.5, 'Annual_Risk_Median column not found',
                ha='center', va='center', fontsize=14, transform=ax1.transAxes)
        ax2.text(0.5, 0.5, 'Data not available',
                ha='center', va='center', fontsize=14, transform=ax2.transAxes)
        plt.tight_layout()
        return fig

    # Histogram - filter out zero/very small values before log10
    risk_values = df['Annual_Risk_Median'].values
    # Filter out values <= 0 or extremely small values that would cause -inf
    valid_risks = risk_values[risk_values > 1e-15]

    if len(valid_risks) > 0:
        ax1.hist(np.log10(valid_risks), bins=20, color='steelblue', alpha=0.7, edgecolor='black')
        ax1.set_xlabel('Log10(Annual Risk)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax1.set_title('Risk Distribution (Histogram)', fontsize=13, fontweight='bold')
        ax1.axvline(x=np.log10(1e-4), color='orange', linestyle='--', linewidth=2, label='WHO Threshold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
    else:
        ax1.text(0.5, 0.5, 'No valid risk values to plot',
                ha='center', va='center', fontsize=14, transform=ax1.transAxes)

    # Box plot by risk classification
    if 'Risk_Classification' in df.columns:
        risk_classes = df['Risk_Classification'].unique()
        data_by_class = [df[df['Risk_Classification'] == rc]['Annual_Risk_Median'].values
                        for rc in risk_classes]

        bp = ax2.boxplot(data_by_class, labels=risk_classes, patch_artist=True)
        for patch in bp['boxes']:
            patch.set_facecolor('lightblue')

        ax2.set_ylabel('Annual Risk (Median)', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Risk Classification', fontsize=12, fontweight='bold')
        ax2.set_title('Risk by Classification', fontsize=13, fontweight='bold')
        ax2.set_yscale('log')
        ax2.grid(True, alpha=0.3, axis='y')
    else:
        ax2.text(0.5, 0.5, 'Risk Classification not available',
                ha='center', va='center', fontsize=14, transform=ax2.transAxes)

    plt.tight_layout()
    return fig


def create_population_impact_plot(df):
    """Create population impact visualization."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    if 'Population_Impact' not in df.columns:
        ax1.text(0.5, 0.5, 'Population_Impact column not found',
                ha='center', va='center', fontsize=14, transform=ax1.transAxes)
        ax2.text(0.5, 0.5, 'Data not available',
                ha='center', va='center', fontsize=14, transform=ax2.transAxes)
        plt.tight_layout()
        return fig

    # Bar chart of population impact
    df_sorted = df.nlargest(15, 'Population_Impact')
    colors = ['#dc3545' if impact > 1000 else '#ffc107' if impact > 100 else '#28a745'
             for impact in df_sorted['Population_Impact']]

    ax1.barh(range(len(df_sorted)), df_sorted['Population_Impact'], color=colors, alpha=0.7)
    ax1.set_yticks(range(len(df_sorted)))

    # Use Scenario_Name if available
    if 'Scenario_Name' in df_sorted.columns:
        ax1.set_yticklabels(df_sorted['Scenario_Name'], fontsize=9)
    else:
        ax1.set_yticklabels([f"Scenario {i+1}" for i in range(len(df_sorted))], fontsize=9)

    ax1.set_xlabel('Expected Annual Illnesses', fontsize=12, fontweight='bold')
    ax1.set_title('Top 15 Scenarios by Population Impact', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='x')

    # Scatter plot: Risk vs Population (only if Annual_Risk_Median exists)
    if 'Annual_Risk_Median' in df.columns:
        scatter = ax2.scatter(df['Annual_Risk_Median'], df['Population_Impact'],
                             s=100, alpha=0.6, c=df['Population_Impact'],
                             cmap='YlOrRd', edgecolors='black', linewidth=0.5)

        ax2.set_xlabel('Annual Risk (Median)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Expected Annual Illnesses', fontsize=12, fontweight='bold')
        ax2.set_title('Risk vs Population Impact', fontsize=13, fontweight='bold')
        ax2.set_xscale('log')
        ax2.grid(True, alpha=0.3)

        cbar = plt.colorbar(scatter, ax=ax2)
        cbar.set_label('Population Impact', fontsize=10)
    else:
        ax2.text(0.5, 0.5, 'Annual_Risk_Median not available',
                ha='center', va='center', fontsize=14, transform=ax2.transAxes)

    plt.tight_layout()
    return fig


def fig_to_bytes(fig, dpi=300):
    """Convert matplotlib figure to bytes for download."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, bbox_inches='tight')
    buf.seek(0)
    return buf.getvalue()


def create_summary_statistics(df):
    """Create summary statistics table."""
    summary = pd.DataFrame({
        'Metric': [
            'Total Scenarios',
            'Compliant Scenarios',
            'Non-Compliant Scenarios',
            'Mean Annual Risk',
            'Median Annual Risk',
            'Min Annual Risk',
            'Max Annual Risk',
            'Total Expected Illnesses',
            'Avg Population Impact',
            'Scenarios with High Risk Classification',
            'Scenarios with Medium Risk Classification',
            'Scenarios with Low Risk Classification'
        ],
        'Value': [
            len(df),
            len(df[df['Compliance_Status'] == 'COMPLIANT']),
            len(df[df['Compliance_Status'] == 'NON-COMPLIANT']),
            f"{df['Annual_Risk_Median'].mean():.2e}",
            f"{df['Annual_Risk_Median'].median():.2e}",
            f"{df['Annual_Risk_Median'].min():.2e}",
            f"{df['Annual_Risk_Median'].max():.2e}",
            f"{df['Population_Impact'].sum():.0f}",
            f"{df['Population_Impact'].mean():.1f}",
            len(df[df['Risk_Classification'] == 'High']) if 'Risk_Classification' in df.columns else 'N/A',
            len(df[df['Risk_Classification'] == 'Medium']) if 'Risk_Classification' in df.columns else 'N/A',
            len(df[df['Risk_Classification'] == 'Low']) if 'Risk_Classification' in df.columns else 'N/A'
        ]
    })

    return summary


def create_zip_bundle(df, plots, results_file):
    """Create ZIP file containing all results, plots, and tables."""
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add main CSV
        zip_file.writestr('results_full.csv', df.to_csv(index=False))

        # Add individual table subsets (with safe column checking)
        if 'Risk_Classification' in df.columns:
            high_risk_df = df[df['Risk_Classification'].isin(['High', 'Medium'])]
            if len(high_risk_df) > 0:
                zip_file.writestr('tables/high_risk_scenarios.csv', high_risk_df.to_csv(index=False))

        if 'Compliance_Status' in df.columns:
            compliant_df = df[df['Compliance_Status'] == 'COMPLIANT']
            if len(compliant_df) > 0:
                zip_file.writestr('tables/compliant_scenarios.csv', compliant_df.to_csv(index=False))

            non_compliant_df = df[df['Compliance_Status'] == 'NON-COMPLIANT']
            if len(non_compliant_df) > 0:
                zip_file.writestr('tables/non_compliant_scenarios.csv', non_compliant_df.to_csv(index=False))

        top_risk_df = df.nlargest(10, 'Annual_Risk_Median')
        zip_file.writestr('tables/top_10_highest_risk.csv', top_risk_df.to_csv(index=False))

        summary_df = create_summary_statistics(df)
        zip_file.writestr('tables/summary_statistics.csv', summary_df.to_csv(index=True))

        # Add plots
        for plot_name, fig in plots.items():
            plot_bytes = fig_to_bytes(fig, dpi=300)
            zip_file.writestr(f'plots/{plot_name}.png', plot_bytes)

        # Add README
        # Generate summary statistics for README
        compliant_count = len(df[df['Compliance_Status'] == 'COMPLIANT']) if 'Compliance_Status' in df.columns else 0
        non_compliant_count = len(df[df['Compliance_Status'] == 'NON-COMPLIANT']) if 'Compliance_Status' in df.columns else 0
        mean_risk = df['Annual_Risk_Median'].mean() if 'Annual_Risk_Median' in df.columns else 0
        total_impact = df['Population_Impact'].sum() if 'Population_Impact' in df.columns else 0

        readme_content = f"""QMRA Batch Assessment Results Package
========================================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Scenarios: {len(df)}

Contents:
---------
1. results_full.csv - Complete results for all scenarios

2. tables/ - Data subsets:
   - high_risk_scenarios.csv (if applicable)
   - compliant_scenarios.csv (if applicable)
   - non_compliant_scenarios.csv (if applicable)
   - top_10_highest_risk.csv
   - summary_statistics.csv

3. plots/ - Visualizations (PNG, 300 DPI):
   - risk_overview.png
   - compliance_distribution.png
   - risk_distribution.png
   - population_impact.png

Summary Statistics:
-------------------
Compliant: {compliant_count} ({compliant_count/len(df)*100:.1f}%)
Non-Compliant: {non_compliant_count} ({non_compliant_count/len(df)*100:.1f}%)
Mean Risk: {mean_risk:.2e}
Total Expected Illnesses: {total_impact:.0f}

---
NIWA Earth Sciences New Zealand
QMRA Batch Processing Tool v1.0
"""
        zip_file.writestr('README.txt', readme_content)

    zip_buffer.seek(0)
    return zip_buffer.getvalue()


def main():
    """Main application."""

    # Header
    st.markdown('<div class="main-header">🦠 QMRA Norovirus Production Tool</div>', unsafe_allow_html=True)
    st.markdown("**Excel-Validated Norovirus Risk Assessment | Production Version 1.0**")

    # Sidebar
    with st.sidebar:
        st.image("niwa_logo.png", use_container_width=True)
        st.markdown("---")

        # Norovirus-Only Production Application
        st.markdown("### 🔬 Pathogen")
        st.success("✅ **Norovirus Only (Validated)**\n\nBeta-Binomial dose-response validated with Excel QMRA_Shellfish_191023_Nino_SUMMER.xlsx\n\n**Parameters:**\n- α = 0.04, β = 0.055 (Teunis et al. 2008)\n- Pr(ill|inf) = 0.5\n- P(susceptible) = 0.74\n- Fractional organism discretization: INT + Binomial")

        # Only norovirus available in this production version
        available_pathogens = ["norovirus"]

        st.markdown("---")

        st.markdown("### Assessment Mode")
        assessment_mode = st.selectbox(
            "Select batch processing type:",
            ["Batch Scenarios", "Spatial Assessment", "Temporal Assessment",
             "Treatment Comparison", "Multi-Pathogen Assessment"]
        )

        st.markdown("---")
        st.markdown("### About")
        st.info("""
        **QMRA Norovirus Production Tool**

        Excel-validated norovirus risk assessments with:
        - ✅ **Excel-exact calculations** (0.00000000% difference)
        - 📚 **Library-based input**: Reusable data libraries
        - 📑 Comprehensive PDF reports
        - 📊 Interactive visualizations
        - 📄 Individual plot downloads (PNG)
        - 📋 Individual table downloads (CSV/Excel)
        - 📦 Complete results bundle (ZIP)
        - ⚙️ Treatment comparisons
        - 🔬 **Norovirus only** (validated pathogen)
        """)

        st.markdown("**NIWA Earth Sciences**  \n**Norovirus Production Version 1.0** | November 2025")

    # Main content
    if assessment_mode == "Batch Scenarios":
        batch_scenarios_page()
    elif assessment_mode == "Spatial Assessment":
        spatial_assessment_page()
    elif assessment_mode == "Temporal Assessment":
        temporal_assessment_page()
    elif assessment_mode == "Treatment Comparison":
        treatment_comparison_page()
    elif assessment_mode == "Multi-Pathogen Assessment":
        multi_pathogen_page()


def batch_scenarios_page():
    """Batch scenarios assessment page."""
    st.markdown('<div class="sub-header">📋 Batch Scenario Processing</div>', unsafe_allow_html=True)

    st.markdown("""
    Run multiple pre-configured scenarios using **three simple data files**:
    - 🌊 **Dilution Data**: Time, Location, Dilution_Factor (empirical from hydrodynamic models)
    - 🦠 **Pathogen Data**: Hockey Stick distribution (X₀, X₅₀, X₁₀₀, P) parameters
    - 📋 **Scenarios**: All scenario parameters (references Location & Pathogen_ID)

    **Key Feature**: Hockey Stick Distribution (McBride 2009)
    - Realistic right-skewed distribution for environmental pathogens
    - P parameter controls tail behavior (default 0.95 for 95th percentile breakpoint)
    - Empirical ECDF for dilution factors from actual modeling output

    **Benefits**: Simple, straightforward, empirical distributions with statistical rigor
    """)

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📁 Input Data", "▶️ Run Assessment", "📊 Results & Reports"])

    with tab1:
        st.markdown("#### Upload Data Files or Use Example Data")

        use_example = st.checkbox("Use example data (15 pre-configured scenarios)", value=True)

        if use_example:
            st.success("✓ Using example data files from `input_data/`")

            dilution_file = "../input_data/dilution_data.csv"
            pathogen_file = "../input_data/pathogen_data.csv"
            scenario_file = "../input_data/scenarios.csv"

            # Show previews in columns
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("**Dilution Data**")
                st.caption("Time-series from models")
                if Path(dilution_file).exists():
                    df_dil = pd.read_csv(dilution_file)
                    st.dataframe(df_dil[['Time', 'Location', 'Dilution_Factor']].head(5),
                               use_container_width=True, height=200)
                    st.caption(f"{len(df_dil)} records, {df_dil['Location'].nunique()} locations")

            with col2:
                st.markdown("**Pathogen Data**")
                st.caption("Hockey Stick parameters (X0, X50, X100, P)")
                if Path(pathogen_file).exists():
                    df_path = pd.read_csv(pathogen_file)
                    cols_to_show = ['Pathogen_ID', 'Pathogen_Type', 'Median_Concentration', 'P_Breakpoint'] \
                                   if 'P_Breakpoint' in df_path.columns \
                                   else ['Pathogen_ID', 'Pathogen_Type', 'Median_Concentration']
                    st.dataframe(df_path[cols_to_show].head(5),
                               use_container_width=True, height=200)
                    st.caption(f"{len(df_path)} pathogens")

            with col3:
                st.markdown("**Scenarios**")
                st.caption("All scenario parameters")
                if Path(scenario_file).exists():
                    df_scen = pd.read_csv(scenario_file)
                    st.dataframe(df_scen[['Scenario_ID', 'Scenario_Name', 'Pathogen_ID', 'Location']].head(5),
                               use_container_width=True, height=200)
                    st.caption(f"{len(df_scen)} scenarios")

        else:
            st.info("Upload all three library files:")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("**1. Dilution Data**")
                st.caption("Time, Location, Dilution_Factor")
                dilution_upload = st.file_uploader("Upload dilution_data.csv", type=['csv'], key='dilution')
                if dilution_upload:
                    dilution_file = save_uploaded_file(dilution_upload)
                    df_dil = pd.read_csv(dilution_file)
                    st.success(f"✓ {len(df_dil)} records")
                else:
                    dilution_file = None

            with col2:
                st.markdown("**2. Pathogen Data**")
                st.caption("Hockey Stick (Min, Median, Max)")
                pathogen_upload = st.file_uploader("Upload pathogen_data.csv", type=['csv'], key='pathogen')
                if pathogen_upload:
                    pathogen_file = save_uploaded_file(pathogen_upload)
                    df_path = pd.read_csv(pathogen_file)
                    st.success(f"✓ {len(df_path)} pathogens")
                else:
                    pathogen_file = None

            with col3:
                st.markdown("**3. Scenarios**")
                st.caption("All parameters")
                scenario_upload = st.file_uploader("Upload scenarios.csv", type=['csv'], key='scenarios')
                if scenario_upload:
                    scenario_file = save_uploaded_file(scenario_upload)
                    df_scen = pd.read_csv(scenario_file)
                    st.success(f"✓ {len(df_scen)} scenarios")
                else:
                    scenario_file = None

        # Help section
        with st.expander("📖 File Format Guide"):
            st.markdown("""
            ### Required Files:

            **1. dilution_data.csv** (3 columns only)
            - `Time` - Date/time of observation
            - `Location` - Site identifier (Site_A, Site_B, etc.)
            - `Dilution_Factor` - Dilution value from hydrodynamic model

            **2. pathogen_data.csv** (7 columns - Hockey Stick parameters)
            Hockey Stick Distribution (McBride 2009) with three sections:
            - Section 1 (X₀ to X₅₀): Linear increase, area = 0.5
            - Section 2 (X₅₀ to X_P): Linear continuation, area = P - 0.5
            - Section 3 (X_P to X₁₀₀): Linear decrease, area = 1 - P

            **Columns:**
            - `Pathogen_ID` - Unique ID (PATH001, PATH002, ...)
            - `Pathogen_Name` - Descriptive name
            - `Pathogen_Type` - **norovirus** (validated), or campylobacter, cryptosporidium, e_coli, rotavirus, salmonella (research mode)
            - `Min_Concentration` - Minimum concentration X₀ (copies/L)
            - `Median_Concentration` - Median concentration X₅₀ (copies/L)
            - `Max_Concentration` - Maximum concentration X₁₀₀ (copies/L)
            - `P_Breakpoint` - Percentile breakpoint as proportion (0-1, default 0.95 for 95th percentile)

            **3. scenarios.csv** (All scenario parameters)

            **Required columns:**
            - `Scenario_ID`, `Scenario_Name`, `Pathogen_ID`, `Location`, `Exposure_Route`
            - `Treatment_LRV`, `Treatment_LRV_Uncertainty`
            - `Ingestion_Volume_mL`, `Volume_Min_mL`, `Volume_Max_mL`
            - `Exposure_Frequency_per_Year`, `Exposed_Population`, `Monte_Carlo_Iterations`
            - `Priority`, `Notes`

            **Optional columns (exposure-specific parameters):**
            - `MHF` - Method Harmonisation Factor (default 1.0; use 18.5 for shellfish to account for bioaccumulation)
            - **For shellfish exposure:**
              - `BAF_Mean`, `BAF_SD`, `BAF_Min`, `BAF_Max` - Bioaccumulation Factor parameters
              - `Meal_Size_Min`, `Meal_Size_Max` - Meal size bounds (grams)
              - `Shellfish_Alpha`, `Shellfish_Beta`, `Shellfish_Gamma` - Log-logistic distribution parameters
            - **For swimming exposure:**
              - `Swim_Rate_Mean`, `Swim_Rate_SD` - Water ingestion rate (mL/hour)
              - `Swim_Rate_Min`, `Swim_Rate_Max` - Rate bounds
              - `Swim_Duration_Min`, `Swim_Duration_Mode`, `Swim_Duration_Max` - Duration (hours)

            **Key Points**:
            - Dilution uses Empirical CDF (ECDF) from all Location data automatically
            - Pathogen uses Hockey Stick distribution (specify X₀, X₅₀, X₁₀₀, P)
            - P (breakpoint percentile) determines distribution shape (0.90-0.99 typical)
            - Scenarios reference Location (not Dilution_ID) and Pathogen_ID
            - Default P=0.95 if column omitted (backwards compatible)
            - MHF adjusts concentration: adjusted_conc = original_conc × MHF
            - Exposure_Route options: 'primary_contact', 'shellfish_consumption', 'contaminated_water'
            """)

    with tab2:
        st.markdown("#### Run Batch Assessment")

        if 'scenario_file' in locals() and scenario_file and 'dilution_file' in locals() and dilution_file and 'pathogen_file' in locals() and pathogen_file:
            # Check all files are valid
            all_files_ready = all([
                scenario_file and Path(scenario_file).exists(),
                dilution_file and Path(dilution_file).exists(),
                pathogen_file and Path(pathogen_file).exists()
            ])

            if all_files_ready:
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown("**Settings:**")
                    output_name = st.text_input("Output filename (without extension):",
                                               value=f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}")

                    iterations = st.slider("Monte Carlo iterations:", 1000, 50000, 10000, 1000)

                with col2:
                    st.markdown("**Actions:**")
                    if st.button("🚀 Run Batch Assessment", type="primary", use_container_width=True):
                        run_batch_assessment_library(scenario_file, dilution_file, pathogen_file, output_name, iterations)
            else:
                st.warning("⚠️ One or more files are missing. Please check the Input Data tab.")

        else:
            st.warning("⚠️ Please provide all three library files in the Input Data tab")

    with tab3:
        display_results_and_reports()


def spatial_assessment_page():
    """Spatial assessment page."""
    st.markdown('<div class="sub-header">🗺️ Spatial Risk Assessment</div>', unsafe_allow_html=True)

    st.markdown("Evaluate risk across multiple sites with different dilution factors from hydrodynamic modeling.")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("#### Input Parameters")

        use_example = st.checkbox("Use example dilution data (6 sites)", value=True)

        if use_example:
            dilution_file = "../input_data/dilution_data/spatial_dilution_6_sites.csv"
        else:
            uploaded = st.file_uploader("Upload dilution CSV", type=['csv'])
            dilution_file = save_uploaded_file(uploaded) if uploaded else None

        pathogen = st.selectbox("Pathogen:", available_pathogens)

        col_a, col_b = st.columns(2)
        with col_a:
            concentration = st.number_input("Effluent concentration (org/L):",
                                          value=1e6, format="%.2e")
            treatment_lrv = st.number_input("Treatment LRV:", value=3.0, step=0.1)

        with col_b:
            volume = st.number_input("Ingestion volume (mL):", value=50.0)
            frequency = st.number_input("Frequency (events/year):", value=25)

        population = st.number_input("Population:", value=15000)
        iterations = st.slider("Monte Carlo iterations:", 1000, 50000, 10000, 1000)

    with col2:
        st.markdown("#### Exposure Route & Parameters")
        exposure_route = st.radio("Route:", ["primary_contact", "shellfish_consumption", "contaminated_water"])

        mhf = st.number_input(
            "MHF (Method Harmonisation Factor):",
            value=1.0,
            min_value=0.1,
            max_value=100.0,
            step=0.1,
            help="Conversion factor between measurement methods (1.0 for water, 18.5 for shellfish)"
        )

        st.markdown("#### Output")
        output_name = st.text_input("Filename:", value="spatial_results")

        if st.button("🚀 Run Spatial Assessment", type="primary", use_container_width=True):
            if dilution_file and Path(dilution_file).exists():
                run_spatial_assessment(
                    dilution_file, pathogen, concentration, exposure_route,
                    volume, frequency, population, treatment_lrv, iterations, output_name
                )
            else:
                st.error("Please provide dilution data file")

    # Results section
    st.markdown("---")
    display_results_and_reports()


def temporal_assessment_page():
    """Temporal assessment page."""
    st.markdown('<div class="sub-header">📅 Temporal Risk Assessment</div>', unsafe_allow_html=True)

    st.markdown("Analyze risk trends over time using pathogen monitoring data.")

    col1, col2 = st.columns([2, 1])

    with col1:
        use_example = st.checkbox("Use example monitoring data (52 weeks)", value=True)

        if use_example:
            monitoring_file = "../input_data/pathogen_concentrations/weekly_monitoring_2024.csv"
        else:
            uploaded = st.file_uploader("Upload monitoring CSV", type=['csv'])
            monitoring_file = save_uploaded_file(uploaded) if uploaded else None

        pathogen = st.selectbox("Pathogen:", available_pathogens)

        col_a, col_b = st.columns(2)
        with col_a:
            treatment_lrv = st.number_input("Treatment LRV:", value=3.0, step=0.1)
            dilution = st.number_input("Dilution factor:", value=100.0)
            volume = st.number_input("Ingestion volume (mL):", value=50.0)

        with col_b:
            frequency = st.number_input("Frequency (events/year):", value=20)
            population = st.number_input("Population:", value=10000)
            iterations = st.slider("Iterations:", 1000, 50000, 10000, 1000)

    with col2:
        exposure_route = st.radio("Exposure route:", ["primary_contact", "shellfish_consumption", "contaminated_water"])

        mhf = st.number_input(
            "MHF (Measurement Harmonisation Factor):",
            value=1.0,
            min_value=0.1,
            max_value=100.0,
            step=0.1,
            help="Conversion between measurement methods"
        )

        output_name = st.text_input("Output filename:", value="temporal_results")

        if st.button("🚀 Run Temporal Assessment", type="primary", use_container_width=True):
            if monitoring_file and Path(monitoring_file).exists():
                run_temporal_assessment(
                    monitoring_file, pathogen, exposure_route, treatment_lrv,
                    dilution, volume, frequency, population, iterations, output_name
                )
            else:
                st.error("Please provide monitoring data file")

    st.markdown("---")
    display_results_and_reports()


def treatment_comparison_page():
    """Treatment comparison page."""
    st.markdown('<div class="sub-header">⚙️ Treatment Scenario Comparison</div>', unsafe_allow_html=True)

    st.markdown("Compare multiple treatment technologies and configurations.")

    # Get available treatment files
    treatment_dir = Path("input_data/treatment_scenarios")
    if treatment_dir.exists():
        treatment_files = list(treatment_dir.glob("*.yaml"))
        treatment_names = [f.stem.replace('_', ' ').title() for f in treatment_files]
    else:
        treatment_files = []
        treatment_names = []

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("#### Select Treatment Scenarios")

        if treatment_files:
            selected = st.multiselect(
                "Choose scenarios to compare:",
                treatment_names,
                default=treatment_names[:3] if len(treatment_names) >= 3 else treatment_names
            )

            selected_files = [treatment_files[treatment_names.index(s)] for s in selected]

            st.info(f"Selected {len(selected)} treatment scenarios for comparison")
        else:
            st.error("No treatment scenario files found in input_data/treatment_scenarios/")
            selected_files = []

        st.markdown("#### Assessment Parameters")
        col_a, col_b = st.columns(2)

        with col_a:
            pathogen = st.selectbox("Pathogen:", available_pathogens)
            raw_conc = st.number_input("Raw concentration (org/L):", value=1e6, format="%.2e")
            dilution = st.number_input("Dilution factor:", value=100.0)

        with col_b:
            volume = st.number_input("Volume (mL):", value=50.0)
            frequency = st.number_input("Frequency/year:", value=20)
            population = st.number_input("Population:", value=10000)

    with col2:
        exposure_route = st.radio("Exposure:", ["primary_contact", "shellfish_consumption", "contaminated_water"])

        mhf = st.number_input(
            "MHF:",
            value=1.0,
            min_value=0.1,
            max_value=100.0,
            step=0.1,
            help="Method Harmonisation Factor"
        )

        iterations = st.slider("Iterations:", 1000, 50000, 10000, 1000)
        output_name = st.text_input("Output:", value="treatment_comparison")

        if st.button("🚀 Run Comparison", type="primary", use_container_width=True):
            if selected_files:
                run_treatment_comparison(
                    selected_files, pathogen, raw_conc, dilution, exposure_route,
                    volume, frequency, population, iterations, output_name
                )
            else:
                st.error("Please select at least one treatment scenario")

    st.markdown("---")
    display_results_and_reports()


def multi_pathogen_page():
    """Multi-pathogen assessment page."""
    st.markdown('<div class="sub-header">🦠 Multi-Pathogen Assessment</div>', unsafe_allow_html=True)

    st.markdown("Evaluate multiple pathogens simultaneously to identify highest risk organisms.")

    col1, col2 = st.columns([2, 1])

    with col1:
        use_example = st.checkbox("Use example data (6 pathogens)", value=True)

        if use_example:
            conc_file = "../input_data/pathogen_concentrations/multi_pathogen_data.csv"
        else:
            uploaded = st.file_uploader("Upload pathogen concentration CSV", type=['csv'])
            conc_file = save_uploaded_file(uploaded) if uploaded else None

        pathogens = st.multiselect(
            "Select pathogens to assess:",
            available_pathogens,
            default=["norovirus"] if production_mode else ["norovirus", "campylobacter", "cryptosporidium"]
        )

        col_a, col_b = st.columns(2)
        with col_a:
            treatment_lrv = st.number_input("Treatment LRV:", value=3.0, step=0.1)
            dilution = st.number_input("Dilution factor:", value=100.0)
            volume = st.number_input("Volume (mL):", value=50.0)

        with col_b:
            frequency = st.number_input("Frequency/year:", value=20)
            population = st.number_input("Population:", value=10000)
            iterations = st.slider("Iterations:", 1000, 50000, 10000, 1000)

    with col2:
        exposure_route = st.radio("Exposure:", ["primary_contact", "shellfish_consumption", "contaminated_water"])

        mhf = st.number_input(
            "MHF:",
            value=1.0,
            min_value=0.1,
            max_value=100.0,
            step=0.1,
            help="Method Harmonisation Factor"
        )

        output_name = st.text_input("Output:", value="multi_pathogen_results")

        if st.button("🚀 Run Multi-Pathogen Assessment", type="primary", use_container_width=True):
            if conc_file and Path(conc_file).exists() and pathogens:
                run_multi_pathogen_assessment(
                    conc_file, pathogens, exposure_route, treatment_lrv,
                    dilution, volume, frequency, population, iterations, output_name
                )
            else:
                st.error("Please provide concentration file and select pathogens")

    st.markdown("---")
    display_results_and_reports()


# Processing functions
def run_batch_assessment_library(scenario_file, dilution_file, pathogen_file, output_name, iterations):
    """Run batch scenario assessment using library-based approach."""
    with st.spinner("🔄 Processing batch scenarios from libraries..."):
        try:
            processor = BatchProcessor(output_dir='outputs/results')

            # Run using simplified three-file method
            results = processor.run_batch_scenarios_from_libraries(
                scenarios_file=scenario_file,
                dilution_data_file=dilution_file,
                pathogen_data_file=pathogen_file,
                output_dir='outputs/results'
            )

            output_csv = "outputs/results/batch_scenarios_results.csv"

            st.session_state['last_results'] = output_csv
            st.session_state['last_assessment'] = 'batch'

            st.success("✅ Batch assessment complete!")
            st.balloons()

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            import traceback
            st.code(traceback.format_exc())


def run_batch_assessment(scenario_file, output_name, iterations):
    """Run batch scenario assessment (legacy single-file method)."""
    with st.spinner("🔄 Processing batch scenarios..."):
        try:
            processor = BatchProcessor(output_dir='outputs/results')

            results = processor.run_batch_scenarios(
                scenario_file=scenario_file,
                output_dir='outputs/results'
            )

            output_csv = f"outputs/results/batch_scenarios_results.csv"

            st.session_state['last_results'] = output_csv
            st.session_state['last_assessment'] = 'batch'

            st.success("✅ Batch assessment complete!")
            st.balloons()

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            import traceback
            st.code(traceback.format_exc())


def run_spatial_assessment(dilution_file, pathogen, concentration, exposure_route,
                           volume, frequency, population, treatment_lrv, iterations, output_name):
    """Run spatial assessment."""
    with st.spinner("🔄 Processing spatial assessment..."):
        try:
            processor = BatchProcessor(output_dir='outputs/results')

            results = processor.run_spatial_assessment(
                dilution_file=dilution_file,
                pathogen=pathogen,
                effluent_concentration=concentration,
                exposure_route=exposure_route,
                volume_ml=volume,
                frequency_per_year=frequency,
                population=population,
                treatment_lrv=treatment_lrv,
                iterations=iterations,
                output_file=f"{output_name}.csv"
            )

            st.session_state['last_results'] = f"outputs/results/{output_name}.csv"
            st.session_state['last_assessment'] = 'spatial'

            st.success("✅ Spatial assessment complete!")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def run_temporal_assessment(monitoring_file, pathogen, exposure_route, treatment_lrv,
                            dilution, volume, frequency, population, iterations, output_name):
    """Run temporal assessment."""
    with st.spinner("🔄 Processing temporal assessment..."):
        try:
            processor = BatchProcessor(output_dir='outputs/results')

            results = processor.run_temporal_assessment(
                monitoring_file=monitoring_file,
                pathogen=pathogen,
                concentration_column=None,
                exposure_route=exposure_route,
                treatment_lrv=treatment_lrv,
                dilution_factor=dilution,
                volume_ml=volume,
                frequency_per_year=frequency,
                population=population,
                iterations=iterations,
                output_file=f"{output_name}.csv"
            )

            st.session_state['last_results'] = f"outputs/results/{output_name}.csv"
            st.session_state['last_assessment'] = 'temporal'

            st.success("✅ Temporal assessment complete!")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def run_treatment_comparison(treatment_files, pathogen, raw_conc, dilution, exposure_route,
                             volume, frequency, population, iterations, output_name):
    """Run treatment comparison."""
    with st.spinner("🔄 Comparing treatment scenarios..."):
        try:
            processor = BatchProcessor(output_dir='outputs/results')

            results = processor.run_treatment_comparison(
                treatment_files=treatment_files,
                pathogen=pathogen,
                raw_concentration=raw_conc,
                dilution_factor=dilution,
                exposure_route=exposure_route,
                volume_ml=volume,
                frequency_per_year=frequency,
                population=population,
                iterations=iterations,
                output_file=f"{output_name}.csv"
            )

            st.session_state['last_results'] = f"outputs/results/{output_name}.csv"
            st.session_state['last_assessment'] = 'treatment'

            st.success("✅ Treatment comparison complete!")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def run_multi_pathogen_assessment(conc_file, pathogens, exposure_route, treatment_lrv,
                                  dilution, volume, frequency, population, iterations, output_name):
    """Run multi-pathogen assessment."""
    with st.spinner("🔄 Processing multi-pathogen assessment..."):
        try:
            processor = BatchProcessor(output_dir='outputs/results')

            results = processor.run_multi_pathogen_assessment(
                concentration_file=conc_file,
                pathogens=pathogens,
                exposure_route=exposure_route,
                treatment_lrv=treatment_lrv,
                dilution_factor=dilution,
                volume_ml=volume,
                frequency_per_year=frequency,
                population=population,
                iterations=iterations,
                output_file=f"{output_name}.csv"
            )

            st.session_state['last_results'] = f"outputs/results/{output_name}.csv"
            st.session_state['last_assessment'] = 'multi_pathogen'

            st.success("✅ Multi-pathogen assessment complete!")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def display_results_and_reports():
    """Display results and generate reports."""
    if 'last_results' in st.session_state:
        results_file = st.session_state['last_results']

        if Path(results_file).exists():
            st.markdown("### 📊 Results")

            df = pd.read_csv(results_file)

            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Scenarios", len(df))

            with col2:
                if 'Compliance_Status' in df.columns:
                    compliant = len(df[df['Compliance_Status'] == 'COMPLIANT'])
                    st.metric("Compliant", compliant, f"{compliant/len(df)*100:.1f}%")
                else:
                    st.metric("Compliant", "N/A")

            with col3:
                if 'Annual_Risk_Median' in df.columns:
                    avg_risk = df['Annual_Risk_Median'].mean()
                    st.metric("Avg Risk", f"{avg_risk:.2e}")
                else:
                    st.metric("Avg Risk", "N/A")

            with col4:
                if 'Population_Impact' in df.columns:
                    total_impact = df['Population_Impact'].sum()
                    st.metric("Total Impact", f"{int(total_impact):,}")
                else:
                    st.metric("Total Impact", "N/A")

            # Interactive data table
            st.markdown("#### Detailed Results")
            st.dataframe(df, use_container_width=True, height=300)

            # Create visualizations
            st.markdown("#### 📊 Visualizations")

            # Create tabs for different plots
            plot_tabs = st.tabs(["Risk Overview", "Compliance Distribution", "Risk Distribution", "Population Impact"])

            plots = {}  # Store plots for download

            with plot_tabs[0]:
                fig1 = create_risk_overview_plot(df)
                st.pyplot(fig1)
                plots['risk_overview'] = fig1

            with plot_tabs[1]:
                fig2 = create_compliance_plot(df)
                st.pyplot(fig2)
                plots['compliance_distribution'] = fig2

            with plot_tabs[2]:
                fig3 = create_risk_distribution_plot(df)
                st.pyplot(fig3)
                plots['risk_distribution'] = fig3

            with plot_tabs[3]:
                fig4 = create_population_impact_plot(df)
                st.pyplot(fig4)
                plots['population_impact'] = fig4

            # Download section with expandable options
            st.markdown("---")
            st.markdown("### 📥 Download Results")

            # Main download buttons row
            col1, col2, col3 = st.columns(3)

            with col1:
                # CSV download
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📄 Download Full CSV",
                    data=csv,
                    file_name=f"{Path(results_file).stem}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            with col2:
                # PDF report
                if st.button("📑 Generate PDF Report", use_container_width=True):
                    generate_pdf_report(results_file, df, plots)

            with col3:
                # Download all bundle
                st.download_button(
                    label="📦 Download All (ZIP)",
                    data=create_zip_bundle(df, plots, results_file),
                    file_name=f"{Path(results_file).stem}_complete_package.zip",
                    mime="application/zip",
                    use_container_width=True
                )

            # Expandable sections for individual downloads
            with st.expander("📊 Download Individual Plots"):
                st.markdown("**Download plots as high-resolution PNG files:**")

                plot_col1, plot_col2 = st.columns(2)

                with plot_col1:
                    st.download_button(
                        "🔹 Risk Overview Plot",
                        data=fig_to_bytes(plots['risk_overview']),
                        file_name="risk_overview.png",
                        mime="image/png",
                        use_container_width=True
                    )

                    st.download_button(
                        "🔹 Compliance Distribution",
                        data=fig_to_bytes(plots['compliance_distribution']),
                        file_name="compliance_distribution.png",
                        mime="image/png",
                        use_container_width=True
                    )

                with plot_col2:
                    st.download_button(
                        "🔹 Risk Distribution",
                        data=fig_to_bytes(plots['risk_distribution']),
                        file_name="risk_distribution.png",
                        mime="image/png",
                        use_container_width=True
                    )

                    st.download_button(
                        "🔹 Population Impact",
                        data=fig_to_bytes(plots['population_impact']),
                        file_name="population_impact.png",
                        mime="image/png",
                        use_container_width=True
                    )

            with st.expander("📋 Download Individual Tables"):
                st.markdown("**Download data subsets as CSV or Excel:**")

                table_col1, table_col2 = st.columns(2)

                with table_col1:
                    # High risk scenarios only (if Risk_Classification exists)
                    if 'Risk_Classification' in df.columns:
                        high_risk_df = df[df['Risk_Classification'].isin(['High', 'Medium'])]
                        if len(high_risk_df) > 0:
                            st.download_button(
                                "🔸 High-Risk Scenarios CSV",
                                data=high_risk_df.to_csv(index=False),
                                file_name="high_risk_scenarios.csv",
                                mime="text/csv",
                                use_container_width=True
                            )

                    # Compliant scenarios only
                    if 'Compliance_Status' in df.columns:
                        compliant_df = df[df['Compliance_Status'] == 'COMPLIANT']
                        if len(compliant_df) > 0:
                            st.download_button(
                                "🔸 Compliant Scenarios CSV",
                                data=compliant_df.to_csv(index=False),
                                file_name="compliant_scenarios.csv",
                                mime="text/csv",
                                use_container_width=True
                            )

                    # Summary statistics
                    summary_df = create_summary_statistics(df)
                    st.download_button(
                        "🔸 Summary Statistics CSV",
                        data=summary_df.to_csv(index=True),
                        file_name="summary_statistics.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

                with table_col2:
                    # Non-compliant scenarios
                    if 'Compliance_Status' in df.columns:
                        non_compliant_df = df[df['Compliance_Status'] == 'NON-COMPLIANT']
                        if len(non_compliant_df) > 0:
                            st.download_button(
                                "🔸 Non-Compliant Scenarios CSV",
                                data=non_compliant_df.to_csv(index=False),
                                file_name="non_compliant_scenarios.csv",
                                mime="text/csv",
                                use_container_width=True
                            )

                    # Top 10 highest risk
                    if 'Annual_Risk_Median' in df.columns:
                        top_risk_df = df.nlargest(10, 'Annual_Risk_Median')
                        st.download_button(
                            "🔸 Top 10 Highest Risk CSV",
                            data=top_risk_df.to_csv(index=False),
                            file_name="top_10_highest_risk.csv",
                            mime="text/csv",
                            use_container_width=True
                        )

                    # Excel format (full results)
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        df.to_excel(writer, sheet_name='All Results', index=False)
                        summary_df.to_excel(writer, sheet_name='Summary Statistics')
                        if 'Risk_Classification' in df.columns:
                            high_risk_df = df[df['Risk_Classification'].isin(['High', 'Medium'])]
                            if len(high_risk_df) > 0:
                                high_risk_df.to_excel(writer, sheet_name='High Risk', index=False)

                    st.download_button(
                        "🔸 Full Results Excel",
                        data=excel_buffer.getvalue(),
                        file_name="qmra_results_full.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )

    else:
        st.info("👆 Run an assessment to see results here")


def generate_pdf_report(csv_file, df, plots=None):
    """Generate and download PDF report."""
    with st.spinner("📑 Generating comprehensive PDF report..."):
        try:
            pdf_file = csv_file.replace('.csv', '_report.pdf')

            generator = QMRAPDFReportGenerator()
            generator.generate_report(df, pdf_file, "QMRA Batch Assessment Report", plots=plots)

            # Read PDF and provide download
            with open(pdf_file, 'rb') as f:
                pdf_data = f.read()

            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_data,
                file_name=Path(pdf_file).name,
                mime="application/pdf",
                use_container_width=True
            )

            st.success(f"✅ PDF report generated: {Path(pdf_file).name}")

        except Exception as e:
            st.error(f"❌ Error generating PDF: {str(e)}")
            import traceback
            st.code(traceback.format_exc())


def save_uploaded_file(uploaded_file):
    """Save uploaded file to temp directory."""
    if uploaded_file:
        temp_dir = Path("temp_uploads")
        temp_dir.mkdir(exist_ok=True)

        file_path = temp_dir / uploaded_file.name
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getvalue())

        return str(file_path)
    return None


if __name__ == '__main__':
    main()
