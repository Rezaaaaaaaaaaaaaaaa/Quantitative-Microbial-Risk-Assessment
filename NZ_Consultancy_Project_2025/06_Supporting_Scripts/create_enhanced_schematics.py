#!/usr/bin/env python3
"""
Enhanced QMRA Schematic Generator - Staff-Friendly Visual Guides
Creates detailed step-by-step diagrams for all staff levels
NIWA Earth Sciences, September 2025
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Arrow, Polygon
import numpy as np
from datetime import datetime
from pathlib import Path

def create_staff_workflow_diagram():
    """Create detailed staff workflow diagram"""

    fig, ax = plt.subplots(figsize=(18, 12))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Title
    ax.text(9, 11.5, 'QMRA Toolkit - Staff Workflow Guide',
            fontsize=20, fontweight='bold', ha='center')

    # User levels
    levels = [
        {'name': 'NEW STAFF\nBeginner', 'x': 3, 'y': 9.5, 'color': '#ffcccb', 'path': 'GUI'},
        {'name': 'EXPERIENCED\nTechnical', 'x': 9, 'y': 9.5, 'color': '#add8e6', 'path': 'Script'},
        {'name': 'EXPERT\nSpecialist', 'x': 15, 'y': 9.5, 'color': '#98fb98', 'path': 'Custom'}
    ]

    # Draw user level boxes
    for level in levels:
        rect = FancyBboxPatch((level['x']-1.5, level['y']-0.8), 3, 1.6,
                             boxstyle="round,pad=0.2",
                             facecolor=level['color'],
                             edgecolor='black',
                             linewidth=2)
        ax.add_patch(rect)
        ax.text(level['x'], level['y'], level['name'],
               fontsize=12, fontweight='bold', ha='center', va='center')

    # Workflow paths
    paths = [
        # Beginner path
        {'steps': [
            {'text': '1. Double-click\nLaunch_GUI.bat', 'x': 3, 'y': 8},
            {'text': '2. Fill GUI form\nwith parameters', 'x': 3, 'y': 6.5},
            {'text': '3. Click "Run\nAssessment"', 'x': 3, 'y': 5},
            {'text': '4. View results\nin popup window', 'x': 3, 'y': 3.5}
        ], 'color': '#ff6b6b'},

        # Technical path
        {'steps': [
            {'text': '1. Open command\nprompt/terminal', 'x': 9, 'y': 8},
            {'text': '2. Run example\nscripts first', 'x': 9, 'y': 6.5},
            {'text': '3. Modify scenarios\nfor your project', 'x': 9, 'y': 5},
            {'text': '4. Generate reports\nand visualizations', 'x': 9, 'y': 3.5}
        ], 'color': '#4ecdc4'},

        # Expert path
        {'steps': [
            {'text': '1. Import toolkit\nmodules in Python', 'x': 15, 'y': 8},
            {'text': '2. Create custom\nanalysis scripts', 'x': 15, 'y': 6.5},
            {'text': '3. Add new pathogens\nor modify models', 'x': 15, 'y': 5},
            {'text': '4. Batch process\nmultiple scenarios', 'x': 15, 'y': 3.5}
        ], 'color': '#45b7d1'}
    ]

    # Draw workflow steps
    for path in paths:
        prev_y = None
        for i, step in enumerate(path['steps']):
            # Step box
            rect = Rectangle((step['x']-1.2, step['y']-0.6), 2.4, 1.2,
                           facecolor=path['color'], alpha=0.7, edgecolor='black')
            ax.add_patch(rect)

            # Step text
            ax.text(step['x'], step['y'], step['text'],
                   fontsize=10, ha='center', va='center', fontweight='bold')

            # Arrow to next step
            if prev_y is not None:
                ax.annotate('', xy=(step['x'], step['y']+0.6),
                           xytext=(step['x'], prev_y-0.6),
                           arrowprops=dict(arrowstyle='->', lw=2, color=path['color']))

            prev_y = step['y']

    # Common output section
    ax.text(9, 2.5, 'COMMON OUTPUTS FOR ALL LEVELS',
           fontsize=14, fontweight='bold', ha='center',
           bbox=dict(boxstyle="round,pad=0.3", facecolor='gold', alpha=0.8))

    outputs = [
        {'name': 'Risk Values &\nCompliance Status', 'x': 4, 'y': 1.5},
        {'name': 'Professional\nVisualizations', 'x': 9, 'y': 1.5},
        {'name': 'Executive Reports\n& Data Tables', 'x': 14, 'y': 1.5}
    ]

    for output in outputs:
        circle = Circle((output['x'], output['y']), 0.8,
                       facecolor='lightgreen', edgecolor='black', alpha=0.8)
        ax.add_patch(circle)
        ax.text(output['x'], output['y'], output['name'],
               fontsize=9, ha='center', va='center', fontweight='bold')

    plt.tight_layout()
    return fig

def create_gui_interface_diagram():
    """Create detailed GUI interface diagram"""

    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Title
    ax.text(8, 11.5, 'QMRA GUI Interface - Step-by-Step Guide',
            fontsize=18, fontweight='bold', ha='center')

    # GUI window mockup
    gui_rect = Rectangle((2, 3), 12, 7, facecolor='lightgray', edgecolor='black', linewidth=2)
    ax.add_patch(gui_rect)

    # Title bar
    title_rect = Rectangle((2, 9.5), 12, 0.5, facecolor='darkblue', edgecolor='black')
    ax.add_patch(title_rect)
    ax.text(8, 9.75, 'QMRA Assessment Toolkit - GUI Interface',
           fontsize=12, fontweight='bold', ha='center', color='white')

    # Form fields with annotations
    fields = [
        {'label': 'Pathogen:', 'x': 3, 'y': 8.8, 'width': 3, 'example': 'Norovirus', 'note': '1. Select from dropdown'},
        {'label': 'Exposure Route:', 'x': 3, 'y': 8.2, 'width': 3, 'example': 'Primary Contact', 'note': '2. Choose exposure type'},
        {'label': 'Concentration:', 'x': 3, 'y': 7.6, 'width': 3, 'example': '10.0 org/100mL', 'note': '3. Enter pathogen level'},
        {'label': 'Ingestion Volume:', 'x': 3, 'y': 7.0, 'width': 3, 'example': '50.0 mL', 'note': '4. Water ingested per event'},
        {'label': 'Events per Year:', 'x': 3, 'y': 6.4, 'width': 3, 'example': '15', 'note': '5. Swimming frequency'},
        {'label': 'Population:', 'x': 3, 'y': 5.8, 'width': 3, 'example': '10000', 'note': '6. People at risk'},
    ]

    for i, field in enumerate(fields):
        # Label
        ax.text(field['x'], field['y'], field['label'], fontsize=10, fontweight='bold')

        # Input box
        input_rect = Rectangle((field['x']+1.5, field['y']-0.15), field['width'], 0.3,
                              facecolor='white', edgecolor='black')
        ax.add_patch(input_rect)

        # Example text
        ax.text(field['x']+3, field['y'], field['example'], fontsize=9, ha='center', va='center')

        # Annotation arrow and note
        ax.annotate(field['note'], xy=(field['x']+field['width']+1.5, field['y']),
                   xytext=(field['x']+field['width']+3, field['y']+0.5),
                   arrowprops=dict(arrowstyle='->', color='red'),
                   fontsize=10, color='red', fontweight='bold')

    # Run button
    run_rect = Rectangle((6, 4.8), 4, 0.6, facecolor='green', edgecolor='black', linewidth=2)
    ax.add_patch(run_rect)
    ax.text(8, 5.1, 'RUN ASSESSMENT', fontsize=14, fontweight='bold', ha='center', color='white')

    # Click annotation
    ax.annotate('7. CLICK HERE TO START!', xy=(8, 4.8), xytext=(11, 4.2),
               arrowprops=dict(arrowstyle='->', color='red', lw=3),
               fontsize=12, color='red', fontweight='bold')

    # Results preview
    ax.text(8, 2.5, 'RESULTS WILL APPEAR IN NEW WINDOW',
           fontsize=14, fontweight='bold', ha='center',
           bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.8))

    # Results mockup (smaller)
    results_rect = Rectangle((10, 0.5), 5, 1.5, facecolor='lightblue', edgecolor='black')
    ax.add_patch(results_rect)
    ax.text(12.5, 1.7, 'Results Window', fontsize=10, fontweight='bold', ha='center')
    ax.text(12.5, 1.4, 'Annual Risk: 2.4e-02', fontsize=9, ha='center')
    ax.text(12.5, 1.1, 'Expected Cases: 240', fontsize=9, ha='center')
    ax.text(12.5, 0.8, 'Status: COMPLIANT', fontsize=9, ha='center', color='green', fontweight='bold')

    plt.tight_layout()
    return fig

def create_risk_interpretation_diagram():
    """Create risk interpretation visual guide"""

    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(8, 9.5, 'Risk Results Interpretation Guide',
            fontsize=20, fontweight='bold', ha='center')

    # Risk scale
    ax.text(8, 8.8, 'Understanding Risk Values - What Do The Numbers Mean?',
           fontsize=14, ha='center', style='italic')

    # Risk thermometer/scale
    scale_x = 2
    scale_width = 12
    scale_height = 0.8

    # Risk ranges with colors and interpretations
    risk_ranges = [
        {'min': 1e-8, 'max': 1e-6, 'color': '#00ff00', 'label': 'EXCELLENT', 'description': 'Very Low Risk - Exceeds all guidelines'},
        {'min': 1e-6, 'max': 1e-4, 'color': '#90ee90', 'label': 'GOOD', 'description': 'Low Risk - Meets NZ drinking water standards'},
        {'min': 1e-4, 'max': 1e-2, 'color': '#ffff00', 'label': 'ACCEPTABLE', 'description': 'Moderate Risk - May need management'},
        {'min': 1e-2, 'max': 1e-1, 'color': '#ffa500', 'label': 'HIGH', 'description': 'Action Required - Exceeds guidelines'},
        {'min': 1e-1, 'max': 1, 'color': '#ff0000', 'label': 'CRITICAL', 'description': 'Immediate Intervention Needed'}
    ]

    # Draw risk scale
    y_pos = 7.5
    for i, risk_range in enumerate(risk_ranges):
        # Color band
        segment_width = scale_width / len(risk_ranges)
        rect = Rectangle((scale_x + i * segment_width, y_pos), segment_width, scale_height,
                        facecolor=risk_range['color'], edgecolor='black', alpha=0.8)
        ax.add_patch(rect)

        # Labels
        center_x = scale_x + i * segment_width + segment_width/2
        ax.text(center_x, y_pos + scale_height/2, risk_range['label'],
               fontsize=10, fontweight='bold', ha='center', va='center')

        # Risk values
        ax.text(center_x, y_pos - 0.3, f"{risk_range['min']:.0e}\nto\n{risk_range['max']:.0e}",
               fontsize=8, ha='center', va='top')

        # Descriptions
        ax.text(center_x, y_pos - 1, risk_range['description'],
               fontsize=9, ha='center', va='top', wrap=True)

    # Example calculations
    ax.text(8, 5.8, 'Real-World Examples - What These Numbers Mean',
           fontsize=14, fontweight='bold', ha='center')

    examples = [
        {
            'title': 'Example 1: Low Risk Beach',
            'risk': '2.4e-04',
            'population': '10,000',
            'cases': '2.4',
            'interpretation': 'About 2-3 people might get sick per year from swimming',
            'x': 4, 'y': 4.5, 'color': '#90ee90'
        },
        {
            'title': 'Example 2: Moderate Risk Lake',
            'risk': '1.2e-02',
            'population': '50,000',
            'cases': '600',
            'interpretation': 'About 600 people might get sick per year - needs action',
            'x': 12, 'y': 4.5, 'color': '#ffa500'
        }
    ]

    for example in examples:
        # Example box
        rect = FancyBboxPatch((example['x']-2.5, example['y']-1), 5, 2,
                             boxstyle="round,pad=0.2",
                             facecolor=example['color'],
                             alpha=0.3, edgecolor='black')
        ax.add_patch(rect)

        # Example content
        ax.text(example['x'], example['y']+0.5, example['title'],
               fontsize=12, fontweight='bold', ha='center')
        ax.text(example['x'], example['y'], f"Annual Risk: {example['risk']}\nPopulation: {example['population']}\nExpected Cases/Year: {example['cases']}",
               fontsize=10, ha='center', va='center')
        ax.text(example['x'], example['y']-0.7, example['interpretation'],
               fontsize=9, ha='center', va='center', style='italic', wrap=True)

    # Compliance guidelines
    ax.text(8, 2.5, 'New Zealand Regulatory Guidelines',
           fontsize=14, fontweight='bold', ha='center')

    guidelines = [
        {'type': 'Drinking Water Equivalent', 'target': '≤ 1e-6', 'description': 'Strictest standard - annual risk', 'color': '#e6f3ff'},
        {'type': 'Recreational Water', 'target': '≤ 1e-3', 'description': 'Per swimming event', 'color': '#fff0e6'},
        {'type': 'Shellfish Consumption', 'target': '≤ 1e-4', 'description': 'Annual risk from eating shellfish', 'color': '#f0fff0'}
    ]

    for i, guideline in enumerate(guidelines):
        rect = Rectangle((1 + i*5, 1), 4, 1, facecolor=guideline['color'], edgecolor='black')
        ax.add_patch(rect)
        ax.text(3 + i*5, 1.7, guideline['type'], fontsize=11, fontweight='bold', ha='center')
        ax.text(3 + i*5, 1.4, f"Target: {guideline['target']}", fontsize=10, ha='center')
        ax.text(3 + i*5, 1.1, guideline['description'], fontsize=9, ha='center')

    plt.tight_layout()
    return fig

def create_troubleshooting_flowchart():
    """Create troubleshooting flowchart"""

    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Title
    ax.text(8, 11.5, 'QMRA Toolkit Troubleshooting Flowchart',
            fontsize=18, fontweight='bold', ha='center')

    # Start
    start = Circle((8, 10.5), 0.5, facecolor='lightgreen', edgecolor='black')
    ax.add_patch(start)
    ax.text(8, 10.5, 'START\nHERE', fontsize=10, fontweight='bold', ha='center', va='center')

    # Problem categories
    problems = [
        {'name': 'GUI Won\'t\nLaunch', 'x': 3, 'y': 9, 'color': '#ffcccb'},
        {'name': 'Error\nMessages', 'x': 8, 'y': 9, 'color': '#ffd1dc'},
        {'name': 'Strange\nResults', 'x': 13, 'y': 9, 'color': '#ffe4e1'}
    ]

    for problem in problems:
        rect = Rectangle((problem['x']-1, problem['y']-0.5), 2, 1,
                        facecolor=problem['color'], edgecolor='black')
        ax.add_patch(rect)
        ax.text(problem['x'], problem['y'], problem['name'],
               fontsize=10, fontweight='bold', ha='center', va='center')

    # Solutions for each problem
    solutions = {
        'gui': [
            {'text': '1. Check Python\ninstalled?', 'x': 3, 'y': 7.5},
            {'text': '2. Run: pip install\n-r requirements.txt', 'x': 3, 'y': 6.5},
            {'text': '3. Try command line:\npython launch_gui.py', 'x': 3, 'y': 5.5},
            {'text': '4. Restart computer\nand try again', 'x': 3, 'y': 4.5}
        ],
        'errors': [
            {'text': 'Read error message\ncarefully', 'x': 8, 'y': 7.5},
            {'text': 'Check input values\n(no negatives/zeros)', 'x': 8, 'y': 6.5},
            {'text': 'Verify pathogen\nconcentration set', 'x': 8, 'y': 5.5},
            {'text': 'Try with default\nexample values', 'x': 8, 'y': 4.5}
        ],
        'results': [
            {'text': 'Check units\n(per L vs per 100mL)', 'x': 13, 'y': 7.5},
            {'text': 'Verify dilution\nfactors applied', 'x': 13, 'y': 6.5},
            {'text': 'Compare to literature\nvalues', 'x': 13, 'y': 5.5},
            {'text': 'Get colleague to\nreview inputs', 'x': 13, 'y': 4.5}
        ]
    }

    colors = ['#ff9999', '#99ccff', '#99ff99']
    for i, (category, solution_list) in enumerate(solutions.items()):
        for j, solution in enumerate(solution_list):
            rect = Rectangle((solution['x']-1.2, solution['y']-0.4), 2.4, 0.8,
                           facecolor=colors[i], alpha=0.7, edgecolor='black')
            ax.add_patch(rect)
            ax.text(solution['x'], solution['y'], solution['text'],
                   fontsize=9, ha='center', va='center')

    # Decision diamonds
    decision_y = 3.5
    ax.text(8, decision_y, 'Problem Solved?', fontsize=12, fontweight='bold', ha='center',
           bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow'))

    # Yes/No paths
    ax.text(5, 2.5, 'YES: Document solution\nfor future reference',
           fontsize=11, ha='center', color='green', fontweight='bold',
           bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.7))

    ax.text(11, 2.5, 'NO: Contact technical\nsupport team',
           fontsize=11, ha='center', color='red', fontweight='bold',
           bbox=dict(boxstyle="round,pad=0.3", facecolor='lightcoral', alpha=0.7))

    # Contact information
    ax.text(8, 1, 'Technical Support: qmra-support@niwa.co.nz\nInclude: Error message, input values, screenshots',
           fontsize=10, ha='center', style='italic',
           bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.5))

    # Draw connecting arrows
    arrow_props = dict(arrowstyle='->', lw=2, color='darkblue')

    # From start to problems
    ax.annotate('', xy=(3, 9.5), xytext=(7.2, 10.2), arrowprops=arrow_props)
    ax.annotate('', xy=(8, 9.5), xytext=(8, 10), arrowprops=arrow_props)
    ax.annotate('', xy=(13, 9.5), xytext=(8.8, 10.2), arrowprops=arrow_props)

    plt.tight_layout()
    return fig

def create_project_template_diagram():
    """Create project setup template diagram"""

    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(7, 9.5, 'QMRA Project Setup Template',
            fontsize=18, fontweight='bold', ha='center')

    # Project phases
    phases = [
        {
            'name': 'PHASE 1: PLANNING',
            'tasks': [
                '• Define objectives',
                '• Identify pathogens',
                '• Select scenarios',
                '• Gather data'
            ],
            'x': 2.5, 'y': 8, 'color': '#ffeb3b'
        },
        {
            'name': 'PHASE 2: SETUP',
            'tasks': [
                '• Create project folder',
                '• Configure toolkit',
                '• Test with examples',
                '• Verify parameters'
            ],
            'x': 7, 'y': 8, 'color': '#2196f3'
        },
        {
            'name': 'PHASE 3: ANALYSIS',
            'tasks': [
                '• Run assessments',
                '• Quality check results',
                '• Sensitivity analysis',
                '• Generate reports'
            ],
            'x': 11.5, 'y': 8, 'color': '#4caf50'
        }
    ]

    for phase in phases:
        # Phase box
        rect = FancyBboxPatch((phase['x']-1.8, phase['y']-1.5), 3.6, 3,
                             boxstyle="round,pad=0.2",
                             facecolor=phase['color'],
                             alpha=0.7, edgecolor='black')
        ax.add_patch(rect)

        # Phase title
        ax.text(phase['x'], phase['y']+1, phase['name'],
               fontsize=12, fontweight='bold', ha='center')

        # Tasks
        for i, task in enumerate(phase['tasks']):
            ax.text(phase['x'], phase['y']+0.3-i*0.3, task,
                   fontsize=10, ha='center')

    # Arrows between phases
    arrow_props = dict(arrowstyle='->', lw=3, color='darkred')
    ax.annotate('', xy=(5.2, 8), xytext=(4.3, 8), arrowprops=arrow_props)
    ax.annotate('', xy=(9.7, 8), xytext=(8.8, 8), arrowprops=arrow_props)

    # Detailed folder structure template
    ax.text(7, 5.5, 'Recommended Project Folder Structure',
           fontsize=14, fontweight='bold', ha='center')

    folder_structure = """
    📁 Project_Name_YYYY/
    ├── 📋 01_Documentation/
    │   ├── project_brief.md
    │   ├── parameters_log.yaml
    │   └── assumptions.txt
    ├── 🔬 02_Analysis/
    │   ├── scripts/
    │   ├── results/
    │   └── validation/
    ├── 📊 03_Outputs/
    │   ├── figures/
    │   ├── tables/
    │   └── reports/
    └── 📦 04_Archive/
        ├── raw_data/
        ├── versions/
        └── backup/
    """

    ax.text(7, 3.5, folder_structure,
           fontsize=10, ha='center', va='top', family='monospace',
           bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.8))

    # Quality checklist
    ax.text(7, 1, 'Quality Assurance Checklist:',
           fontsize=12, fontweight='bold', ha='center')

    checklist = [
        '✓ Parameters documented and verified',
        '✓ Results peer-reviewed by colleague',
        '✓ Compliance with NZ guidelines checked',
        '✓ Professional reports generated',
        '✓ All files archived and backed up'
    ]

    for i, item in enumerate(checklist):
        ax.text(7, 0.5-i*0.2, item, fontsize=10, ha='center')

    plt.tight_layout()
    return fig

def main():
    """Generate all enhanced schematics for staff"""

    print("QMRA TOOLKIT - ENHANCED STAFF SCHEMATICS GENERATOR")
    print("Creating detailed visual guides for all staff levels...")
    print("=" * 80)

    # Create output directory
    output_dir = Path("../03_Visualizations")
    output_dir.mkdir(exist_ok=True)

    # Generate all enhanced schematics
    schematics = [
        ("Staff_Workflow_Guide", create_staff_workflow_diagram),
        ("GUI_Interface_Guide", create_gui_interface_diagram),
        ("Risk_Interpretation_Guide", create_risk_interpretation_diagram),
        ("Troubleshooting_Flowchart", create_troubleshooting_flowchart),
        ("Project_Template_Guide", create_project_template_diagram)
    ]

    generated_files = []

    for name, func in schematics:
        print(f"Creating {name}...")
        fig = func()

        # Save as high-resolution PNG
        png_file = output_dir / f"{name}.png"
        fig.savefig(png_file, dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')

        # Save as PDF for printing
        pdf_file = output_dir / f"{name}.pdf"
        fig.savefig(pdf_file, bbox_inches='tight',
                   facecolor='white', edgecolor='none')

        plt.close(fig)
        generated_files.extend([png_file, pdf_file])
        print(f"  Saved: {png_file.name} and {pdf_file.name}")

    print("\n" + "=" * 80)
    print("ENHANCED STAFF SCHEMATICS GENERATION COMPLETE")
    print("=" * 80)
    print("Generated Files:")
    for file in generated_files:
        print(f"  {file.name}")

    print(f"\nAll {len(generated_files)} files saved to: {output_dir}")
    print("\nThese visual guides provide:")
    print("• Step-by-step workflow instructions for all staff levels")
    print("• Detailed GUI interface walkthrough")
    print("• Risk interpretation with real-world examples")
    print("• Troubleshooting flowchart for common issues")
    print("• Project setup template and best practices")
    print("\nPerfect for staff training, onboarding, and daily reference!")

if __name__ == "__main__":
    main()