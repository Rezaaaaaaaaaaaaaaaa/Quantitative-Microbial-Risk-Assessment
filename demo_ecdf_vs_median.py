"""
Demonstration: ECDF vs Median-Only Approach

Shows why using the full ECDF distribution from hydrodynamic data
is better than using only the median value.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Batch_Processing_App'))

from qmra_core.monte_carlo import (
    MonteCarloSimulator,
    create_empirical_cdf_from_data,
    create_hockey_stick_distribution
)

print("=" * 80)
print("DEMONSTRATION: Impact of Using Full ECDF vs. Median-Only")
print("=" * 80)

# Load actual dilution data from your spatial file
dilution_file = "Batch_Processing_App/input_data/dilution_data/spatial_dilution_6_sites.csv"

if os.path.exists(dilution_file):
    dilution_df = pd.read_csv(dilution_file)

    # Focus on one site
    site_name = "Site_50m"
    site_data = dilution_df[dilution_df['Site_Name'] == site_name]['Dilution_Factor'].values

    print(f"\nAnalyzing: {site_name}")
    print(f"Number of hydrodynamic simulations: {len(site_data)}")
    print(f"Dilution range: {site_data.min():.2f} to {site_data.max():.2f}")
    print(f"Median dilution: {np.median(site_data):.2f}")
    print(f"Mean dilution: {np.mean(site_data):.2f}")
    print(f"Std deviation: {np.std(site_data):.2f}")
else:
    # Use simulated data if file not found
    print("\n[Using simulated dilution data for demonstration]")
    site_name = "Simulated_Site"
    np.random.seed(42)
    site_data = np.random.lognormal(mean=np.log(7.5), sigma=0.5, size=100)

# Setup QMRA parameters
pathogen_min = 1e4
pathogen_median = 1e6
pathogen_max = 1e8
treatment_lrv = 3.0
n_iterations = 10000

print(f"\nQMRA Parameters:")
print(f"  Pathogen concentration: Hockey Stick (min={pathogen_min:.0e}, median={pathogen_median:.0e}, max={pathogen_max:.0e})")
print(f"  Treatment LRV: {treatment_lrv}")
print(f"  Monte Carlo iterations: {n_iterations:,}")

# === APPROACH 1: Current Method (Median Only) ===
print(f"\n{'-'*80}")
print("APPROACH 1: Current Method (Using Median Dilution Only)")
print(f"{'-'*80}")

median_dilution = np.median(site_data)
print(f"Using single dilution value: {median_dilution:.2f}")

mc1 = MonteCarloSimulator(random_seed=42)

# Add pathogen distribution
pathogen_dist = create_hockey_stick_distribution(
    x_min=pathogen_min,
    x_median=pathogen_median,
    x_max=pathogen_max,
    name="pathogen"
)
mc1.add_distribution("pathogen", pathogen_dist)

# Run simulation with fixed dilution
def qmra_model_median(samples):
    influent = samples["pathogen"]
    post_treatment = influent / (10 ** treatment_lrv)
    exposure_conc = post_treatment / median_dilution  # Fixed value
    return exposure_conc

results1 = mc1.run_simulation(qmra_model_median, n_iterations=n_iterations)

print(f"\nResults (Median-Only Approach):")
print(f"  Mean exposure: {results1.statistics['mean']:.2e} organisms/L")
print(f"  Median exposure: {results1.statistics['median']:.2e} organisms/L")
print(f"  5th percentile: {results1.percentiles['5%']:.2e} organisms/L")
print(f"  95th percentile: {results1.percentiles['95%']:.2e} organisms/L")
print(f"  Std deviation: {results1.statistics['std']:.2e} organisms/L")

# === APPROACH 2: New Method (Full ECDF) ===
print(f"\n{'-'*80}")
print("APPROACH 2: New Method (Using Full ECDF Distribution)")
print(f"{'-'*80}")

print(f"Using all {len(site_data)} dilution values from ECDF")

mc2 = MonteCarloSimulator(random_seed=42)

# Add pathogen distribution
mc2.add_distribution("pathogen", pathogen_dist)

# Add dilution ECDF
dilution_dist = create_empirical_cdf_from_data(site_data, name="dilution")
mc2.add_distribution("dilution", dilution_dist)

# Run simulation with ECDF dilution
def qmra_model_ecdf(samples):
    influent = samples["pathogen"]
    dilution = samples["dilution"]  # Sampled from ECDF
    post_treatment = influent / (10 ** treatment_lrv)
    exposure_conc = post_treatment / dilution
    return exposure_conc

results2 = mc2.run_simulation(qmra_model_ecdf, n_iterations=n_iterations)

print(f"\nResults (ECDF Approach):")
print(f"  Mean exposure: {results2.statistics['mean']:.2e} organisms/L")
print(f"  Median exposure: {results2.statistics['median']:.2e} organisms/L")
print(f"  5th percentile: {results2.percentiles['5%']:.2e} organisms/L")
print(f"  95th percentile: {results2.percentiles['95%']:.2e} organisms/L")
print(f"  Std deviation: {results2.statistics['std']:.2e} organisms/L")

# === COMPARISON ===
print(f"\n{'='*80}")
print("COMPARISON: Impact of Using Full Distribution")
print(f"{'='*80}")

mean_diff = (results2.statistics['mean'] - results1.statistics['mean']) / results1.statistics['mean'] * 100
median_diff = (results2.statistics['median'] - results1.statistics['median']) / results1.statistics['median'] * 100
p95_diff = (results2.percentiles['95%'] - results1.percentiles['95%']) / results1.percentiles['95%'] * 100
std_ratio = results2.statistics['std'] / results1.statistics['std']

print(f"\nKey Differences:")
print(f"  Mean exposure change: {mean_diff:+.1f}%")
print(f"  Median exposure change: {median_diff:+.1f}%")
print(f"  95th percentile change: {p95_diff:+.1f}%")
print(f"  Uncertainty increase: {std_ratio:.2f}x (std deviation ratio)")

print(f"\nInterpretation:")
if abs(mean_diff) > 10 or abs(p95_diff) > 15:
    print(f"  [!] SIGNIFICANT DIFFERENCE! Using median-only misses important uncertainty.")
    print(f"  The full ECDF approach provides more realistic risk estimates.")
else:
    print(f"  Moderate difference. ECDF still provides better uncertainty characterization.")

# Generate comparison plots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Dilution data and ECDF
ax1 = axes[0, 0]
sorted_data = np.sort(site_data)
ecdf_probs = np.arange(1, len(sorted_data) + 1) / len(sorted_data) * 100
ax1.plot(sorted_data, ecdf_probs, 'b-', linewidth=2, label='Full ECDF')
ax1.axvline(median_dilution, color='r', linestyle='--', linewidth=2, label=f'Median: {median_dilution:.2f}')
ax1.set_xlabel('Dilution Factor')
ax1.set_ylabel('Cumulative Probability (%)')
ax1.set_title('Dilution Data: ECDF vs Median-Only')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Exposure concentration distributions
ax2 = axes[0, 1]
bins = np.logspace(np.log10(min(results1.samples.min(), results2.samples.min())),
                   np.log10(max(results1.samples.max(), results2.samples.max())),
                   50)
ax2.hist(results1.samples, bins=bins, alpha=0.5, label='Median-Only', density=True, color='red')
ax2.hist(results2.samples, bins=bins, alpha=0.5, label='Full ECDF', density=True, color='blue')
ax2.set_xlabel('Exposure Concentration (organisms/L)')
ax2.set_ylabel('Probability Density')
ax2.set_title('Exposure Concentration Distribution')
ax2.set_xscale('log')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Plot 3: Box plot comparison
ax3 = axes[1, 0]
box_data = [results1.samples, results2.samples]
bp = ax3.boxplot(box_data, labels=['Median-Only', 'Full ECDF'], patch_artist=True)
bp['boxes'][0].set_facecolor('lightcoral')
bp['boxes'][1].set_facecolor('lightblue')
ax3.set_ylabel('Exposure Concentration (organisms/L)')
ax3.set_title('Comparison: Box Plots')
ax3.set_yscale('log')
ax3.grid(True, alpha=0.3, axis='y')

# Plot 4: Percentile comparison
ax4 = axes[1, 1]
percentiles = [5, 10, 25, 50, 75, 90, 95, 99]
median_percs = [np.percentile(results1.samples, p) for p in percentiles]
ecdf_percs = [np.percentile(results2.samples, p) for p in percentiles]

x = np.arange(len(percentiles))
width = 0.35
ax4.bar(x - width/2, median_percs, width, label='Median-Only', color='lightcoral', alpha=0.8)
ax4.bar(x + width/2, ecdf_percs, width, label='Full ECDF', color='lightblue', alpha=0.8)
ax4.set_xlabel('Percentile')
ax4.set_ylabel('Exposure Concentration (organisms/L)')
ax4.set_title('Percentile Comparison')
ax4.set_xticks(x)
ax4.set_xticklabels([f'{p}th' for p in percentiles])
ax4.set_yscale('log')
ax4.legend()
ax4.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('demo_ecdf_vs_median_comparison.png', dpi=150)
print(f"\nComparison plot saved: demo_ecdf_vs_median_comparison.png")

# Summary
print(f"\n{'='*80}")
print("CONCLUSION")
print(f"{'='*80}")
print(f"\nUsing the full ECDF distribution:")
print(f"  [+] Captures the full range of dilution variability")
print(f"  [+] Provides more realistic uncertainty bounds")
print(f"  [+] Better represents worst-case scenarios (low dilution events)")
print(f"  [+] Uses all {len(site_data)} hydrodynamic simulations (not just median)")
print(f"\nRecommendation: Update batch processor to use ECDF for dilution sampling!")
