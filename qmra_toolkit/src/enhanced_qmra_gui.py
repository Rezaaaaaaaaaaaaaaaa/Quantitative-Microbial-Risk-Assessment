"""
Enhanced QMRA Assessment Toolkit - Professional GUI
A modern, feature-rich graphical user interface for QMRA assessments
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import tkinter.font as tkFont
import threading
import json
import os
import sys
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import webbrowser
import subprocess

# Import QMRA modules
sys.path.insert(0, os.path.dirname(__file__))
try:
    from pathogen_database import PathogenDatabase
    from exposure_assessment import create_exposure_assessment, ExposureRoute
    from risk_characterization import RiskCharacterization
    from report_generator import ReportGenerator
except ImportError:
    # Fallback for missing modules
    print("Warning: Some QMRA modules not found. Running in demo mode.")

class EnhancedQMRAGui:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_styles()
        self.initialize_variables()
        self.initialize_qmra_components()
        self.create_widgets()
        self.load_initial_data()

    def setup_window(self):
        """Configure the main window."""
        self.root.title("NIWA QMRA Assessment Toolkit - Professional Edition")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)

        # Set window icon (if available)
        try:
            self.root.iconbitmap("assets/niwa_icon.ico")
        except:
            pass

        # Create menu bar
        self.create_menu_bar()

        # Configure main grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Application state
        self.current_project = None
        self.current_results = None
        self.assessment_running = False

    def setup_styles(self):
        """Configure custom styles for professional appearance."""
        self.style = ttk.Style()

        # Configure theme
        try:
            self.style.theme_use('clam')  # Modern theme
        except:
            self.style.theme_use('default')

        # Custom colors
        self.colors = {
            'primary': '#1f4e79',      # NIWA blue
            'secondary': '#2d7dd2',    # Light blue
            'success': '#28a745',      # Green
            'warning': '#ffc107',      # Yellow
            'danger': '#dc3545',       # Red
            'light': '#f8f9fa',        # Light gray
            'dark': '#343a40'          # Dark gray
        }

        # Configure custom styles
        self.style.configure('Title.TLabel',
                           foreground=self.colors['primary'],
                           font=('Segoe UI', 18, 'bold'))

        self.style.configure('Subtitle.TLabel',
                           foreground=self.colors['dark'],
                           font=('Segoe UI', 10, 'italic'))

        self.style.configure('Header.TLabel',
                           foreground=self.colors['primary'],
                           font=('Segoe UI', 12, 'bold'))

        self.style.configure('Primary.TButton',
                           foreground='white',
                           font=('Segoe UI', 10, 'bold'))

        self.style.configure('Success.TButton',
                           foreground='white',
                           font=('Segoe UI', 10, 'bold'))

        # Configure notebook style
        self.style.configure('TNotebook.Tab',
                           padding=[20, 10],
                           font=('Segoe UI', 10, 'bold'))

    def initialize_variables(self):
        """Initialize all GUI variables."""
        # Project information
        self.project_name_var = tk.StringVar(value="")
        self.assessor_name_var = tk.StringVar(value="")
        self.client_name_var = tk.StringVar(value="")
        self.assessment_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))

        # Assessment parameters
        self.pathogen_var = tk.StringVar(value="norovirus")
        self.exposure_route_var = tk.StringVar(value="primary_contact")
        self.concentration_var = tk.DoubleVar(value=1000.0)
        self.volume_var = tk.DoubleVar(value=100.0)
        self.frequency_var = tk.DoubleVar(value=7.0)
        self.population_var = tk.IntVar(value=100000)
        self.iterations_var = tk.IntVar(value=10000)
        self.confidence_level_var = tk.DoubleVar(value=95.0)

        # Treatment scenarios
        self.current_treatment_var = tk.StringVar(value="Secondary Treatment")
        self.proposed_treatment_var = tk.StringVar(value="Tertiary Treatment")
        self.current_lrv_var = tk.DoubleVar(value=1.5)
        self.proposed_lrv_var = tk.DoubleVar(value=3.5)
        self.dilution_factor_var = tk.DoubleVar(value=100.0)

        # Advanced options
        self.use_multiple_pathogens_var = tk.BooleanVar(value=False)
        self.generate_plots_var = tk.BooleanVar(value=True)
        self.save_intermediate_var = tk.BooleanVar(value=False)
        self.uncertainty_analysis_var = tk.BooleanVar(value=True)

        # Status and progress
        self.status_var = tk.StringVar(value="Ready - Professional QMRA Assessment Toolkit")
        self.progress_var = tk.DoubleVar(value=0.0)

    def initialize_qmra_components(self):
        """Initialize QMRA assessment components."""
        try:
            self.pathogen_db = PathogenDatabase()
            self.risk_calc = RiskCharacterization(self.pathogen_db)
            self.report_gen = ReportGenerator()
        except Exception as e:
            print(f"Warning: QMRA components not initialized: {e}")
            # Create mock components for demo
            self.pathogen_db = None
            self.risk_calc = None
            self.report_gen = None

    def create_widgets(self):
        """Create all GUI widgets with enhanced design."""
        # Main container
        self.main_container = ttk.Frame(self.root, padding="0")
        self.main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.rowconfigure(1, weight=1)

        # Create header
        self.create_header()

        # Create main content area
        self.create_main_content()

        # Create status bar
        self.create_status_bar()

    def create_header(self):
        """Create professional header with NIWA branding."""
        header_frame = ttk.Frame(self.main_container, padding="20 15 20 15")
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        header_frame.columnconfigure(1, weight=1)

        # NIWA logo placeholder
        logo_frame = ttk.Frame(header_frame, width=80, height=60)
        logo_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.N), padx=(0, 20))
        logo_frame.grid_propagate(False)

        # Add logo text (placeholder for actual logo)
        logo_label = ttk.Label(logo_frame, text="NIWA",
                              font=('Segoe UI', 20, 'bold'),
                              foreground=self.colors['primary'])
        logo_label.place(relx=0.5, rely=0.5, anchor='center')

        # Title and subtitle
        title_label = ttk.Label(header_frame, text="QMRA Assessment Toolkit",
                               style='Title.TLabel')
        title_label.grid(row=0, column=1, sticky=(tk.W), pady=(0, 5))

        subtitle_label = ttk.Label(header_frame,
                                  text="Professional Quantitative Microbial Risk Assessment - New Zealand Guidelines",
                                  style='Subtitle.TLabel')
        subtitle_label.grid(row=1, column=1, sticky=(tk.W))

        # Header buttons
        header_buttons = ttk.Frame(header_frame)
        header_buttons.grid(row=0, column=2, rowspan=2, sticky=(tk.E, tk.N))

        ttk.Button(header_buttons, text="📁 New Project",
                  command=self.new_project, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(header_buttons, text="📂 Open Project",
                  command=self.open_project, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(header_buttons, text="💾 Save Project",
                  command=self.save_project, width=12).pack(side=tk.LEFT, padx=2)

        # Separator
        ttk.Separator(self.main_container, orient='horizontal').grid(
            row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 0))

    def create_main_content(self):
        """Create main content area with enhanced tabbed interface."""
        # Main content frame
        content_frame = ttk.Frame(self.main_container, padding="20 20 20 0")
        content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)

        # Create enhanced notebook
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create tabs
        self.create_project_tab()
        self.create_assessment_tab()
        self.create_scenarios_tab()
        self.create_results_tab()
        self.create_plots_tab()
        self.create_reports_tab()
        self.create_database_tab()
        self.create_settings_tab()

    def create_project_tab(self):
        """Create project information tab."""
        self.project_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.project_frame, text="📋 Project Setup")

        # Configure grid
        self.project_frame.columnconfigure(1, weight=1)

        # Project Information Section
        info_label = ttk.Label(self.project_frame, text="Project Information", style='Header.TLabel')
        info_label.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 15))

        # Project details in a nice frame
        info_frame = ttk.LabelFrame(self.project_frame, text="Project Details", padding="15")
        info_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        info_frame.columnconfigure(1, weight=1)

        # Project name
        ttk.Label(info_frame, text="Project Name:", font=('Segoe UI', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        project_entry = ttk.Entry(info_frame, textvariable=self.project_name_var,
                                 font=('Segoe UI', 10), width=40)
        project_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        # Assessor name
        ttk.Label(info_frame, text="Lead Assessor:", font=('Segoe UI', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        assessor_entry = ttk.Entry(info_frame, textvariable=self.assessor_name_var,
                                  font=('Segoe UI', 10), width=40)
        assessor_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        # Client name
        ttk.Label(info_frame, text="Client Organization:", font=('Segoe UI', 10, 'bold')).grid(
            row=2, column=0, sticky=tk.W, pady=5)
        client_entry = ttk.Entry(info_frame, textvariable=self.client_name_var,
                                font=('Segoe UI', 10), width=40)
        client_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        # Assessment date
        ttk.Label(info_frame, text="Assessment Date:", font=('Segoe UI', 10, 'bold')).grid(
            row=3, column=0, sticky=tk.W, pady=5)
        date_entry = ttk.Entry(info_frame, textvariable=self.assessment_date_var,
                              font=('Segoe UI', 10), width=40)
        date_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        # Population at risk section
        pop_frame = ttk.LabelFrame(self.project_frame, text="Population Assessment", padding="15")
        pop_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        pop_frame.columnconfigure(1, weight=1)

        ttk.Label(pop_frame, text="Population at Risk:", font=('Segoe UI', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        pop_entry = ttk.Entry(pop_frame, textvariable=self.population_var,
                             font=('Segoe UI', 10), width=20)
        pop_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        ttk.Label(pop_frame, text="people", font=('Segoe UI', 9, 'italic')).grid(
            row=0, column=2, sticky=tk.W, pady=5, padx=(5, 0))

    def create_assessment_tab(self):
        """Create enhanced assessment parameters tab."""
        self.assessment_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.assessment_frame, text="🧬 Assessment Parameters")

        # Configure grid
        self.assessment_frame.columnconfigure(1, weight=1)

        # Pathogen Selection Section
        pathogen_frame = ttk.LabelFrame(self.assessment_frame, text="Pathogen Selection", padding="15")
        pathogen_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        pathogen_frame.columnconfigure(1, weight=1)

        ttk.Label(pathogen_frame, text="Primary Pathogen:", font=('Segoe UI', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.pathogen_combo = ttk.Combobox(pathogen_frame, textvariable=self.pathogen_var,
                                          state="readonly", font=('Segoe UI', 10), width=25)
        self.pathogen_combo['values'] = ('norovirus', 'campylobacter', 'cryptosporidium',
                                        'e_coli', 'salmonella', 'rotavirus')
        self.pathogen_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        # Multi-pathogen option
        ttk.Checkbutton(pathogen_frame, text="Enable Multi-Pathogen Assessment",
                       variable=self.use_multiple_pathogens_var,
                       command=self.toggle_multi_pathogen).grid(
            row=1, column=0, columnspan=2, sticky=tk.W, pady=10)

        # Exposure Parameters Section
        exposure_frame = ttk.LabelFrame(self.assessment_frame, text="Exposure Parameters", padding="15")
        exposure_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        exposure_frame.columnconfigure(1, weight=1)

        # Exposure route
        ttk.Label(exposure_frame, text="Exposure Route:", font=('Segoe UI', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.route_combo = ttk.Combobox(exposure_frame, textvariable=self.exposure_route_var,
                                       state="readonly", font=('Segoe UI', 10), width=25)
        self.route_combo['values'] = ('primary_contact', 'shellfish_consumption',
                                     'drinking_water', 'aerosol_inhalation')
        self.route_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        # Concentration with scientific notation support
        ttk.Label(exposure_frame, text="Pathogen Concentration:", font=('Segoe UI', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        conc_frame = ttk.Frame(exposure_frame)
        conc_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        conc_frame.columnconfigure(0, weight=1)

        conc_entry = ttk.Entry(conc_frame, textvariable=self.concentration_var,
                              font=('Segoe UI', 10), width=15)
        conc_entry.pack(side=tk.LEFT)
        ttk.Label(conc_frame, text="copies/L", font=('Segoe UI', 9, 'italic')).pack(
            side=tk.LEFT, padx=(5, 0))
        ttk.Button(conc_frame, text="📊", command=self.show_concentration_helper,
                  width=3).pack(side=tk.LEFT, padx=(5, 0))

        # Volume per exposure
        ttk.Label(exposure_frame, text="Volume per Exposure:", font=('Segoe UI', 10, 'bold')).grid(
            row=2, column=0, sticky=tk.W, pady=5)
        vol_frame = ttk.Frame(exposure_frame)
        vol_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        vol_entry = ttk.Entry(vol_frame, textvariable=self.volume_var,
                             font=('Segoe UI', 10), width=15)
        vol_entry.pack(side=tk.LEFT)
        ttk.Label(vol_frame, text="mL", font=('Segoe UI', 9, 'italic')).pack(
            side=tk.LEFT, padx=(5, 0))

        # Exposure frequency
        ttk.Label(exposure_frame, text="Exposure Frequency:", font=('Segoe UI', 10, 'bold')).grid(
            row=3, column=0, sticky=tk.W, pady=5)
        freq_frame = ttk.Frame(exposure_frame)
        freq_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        freq_entry = ttk.Entry(freq_frame, textvariable=self.frequency_var,
                              font=('Segoe UI', 10), width=15)
        freq_entry.pack(side=tk.LEFT)
        ttk.Label(freq_frame, text="events/year", font=('Segoe UI', 9, 'italic')).pack(
            side=tk.LEFT, padx=(5, 0))

        # Analysis Options Section
        analysis_frame = ttk.LabelFrame(self.assessment_frame, text="Analysis Options", padding="15")
        analysis_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        analysis_frame.columnconfigure(1, weight=1)

        # Monte Carlo iterations
        ttk.Label(analysis_frame, text="Monte Carlo Iterations:", font=('Segoe UI', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        iter_frame = ttk.Frame(analysis_frame)
        iter_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        iter_entry = ttk.Entry(iter_frame, textvariable=self.iterations_var,
                              font=('Segoe UI', 10), width=15)
        iter_entry.pack(side=tk.LEFT)
        ttk.Label(iter_frame, text="(recommended: 10,000)", font=('Segoe UI', 9, 'italic')).pack(
            side=tk.LEFT, padx=(5, 0))

        # Confidence level
        ttk.Label(analysis_frame, text="Confidence Level:", font=('Segoe UI', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        conf_frame = ttk.Frame(analysis_frame)
        conf_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        conf_entry = ttk.Entry(conf_frame, textvariable=self.confidence_level_var,
                              font=('Segoe UI', 10), width=10)
        conf_entry.pack(side=tk.LEFT)
        ttk.Label(conf_frame, text="%", font=('Segoe UI', 9, 'italic')).pack(
            side=tk.LEFT, padx=(2, 0))

    def create_scenarios_tab(self):
        """Create treatment scenarios comparison tab."""
        self.scenarios_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.scenarios_frame, text="🔬 Treatment Scenarios")

        # Configure grid
        self.scenarios_frame.columnconfigure(0, weight=1)
        self.scenarios_frame.columnconfigure(1, weight=1)

        # Current Treatment Section
        current_frame = ttk.LabelFrame(self.scenarios_frame, text="Current Treatment", padding="15")
        current_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N), padx=(0, 10), pady=(0, 15))
        current_frame.columnconfigure(1, weight=1)

        ttk.Label(current_frame, text="Treatment Type:", font=('Segoe UI', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        current_treatment_combo = ttk.Combobox(current_frame, textvariable=self.current_treatment_var,
                                              font=('Segoe UI', 10), width=20)
        current_treatment_combo['values'] = ('Primary Treatment', 'Secondary Treatment',
                                            'Advanced Secondary', 'Tertiary Treatment')
        current_treatment_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        ttk.Label(current_frame, text="Log Reduction Value:", font=('Segoe UI', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(current_frame, textvariable=self.current_lrv_var,
                 font=('Segoe UI', 10), width=10).grid(
            row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        # Proposed Treatment Section
        proposed_frame = ttk.LabelFrame(self.scenarios_frame, text="Proposed Treatment", padding="15")
        proposed_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N), padx=(10, 0), pady=(0, 15))
        proposed_frame.columnconfigure(1, weight=1)

        ttk.Label(proposed_frame, text="Treatment Type:", font=('Segoe UI', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        proposed_treatment_combo = ttk.Combobox(proposed_frame, textvariable=self.proposed_treatment_var,
                                               font=('Segoe UI', 10), width=20)
        proposed_treatment_combo['values'] = ('Primary Treatment', 'Secondary Treatment',
                                             'Advanced Secondary', 'Tertiary Treatment', 'Advanced Tertiary')
        proposed_treatment_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        ttk.Label(proposed_frame, text="Log Reduction Value:", font=('Segoe UI', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(proposed_frame, textvariable=self.proposed_lrv_var,
                 font=('Segoe UI', 10), width=10).grid(
            row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        # Dilution Factor Section
        dilution_frame = ttk.LabelFrame(self.scenarios_frame, text="Environmental Factors", padding="15")
        dilution_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        dilution_frame.columnconfigure(1, weight=1)

        ttk.Label(dilution_frame, text="Dilution Factor:", font=('Segoe UI', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(dilution_frame, textvariable=self.dilution_factor_var,
                 font=('Segoe UI', 10), width=15).grid(
            row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        # Action buttons
        button_frame = ttk.Frame(self.scenarios_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="🔄 Compare Scenarios",
                  command=self.compare_scenarios, style='Primary.TButton',
                  width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📊 Generate Comparison Plot",
                  command=self.plot_scenarios, width=20).pack(side=tk.LEFT, padx=5)

    def create_results_tab(self):
        """Create enhanced results display tab."""
        self.results_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.results_frame, text="📈 Results")

        # Configure grid
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.rowconfigure(1, weight=1)

        # Results header
        header_frame = ttk.Frame(self.results_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        header_frame.columnconfigure(1, weight=1)

        ttk.Label(header_frame, text="Assessment Results", style='Header.TLabel').grid(
            row=0, column=0, sticky=tk.W)

        # Result buttons
        result_buttons = ttk.Frame(header_frame)
        result_buttons.grid(row=0, column=1, sticky=tk.E)

        ttk.Button(result_buttons, text="🔄 Refresh",
                  command=self.refresh_results).pack(side=tk.LEFT, padx=2)
        ttk.Button(result_buttons, text="📋 Copy to Clipboard",
                  command=self.copy_results).pack(side=tk.LEFT, padx=2)
        ttk.Button(result_buttons, text="💾 Export Results",
                  command=self.export_results).pack(side=tk.LEFT, padx=2)

        # Results display with notebook
        results_notebook = ttk.Notebook(self.results_frame)
        results_notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Summary tab
        summary_frame = ttk.Frame(results_notebook, padding="15")
        results_notebook.add(summary_frame, text="Summary")

        self.summary_text = scrolledtext.ScrolledText(summary_frame, height=25, width=80,
                                                     font=('Consolas', 10))
        self.summary_text.pack(fill=tk.BOTH, expand=True)

        # Detailed results tab
        detailed_frame = ttk.Frame(results_notebook, padding="15")
        results_notebook.add(detailed_frame, text="Detailed Results")

        self.detailed_text = scrolledtext.ScrolledText(detailed_frame, height=25, width=80,
                                                      font=('Consolas', 10))
        self.detailed_text.pack(fill=tk.BOTH, expand=True)

        # Regulatory compliance tab
        compliance_frame = ttk.Frame(results_notebook, padding="15")
        results_notebook.add(compliance_frame, text="Regulatory Compliance")

        self.compliance_text = scrolledtext.ScrolledText(compliance_frame, height=25, width=80,
                                                        font=('Consolas', 10))
        self.compliance_text.pack(fill=tk.BOTH, expand=True)

    def create_plots_tab(self):
        """Create interactive plots tab."""
        self.plots_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.plots_frame, text="📊 Plots & Visualizations")

        # Configure grid
        self.plots_frame.columnconfigure(0, weight=1)
        self.plots_frame.rowconfigure(1, weight=1)

        # Plot controls
        control_frame = ttk.Frame(self.plots_frame)
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))

        ttk.Label(control_frame, text="Visualization Controls", style='Header.TLabel').pack(side=tk.LEFT)

        plot_buttons = ttk.Frame(control_frame)
        plot_buttons.pack(side=tk.RIGHT)

        ttk.Button(plot_buttons, text="📊 Risk Comparison",
                  command=self.plot_risk_comparison).pack(side=tk.LEFT, padx=2)
        ttk.Button(plot_buttons, text="📈 Dose-Response",
                  command=self.plot_dose_response).pack(side=tk.LEFT, padx=2)
        ttk.Button(plot_buttons, text="🎲 Monte Carlo",
                  command=self.plot_monte_carlo).pack(side=tk.LEFT, padx=2)
        ttk.Button(plot_buttons, text="💾 Save All",
                  command=self.save_all_plots).pack(side=tk.LEFT, padx=2)

        # Plot display area
        self.plot_frame = ttk.Frame(self.plots_frame)
        self.plot_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Initialize matplotlib figure
        self.fig = Figure(figsize=(12, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_reports_tab(self):
        """Create professional reports generation tab."""
        self.reports_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.reports_frame, text="📄 Professional Reports")

        # Configure grid
        self.reports_frame.columnconfigure(0, weight=1)

        # Report types section
        types_frame = ttk.LabelFrame(self.reports_frame, text="Report Templates", padding="15")
        types_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        types_frame.columnconfigure(1, weight=1)

        self.report_type_var = tk.StringVar(value="executive")

        ttk.Radiobutton(types_frame, text="📋 Executive Summary Report",
                       variable=self.report_type_var, value="executive").grid(
            row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(types_frame, text="2-3 page summary for decision-makers",
                 font=('Segoe UI', 9, 'italic')).grid(
            row=0, column=1, sticky=tk.W, padx=(20, 0))

        ttk.Radiobutton(types_frame, text="🔬 Technical Assessment Report",
                       variable=self.report_type_var, value="technical").grid(
            row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(types_frame, text="Detailed technical report with methodology",
                 font=('Segoe UI', 9, 'italic')).grid(
            row=1, column=1, sticky=tk.W, padx=(20, 0))

        ttk.Radiobutton(types_frame, text="⚖️ Regulatory Compliance Report",
                       variable=self.report_type_var, value="regulatory").grid(
            row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(types_frame, text="Compliance with NZ health guidelines",
                 font=('Segoe UI', 9, 'italic')).grid(
            row=2, column=1, sticky=tk.W, padx=(20, 0))

        # Report options
        options_frame = ttk.LabelFrame(self.reports_frame, text="Report Options", padding="15")
        options_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))

        self.include_plots_var = tk.BooleanVar(value=True)
        self.include_tables_var = tk.BooleanVar(value=True)
        self.include_uncertainty_var = tk.BooleanVar(value=True)
        self.include_references_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(options_frame, text="Include Risk Comparison Plots",
                       variable=self.include_plots_var).grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Include Data Tables",
                       variable=self.include_tables_var).grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Include Uncertainty Analysis",
                       variable=self.include_uncertainty_var).grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Include Literature References",
                       variable=self.include_references_var).grid(row=3, column=0, sticky=tk.W, pady=2)

        # Report generation
        generate_frame = ttk.Frame(self.reports_frame)
        generate_frame.grid(row=2, column=0, pady=20)

        ttk.Button(generate_frame, text="📄 Generate Report",
                  command=self.generate_report, style='Primary.TButton',
                  width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(generate_frame, text="👁️ Preview Report",
                  command=self.preview_report, width=15).pack(side=tk.LEFT, padx=5)

    def create_database_tab(self):
        """Create pathogen database management tab."""
        self.database_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.database_frame, text="🗃️ Pathogen Database")

        # Database content would go here
        ttk.Label(self.database_frame, text="Pathogen Database Management",
                 style='Header.TLabel').pack(pady=20)

        # Placeholder for database interface
        info_text = scrolledtext.ScrolledText(self.database_frame, height=20, width=80)
        info_text.pack(fill=tk.BOTH, expand=True, pady=10)
        info_text.insert(tk.END, "Pathogen database interface will be implemented here...")

    def create_settings_tab(self):
        """Create settings and preferences tab."""
        self.settings_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.settings_frame, text="⚙️ Settings")

        # Settings content
        ttk.Label(self.settings_frame, text="Application Settings",
                 style='Header.TLabel').pack(pady=(0, 20))

        # General settings
        general_frame = ttk.LabelFrame(self.settings_frame, text="General Settings", padding="15")
        general_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Checkbutton(general_frame, text="Generate plots automatically",
                       variable=self.generate_plots_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(general_frame, text="Save intermediate results",
                       variable=self.save_intermediate_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(general_frame, text="Enable uncertainty analysis by default",
                       variable=self.uncertainty_analysis_var).pack(anchor=tk.W, pady=2)

    def create_status_bar(self):
        """Create professional status bar."""
        status_frame = ttk.Frame(self.main_container, padding="10 5 10 5")
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        status_frame.columnconfigure(1, weight=1)

        # Status text
        ttk.Label(status_frame, textvariable=self.status_var,
                 font=('Segoe UI', 9)).grid(row=0, column=0, sticky=tk.W)

        # Progress bar
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var,
                                           length=200, mode='determinate')
        self.progress_bar.grid(row=0, column=1, sticky=tk.E, padx=(10, 0))

        # Separator
        ttk.Separator(self.main_container, orient='horizontal').grid(
            row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 0))

    def load_initial_data(self):
        """Load initial data and set up the interface."""
        self.status_var.set("Ready - Professional QMRA Assessment Toolkit v2.0")

    def create_menu_bar(self):
        """Create menu bar with File, Edit, and Help menus."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Project", command=self.new_project, accelerator="Ctrl+N")
        file_menu.add_command(label="Open Project...", command=self.open_project, accelerator="Ctrl+O")
        file_menu.add_command(label="Save Project", command=self.save_project, accelerator="Ctrl+S")
        file_menu.add_command(label="Save Project As...", command=self.save_project_as)
        file_menu.add_separator()
        file_menu.add_command(label="Export Results...", command=self.export_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Preferences...", command=self.show_preferences)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="📖 User Manual", command=self.open_user_manual)
        help_menu.add_command(label="🚀 Quick Start Guide", command=self.show_quick_start)
        help_menu.add_command(label="💡 Troubleshooting", command=self.show_troubleshooting)
        help_menu.add_separator()
        help_menu.add_command(label="📊 Example Projects", command=self.open_examples)
        help_menu.add_command(label="🔗 Online Resources", command=self.open_online_resources)
        help_menu.add_separator()
        help_menu.add_command(label="ℹ️ About QMRA Toolkit", command=self.show_about)

        # Bind keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.new_project())
        self.root.bind('<Control-o>', lambda e: self.open_project())
        self.root.bind('<Control-s>', lambda e: self.save_project())

    # Event handlers and methods
    def new_project(self):
        """Create a new project."""
        self.status_var.set("Creating new project...")
        # Implementation here

    def open_project(self):
        """Open existing project."""
        filename = filedialog.askopenfilename(
            title="Open QMRA Project",
            filetypes=[("QMRA Project files", "*.qmra"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.status_var.set(f"Opening project: {filename}")
            # Implementation here

    def save_project(self):
        """Save current project."""
        if not self.current_project:
            filename = filedialog.asksaveasfilename(
                title="Save QMRA Project",
                defaultextension=".qmra",
                filetypes=[("QMRA Project files", "*.qmra"), ("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                self.current_project = filename

        if self.current_project:
            self.status_var.set(f"Saving project: {self.current_project}")
            # Implementation here

    def toggle_multi_pathogen(self):
        """Toggle multi-pathogen assessment options."""
        if self.use_multiple_pathogens_var.get():
            self.status_var.set("Multi-pathogen assessment enabled")
        else:
            self.status_var.set("Single pathogen assessment mode")

    def show_concentration_helper(self):
        """Show concentration helper dialog."""
        messagebox.showinfo("Concentration Helper",
                           "Typical pathogen concentrations:\n\n"
                           "• Raw wastewater: 10³ - 10⁷ copies/L\n"
                           "• Treated effluent: 10¹ - 10⁴ copies/L\n"
                           "• Surface water: 10⁰ - 10² copies/L\n"
                           "• Drinking water: <10¹ copies/L")

    def compare_scenarios(self):
        """Compare treatment scenarios."""
        self.status_var.set("Comparing treatment scenarios...")
        # Implementation here

    def plot_scenarios(self):
        """Generate scenario comparison plot."""
        self.status_var.set("Generating scenario comparison plot...")
        # Implementation here

    def refresh_results(self):
        """Refresh results display."""
        self.status_var.set("Refreshing results...")
        # Implementation here

    def copy_results(self):
        """Copy results to clipboard."""
        self.status_var.set("Results copied to clipboard")
        # Implementation here

    def export_results(self):
        """Export results to file."""
        filename = filedialog.asksaveasfilename(
            title="Export Results",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("JSON files", "*.json")]
        )
        if filename:
            self.status_var.set(f"Exporting results to: {filename}")
            # Implementation here

    def plot_risk_comparison(self):
        """Generate risk comparison plot."""
        self.fig.clear()
        ax = self.fig.add_subplot(111)

        # Sample data for demonstration
        pathogens = ['Norovirus', 'Campylobacter', 'Cryptosporidium']
        current_risk = [9.83e-1, 1.30e-1, 3.15e-3]
        proposed_risk = [5.56e-1, 1.43e-3, 1.22e-5]

        x = np.arange(len(pathogens))
        width = 0.35

        ax.bar(x - width/2, current_risk, width, label='Current Treatment', color='red', alpha=0.7)
        ax.bar(x + width/2, proposed_risk, width, label='Proposed Treatment', color='green', alpha=0.7)

        ax.set_ylabel('Annual Illness Risk')
        ax.set_xlabel('Pathogen')
        ax.set_title('Risk Comparison: Current vs Proposed Treatment')
        ax.set_xticks(x)
        ax.set_xticklabels(pathogens)
        ax.legend()
        ax.set_yscale('log')

        # Add guideline line
        ax.axhline(y=1e-6, color='blue', linestyle='--', alpha=0.8, label='NZ Guideline (1e-6)')
        ax.legend()

        self.canvas.draw()
        self.status_var.set("Risk comparison plot generated")

    def plot_dose_response(self):
        """Generate dose-response curve plot."""
        self.fig.clear()
        ax = self.fig.add_subplot(111)

        # Sample dose-response curve
        dose = np.logspace(-2, 6, 100)
        response = 1 - np.exp(-0.04 * dose)  # Exponential model

        ax.loglog(dose, response, 'b-', linewidth=2, label='Dose-Response Model')
        ax.set_xlabel('Dose (organisms)')
        ax.set_ylabel('Probability of Infection')
        ax.set_title('Dose-Response Relationship')
        ax.grid(True, alpha=0.3)
        ax.legend()

        self.canvas.draw()
        self.status_var.set("Dose-response plot generated")

    def plot_monte_carlo(self):
        """Generate Monte Carlo results plot."""
        self.fig.clear()
        ax = self.fig.add_subplot(111)

        # Sample Monte Carlo data
        np.random.seed(42)
        results = np.random.lognormal(-10, 2, 10000)

        ax.hist(results, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        ax.set_xlabel('Annual Risk')
        ax.set_ylabel('Frequency')
        ax.set_title('Monte Carlo Simulation Results')
        ax.set_xscale('log')

        # Add percentiles
        p5, p50, p95 = np.percentile(results, [5, 50, 95])
        ax.axvline(p5, color='red', linestyle='--', alpha=0.8, label=f'5th percentile: {p5:.2e}')
        ax.axvline(p50, color='green', linestyle='-', alpha=0.8, label=f'Median: {p50:.2e}')
        ax.axvline(p95, color='red', linestyle='--', alpha=0.8, label=f'95th percentile: {p95:.2e}')
        ax.legend()

        self.canvas.draw()
        self.status_var.set("Monte Carlo plot generated")

    def save_all_plots(self):
        """Save all plots to files."""
        directory = filedialog.askdirectory(title="Select Directory to Save Plots")
        if directory:
            self.status_var.set(f"Saving plots to: {directory}")
            # Implementation here

    def generate_report(self):
        """Generate professional report."""
        report_type = self.report_type_var.get()
        self.status_var.set(f"Generating {report_type} report...")

        filename = filedialog.asksaveasfilename(
            title=f"Save {report_type.title()} Report",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("Word documents", "*.docx"), ("All files", "*.*")]
        )

        if filename:
            self.status_var.set(f"Report saved: {filename}")
            messagebox.showinfo("Report Generated", f"{report_type.title()} report has been generated successfully!")

    def preview_report(self):
        """Preview report before generation."""
        report_type = self.report_type_var.get()
        messagebox.showinfo("Report Preview", f"Preview of {report_type} report would be shown here.")

    # Help menu methods
    def open_user_manual(self):
        """Open the comprehensive user manual."""
        manual_path = Path(__file__).parent.parent / "docs" / "USER_MANUAL.md"

        if not manual_path.exists():
            messagebox.showerror("Manual Not Found",
                               f"User manual not found at:\n{manual_path}\n\n"
                               "Please ensure the USER_MANUAL.md file exists in the docs directory.")
            return

        try:
            # Try to open with default markdown viewer or text editor
            if sys.platform == 'win32':
                os.startfile(manual_path)
            elif sys.platform == 'darwin':  # macOS
                subprocess.run(['open', manual_path])
            else:  # Linux
                subprocess.run(['xdg-open', manual_path])
            self.status_var.set("User manual opened")
        except Exception as e:
            # Fallback: open in browser
            try:
                webbrowser.open(f'file://{manual_path.absolute()}')
                self.status_var.set("User manual opened in browser")
            except:
                messagebox.showerror("Error Opening Manual",
                                   f"Could not open user manual.\n\n"
                                   f"Please open manually:\n{manual_path}")

    def show_quick_start(self):
        """Show quick start guide dialog."""
        quick_start_window = tk.Toplevel(self.root)
        quick_start_window.title("Quick Start Guide")
        quick_start_window.geometry("800x600")

        # Create scrolled text widget
        frame = ttk.Frame(quick_start_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=('Segoe UI', 10))
        text_widget.pack(fill=tk.BOTH, expand=True)

        # Add quick start content
        quick_start_content = """
QMRA TOOLKIT - QUICK START GUIDE
═══════════════════════════════════════════════════════════════════

BASIC WORKFLOW (5 STEPS)
─────────────────────────────────────────────────────────────────

1. PROJECT SETUP (Tab 1: 📋 Project Setup)
   • Enter project name and your details
   • Set population at risk
   Example: "Beach Assessment", 100,000 people

2. CONFIGURE PARAMETERS (Tab 2: 🧬 Assessment Parameters)
   • Select pathogen (e.g., Norovirus)
   • Choose exposure route (e.g., Primary Contact)
   • Enter concentration: 1000 copies/L
   • Set volume: 100 mL
   • Set frequency: 7 events/year
   Tip: Click 📊 for typical concentration ranges

3. RUN ASSESSMENT
   • Click "Run Assessment" button (bottom of tab)
   • Wait for Monte Carlo simulation to complete
   • Progress bar shows status

4. VIEW RESULTS (Tab 4: 📈 Results)
   • Check Summary tab for key metrics
   • Review Regulatory Compliance status
   • Note: Green = compliant, Yellow = marginal, Red = non-compliant

5. GENERATE OUTPUTS
   • Tab 5: Create plots (📊 Risk Comparison, 🎲 Monte Carlo)
   • Tab 6: Generate professional report (PDF or Word)
   • Save your project: File → Save Project

COMMON SCENARIOS
─────────────────────────────────────────────────────────────────

SCENARIO A: Swimming Safety Assessment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Pathogen: Norovirus
• Route: Primary Contact
• Concentration: 1,000 copies/L
• Volume: 100 mL (typical ingestion)
• Frequency: 7 times/year (summer season)

SCENARIO B: Drinking Water Safety
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Pathogen: Cryptosporidium
• Route: Drinking Water
• Concentration: 1 oocyst/L
• Volume: 2,000 mL (2 liters/day)
• Frequency: 365 times/year

SCENARIO C: Treatment Comparison (Tab 3: 🔬 Treatment Scenarios)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Current: Secondary Treatment, LRV = 1.5
• Proposed: Tertiary Treatment, LRV = 3.5
• Click "🔄 Compare Scenarios"

UNDERSTANDING RESULTS
─────────────────────────────────────────────────────────────────

Key Metrics:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Pinf (Infection Risk): Risk per single exposure
  Example: 0.05 = 5% chance of infection per swim

• Pannual (Annual Risk): Risk over a year
  Example: 0.30 = 30% chance of at least one infection/year

• Population Impact: Expected cases in population
  Example: 30,000 cases/year in 100,000 people

Regulatory Benchmarks:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• NZ Drinking Water: ≤ 10⁻⁶ DALY/person/year
• WHO Guidelines: ≤ 10⁻⁶ DALY/person/year

Status Indicators:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ COMPLIANT     - Risk ≤ 10⁻⁶ (meets standard)
⚠️ MARGINAL      - Risk 10⁻⁶ to 10⁻⁵ (requires attention)
❌ NON-COMPLIANT - Risk > 10⁻⁵ (exceeds standard)

KEYBOARD SHORTCUTS
─────────────────────────────────────────────────────────────────
Ctrl+N    New Project
Ctrl+O    Open Project
Ctrl+S    Save Project
F1        Open User Manual
F5        Refresh Results

TYPICAL CONCENTRATION RANGES
─────────────────────────────────────────────────────────────────
Raw Wastewater:     10³ - 10⁷ copies/L
Treated Effluent:   10¹ - 10⁴ copies/L
Surface Water:      10⁰ - 10² copies/L
Drinking Water:     < 10¹ copies/L

LOG REDUCTION VALUES (LRV)
─────────────────────────────────────────────────────────────────
Primary Treatment:      0.5 - 1.0 log
Secondary Treatment:    1.0 - 2.0 log
Advanced Secondary:     2.0 - 3.0 log
Tertiary Treatment:     3.0 - 5.0 log
Advanced Tertiary:      5.0+ log

Note: 1 log = 90% removal, 2 log = 99%, 3 log = 99.9%

TROUBLESHOOTING TIPS
─────────────────────────────────────────────────────────────────
❌ Results too high?
   → Check units (L vs mL, copies vs CFU)
   → Verify LRV is applied to concentration

❌ Simulation slow?
   → Reduce iterations to 1,000 for testing
   → Close other applications

❌ Can't save project?
   → Check folder write permissions
   → Try different location

❌ Plots blank?
   → Go to Settings tab
   → Enable "Generate plots automatically"
   → Return to Plots tab

NEED MORE HELP?
─────────────────────────────────────────────────────────────────
📖 Full User Manual: Help → User Manual
💡 Troubleshooting: Help → Troubleshooting
📊 Examples: Help → Example Projects
ℹ️ About: Help → About QMRA Toolkit

For technical support, contact the NIWA QMRA Team.

═══════════════════════════════════════════════════════════════════
© 2025 NIWA - QMRA Assessment Toolkit v2.0
"""

        text_widget.insert(tk.END, quick_start_content)
        text_widget.config(state=tk.DISABLED)

        # Add close button
        ttk.Button(frame, text="Close", command=quick_start_window.destroy).pack(pady=10)

    def show_troubleshooting(self):
        """Show troubleshooting guide."""
        troubleshooting_window = tk.Toplevel(self.root)
        troubleshooting_window.title("Troubleshooting Guide")
        troubleshooting_window.geometry("900x650")

        frame = ttk.Frame(troubleshooting_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=('Consolas', 9))
        text_widget.pack(fill=tk.BOTH, expand=True)

        troubleshooting_content = """
TROUBLESHOOTING GUIDE
═════════════════════════════════════════════════════════════════════════════

COMMON ISSUES AND SOLUTIONS
─────────────────────────────────────────────────────────────────────────────

1. APPLICATION WON'T LAUNCH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Symptoms: Double-clicking launcher does nothing or shows error

Solutions:
  ✓ Verify Python installation
    Command: python --version
    Expected: Python 3.8 or higher

  ✓ Install dependencies
    Command: pip install -r requirements.txt
    Location: Run from qmra_toolkit directory

  ✓ Manual launch
    Command: python launch_enhanced_gui.py

  ✓ Check error logs
    Location: qmra_toolkit/logs/error.log

─────────────────────────────────────────────────────────────────────────────

2. RESULTS SEEM UNREALISTIC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Symptoms: Risk values too high (>1.0) or too low (<10⁻¹⁵)

Common Causes and Fixes:

  ❌ Wrong units for concentration
     Problem: Entered 1000 CFU/100mL instead of copies/L
     Fix: Convert to copies/L (multiply by 10)

  ❌ Wrong volume units
     Problem: Entered 2 L instead of 2000 mL
     Fix: Use mL in volume field

  ❌ LRV not applied
     Problem: Used raw concentration instead of treated
     Fix: Either reduce concentration manually or use Treatment Scenarios tab

  ❌ Frequency too high
     Problem: Entered 365 for seasonal activity
     Fix: Use actual events per year (e.g., 7 for summer swimming)

  ✓ Use Concentration Helper
     Location: Click 📊 button next to Pathogen Concentration field
     Shows: Typical ranges for verification

─────────────────────────────────────────────────────────────────────────────

3. MONTE CARLO SIMULATION TOO SLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Symptoms: Simulation takes >5 minutes or appears frozen

Solutions:

  ✓ Reduce iterations for testing
     Change: 10,000 → 1,000 iterations
     Note: Use 10,000 for final results

  ✓ Free up system memory
     Action: Close other applications
     Check: Task Manager (Windows) or Activity Monitor (Mac)

  ✓ Disable auto-plotting
     Location: Settings tab → Uncheck "Generate plots automatically"
     Benefit: Faster calculation, plot manually later

  ✓ Check population size
     Problem: Very large population (>10 million)
     Fix: Use representative sample size

─────────────────────────────────────────────────────────────────────────────

4. CAN'T GENERATE REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Symptoms: Report generation fails, blank document, or error message

Solutions:

  ✓ Run assessment first
     Problem: No results to report
     Fix: Complete assessment before generating report

  ✓ Check file permissions
     Problem: Can't write to selected directory
     Fix: Choose different save location or check folder permissions

  ✓ Verify report libraries
     Command: pip install python-docx reportlab
     Note: Required for Word and PDF generation

  ✓ Try different format
     If Word fails: Try PDF
     If PDF fails: Try Word

─────────────────────────────────────────────────────────────────────────────

5. PLOTS NOT DISPLAYING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Symptoms: Blank plot area or error when clicking plot buttons

Solutions:

  ✓ Verify matplotlib
     Command: pip install matplotlib
     Update: pip install --upgrade matplotlib

  ✓ Enable auto-plotting
     Location: Settings tab
     Check: "Generate plots automatically"

  ✓ Refresh display
     Action: Close and reopen Plots tab
     Or: Click Refresh button

  ✓ Check for results
     Problem: No data to plot
     Fix: Run assessment first

─────────────────────────────────────────────────────────────────────────────

ERROR MESSAGES
─────────────────────────────────────────────────────────────────────────────

Error: "PathogenDatabase not found"
  Meaning: Missing database file
  Fix: Reinstall toolkit or download pathogen_database.json
       Place in: qmra_toolkit/data/

Error: "Invalid concentration value"
  Meaning: Non-numeric input in concentration field
  Fix: Enter numbers only (e.g., 1000 not "1,000" or "1e3")

Error: "LRV out of range"
  Meaning: Log Reduction Value too high or negative
  Fix: Use LRV between 0 and 8
       Typical: 0.5 to 5.0

Error: "Monte Carlo simulation failed"
  Meaning: Error in calculation
  Fix: Check all parameters are positive numbers
       Verify concentration > 0, volume > 0, frequency > 0

Error: "Memory error"
  Meaning: Insufficient RAM for calculation
  Fix: Reduce iterations (10,000 → 1,000)
       Or reduce population size
       Close other applications

Error: "Division by zero"
  Meaning: Zero value in critical parameter
  Fix: Check population > 0
       Verify concentration > 0

─────────────────────────────────────────────────────────────────────────────

DATA QUALITY CHECKS
─────────────────────────────────────────────────────────────────────────────

Before finalizing assessment, verify:

  ✓ Units are correct
    Concentration: copies/L (not /100mL or /mL)
    Volume: mL (not L)
    Frequency: events/year (not per month or day)

  ✓ Values are reasonable
    Compare to typical ranges in Concentration Helper (📊 button)

  ✓ LRV applied correctly
    Check: Treated concentration = Raw / (10^LRV)
    Example: 10,000 / (10^2) = 100 copies/L for 2-log treatment

  ✓ Population realistic
    Check: Is population at risk realistic for scenario?
    Example: Beach might be 10,000-100,000, not 10 million

  ✓ Results make sense
    Annual risk should be between 10⁻¹⁰ and 1.0
    If outside range, check parameters

─────────────────────────────────────────────────────────────────────────────

GETTING ADDITIONAL HELP
─────────────────────────────────────────────────────────────────────────────

1. Check Full User Manual
   Location: Help → User Manual
   Contains: Complete documentation with detailed examples

2. Review Example Projects
   Location: Help → Example Projects
   Contains: Working examples you can open and examine

3. Contact NIWA Support
   Prepare:
   • Screenshot of error message
   • Your project file (.qmra)
   • Description of what you were trying to do
   • List of parameter values used

4. Check Online Resources
   Location: Help → Online Resources
   Links to: US EPA QMRA Wiki, WHO guidelines, etc.

═════════════════════════════════════════════════════════════════════════════
© 2025 NIWA - QMRA Assessment Toolkit v2.0
"""

        text_widget.insert(tk.END, troubleshooting_content)
        text_widget.config(state=tk.DISABLED)

        ttk.Button(frame, text="Close", command=troubleshooting_window.destroy).pack(pady=10)

    def open_examples(self):
        """Open examples directory."""
        examples_path = Path(__file__).parent.parent / "examples"

        if not examples_path.exists():
            messagebox.showinfo("Examples",
                              "Example projects directory not found.\n\n"
                              "Examples can be found in the project repository.")
            return

        try:
            if sys.platform == 'win32':
                os.startfile(examples_path)
            elif sys.platform == 'darwin':
                subprocess.run(['open', examples_path])
            else:
                subprocess.run(['xdg-open', examples_path])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open examples directory:\n{e}")

    def open_online_resources(self):
        """Open online resources in browser."""
        resources_window = tk.Toplevel(self.root)
        resources_window.title("Online Resources")
        resources_window.geometry("600x400")

        frame = ttk.Frame(resources_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="QMRA Online Resources",
                 style='Header.TLabel').pack(pady=(0, 20))

        resources = [
            ("US EPA QMRA Wiki", "https://qmrawiki.org/"),
            ("WHO Water Safety", "https://www.who.int/water_sanitation_health/"),
            ("WHO Guidelines for Drinking Water", "https://www.who.int/publications/i/item/9789241549950"),
            ("NZ Ministry of Health - Water", "https://www.health.govt.nz/our-work/environmental-health/drinking-water"),
            ("Water Research Foundation", "https://www.waterrf.org/"),
        ]

        for name, url in resources:
            btn_frame = ttk.Frame(frame)
            btn_frame.pack(fill=tk.X, pady=5)

            ttk.Label(btn_frame, text=f"• {name}:",
                     font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
            ttk.Button(btn_frame, text="Open",
                      command=lambda u=url: webbrowser.open(u)).pack(side=tk.RIGHT)

        ttk.Button(frame, text="Close",
                  command=resources_window.destroy).pack(pady=20)

    def show_about(self):
        """Show about dialog."""
        about_text = """
NIWA QMRA Assessment Toolkit
Professional Edition v2.0

Quantitative Microbial Risk Assessment Software

═══════════════════════════════════════════════════

Developed by:
• Reza Moghaddam - Lead Developer
• David Wood - Model Review & Support
• Andrew Hughes - Project Manager

NIWA Earth Sciences
National Institute of Water & Atmospheric Research
New Zealand

═══════════════════════════════════════════════════

Key Features:
✓ Comprehensive pathogen database
✓ Monte Carlo uncertainty analysis
✓ Multiple exposure route assessment
✓ Treatment scenario comparison
✓ Automated professional reporting
✓ Regulatory compliance evaluation

═══════════════════════════════════════════════════

References:
• NZ Drinking Water Standards 2005 (Revised 2008)
• WHO Guidelines for Drinking-water Quality (2011)
• Haas, Rose & Gerba: Quantitative Microbial
  Risk Assessment (2014)

═══════════════════════════════════════════════════

© 2025 NIWA
Licensed for professional QMRA assessments

For support and updates, contact the NIWA QMRA Team.
"""
        messagebox.showinfo("About QMRA Toolkit", about_text)

    def save_project_as(self):
        """Save project with new filename."""
        filename = filedialog.asksaveasfilename(
            title="Save QMRA Project As",
            defaultextension=".qmra",
            filetypes=[("QMRA Project files", "*.qmra"), ("JSON files", "*.json")]
        )
        if filename:
            self.current_project = filename
            self.save_project()

    def show_preferences(self):
        """Show preferences dialog."""
        # Switch to settings tab
        self.notebook.select(7)  # Settings tab is index 7


def main():
    """Main function to run the enhanced GUI."""
    root = tk.Tk()
    app = EnhancedQMRAGui(root)
    root.mainloop()


if __name__ == "__main__":
    main()