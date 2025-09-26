#!/usr/bin/env python3
"""
QMRA Project Schematic Generator
Creates technical diagrams and flowcharts for staff understanding
NIWA Earth Sciences, September 2025
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Arrow
import numpy as np
from datetime import datetime
from pathlib import Path

def create_qmra_framework_diagram():
    """Create QMRA 4-step framework diagram"""

    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(8, 9.5, 'QMRA Framework - The 4-Step Process',
            fontsize=20, fontweight='bold', ha='center')

    # Step boxes
    steps = [
        {'title': '1. HAZARD\nIDENTIFICATION', 'x': 2, 'y': 6, 'color': '#ff6b6b'},
        {'title': '2. EXPOSURE\nASSESSMENT', 'x': 6, 'y': 6, 'color': '#4ecdc4'},
        {'title': '3. DOSE-RESPONSE\nMODELING', 'x': 10, 'y': 6, 'color': '#45b7d1'},
        {'title': '4. RISK\nCHARACTERIZATION', 'x': 14, 'y': 6, 'color': '#96ceb4'}
    ]

    # Draw step boxes
    for step in steps:
        # Main box
        box = FancyBboxPatch((step['x']-1.5, step['y']-1), 3, 2,
                            boxstyle="round,pad=0.1",
                            facecolor=step['color'],
                            edgecolor='black',
                            alpha=0.8)
        ax.add_patch(box)

        # Step title
        ax.text(step['x'], step['y'], step['title'],
               fontsize=12, fontweight='bold', ha='center', va='center')

    # Arrows between steps
    arrow_props = dict(arrowstyle='->', lw=3, color='darkblue')
    ax.annotate('', xy=(4.5, 6), xytext=(3.5, 6), arrowprops=arrow_props)
    ax.annotate('', xy=(8.5, 6), xytext=(7.5, 6), arrowprops=arrow_props)
    ax.annotate('', xy=(12.5, 6), xytext=(11.5, 6), arrowprops=arrow_props)

    # Step details
    details = [
        {'x': 2, 'y': 3.5, 'text': '• Pathogen selection\n• Literature review\n• Dose-response data\n• Environmental survival'},
        {'x': 6, 'y': 3.5, 'text': '• Exposure routes\n• Concentrations\n• Contact frequency\n• Population at risk'},
        {'x': 10, 'y': 3.5, 'text': '• Mathematical models\n• Beta-Poisson\n• Exponential\n• Probability calculation'},
        {'x': 14, 'y': 3.5, 'text': '• Risk calculation\n• Uncertainty analysis\n• Population impact\n• Regulatory compliance'}
    ]

    for detail in details:
        ax.text(detail['x'], detail['y'], detail['text'],
               fontsize=10, ha='center', va='top',
               bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))

    # Add toolkit reference
    ax.text(8, 0.5, 'NIWA QMRA Assessment Toolkit Implementation',
           fontsize=14, ha='center', style='italic',
           bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.5))

    plt.tight_layout()
    return fig

def create_treatment_train_diagram():
    """Create wastewater treatment train diagram"""

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Title
    ax.text(8, 7.5, 'Wastewater Treatment Train - Pathogen Removal',
            fontsize=18, fontweight='bold', ha='center')

    # Treatment stages
    stages = [
        {'name': 'RAW\nWASTEWATER', 'x': 1.5, 'y': 5, 'width': 2, 'height': 1.5, 'color': '#8b4513'},
        {'name': 'PRIMARY\nTREATMENT', 'x': 4.5, 'y': 5, 'width': 2, 'height': 1.5, 'color': '#cd853f'},
        {'name': 'SECONDARY\nTREATMENT', 'x': 7.5, 'y': 5, 'width': 2, 'height': 1.5, 'color': '#4682b4'},
        {'name': 'TERTIARY\nTREATMENT', 'x': 10.5, 'y': 5, 'width': 2, 'height': 1.5, 'color': '#32cd32'},
        {'name': 'DISCHARGE\nTO HARBOR', 'x': 13.5, 'y': 5, 'width': 2, 'height': 1.5, 'color': '#1e90ff'}
    ]

    # Draw treatment stages
    for stage in stages:
        rect = Rectangle((stage['x']-stage['width']/2, stage['y']-stage['height']/2),
                        stage['width'], stage['height'],
                        facecolor=stage['color'], edgecolor='black', alpha=0.7)
        ax.add_patch(rect)

        ax.text(stage['x'], stage['y'], stage['name'],
               fontsize=10, fontweight='bold', ha='center', va='center', color='white')

    # Flow arrows
    arrow_props = dict(arrowstyle='->', lw=4, color='blue')
    positions = [2.5, 5.5, 8.5, 11.5]
    for pos in positions:
        ax.annotate('', xy=(pos+1, 5), xytext=(pos, 5), arrowprops=arrow_props)

    # Pathogen concentrations
    concentrations = ['1e6\norg/L', '8e5\norg/L', '1e5\norg/L', '3e2\norg/L', '3\norg/L']
    x_positions = [1.5, 4.5, 7.5, 10.5, 13.5]

    for i, (conc, x) in enumerate(zip(concentrations, x_positions)):
        ax.text(x, 3.5, conc, fontsize=11, ha='center', va='center', fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.8))

    # LRV indicators
    lrv_labels = ['', '0.1 LRV', '1.0 LRV', '2.5 LRV', '100x dilution']
    lrv_positions = [3, 6, 9, 12]

    for lrv, x in zip(lrv_labels[1:], lrv_positions):
        ax.text(x, 6.5, lrv, fontsize=10, ha='center', va='center',
               bbox=dict(boxstyle="round,pad=0.2", facecolor='lightgreen', alpha=0.8))

    # Legend
    ax.text(8, 1.5, 'LRV = Log Reduction Value | 1 LRV = 90% removal | 2 LRV = 99% removal | 3 LRV = 99.9% removal',
           fontsize=12, ha='center',
           bbox=dict(boxstyle="round,pad=0.3", facecolor='lightcyan', alpha=0.8))

    plt.tight_layout()
    return fig

def create_toolkit_architecture_diagram():
    """Create toolkit architecture diagram"""

    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(7, 9.5, 'QMRA Toolkit Architecture',
            fontsize=18, fontweight='bold', ha='center')

    # User interfaces layer
    interfaces = [
        {'name': '🖥️ GUI\nInterface', 'x': 3, 'y': 8, 'color': '#ff6b6b'},
        {'name': '⌨️ Command\nLine', 'x': 7, 'y': 8, 'color': '#4ecdc4'},
        {'name': '📝 Custom\nScripts', 'x': 11, 'y': 8, 'color': '#45b7d1'}
    ]

    for interface in interfaces:
        rect = FancyBboxPatch((interface['x']-1, interface['y']-0.5), 2, 1,
                             boxstyle="round,pad=0.1",
                             facecolor=interface['color'],
                             alpha=0.8)
        ax.add_patch(rect)
        ax.text(interface['x'], interface['y'], interface['name'],
               fontsize=10, ha='center', va='center', fontweight='bold')

    # Core engines layer
    ax.text(7, 6.8, 'CORE PROCESSING ENGINES',
           fontsize=14, fontweight='bold', ha='center')

    engines = [
        {'name': '🦠\nPathogen\nDatabase', 'x': 2, 'y': 5.5, 'color': '#ffb3ba'},
        {'name': '💧\nExposure\nAssessment', 'x': 5, 'y': 5.5, 'color': '#bae1ff'},
        {'name': '🎲\nMonte Carlo\nSimulation', 'x': 8, 'y': 5.5, 'color': '#baffc9'},
        {'name': '⚠️\nRisk\nCharacterization', 'x': 11, 'y': 5.5, 'color': '#ffffba'}
    ]

    for engine in engines:
        rect = Rectangle((engine['x']-0.8, engine['y']-0.8), 1.6, 1.6,
                        facecolor=engine['color'], edgecolor='black', alpha=0.8)
        ax.add_patch(rect)
        ax.text(engine['x'], engine['y'], engine['name'],
               fontsize=9, ha='center', va='center', fontweight='bold')

    # Output layer
    ax.text(7, 3.8, 'OUTPUT GENERATORS',
           fontsize=14, fontweight='bold', ha='center')

    outputs = [
        {'name': '📊\nVisualization', 'x': 2.5, 'y': 2.5, 'color': '#ffd1dc'},
        {'name': '📋\nReports', 'x': 5.5, 'y': 2.5, 'color': '#e0e0e0'},
        {'name': '📈\nTables', 'x': 8.5, 'y': 2.5, 'color': '#d1ffd1'},
        {'name': '💾\nData Export', 'x': 11.5, 'y': 2.5, 'color': '#fff0d1'}
    ]

    for output in outputs:
        circle = Circle((output['x'], output['y']), 0.6,
                       facecolor=output['color'], edgecolor='black', alpha=0.8)
        ax.add_patch(circle)
        ax.text(output['x'], output['y'], output['name'],
               fontsize=9, ha='center', va='center', fontweight='bold')

    # Connection arrows
    # From interfaces to engines
    for i in range(len(interfaces)):
        for j in range(len(engines)):
            ax.plot([interfaces[i]['x'], engines[j]['x']],
                   [interfaces[i]['y']-0.5, engines[j]['y']+0.8],
                   'k--', alpha=0.3, lw=1)

    # From engines to outputs
    for i in range(len(engines)):
        for j in range(len(outputs)):
            ax.plot([engines[i]['x'], outputs[j]['x']],
                   [engines[i]['y']-0.8, outputs[j]['y']+0.6],
                   'k-', alpha=0.2, lw=1)

    # Add workflow arrows
    arrow_props = dict(arrowstyle='->', lw=2, color='darkblue')
    ax.annotate('', xy=(7, 6.2), xytext=(7, 7.5), arrowprops=arrow_props)
    ax.annotate('', xy=(7, 3.2), xytext=(7, 4.7), arrowprops=arrow_props)

    # Add labels
    ax.text(0.5, 8, 'USER\nINTERFACES', fontsize=12, fontweight='bold',
           rotation=90, va='center', ha='center')
    ax.text(0.5, 5.5, 'PROCESSING\nLAYER', fontsize=12, fontweight='bold',
           rotation=90, va='center', ha='center')
    ax.text(0.5, 2.5, 'OUTPUT\nLAYER', fontsize=12, fontweight='bold',
           rotation=90, va='center', ha='center')

    plt.tight_layout()
    return fig

def create_data_flow_diagram():
    """Create data flow diagram showing input to output"""

    fig, ax = plt.subplots(figsize=(15, 8))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Title
    ax.text(7.5, 7.5, 'QMRA Data Flow - From Input to Deliverables',
            fontsize=16, fontweight='bold', ha='center')

    # Input section
    ax.text(2.5, 6.8, 'INPUT DATA', fontsize=14, fontweight='bold', ha='center')

    inputs = [
        '🦠 Pathogen Parameters',
        '💧 Exposure Scenarios',
        '⚙️ Treatment Data',
        '🎯 Regulatory Guidelines'
    ]

    for i, inp in enumerate(inputs):
        y_pos = 6.2 - i*0.4
        rect = Rectangle((0.5, y_pos-0.15), 4, 0.3,
                        facecolor='lightblue', edgecolor='black', alpha=0.7)
        ax.add_patch(rect)
        ax.text(2.5, y_pos, inp, fontsize=10, ha='center', va='center')

    # Processing section
    ax.text(7.5, 6.8, 'PROCESSING ENGINE', fontsize=14, fontweight='bold', ha='center')

    # Central processing box
    process_box = FancyBboxPatch((6, 4), 3, 2.5,
                                boxstyle="round,pad=0.2",
                                facecolor='lightyellow',
                                edgecolor='black')
    ax.add_patch(process_box)

    ax.text(7.5, 5.8, 'MONTE CARLO', fontsize=12, fontweight='bold', ha='center')
    ax.text(7.5, 5.4, 'SIMULATION', fontsize=12, fontweight='bold', ha='center')
    ax.text(7.5, 5.0, '10,000 iterations', fontsize=10, ha='center')
    ax.text(7.5, 4.6, 'Statistical analysis', fontsize=10, ha='center')
    ax.text(7.5, 4.2, 'Uncertainty quantification', fontsize=10, ha='center')

    # Output section
    ax.text(12.5, 6.8, 'DELIVERABLES', fontsize=14, fontweight='bold', ha='center')

    outputs = [
        '📋 Executive Reports',
        '📊 Professional Plots',
        '📈 Data Tables (CSV)',
        '📄 Compliance Reports'
    ]

    for i, out in enumerate(outputs):
        y_pos = 6.2 - i*0.4
        rect = Rectangle((10.5, y_pos-0.15), 4, 0.3,
                        facecolor='lightgreen', edgecolor='black', alpha=0.7)
        ax.add_patch(rect)
        ax.text(12.5, y_pos, out, fontsize=10, ha='center', va='center')

    # Flow arrows
    arrow_props = dict(arrowstyle='->', lw=3, color='darkblue')
    ax.annotate('', xy=(5.8, 5.2), xytext=(4.7, 5.2), arrowprops=arrow_props)
    ax.annotate('', xy=(10.3, 5.2), xytext=(9.2, 5.2), arrowprops=arrow_props)

    # Quality indicators
    ax.text(7.5, 2.5, '✅ Quality Assurance Features',
           fontsize=12, fontweight='bold', ha='center')

    quality_items = [
        '• Peer-reviewed pathogen database',
        '• Literature-validated dose-response models',
        '• Conservative exposure assumptions',
        '• Comprehensive uncertainty analysis',
        '• Professional visualization standards'
    ]

    for i, item in enumerate(quality_items):
        ax.text(7.5, 2.0 - i*0.25, item, fontsize=10, ha='center')

    plt.tight_layout()
    return fig

def main():
    """Generate all technical schematics"""

    print("=" * 80)
    print("QMRA TOOLKIT - TECHNICAL SCHEMATIC GENERATOR")
    print("Creating staff-friendly diagrams and flowcharts...")
    print("=" * 80)

    # Create output directory
    output_dir = Path("../03_Visualizations")
    output_dir.mkdir(exist_ok=True)

    # Generate all schematics
    schematics = [
        ("QMRA_Framework_Diagram", create_qmra_framework_diagram),
        ("Treatment_Train_Diagram", create_treatment_train_diagram),
        ("Toolkit_Architecture", create_toolkit_architecture_diagram),
        ("Data_Flow_Diagram", create_data_flow_diagram)
    ]

    for name, func in schematics:
        print(f"Creating {name}...")
        fig = func()

        # Save as high-resolution PNG
        output_file = output_dir / f"{name}.png"
        fig.savefig(output_file, dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')

        # Save as PDF for printing
        pdf_file = output_dir / f"{name}.pdf"
        fig.savefig(pdf_file, bbox_inches='tight',
                   facecolor='white', edgecolor='none')

        plt.close(fig)
        print(f"  ✅ Saved: {output_file}")
        print(f"  ✅ Saved: {pdf_file}")

    print("\n" + "=" * 80)
    print("TECHNICAL SCHEMATICS GENERATION COMPLETE")
    print("=" * 80)
    print("Generated Files:")
    print("  📊 QMRA_Framework_Diagram.png & .pdf")
    print("  🏭 Treatment_Train_Diagram.png & .pdf")
    print("  🏗️ Toolkit_Architecture.png & .pdf")
    print("  📈 Data_Flow_Diagram.png & .pdf")
    print("\nAll schematics are staff-friendly with clear visual explanations!")
    print("Use these for training, presentations, and technical documentation.")

if __name__ == "__main__":
    main()