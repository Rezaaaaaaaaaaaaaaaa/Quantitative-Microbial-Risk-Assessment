"""
QMRA Assessment Toolkit - Graphical User Interface
A user-friendly GUI for conducting quantitative microbial risk assessments
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Import QMRA modules
sys.path.insert(0, os.path.dirname(__file__))
from pathogen_database import PathogenDatabase
from exposure_assessment import create_exposure_assessment, ExposureRoute
from risk_characterization import RiskCharacterization
from report_generator import ReportGenerator

class QMRAGui:
    def __init__(self, root):
        self.root = root
        self.root.title("QMRA Assessment Toolkit - NIWA")
        self.root.geometry("1000x800")
        self.root.minsize(800, 600)

        # Initialize QMRA components
        try:
            self.pathogen_db = PathogenDatabase()
            self.risk_calc = RiskCharacterization(self.pathogen_db)
            self.report_gen = ReportGenerator()
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Failed to initialize QMRA components: {e}")
            return

        # Variables for form data
        self.pathogen_var = tk.StringVar()
        self.exposure_route_var = tk.StringVar()
        self.concentration_var = tk.DoubleVar()
        self.volume_var = tk.DoubleVar()
        self.frequency_var = tk.DoubleVar()
        self.population_var = tk.IntVar()
        self.iterations_var = tk.IntVar()

        # Results storage
        self.current_results = None

        # Set default values
        self.set_default_values()

        # Create GUI elements
        self.create_widgets()

        # Load available pathogens
        self.load_pathogens()

    def set_default_values(self):
        """Set default values for the form."""
        self.pathogen_var.set("norovirus")
        self.exposure_route_var.set("primary_contact")
        self.concentration_var.set(10.0)
        self.volume_var.set(50.0)
        self.frequency_var.set(10.0)
        self.population_var.set(10000)
        self.iterations_var.set(10000)

    def create_widgets(self):
        """Create all GUI widgets."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="QMRA Assessment Toolkit",
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Subtitle
        subtitle_label = ttk.Label(main_frame, text="Quantitative Microbial Risk Assessment - NIWA",
                                  font=('Arial', 10, 'italic'))
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))

        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.rowconfigure(2, weight=1)

        # Assessment tab
        self.assessment_frame = ttk.Frame(notebook, padding="10")
        notebook.add(self.assessment_frame, text="Risk Assessment")

        # Results tab
        self.results_frame = ttk.Frame(notebook, padding="10")
        notebook.add(self.results_frame, text="Results")

        # Pathogen Info tab
        self.info_frame = ttk.Frame(notebook, padding="10")
        notebook.add(self.info_frame, text="Pathogen Database")

        # Create assessment widgets
        self.create_assessment_widgets()

        # Create results widgets
        self.create_results_widgets()

        # Create pathogen info widgets
        self.create_info_widgets()

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var,
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))

    def create_assessment_widgets(self):
        """Create widgets for the assessment tab."""
        # Pathogen selection
        ttk.Label(self.assessment_frame, text="Pathogen:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.pathogen_combo = ttk.Combobox(self.assessment_frame, textvariable=self.pathogen_var,
                                          state="readonly", width=20)
        self.pathogen_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        self.pathogen_combo.bind('<<ComboboxSelected>>', self.on_pathogen_changed)

        # Exposure route selection
        ttk.Label(self.assessment_frame, text="Exposure Route:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.route_combo = ttk.Combobox(self.assessment_frame, textvariable=self.exposure_route_var,
                                       state="readonly", width=20)
        self.route_combo['values'] = ('primary_contact', 'shellfish_consumption')
        self.route_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        self.route_combo.bind('<<ComboboxSelected>>', self.on_route_changed)

        # Concentration
        ttk.Label(self.assessment_frame, text="Concentration (org/100mL):").grid(row=2, column=0, sticky=tk.W, pady=2)
        conc_entry = ttk.Entry(self.assessment_frame, textvariable=self.concentration_var, width=20)
        conc_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))

        # Volume/Consumption
        self.volume_label = ttk.Label(self.assessment_frame, text="Volume per event (mL):")
        self.volume_label.grid(row=3, column=0, sticky=tk.W, pady=2)
        volume_entry = ttk.Entry(self.assessment_frame, textvariable=self.volume_var, width=20)
        volume_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))

        # Frequency
        self.frequency_label = ttk.Label(self.assessment_frame, text="Frequency (events/year):")
        self.frequency_label.grid(row=4, column=0, sticky=tk.W, pady=2)
        freq_entry = ttk.Entry(self.assessment_frame, textvariable=self.frequency_var, width=20)
        freq_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))

        # Population
        ttk.Label(self.assessment_frame, text="Population Size:").grid(row=5, column=0, sticky=tk.W, pady=2)
        pop_entry = ttk.Entry(self.assessment_frame, textvariable=self.population_var, width=20)
        pop_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))

        # Monte Carlo iterations
        ttk.Label(self.assessment_frame, text="Monte Carlo Iterations:").grid(row=6, column=0, sticky=tk.W, pady=2)
        iter_entry = ttk.Entry(self.assessment_frame, textvariable=self.iterations_var, width=20)
        iter_entry.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))

        # Buttons frame
        button_frame = ttk.Frame(self.assessment_frame)
        button_frame.grid(row=7, column=0, columnspan=3, pady=20)

        # Run Assessment button
        self.run_button = ttk.Button(button_frame, text="Run Assessment",
                                    command=self.run_assessment, style="Accent.TButton")
        self.run_button.pack(side=tk.LEFT, padx=5)

        # Generate Report button
        self.report_button = ttk.Button(button_frame, text="Generate Report",
                                       command=self.generate_report, state=tk.DISABLED)
        self.report_button.pack(side=tk.LEFT, padx=5)

        # Save Results button
        self.save_button = ttk.Button(button_frame, text="Save Results",
                                     command=self.save_results, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Progress bar
        self.progress = ttk.Progressbar(self.assessment_frame, mode='indeterminate')
        self.progress.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        # Configure column weight
        self.assessment_frame.columnconfigure(1, weight=1)

    def create_results_widgets(self):
        """Create widgets for the results tab."""
        # Results text area
        self.results_text = scrolledtext.ScrolledText(self.results_frame, height=30, width=80)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        # Configure grid weights
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.rowconfigure(0, weight=1)

    def create_info_widgets(self):
        """Create widgets for the pathogen info tab."""
        # Pathogen selection for info
        info_frame = ttk.Frame(self.info_frame)
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(info_frame, text="Select Pathogen:").pack(side=tk.LEFT, padx=(0, 10))

        self.info_pathogen_var = tk.StringVar()
        info_combo = ttk.Combobox(info_frame, textvariable=self.info_pathogen_var,
                                 state="readonly", width=20)
        info_combo.pack(side=tk.LEFT, padx=(0, 10))
        info_combo.bind('<<ComboboxSelected>>', self.show_pathogen_info)

        # Info display area
        self.info_text = scrolledtext.ScrolledText(self.info_frame, height=25, width=80)
        self.info_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        # Configure grid weights
        self.info_frame.columnconfigure(0, weight=1)
        self.info_frame.rowconfigure(1, weight=1)

        # Store combo reference for loading pathogens
        self.info_combo = info_combo

    def load_pathogens(self):
        """Load available pathogens into combo boxes."""
        try:
            pathogens = self.pathogen_db.get_available_pathogens()
            self.pathogen_combo['values'] = pathogens
            self.info_combo['values'] = pathogens

            # Set default selections
            if pathogens:
                self.pathogen_var.set(pathogens[0])
                self.info_pathogen_var.set(pathogens[0])
                self.show_pathogen_info()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load pathogens: {e}")

    def on_pathogen_changed(self, event=None):
        """Handle pathogen selection change."""
        self.update_status(f"Selected pathogen: {self.pathogen_var.get()}")

    def on_route_changed(self, event=None):
        """Handle exposure route change and update labels."""
        route = self.exposure_route_var.get()

        if route == "primary_contact":
            self.volume_label.config(text="Volume per event (mL):")
            self.frequency_label.config(text="Frequency (events/year):")
            self.volume_var.set(50.0)
            self.frequency_var.set(10.0)
        elif route == "shellfish_consumption":
            self.volume_label.config(text="Consumption per serving (g):")
            self.frequency_label.config(text="Servings per year:")
            self.volume_var.set(150.0)
            self.frequency_var.set(12.0)

    def show_pathogen_info(self, event=None):
        """Display information about the selected pathogen."""
        try:
            pathogen_name = self.info_pathogen_var.get()
            if not pathogen_name:
                return

            pathogen_info = self.pathogen_db.get_pathogen_info(pathogen_name)

            # Format pathogen information
            info_text = f"Pathogen Information: {pathogen_info['name']}\n"
            info_text += "=" * 50 + "\n\n"

            info_text += f"Type: {pathogen_info.get('pathogen_type', 'Unknown')}\n\n"

            # Dose-response models
            info_text += "Dose-Response Models:\n"
            info_text += "-" * 20 + "\n"

            for model_name, model_data in pathogen_info.get('dose_response_models', {}).items():
                info_text += f"\n{model_name.upper()} Model:\n"

                if model_name == 'beta_poisson':
                    info_text += f"  α (alpha): {model_data.get('alpha', 'N/A')}\n"
                    info_text += f"  β (beta): {model_data.get('beta', 'N/A')}\n"
                elif model_name == 'exponential':
                    info_text += f"  r: {model_data.get('r', 'N/A')}\n"

                info_text += f"  Source: {model_data.get('source', 'N/A')}\n"
                info_text += f"  Notes: {model_data.get('notes', 'N/A')}\n"

            # Health impact data
            info_text += f"\nHealth Impact Data:\n"
            info_text += "-" * 20 + "\n"
            info_text += f"Illness-to-Infection Ratio: {pathogen_info.get('illness_to_infection_ratio', 'N/A')}\n"
            info_text += f"DALYs per Case: {pathogen_info.get('dalys_per_case', 'N/A')}\n"

            # Exposure routes
            info_text += f"\nValid Exposure Routes:\n"
            info_text += "-" * 20 + "\n"
            for route in pathogen_info.get('exposure_routes', []):
                info_text += f"  • {route}\n"

            # Environmental data
            env_data = pathogen_info.get('environmental_data', {})
            if env_data:
                info_text += f"\nEnvironmental Data:\n"
                info_text += "-" * 20 + "\n"
                info_text += f"Survival Time: {env_data.get('survival_time_days', 'N/A')} days\n"
                info_text += f"Inactivation Rate: {env_data.get('inactivation_rate_per_day', 'N/A')} per day\n"

                # Typical concentrations
                conc_data = env_data.get('typical_concentrations', {})
                if conc_data:
                    info_text += f"\nTypical Concentrations:\n"
                    for matrix, conc in conc_data.items():
                        info_text += f"  {matrix.replace('_', ' ').title()}: {conc} org/L\n"

            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, info_text)

        except Exception as e:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, f"Error loading pathogen information: {e}")

    def run_assessment(self):
        """Run the QMRA assessment in a separate thread."""
        # Validate inputs
        if not self.validate_inputs():
            return

        # Disable run button and show progress
        self.run_button.config(state=tk.DISABLED)
        self.progress.start()
        self.update_status("Running assessment...")

        # Run assessment in separate thread
        thread = threading.Thread(target=self._run_assessment_thread)
        thread.daemon = True
        thread.start()

    def _run_assessment_thread(self):
        """Run assessment in background thread."""
        try:
            # Get form values
            pathogen = self.pathogen_var.get()
            route = self.exposure_route_var.get()
            concentration = self.concentration_var.get()
            volume = self.volume_var.get()
            frequency = self.frequency_var.get()
            population = self.population_var.get()
            iterations = self.iterations_var.get()

            # Create exposure assessment
            route_enum = ExposureRoute.PRIMARY_CONTACT if route == "primary_contact" else ExposureRoute.SHELLFISH_CONSUMPTION

            if route == "primary_contact":
                params = {
                    "water_ingestion_volume": volume,
                    "exposure_frequency": frequency
                }
            else:
                params = {
                    "shellfish_consumption": volume,
                    "consumption_frequency": frequency
                }

            exposure_model = create_exposure_assessment(route_enum, params)
            exposure_model.set_pathogen_concentration(concentration)

            # Run comprehensive assessment
            results = self.risk_calc.run_comprehensive_assessment(
                pathogen_name=pathogen,
                exposure_assessment=exposure_model,
                population_size=population,
                n_samples=iterations
            )

            # Store results
            self.current_results = results

            # Update GUI in main thread
            self.root.after(0, self._update_results, results)

        except Exception as e:
            self.root.after(0, self._handle_error, str(e))

    def _update_results(self, results):
        """Update results display (called from main thread)."""
        try:
            # Format results
            results_text = f"QMRA Assessment Results\n"
            results_text += "=" * 50 + "\n\n"

            results_text += f"Assessment Parameters:\n"
            results_text += f"  Pathogen: {self.pathogen_var.get()}\n"
            results_text += f"  Exposure Route: {self.exposure_route_var.get()}\n"
            results_text += f"  Concentration: {self.concentration_var.get()} org/100mL\n"
            results_text += f"  Volume: {self.volume_var.get()} {'mL' if self.exposure_route_var.get() == 'primary_contact' else 'g'}\n"
            results_text += f"  Frequency: {self.frequency_var.get()} events/year\n"
            results_text += f"  Population: {self.population_var.get():,}\n"
            results_text += f"  Monte Carlo Iterations: {self.iterations_var.get():,}\n\n"

            # Risk metrics
            for metric_name, result in results.items():
                results_text += f"{metric_name.replace('_', ' ').title()}:\n"
                results_text += f"  Mean: {result.statistics['mean']:.2e}\n"
                results_text += f"  Median: {result.statistics['median']:.2e}\n"
                results_text += f"  95th Percentile: {result.statistics['p95']:.2e}\n"

                if result.population_risks:
                    expected_cases = result.population_risks['expected_cases_per_year']
                    results_text += f"  Expected cases per year: {expected_cases:.1f}\n"

                results_text += "\n"

            # Regulatory compliance
            if 'annual_risk' in results:
                annual_result = results['annual_risk']
                compliance = self.risk_calc.evaluate_regulatory_compliance(annual_result)

                results_text += "Regulatory Compliance:\n"
                for threshold, compliant in compliance.items():
                    status = "PASS" if compliant else "FAIL"
                    results_text += f"  {threshold}: {status}\n"

            # Update results display
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(1.0, results_text)

            # Enable buttons
            self.report_button.config(state=tk.NORMAL)
            self.save_button.config(state=tk.NORMAL)

            self.update_status("Assessment completed successfully")

        except Exception as e:
            self._handle_error(f"Error updating results: {e}")
        finally:
            # Re-enable run button and stop progress
            self.run_button.config(state=tk.NORMAL)
            self.progress.stop()

    def _handle_error(self, error_message):
        """Handle errors (called from main thread)."""
        self.run_button.config(state=tk.NORMAL)
        self.progress.stop()
        self.update_status("Assessment failed")
        messagebox.showerror("Assessment Error", error_message)

    def validate_inputs(self):
        """Validate user inputs."""
        try:
            if not self.pathogen_var.get():
                raise ValueError("Please select a pathogen")

            if not self.exposure_route_var.get():
                raise ValueError("Please select an exposure route")

            if self.concentration_var.get() <= 0:
                raise ValueError("Concentration must be positive")

            if self.volume_var.get() <= 0:
                raise ValueError("Volume/consumption must be positive")

            if self.frequency_var.get() <= 0:
                raise ValueError("Frequency must be positive")

            if self.population_var.get() <= 0:
                raise ValueError("Population size must be positive")

            if self.iterations_var.get() < 1000:
                raise ValueError("Monte Carlo iterations should be at least 1000")

            return True

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return False

    def generate_report(self):
        """Generate a Word report from current results."""
        if not self.current_results:
            messagebox.showwarning("No Results", "Please run an assessment first")
            return

        try:
            # Get save location
            filename = filedialog.asksaveasfilename(
                defaultextension=".docx",
                filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")],
                title="Save Report As"
            )

            if not filename:
                return

            self.update_status("Generating report...")

            # Project information
            project_info = {
                'title': f'QMRA Assessment - {self.pathogen_var.get().title()}',
                'project_name': 'QMRA Toolkit Assessment',
                'location': 'Generated via QMRA GUI',
                'client': 'NIWA',
                'assessment_date': datetime.now().strftime('%B %d, %Y'),
                'pathogen': self.pathogen_var.get(),
                'exposure_route': self.exposure_route_var.get(),
                'concentration': self.concentration_var.get(),
                'volume': self.volume_var.get(),
                'frequency': self.frequency_var.get(),
                'population': self.population_var.get()
            }

            # Generate report
            self.report_gen.create_regulatory_report(
                project_info=project_info,
                risk_results=self.current_results,
                exposure_params=project_info,
                output_file=filename
            )

            self.update_status(f"Report saved: {filename}")
            messagebox.showinfo("Report Generated", f"Report saved successfully:\n{filename}")

        except Exception as e:
            messagebox.showerror("Report Error", f"Failed to generate report: {e}")
            self.update_status("Report generation failed")

    def save_results(self):
        """Save results to JSON file."""
        if not self.current_results:
            messagebox.showwarning("No Results", "Please run an assessment first")
            return

        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
                title="Save Results As"
            )

            if not filename:
                return

            # Convert results to serializable format
            results_dict = {}
            for metric_name, result in self.current_results.items():
                results_dict[metric_name] = {
                    "pathogen": result.pathogen_name,
                    "risk_metric": result.risk_metric.value,
                    "statistics": result.statistics,
                    "population_risks": result.population_risks
                }

            # Add assessment parameters
            results_dict["assessment_parameters"] = {
                "pathogen": self.pathogen_var.get(),
                "exposure_route": self.exposure_route_var.get(),
                "concentration": self.concentration_var.get(),
                "volume": self.volume_var.get(),
                "frequency": self.frequency_var.get(),
                "population": self.population_var.get(),
                "iterations": self.iterations_var.get(),
                "timestamp": datetime.now().isoformat()
            }

            # Save to file
            with open(filename, 'w') as f:
                json.dump(results_dict, f, indent=2, default=str)

            self.update_status(f"Results saved: {filename}")
            messagebox.showinfo("Results Saved", f"Results saved successfully:\n{filename}")

        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save results: {e}")

    def update_status(self, message):
        """Update status bar message."""
        self.status_var.set(message)

def main():
    """Run the QMRA GUI application."""
    root = tk.Tk()

    # Set up styling
    style = ttk.Style()

    # Configure styles
    style.configure("Accent.TButton", foreground="white", background="#0078d4")

    # Create and run application
    app = QMRAGui(root)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.quit()

if __name__ == "__main__":
    main()