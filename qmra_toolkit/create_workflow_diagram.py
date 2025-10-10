#!/usr/bin/env python3
"""
Create QMRA Workflow Diagram for Web Application
Generates a visual flowchart showing analysis routes and report tiers
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

def create_qmra_workflow_diagram():
    """Create comprehensive QMRA workflow diagram."""

    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Colors
    tier1_color = '#E8F5E9'  # Light green
    tier2_color = '#FFF9C4'  # Light yellow
    tier3_color = '#FFE0B2'  # Light orange
    route_color = '#E1F5FE'  # Light blue
    header_color = '#1f4e79'  # NIWA blue

    # Title
    ax.text(8, 11.5, 'NIWA QMRA Toolkit - Analysis Workflow & Report Tiers',
            ha='center', va='top', fontsize=20, weight='bold', color=header_color)

    # === TIER BOXES (Left side) ===

    # Tier 1: Quick Assessment
    tier1_box = FancyBboxPatch((0.5, 8.5), 4.5, 2.3,
                               boxstyle="round,pad=0.1",
                               edgecolor=header_color, facecolor=tier1_color,
                               linewidth=2, zorder=1)
    ax.add_patch(tier1_box)

    ax.text(2.75, 10.5, 'TIER 1: Quick Assessment', ha='center', fontsize=12, weight='bold')
    ax.text(2.75, 10.1, '⏱ Time: 5-10 minutes', ha='center', fontsize=9)
    ax.text(1, 9.7, '• Single pathogen', fontsize=8)
    ax.text(1, 9.4, '• Fixed parameters', fontsize=8)
    ax.text(1, 9.1, '• 10,000 iterations', fontsize=8)
    ax.text(1, 8.8, '📊 Output: Summary metrics', fontsize=8, style='italic')

    # Tier 2: Standard Assessment
    tier2_box = FancyBboxPatch((0.5, 5.8), 4.5, 2.3,
                               boxstyle="round,pad=0.1",
                               edgecolor=header_color, facecolor=tier2_color,
                               linewidth=2, zorder=1)
    ax.add_patch(tier2_box)

    ax.text(2.75, 7.8, 'TIER 2: Standard Assessment', ha='center', fontsize=12, weight='bold')
    ax.text(2.75, 7.4, '⏱ Time: 15-30 minutes', ha='center', fontsize=9)
    ax.text(1, 7.0, '• Multiple scenarios', fontsize=8)
    ax.text(1, 6.7, '• MetOcean dilution data', fontsize=8)
    ax.text(1, 6.4, '• Treatment comparison', fontsize=8)
    ax.text(1, 6.1, '📊 Output: Full report + charts', fontsize=8, style='italic')

    # Tier 3: Comprehensive Assessment
    tier3_box = FancyBboxPatch((0.5, 3.1), 4.5, 2.3,
                               boxstyle="round,pad=0.1",
                               edgecolor=header_color, facecolor=tier3_color,
                               linewidth=2, zorder=1)
    ax.add_patch(tier3_box)

    ax.text(2.75, 5.1, 'TIER 3: Comprehensive', ha='center', fontsize=12, weight='bold')
    ax.text(2.75, 4.7, '⏱ Time: 1-2 hours', ha='center', fontsize=9)
    ax.text(1, 4.3, '• Multi-pathogen analysis', fontsize=8)
    ax.text(1, 4.0, '• Sensitivity analysis', fontsize=8)
    ax.text(1, 3.7, '• Uncertainty quantification', fontsize=8)
    ax.text(1, 3.4, '📊 Output: Technical report', fontsize=8, style='italic')

    # === ANALYSIS ROUTES (Center) ===

    # Route 1: Swimming/Primary Contact
    route1_box = FancyBboxPatch((5.5, 8.5), 4.5, 2.3,
                                boxstyle="round,pad=0.1",
                                edgecolor='#0277BD', facecolor=route_color,
                                linewidth=2, zorder=1)
    ax.add_patch(route1_box)

    ax.text(7.75, 10.5, '🏊 Route 1: Swimming', ha='center', fontsize=12, weight='bold', color='#0277BD')
    ax.text(6, 10.0, 'Exposure:', fontsize=9, weight='bold')
    ax.text(6, 9.7, '  • Primary contact (skin)', fontsize=8)
    ax.text(6, 9.4, '  • Ingestion: 25-100 mL', fontsize=8)
    ax.text(6, 9.1, '  • Frequency: 5-30/year', fontsize=8)
    ax.text(6, 8.8, 'Risk Target: ≤ 1×10⁻³', fontsize=8, style='italic', color='red')

    # Route 2: Shellfish
    route2_box = FancyBboxPatch((5.5, 5.8), 4.5, 2.3,
                                boxstyle="round,pad=0.1",
                                edgecolor='#0277BD', facecolor=route_color,
                                linewidth=2, zorder=1)
    ax.add_patch(route2_box)

    ax.text(7.75, 7.8, '🦪 Route 2: Shellfish', ha='center', fontsize=12, weight='bold', color='#0277BD')
    ax.text(6, 7.3, 'Exposure:', fontsize=9, weight='bold')
    ax.text(6, 7.0, '  • Consumption: 100-200g', fontsize=8)
    ax.text(6, 6.7, '  • Bioaccumulation: 10-100×', fontsize=8)
    ax.text(6, 6.4, '  • Frequency: 6-24/year', fontsize=8)
    ax.text(6, 6.1, 'Risk Target: ≤ 1×10⁻⁴', fontsize=8, style='italic', color='red')

    # Route 3: Multi-Site Comparison
    route3_box = FancyBboxPatch((5.5, 3.1), 4.5, 2.3,
                                boxstyle="round,pad=0.1",
                                edgecolor='#0277BD', facecolor=route_color,
                                linewidth=2, zorder=1)
    ax.add_patch(route3_box)

    ax.text(7.75, 5.1, '📍 Route 3: Multi-Site', ha='center', fontsize=12, weight='bold', color='#0277BD')
    ax.text(6, 4.6, 'Analysis:', fontsize=9, weight='bold')
    ax.text(6, 4.3, '  • Distance gradients', fontsize=8)
    ax.text(6, 4.0, '  • Multiple outfalls', fontsize=8)
    ax.text(6, 3.7, '  • Treatment scenarios', fontsize=8)
    ax.text(6, 3.4, 'Output: Spatial risk map', fontsize=8, style='italic')

    # === WORKFLOW STEPS (Right side) ===

    # Step boxes
    steps = [
        ('1. Load Data', 10.5, '• Pathogen concentrations\n• Dilution factors\n• Treatment LRVs'),
        ('2. Configure', 9.2, '• Select route\n• Set parameters\n• Choose tier'),
        ('3. Run Analysis', 7.9, '• Monte Carlo\n• 10K iterations\n• 2-5 seconds'),
        ('4. Review Results', 6.6, '• Risk metrics\n• Compliance check\n• Visualizations'),
        ('5. Generate Report', 5.3, '• PDF/Word/CSV\n• Charts included\n• Regulatory format')
    ]

    for i, (title, y_pos, content) in enumerate(steps):
        step_box = FancyBboxPatch((10.5, y_pos-0.5), 5, 1.0,
                                  boxstyle="round,pad=0.08",
                                  edgecolor=header_color, facecolor='white',
                                  linewidth=1.5, zorder=1)
        ax.add_patch(step_box)

        ax.text(11, y_pos+0.25, title, fontsize=10, weight='bold', color=header_color)
        for j, line in enumerate(content.split('\n')):
            ax.text(11, y_pos+0.05 - j*0.2, line, fontsize=7)

    # === CONNECTIONS ===

    # Arrows from tiers to routes
    arrow_props = dict(arrowstyle='->', lw=1.5, color='#666666')

    # Tier 1 -> Route 1
    ax.annotate('', xy=(5.5, 9.7), xytext=(5.0, 9.7),
                arrowprops=arrow_props)

    # Tier 2 -> Route 2
    ax.annotate('', xy=(5.5, 7.0), xytext=(5.0, 7.0),
                arrowprops=arrow_props)

    # Tier 3 -> Route 3
    ax.annotate('', xy=(5.5, 4.3), xytext=(5.0, 4.3),
                arrowprops=arrow_props)

    # Routes to workflow
    ax.annotate('', xy=(10.5, 9.0), xytext=(10.0, 9.5),
                arrowprops=arrow_props)

    # === LEGEND ===
    legend_y = 1.8
    ax.text(1, legend_y, '📋 Report Outputs:', fontsize=10, weight='bold')
    ax.text(1, legend_y-0.3, '• Tier 1: Summary metrics (CSV)', fontsize=8)
    ax.text(1, legend_y-0.5, '• Tier 2: Full report (Word/PDF)', fontsize=8)
    ax.text(1, legend_y-0.7, '• Tier 3: Technical + appendices', fontsize=8)

    ax.text(6, legend_y, '🎯 Key Features:', fontsize=10, weight='bold')
    ax.text(6, legend_y-0.3, '• Validated dose-response models', fontsize=8)
    ax.text(6, legend_y-0.5, '• MetOcean dilution integration', fontsize=8)
    ax.text(6, legend_y-0.7, '• NZ regulatory compliance', fontsize=8)

    # === FOOTER ===
    ax.text(8, 0.3, 'Start at Tier 1 for quick screening → Move to Tier 2/3 for detailed analysis',
            ha='center', fontsize=9, style='italic',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.tight_layout()
    return fig

if __name__ == '__main__':
    fig = create_qmra_workflow_diagram()

    # Save as high-resolution image
    output_path = 'static/qmra_workflow_diagram.png'
    fig.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
    print(f"Workflow diagram saved to: {output_path}")

    plt.show()
