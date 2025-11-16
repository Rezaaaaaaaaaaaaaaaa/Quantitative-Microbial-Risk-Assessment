#!/usr/bin/env python3
"""
PDF Report Generator for QMRA Batch Processing
==============================================

Generates comprehensive PDF reports with visualizations and analysis.

Author: NIWA Earth Sciences New Zealand
Date: October 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
import io


class QMRAPDFReportGenerator:
    """Generate comprehensive PDF reports for QMRA batch assessments."""

    def __init__(self):
        """Initialize PDF report generator."""
        self.colors = {
            'compliant': '#28a745',
            'non_compliant': '#dc3545',
            'high': '#dc3545',
            'medium': '#ffc107',
            'low': '#28a745',
            'negligible': '#17a2b8'
        }

    def generate_report(self, results_df, output_file, report_title="QMRA Batch Assessment Report", plots=None):
        """
        Generate comprehensive PDF report from batch results.

        Parameters:
        -----------
        results_df : pd.DataFrame
            Results from batch processing
        output_file : str
            Output PDF filename
        report_title : str
            Title for the report
        plots : dict, optional
            Dictionary of pre-generated matplotlib figures from web app
            Expected keys: 'risk_overview', 'compliance_distribution',
                          'risk_distribution', 'population_impact'
        """
        # Create PDF
        with PdfPages(output_file) as pdf:
            # Page 1: Title page
            self._add_title_page(pdf, report_title, results_df)

            # Page 2: Executive summary
            self._add_executive_summary(pdf, results_df)

            # Page 3: Risk overview chart (use web app plot if available)
            if plots and 'risk_overview' in plots:
                self._add_pregenerated_plot(pdf, plots['risk_overview'], 'Risk Overview')
            else:
                self._add_risk_overview_chart(pdf, results_df)

            # Page 4: Compliance status (use web app plot if available)
            if plots and 'compliance_distribution' in plots:
                self._add_pregenerated_plot(pdf, plots['compliance_distribution'], 'Compliance Status')
            else:
                self._add_compliance_chart(pdf, results_df)

            # Page 5: Risk distribution (use web app plot if available)
            if plots and 'risk_distribution' in plots:
                self._add_pregenerated_plot(pdf, plots['risk_distribution'], 'Risk Distribution')
            else:
                self._add_priority_analysis(pdf, results_df)

            # Page 6: Population impact (use web app plot if available)
            if plots and 'population_impact' in plots:
                self._add_pregenerated_plot(pdf, plots['population_impact'], 'Population Impact')

            # Page 7: Treatment comparison (if multiple treatments)
            if 'Treatment_LRV' in results_df.columns:
                self._add_treatment_comparison(pdf, results_df)

            # Page 8: Pathogen comparison (if multiple pathogens)
            if len(results_df['Pathogen'].unique()) > 1:
                self._add_pathogen_comparison(pdf, results_df)

            # Page 9: Detailed results table
            self._add_detailed_table(pdf, results_df)

            # Page 10: Recommendations
            self._add_recommendations(pdf, results_df)

            # Add metadata
            d = pdf.infodict()
            d['Title'] = report_title
            d['Author'] = 'NIWA QMRA Toolkit'
            d['Subject'] = 'Quantitative Microbial Risk Assessment - Batch Results'
            d['CreationDate'] = datetime.now()

        print(f"PDF report generated: {output_file}")

    def _add_pregenerated_plot(self, pdf, fig, title):
        """
        Add a pre-generated matplotlib figure to the PDF.

        Parameters:
        -----------
        pdf : PdfPages
            PDF file object
        fig : matplotlib.figure.Figure
            Pre-generated matplotlib figure from web app
        title : str
            Title for the page (optional, as figure may have its own title)
        """
        # Save the figure to PDF as-is
        pdf.savefig(fig, bbox_inches='tight')

    def _add_title_page(self, pdf, title, results_df):
        """Add title page."""
        fig = plt.figure(figsize=(8.5, 11))
        ax = fig.add_subplot(111)
        ax.axis('off')

        # Title
        ax.text(0.5, 0.7, title,
                ha='center', va='center', fontsize=24, fontweight='bold')

        # Subtitle
        ax.text(0.5, 0.62, 'Comprehensive Risk Assessment Results',
                ha='center', va='center', fontsize=16, color='gray')

        # Summary box
        n_scenarios = len(results_df)
        n_compliant = len(results_df[results_df['Compliance_Status'] == 'COMPLIANT'])
        n_non_compliant = n_scenarios - n_compliant

        summary_text = f"""
        Assessment Summary

        Total Scenarios: {n_scenarios}
        Compliant: {n_compliant} ({n_compliant/n_scenarios*100:.1f}%)
        Non-Compliant: {n_non_compliant} ({n_non_compliant/n_scenarios*100:.1f}%)

        Date: {datetime.now().strftime('%B %d, %Y')}
        """

        ax.text(0.5, 0.4, summary_text,
                ha='center', va='center', fontsize=12,
                bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))

        # Footer
        ax.text(0.5, 0.1, 'NIWA Earth Sciences New Zealand\nQMRA Toolkit v1.0',
                ha='center', va='center', fontsize=10, color='gray', style='italic')

        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _add_executive_summary(self, pdf, results_df):
        """Add executive summary page."""
        fig = plt.figure(figsize=(8.5, 11))
        ax = fig.add_subplot(111)
        ax.axis('off')

        # Title
        ax.text(0.5, 0.95, 'Executive Summary',
                ha='center', va='top', fontsize=18, fontweight='bold')

        # Key findings
        y_pos = 0.85

        # Overall statistics
        stats_text = "Overall Assessment Statistics\n" + "="*50
        ax.text(0.1, y_pos, stats_text, fontsize=12, fontweight='bold', family='monospace')
        y_pos -= 0.05

        n_scenarios = len(results_df)
        n_compliant = len(results_df[results_df['Compliance_Status'] == 'COMPLIANT'])
        avg_risk = results_df['Annual_Risk_Median'].mean()
        max_risk = results_df['Annual_Risk_Median'].max()
        total_impact = results_df['Population_Impact'].sum()

        stats = f"""
Total Scenarios Assessed: {n_scenarios}
Compliance Rate: {n_compliant/n_scenarios*100:.1f}% ({n_compliant}/{n_scenarios})
Average Annual Risk: {avg_risk:.2e}
Maximum Annual Risk: {max_risk:.2e}
Total Predicted Illnesses: {int(total_impact):,}
        """
        ax.text(0.1, y_pos, stats, fontsize=10, family='monospace', va='top')
        y_pos -= 0.2

        # High risk scenarios
        ax.text(0.1, y_pos, '\nHigh Risk Scenarios (Top 5)', fontsize=12, fontweight='bold')
        y_pos -= 0.05

        top_5 = results_df.nlargest(5, 'Annual_Risk_Median')[['Scenario_Name', 'Annual_Risk_Median', 'Population_Impact']]
        for idx, row in top_5.iterrows():
            scenario_text = f"  {row['Scenario_Name'][:40]:45s} Risk: {row['Annual_Risk_Median']:.2e}  Impact: {int(row['Population_Impact']):,}"
            ax.text(0.1, y_pos, scenario_text, fontsize=9, family='monospace')
            y_pos -= 0.04

        y_pos -= 0.05

        # Compliant scenarios
        compliant = results_df[results_df['Compliance_Status'] == 'COMPLIANT']
        if len(compliant) > 0:
            ax.text(0.1, y_pos, '\nCompliant Scenarios', fontsize=12, fontweight='bold')
            y_pos -= 0.05
            for idx, row in compliant.iterrows():
                scenario_text = f"  {row['Scenario_Name'][:45]:45s} Risk: {row['Annual_Risk_Median']:.2e}"
                ax.text(0.1, y_pos, scenario_text, fontsize=9, family='monospace')
                y_pos -= 0.04
        else:
            ax.text(0.1, y_pos, '\nNo Compliant Scenarios', fontsize=12, fontweight='bold', color='red')
            y_pos -= 0.05
            ax.text(0.1, y_pos, 'All assessed scenarios exceed WHO risk thresholds.\nImmediate action required.',
                   fontsize=10, color='red')

        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _add_risk_overview_chart(self, pdf, results_df):
        """Add risk overview bar chart."""
        fig, ax = plt.subplots(figsize=(11, 8.5))

        # Sort by risk
        df_sorted = results_df.sort_values('Annual_Risk_Median', ascending=True)

        # Create colors based on compliance
        colors = [self.colors['compliant'] if status == 'COMPLIANT' else self.colors['non_compliant']
                  for status in df_sorted['Compliance_Status']]

        # Create horizontal bar chart
        y_pos = np.arange(len(df_sorted))
        ax.barh(y_pos, df_sorted['Annual_Risk_Median'], color=colors, alpha=0.7, edgecolor='black')

        # Customize
        ax.set_yticks(y_pos)
        ax.set_yticklabels(df_sorted['Scenario_Name'], fontsize=8)
        ax.set_xlabel('Annual Infection Risk (Median)', fontsize=12, fontweight='bold')
        ax.set_title('Risk Assessment Overview - All Scenarios', fontsize=14, fontweight='bold', pad=20)

        # Add WHO threshold line
        ax.axvline(x=1e-4, color='orange', linestyle='--', linewidth=2, label='WHO Threshold (10⁻⁴)')

        # Log scale
        ax.set_xscale('log')
        ax.grid(True, alpha=0.3, axis='x')

        # Legend
        compliant_patch = mpatches.Patch(color=self.colors['compliant'], label='Compliant', alpha=0.7)
        non_compliant_patch = mpatches.Patch(color=self.colors['non_compliant'], label='Non-Compliant', alpha=0.7)
        ax.legend(handles=[compliant_patch, non_compliant_patch], loc='lower right', fontsize=10)

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _add_compliance_chart(self, pdf, results_df):
        """Add compliance status pie chart."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 8.5))

        # Compliance pie chart
        compliance_counts = results_df['Compliance_Status'].value_counts()
        colors_compliance = [self.colors['compliant'] if status == 'COMPLIANT' else self.colors['non_compliant']
                           for status in compliance_counts.index]

        wedges, texts, autotexts = ax1.pie(compliance_counts.values,
                                            labels=compliance_counts.index,
                                            autopct='%1.1f%%',
                                            colors=colors_compliance,
                                            startangle=90,
                                            textprops={'fontsize': 12})

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        ax1.set_title('Compliance Status', fontsize=14, fontweight='bold', pad=20)

        # Priority pie chart
        if 'Priority' in results_df.columns:
            priority_counts = results_df['Priority'].value_counts()
            colors_priority = [self.colors.get(p.lower(), 'gray') for p in priority_counts.index]

            wedges2, texts2, autotexts2 = ax2.pie(priority_counts.values,
                                                   labels=priority_counts.index,
                                                   autopct='%1.1f%%',
                                                   colors=colors_priority,
                                                   startangle=90,
                                                   textprops={'fontsize': 12})

            for autotext in autotexts2:
                autotext.set_color('white')
                autotext.set_fontweight('bold')

            ax2.set_title('Priority Distribution', fontsize=14, fontweight='bold', pad=20)

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _add_priority_analysis(self, pdf, results_df):
        """Add priority-based analysis."""
        fig, ax = plt.subplots(figsize=(11, 8.5))

        if 'Priority' not in results_df.columns:
            ax.text(0.5, 0.5, 'Priority data not available',
                   ha='center', va='center', fontsize=14)
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
            return

        # Group by priority
        priority_order = ['High', 'Medium', 'Low']
        priority_data = []

        for priority in priority_order:
            subset = results_df[results_df['Priority'] == priority]
            if len(subset) > 0:
                priority_data.append({
                    'Priority': priority,
                    'Count': len(subset),
                    'Avg_Risk': subset['Annual_Risk_Median'].mean(),
                    'Total_Impact': subset['Population_Impact'].sum()
                })

        if not priority_data:
            ax.text(0.5, 0.5, 'No priority data', ha='center', va='center')
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
            return

        priority_df = pd.DataFrame(priority_data)

        # Create grouped bar chart
        x = np.arange(len(priority_df))
        width = 0.25

        ax2 = ax.twinx()

        # Plot bars
        bars1 = ax.bar(x - width, priority_df['Count'], width,
                       label='Scenario Count', color='steelblue', alpha=0.7)
        bars2 = ax.bar(x, priority_df['Avg_Risk'], width,
                       label='Avg Annual Risk', color='coral', alpha=0.7)
        bars3 = ax2.bar(x + width, priority_df['Total_Impact'], width,
                        label='Total Impact', color='green', alpha=0.7)

        # Customize
        ax.set_xlabel('Priority Level', fontsize=12, fontweight='bold')
        ax.set_ylabel('Count / Risk', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Total Population Impact', fontsize=12, fontweight='bold')
        ax.set_title('Priority-Based Risk Analysis', fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(priority_df['Priority'])

        # Legends
        ax.legend(loc='upper left', fontsize=10)
        ax2.legend(loc='upper right', fontsize=10)

        ax.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _add_treatment_comparison(self, pdf, results_df):
        """Add treatment effectiveness comparison."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8.5))

        # Group by treatment LRV
        treatment_groups = results_df.groupby('Treatment_LRV').agg({
            'Annual_Risk_Median': 'mean',
            'Population_Impact': 'sum',
            'Scenario_ID': 'count'
        }).reset_index()

        treatment_groups.columns = ['Treatment_LRV', 'Avg_Risk', 'Total_Impact', 'Count']
        treatment_groups = treatment_groups.sort_values('Treatment_LRV')

        # Plot 1: Risk vs Treatment LRV
        ax1.plot(treatment_groups['Treatment_LRV'], treatment_groups['Avg_Risk'],
                marker='o', markersize=10, linewidth=2, color='darkred')
        ax1.set_xlabel('Treatment Log Reduction Value (LRV)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Average Annual Risk', fontsize=12, fontweight='bold')
        ax1.set_title('Treatment Effectiveness - Risk Reduction', fontsize=14, fontweight='bold')
        ax1.axhline(y=1e-4, color='orange', linestyle='--', linewidth=2, label='WHO Threshold')
        ax1.set_yscale('log')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Plot 2: Population impact
        ax2.bar(treatment_groups['Treatment_LRV'].astype(str), treatment_groups['Total_Impact'],
               color='steelblue', alpha=0.7, edgecolor='black')
        ax2.set_xlabel('Treatment LRV', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Total Expected Illnesses', fontsize=12, fontweight='bold')
        ax2.set_title('Treatment Effectiveness - Population Impact', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _add_pathogen_comparison(self, pdf, results_df):
        """Add pathogen comparison chart."""
        fig, ax = plt.subplots(figsize=(11, 8.5))

        # Group by pathogen
        pathogen_groups = results_df.groupby('Pathogen').agg({
            'Annual_Risk_Median': ['mean', 'min', 'max'],
            'Scenario_ID': 'count'
        }).reset_index()

        pathogen_groups.columns = ['Pathogen', 'Avg_Risk', 'Min_Risk', 'Max_Risk', 'Count']
        pathogen_groups = pathogen_groups.sort_values('Avg_Risk', ascending=False)

        # Create bar chart with error bars
        x = np.arange(len(pathogen_groups))
        bars = ax.bar(x, pathogen_groups['Avg_Risk'],
                     color='darkblue', alpha=0.7, edgecolor='black')

        # Add error bars showing range
        errors = [pathogen_groups['Avg_Risk'] - pathogen_groups['Min_Risk'],
                 pathogen_groups['Max_Risk'] - pathogen_groups['Avg_Risk']]
        ax.errorbar(x, pathogen_groups['Avg_Risk'], yerr=errors,
                   fmt='none', ecolor='black', capsize=5, capthick=2)

        # Customize
        ax.set_xlabel('Pathogen', fontsize=12, fontweight='bold')
        ax.set_ylabel('Annual Infection Risk', fontsize=12, fontweight='bold')
        ax.set_title('Pathogen Risk Comparison', fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(pathogen_groups['Pathogen'], rotation=45, ha='right')
        ax.set_yscale('log')

        # Add WHO threshold
        ax.axhline(y=1e-4, color='orange', linestyle='--', linewidth=2, label='WHO Threshold')

        ax.grid(True, alpha=0.3, axis='y')
        ax.legend()

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _add_detailed_table(self, pdf, results_df):
        """Add detailed results table."""
        fig, ax = plt.subplots(figsize=(11, 8.5))
        ax.axis('tight')
        ax.axis('off')

        # Select key columns
        table_cols = ['Scenario_ID', 'Scenario_Name', 'Pathogen', 'Annual_Risk_Median',
                     'Population_Impact', 'Compliance_Status']

        # Filter columns that exist
        table_cols = [col for col in table_cols if col in results_df.columns]
        table_data = results_df[table_cols].copy()

        # Format numbers
        if 'Annual_Risk_Median' in table_data.columns:
            table_data['Annual_Risk_Median'] = table_data['Annual_Risk_Median'].apply(lambda x: f'{x:.2e}')
        if 'Population_Impact' in table_data.columns:
            table_data['Population_Impact'] = table_data['Population_Impact'].apply(lambda x: f'{int(x):,}')

        # Truncate scenario names
        if 'Scenario_Name' in table_data.columns:
            table_data['Scenario_Name'] = table_data['Scenario_Name'].str[:30]

        # Create table
        table = ax.table(cellText=table_data.values,
                        colLabels=table_data.columns,
                        cellLoc='left',
                        loc='center',
                        bbox=[0, 0, 1, 1])

        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 2)

        # Style header
        for i in range(len(table_cols)):
            table[(0, i)].set_facecolor('#4472C4')
            table[(0, i)].set_text_props(weight='bold', color='white')

        # Color rows based on compliance
        for i in range(len(table_data)):
            if 'Compliance_Status' in table_data.columns:
                status = results_df.iloc[i]['Compliance_Status']
                color = '#d4edda' if status == 'COMPLIANT' else '#f8d7da'
                for j in range(len(table_cols)):
                    table[(i+1, j)].set_facecolor(color)

        ax.set_title('Detailed Results Summary', fontsize=14, fontweight='bold', pad=20)

        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _add_recommendations(self, pdf, results_df):
        """Add recommendations page."""
        fig = plt.figure(figsize=(8.5, 11))
        ax = fig.add_subplot(111)
        ax.axis('off')

        # Title
        ax.text(0.5, 0.95, 'Recommendations',
                ha='center', va='top', fontsize=18, fontweight='bold')

        y_pos = 0.88

        # Analyze results and generate recommendations
        non_compliant = results_df[results_df['Compliance_Status'] == 'NON-COMPLIANT']
        high_priority = results_df[results_df.get('Priority', '') == 'High']

        recommendations = []

        if len(non_compliant) > 0:
            recommendations.append(
                f"1. IMMEDIATE ACTION REQUIRED\n"
                f"   {len(non_compliant)} scenarios ({len(non_compliant)/len(results_df)*100:.1f}%) exceed WHO risk thresholds.\n"
                f"   Priority should be given to high-risk, high-population scenarios."
            )

        if len(high_priority) > 0:
            recommendations.append(
                f"\n2. HIGH PRIORITY SCENARIOS\n"
                f"   {len(high_priority)} scenarios require immediate attention.\n"
                f"   Focus on treatment upgrades and improved dilution."
            )

        # Treatment recommendations
        if 'Treatment_LRV' in results_df.columns:
            low_treatment = results_df[results_df['Treatment_LRV'] < 3.0]
            if len(low_treatment) > 0:
                recommendations.append(
                    f"\n3. TREATMENT UPGRADES RECOMMENDED\n"
                    f"   {len(low_treatment)} scenarios have inadequate treatment (LRV < 3.0).\n"
                    f"   Consider UV disinfection (LRV 8.0) or MBR (LRV 9.3) upgrades."
                )

        # Dilution recommendations
        if 'Dilution_Factor' in results_df.columns:
            poor_dilution = results_df[results_df['Dilution_Factor'] < 50]
            if len(poor_dilution) > 0:
                recommendations.append(
                    f"\n4. IMPROVE DILUTION CONDITIONS\n"
                    f"   {len(poor_dilution)} scenarios have poor dilution (< 50x).\n"
                    f"   Review discharge locations and outfall design."
                )

        # Population recommendations
        if 'Population' in results_df.columns and 'Annual_Risk_Median' in results_df.columns:
            high_impact = results_df[results_df['Population_Impact'] > 1000]
            if len(high_impact) > 0:
                recommendations.append(
                    f"\n5. POPULATION EXPOSURE MANAGEMENT\n"
                    f"   {len(high_impact)} scenarios affect > 1,000 people annually.\n"
                    f"   Consider beach closures during high-risk periods."
                )

        # Success stories
        compliant = results_df[results_df['Compliance_Status'] == 'COMPLIANT']
        if len(compliant) > 0:
            recommendations.append(
                f"\n6. SUCCESS CASES\n"
                f"   {len(compliant)} scenario(s) meet WHO guidelines.\n"
                f"   These demonstrate effective risk management strategies."
            )

        # Print recommendations
        for rec in recommendations:
            ax.text(0.1, y_pos, rec, fontsize=10, va='top', family='monospace')
            y_pos -= 0.12

        # Footer
        ax.text(0.5, 0.05,
               'For detailed methodology and guidelines, consult:\n'
               'WHO (2016) QMRA Application for Water Safety Management',
               ha='center', va='bottom', fontsize=8, style='italic', color='gray')

        pdf.savefig(fig, bbox_inches='tight')
        plt.close()


def generate_batch_pdf_report(csv_file, output_pdf=None, title="QMRA Batch Assessment Report", plots=None):
    """
    Convenience function to generate PDF report from CSV file.

    Parameters:
    -----------
    csv_file : str
        Path to batch results CSV file
    output_pdf : str, optional
        Output PDF filename (auto-generated if None)
    title : str
        Report title
    plots : dict, optional
        Dictionary of pre-generated matplotlib figures from web app
    """
    # Read CSV
    results_df = pd.read_csv(csv_file)

    # Generate output filename if not provided
    if output_pdf is None:
        output_pdf = csv_file.replace('.csv', '_report.pdf')

    # Generate report
    generator = QMRAPDFReportGenerator()
    generator.generate_report(results_df, output_pdf, title, plots=plots)

    return output_pdf


if __name__ == '__main__':
    # Test with existing results
    import sys

    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
        output_pdf = sys.argv[2] if len(sys.argv) > 2 else None
        generate_batch_pdf_report(csv_file, output_pdf)
    else:
        print("Usage: python pdf_report_generator.py <results.csv> [output.pdf]")
