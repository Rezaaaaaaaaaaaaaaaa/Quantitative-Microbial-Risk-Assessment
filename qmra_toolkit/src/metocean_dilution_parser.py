#!/usr/bin/env python3
"""
MetOcean Dilution Data Parser
Processes hydrodynamic modeling output for QMRA dilution factors

Handles tab-delimited concentration files from MetOcean Solutions dispersion modeling
Format: year, month, day, hour_utc, minutes, sec, C_surf[g/m3], C_mid[g/m3], C_nearbed[g/m3]
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import glob


class MetOceanDilutionParser:
    """
    Parser for MetOcean hydrodynamic modeling concentration data.

    Calculates dilution factors from modeled concentration timeseries.
    Source concentration in model assumed to be 1.0 g/m³ unless specified.
    """

    def __init__(self, source_concentration: float = 1.0):
        """
        Initialize parser.

        Args:
            source_concentration: Source concentration used in model (g/m³), default 1.0
        """
        self.source_concentration = source_concentration
        self.data = None
        self.site_name = None
        self.scenario = None

    def parse_file(self, file_path: str) -> pd.DataFrame:
        """
        Parse a single MetOcean concentration file.

        Args:
            file_path: Path to concentration file

        Returns:
            DataFrame with parsed concentration data

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Dilution data file not found: {file_path}")

        # Extract site name and scenario from filename
        # Format: SITE_SCENARIO_nodieoff-hybrid_conc.txt
        # Example: W1_nina_nodieoff-hybrid_conc.txt
        filename = file_path.stem
        parts = filename.split('_')

        if len(parts) >= 2:
            self.site_name = parts[0]  # e.g., 'W1', 'E5'
            self.scenario = parts[1]    # e.g., 'nina', 'nino'
        else:
            self.site_name = filename
            self.scenario = 'unknown'

        # Read tab-delimited file
        try:
            df = pd.read_csv(file_path, sep='\t')
        except Exception as e:
            raise ValueError(f"Error reading file {file_path}: {e}")

        # Validate expected columns
        required_cols = ['C_surf[g/m3]', 'C_mid[g/m3]', 'C_nearbed[g/m3]']
        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        # Create datetime column
        if all(col in df.columns for col in ['year', 'month', 'day', 'hour_utc']):
            df['datetime'] = pd.to_datetime(
                df[['year', 'month', 'day', 'hour_utc']].rename(
                    columns={'hour_utc': 'hour'}
                ),
                errors='coerce'
            )

        self.data = df
        return df

    def calculate_dilution_factors(self, depth: str = 'surf') -> np.ndarray:
        """
        Calculate dilution factors from concentration data.

        Dilution Factor = Source Concentration / Ambient Concentration

        Args:
            depth: Depth level ('surf', 'mid', 'nearbed'), default 'surf'

        Returns:
            Array of dilution factors (excludes zeros/infinities)

        Raises:
            ValueError: If data not loaded or invalid depth specified
        """
        if self.data is None:
            raise ValueError("No data loaded. Call parse_file() first.")

        valid_depths = ['surf', 'mid', 'nearbed']
        if depth not in valid_depths:
            raise ValueError(f"Invalid depth '{depth}'. Must be one of {valid_depths}")

        # Get concentration column
        conc_col = f'C_{depth}[g/m3]'

        if conc_col not in self.data.columns:
            raise ValueError(f"Column {conc_col} not found in data")

        concentrations = self.data[conc_col].values

        # Calculate dilution factors, handling zeros
        # DF = Source / Ambient
        # Exclude zero concentrations (infinite dilution)
        non_zero_mask = concentrations > 0
        dilution_factors = np.full_like(concentrations, np.nan, dtype=float)

        dilution_factors[non_zero_mask] = (
            self.source_concentration / concentrations[non_zero_mask]
        )

        # Return only valid (non-zero, non-infinite) dilution factors
        valid_dfs = dilution_factors[~np.isnan(dilution_factors) & ~np.isinf(dilution_factors)]

        return valid_dfs

    def get_dilution_statistics(self, depth: str = 'surf') -> Dict[str, float]:
        """
        Calculate statistical summary of dilution factors.

        Provides percentiles for conservative (10th), typical (50th),
        and optimistic (90th) dilution scenarios.

        Args:
            depth: Depth level ('surf', 'mid', 'nearbed')

        Returns:
            Dictionary with dilution factor statistics
        """
        dfs = self.calculate_dilution_factors(depth)

        if len(dfs) == 0:
            return {
                'count': 0,
                'mean': np.nan,
                'median': np.nan,
                'min': np.nan,
                'max': np.nan,
                'p10': np.nan,
                'p50': np.nan,
                'p90': np.nan,
                'p95': np.nan,
            }

        stats = {
            'count': len(dfs),
            'mean': np.mean(dfs),
            'median': np.median(dfs),
            'std': np.std(dfs),
            'min': np.min(dfs),
            'max': np.max(dfs),
            'p10': np.percentile(dfs, 10),   # Conservative (low dilution)
            'p50': np.percentile(dfs, 50),   # Typical (median)
            'p90': np.percentile(dfs, 90),   # Optimistic (high dilution)
            'p95': np.percentile(dfs, 95),
        }

        return stats

    def get_concentration_statistics(self, depth: str = 'surf') -> Dict[str, float]:
        """
        Calculate statistical summary of ambient concentrations.

        Args:
            depth: Depth level ('surf', 'mid', 'nearbed')

        Returns:
            Dictionary with concentration statistics (g/m³)
        """
        if self.data is None:
            raise ValueError("No data loaded")

        conc_col = f'C_{depth}[g/m3]'
        concentrations = self.data[conc_col].values

        # Exclude zeros for non-zero statistics
        non_zero_concs = concentrations[concentrations > 0]

        stats = {
            'count_all': len(concentrations),
            'count_nonzero': len(non_zero_concs),
            'mean': np.mean(concentrations),
            'mean_nonzero': np.mean(non_zero_concs) if len(non_zero_concs) > 0 else np.nan,
            'median': np.median(concentrations),
            'median_nonzero': np.median(non_zero_concs) if len(non_zero_concs) > 0 else np.nan,
            'p10': np.percentile(non_zero_concs, 10) if len(non_zero_concs) > 0 else np.nan,
            'p50': np.percentile(non_zero_concs, 50) if len(non_zero_concs) > 0 else np.nan,
            'p90': np.percentile(non_zero_concs, 90) if len(non_zero_concs) > 0 else np.nan,
            'p95': np.percentile(non_zero_concs, 95) if len(non_zero_concs) > 0 else np.nan,
            'max': np.max(concentrations),
        }

        return stats

    def get_recommended_dilution(self, depth: str = 'surf', conservatism: str = 'conservative') -> float:
        """
        Get recommended dilution factor for QMRA based on conservatism level.

        Args:
            depth: Depth level ('surf' for swimming, 'nearbed' for shellfish)
            conservatism: 'conservative' (p10), 'typical' (p50), 'optimistic' (p90)

        Returns:
            Recommended dilution factor
        """
        stats = self.get_dilution_statistics(depth)

        conservatism_map = {
            'conservative': stats['p10'],  # 10th percentile = low dilution = protective
            'typical': stats['p50'],       # 50th percentile = median
            'optimistic': stats['p90'],    # 90th percentile = high dilution
        }

        if conservatism not in conservatism_map:
            raise ValueError(f"Invalid conservatism '{conservatism}'. Must be 'conservative', 'typical', or 'optimistic'")

        return conservatism_map[conservatism]


class MetOceanDatasetManager:
    """
    Manager for multiple MetOcean dilution data files.

    Handles site selection, scenario comparison, and multi-site analysis.
    """

    def __init__(self, data_directory: str, source_concentration: float = 1.0):
        """
        Initialize dataset manager.

        Args:
            data_directory: Directory containing dilution data files
            source_concentration: Source concentration used in modeling (g/m³)
        """
        self.data_directory = Path(data_directory)
        self.source_concentration = source_concentration
        self.available_files = []
        self.sites = []
        self.scenarios = []

        self._scan_directory()

    def _scan_directory(self):
        """Scan directory for available dilution data files."""
        if not self.data_directory.exists():
            raise FileNotFoundError(f"Data directory not found: {self.data_directory}")

        # Find all concentration files
        pattern = str(self.data_directory / "*_nodieoff-hybrid_conc.txt")
        self.available_files = glob.glob(pattern)

        if not self.available_files:
            # Try alternative pattern
            pattern = str(self.data_directory / "*_conc.txt")
            self.available_files = glob.glob(pattern)

        # Extract unique sites and scenarios
        sites_set = set()
        scenarios_set = set()

        for file_path in self.available_files:
            filename = Path(file_path).stem
            parts = filename.split('_')

            if len(parts) >= 2:
                sites_set.add(parts[0])
                scenarios_set.add(parts[1])

        self.sites = sorted(list(sites_set))
        self.scenarios = sorted(list(scenarios_set))

    def get_available_sites(self) -> List[str]:
        """Get list of available monitoring sites."""
        return self.sites

    def get_available_scenarios(self) -> List[str]:
        """Get list of available scenarios (e.g., nina, nino)."""
        return self.scenarios

    def get_file_for_site_scenario(self, site: str, scenario: str) -> Optional[str]:
        """
        Find file for specific site and scenario combination.

        Args:
            site: Site identifier (e.g., 'W1', 'E5')
            scenario: Scenario identifier (e.g., 'nina', 'nino')

        Returns:
            File path if found, None otherwise
        """
        pattern = f"{site}_{scenario}_"

        for file_path in self.available_files:
            if pattern in Path(file_path).name:
                return file_path

        return None

    def get_dilution_for_site(
        self,
        site: str,
        scenario: str,
        depth: str = 'surf',
        conservatism: str = 'conservative'
    ) -> Optional[float]:
        """
        Get recommended dilution factor for specific site/scenario.

        Args:
            site: Site identifier
            scenario: Scenario identifier
            depth: Depth level
            conservatism: Conservatism level

        Returns:
            Dilution factor or None if site/scenario not found
        """
        file_path = self.get_file_for_site_scenario(site, scenario)

        if not file_path:
            return None

        parser = MetOceanDilutionParser(self.source_concentration)
        parser.parse_file(file_path)

        return parser.get_recommended_dilution(depth, conservatism)

    def compare_scenarios(
        self,
        site: str,
        depth: str = 'surf'
    ) -> Dict[str, Dict[str, float]]:
        """
        Compare dilution statistics across scenarios for a given site.

        Args:
            site: Site identifier
            depth: Depth level

        Returns:
            Dictionary of {scenario: dilution_stats}
        """
        results = {}

        for scenario in self.scenarios:
            file_path = self.get_file_for_site_scenario(site, scenario)

            if file_path:
                parser = MetOceanDilutionParser(self.source_concentration)
                parser.parse_file(file_path)
                results[scenario] = parser.get_dilution_statistics(depth)

        return results

    def get_site_summary(self) -> pd.DataFrame:
        """
        Create summary table of all sites and scenarios.

        Returns:
            DataFrame with site, scenario, and dilution statistics
        """
        summary_data = []

        for site in self.sites:
            for scenario in self.scenarios:
                file_path = self.get_file_for_site_scenario(site, scenario)

                if file_path:
                    parser = MetOceanDilutionParser(self.source_concentration)
                    try:
                        parser.parse_file(file_path)

                        for depth in ['surf', 'mid', 'nearbed']:
                            stats = parser.get_dilution_statistics(depth)

                            summary_data.append({
                                'site': site,
                                'scenario': scenario,
                                'depth': depth,
                                'count': stats['count'],
                                'mean_dilution': stats['mean'],
                                'median_dilution': stats['median'],
                                'p10_dilution': stats['p10'],
                                'p90_dilution': stats['p90'],
                            })
                    except Exception as e:
                        print(f"Warning: Error processing {file_path}: {e}")
                        continue

        return pd.DataFrame(summary_data)


# Convenience functions
def parse_dilution_file(file_path: str, depth: str = 'surf', conservatism: str = 'conservative') -> float:
    """
    Quick function to get dilution factor from a single file.

    Args:
        file_path: Path to dilution data file
        depth: Depth level ('surf', 'mid', 'nearbed')
        conservatism: Conservatism level

    Returns:
        Recommended dilution factor
    """
    parser = MetOceanDilutionParser()
    parser.parse_file(file_path)
    return parser.get_recommended_dilution(depth, conservatism)


def get_dilution_range(file_path: str, depth: str = 'surf') -> Tuple[float, float, float]:
    """
    Get dilution factor range (conservative, typical, optimistic).

    Args:
        file_path: Path to dilution data file
        depth: Depth level

    Returns:
        Tuple of (conservative_DF, typical_DF, optimistic_DF)
    """
    parser = MetOceanDilutionParser()
    parser.parse_file(file_path)

    stats = parser.get_dilution_statistics(depth)

    return (stats['p10'], stats['p50'], stats['p90'])


if __name__ == "__main__":
    # Example usage and testing
    print("MetOcean Dilution Data Parser")
    print("=" * 60)

    # Example: Parse single file
    example_file = r"O:\NPD22201\RawData\From_MetOcean\sites_NPWWTP_hybrid\W1_nina_nodieoff-hybrid_conc.txt"

    if Path(example_file).exists():
        parser = MetOceanDilutionParser(source_concentration=1.0)
        parser.parse_file(example_file)

        print(f"\nSite: {parser.site_name}")
        print(f"Scenario: {parser.scenario}")
        print(f"Data points: {len(parser.data)}")

        print("\n--- Surface Dilution Statistics ---")
        stats = parser.get_dilution_statistics('surf')
        for key, value in stats.items():
            print(f"{key:15s}: {value:,.1f}")

        print("\n--- Recommended Dilution Factors ---")
        print(f"Conservative (p10): {parser.get_recommended_dilution('surf', 'conservative'):,.0f}:1")
        print(f"Typical (p50):      {parser.get_recommended_dilution('surf', 'typical'):,.0f}:1")
        print(f"Optimistic (p90):   {parser.get_recommended_dilution('surf', 'optimistic'):,.0f}:1")

    else:
        print(f"\nExample file not found: {example_file}")
        print("Adjust path or test with your own data files.")
