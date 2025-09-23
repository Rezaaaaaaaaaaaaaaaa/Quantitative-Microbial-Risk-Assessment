#!/usr/bin/env python3
"""
Create QMRA Assessment Toolkit Schematic Diagram
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_qmra_schematic():
    """Create a simple, clean QMRA assessment toolkit schematic diagram."""

    # Create figure and axis
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Define colors
    input_color = '#E3F2FD'    # Light blue
    process_color = '#FFF3E0'   # Light orange
    output_color = '#E8F5E8'    # Light green
    arrow_color = '#424242'     # Dark gray

    # Title
    ax.text(6, 7.5, 'QMRA Assessment Toolkit Workflow',
            fontsize=14, fontweight='bold', ha='center')

    # INPUTS (Left column)
    ax.text(2, 6.5, 'INPUTS', fontsize=11, fontweight='bold', ha='center')

    inputs = [
        'Water Quality Data',
        'Pathogen Concentrations',
        'Log Reduction Values',
        'Exposure Scenarios'
    ]

    for i, text in enumerate(inputs):
        y_pos = 5.5 - i * 0.8
        box = FancyBboxPatch((0.5, y_pos-0.25), 3, 0.5,
                            boxstyle="round,pad=0.05",
                            facecolor=input_color,
                            edgecolor='#1976D2',
                            linewidth=1)
        ax.add_patch(box)
        ax.text(2, y_pos, text, fontsize=9, ha='center', va='center')

    # PROCESSING (Center column)
    ax.text(6, 6.5, 'PYTHON TOOLKIT', fontsize=11, fontweight='bold', ha='center')

    processes = [
        'Norovirus Database',
        'Monte Carlo Simulation',
        'Dose-Response Models',
        'Risk Calculation'
    ]

    for i, text in enumerate(processes):
        y_pos = 5.5 - i * 0.8
        box = FancyBboxPatch((4.5, y_pos-0.25), 3, 0.5,
                            boxstyle="round,pad=0.05",
                            facecolor=process_color,
                            edgecolor='#FF9800',
                            linewidth=1)
        ax.add_patch(box)
        ax.text(6, y_pos, text, fontsize=9, ha='center', va='center')

    # OUTPUTS (Right column)
    ax.text(10, 6.5, 'OUTPUTS', fontsize=11, fontweight='bold', ha='center')

    outputs = [
        'Risk Assessment Results',
        'Compliance Reports',
        'Health Risk Estimates',
        'Decision Support'
    ]

    for i, text in enumerate(outputs):
        y_pos = 5.5 - i * 0.8
        box = FancyBboxPatch((8.5, y_pos-0.25), 3, 0.5,
                            boxstyle="round,pad=0.05",
                            facecolor=output_color,
                            edgecolor='#388E3C',
                            linewidth=1)
        ax.add_patch(box)
        ax.text(10, y_pos, text, fontsize=9, ha='center', va='center')

    # ARROWS - Simple horizontal flow
    # Input to Processing
    arrow1 = patches.FancyArrowPatch((3.5, 4), (4.5, 4),
                                    arrowstyle='->', mutation_scale=20,
                                    color=arrow_color, linewidth=2)
    ax.add_patch(arrow1)

    # Processing to Output
    arrow2 = patches.FancyArrowPatch((7.5, 4), (8.5, 4),
                                    arrowstyle='->', mutation_scale=20,
                                    color=arrow_color, linewidth=2)
    ax.add_patch(arrow2)

    # Simple workflow description
    ax.text(6, 1.5, 'Simple Linear Workflow: Data Input → Python Processing → Risk Output',
            fontsize=11, ha='center', style='italic')

    ax.text(6, 1, 'Modular design for easy updates and Earth Sciences New Zealand integration',
            fontsize=10, ha='center', color='#666666')

    # Save the diagram
    plt.tight_layout()
    plt.savefig('qmra_assessment_toolkit_schematic.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig('qmra_assessment_toolkit_schematic.pdf', bbox_inches='tight',
                facecolor='white', edgecolor='none')

    print("QMRA Assessment Toolkit schematic diagram created:")
    print("- qmra_assessment_toolkit_schematic.png")
    print("- qmra_assessment_toolkit_schematic.pdf")

    plt.show()

    return 'qmra_assessment_toolkit_schematic.png'

if __name__ == '__main__':
    create_qmra_schematic()