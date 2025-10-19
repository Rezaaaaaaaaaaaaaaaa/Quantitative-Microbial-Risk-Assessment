"""
Pathogen Database Module for QMRA Toolkit

This module provides access to pathogen-specific parameters including dose-response
relationships, illness ratios, and environmental data for quantitative microbial
risk assessment.
"""

import json
import os
from typing import Dict, List, Optional
from pathlib import Path


class PathogenDatabase:
    """
    Manages pathogen data including dose-response parameters and environmental characteristics.
    """

    def __init__(self, data_file_path: Optional[str] = None):
        """
        Initialize pathogen database.

        Args:
            data_file_path: Path to pathogen parameters JSON file. If None, uses default.
        """
        if data_file_path is None:
            # Default path relative to this module (qmra_core/data/)
            current_dir = Path(__file__).parent
            data_file_path = current_dir / "data" / "pathogen_parameters.json"

        self.data_file_path = Path(data_file_path)
        self.pathogen_data = self._load_pathogen_data()

    def _load_pathogen_data(self) -> Dict:
        """Load pathogen data from JSON file."""
        try:
            with open(self.data_file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Pathogen data file not found: {self.data_file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in pathogen data file: {e}")

    def get_available_pathogens(self) -> List[str]:
        """
        Get list of available pathogens in the database.

        Returns:
            List of pathogen names
        """
        return list(self.pathogen_data.keys())

    def get_pathogen_info(self, pathogen_name: str) -> Dict:
        """
        Get complete pathogen information.

        Args:
            pathogen_name: Name of the pathogen

        Returns:
            Dictionary containing all pathogen data

        Raises:
            ValueError: If pathogen not found in database
        """
        pathogen_name = pathogen_name.lower()
        if pathogen_name not in self.pathogen_data:
            available = ', '.join(self.get_available_pathogens())
            raise ValueError(f"Pathogen '{pathogen_name}' not found. Available: {available}")

        return self.pathogen_data[pathogen_name]

    def get_dose_response_parameters(self, pathogen_name: str, model_type: str = "beta_poisson") -> Dict:
        """
        Get dose-response model parameters for a specific pathogen.

        Args:
            pathogen_name: Name of the pathogen
            model_type: Type of dose-response model ("beta_poisson" or "exponential")

        Returns:
            Dictionary containing model parameters

        Raises:
            ValueError: If pathogen or model type not found
        """
        pathogen_info = self.get_pathogen_info(pathogen_name)

        if "dose_response_models" not in pathogen_info:
            raise ValueError(f"No dose-response models available for {pathogen_name}")

        models = pathogen_info["dose_response_models"]
        if model_type not in models:
            available_models = ', '.join(models.keys())
            raise ValueError(f"Model '{model_type}' not available for {pathogen_name}. Available: {available_models}")

        return models[model_type]

    def get_environmental_data(self, pathogen_name: str) -> Dict:
        """
        Get environmental data for a pathogen.

        Args:
            pathogen_name: Name of the pathogen

        Returns:
            Dictionary containing environmental data
        """
        pathogen_info = self.get_pathogen_info(pathogen_name)
        return pathogen_info.get("environmental_data", {})

    def get_health_impact_data(self, pathogen_name: str) -> Dict:
        """
        Get health impact data including DALYs and illness ratios.

        Args:
            pathogen_name: Name of the pathogen

        Returns:
            Dictionary containing health impact data
        """
        pathogen_info = self.get_pathogen_info(pathogen_name)

        return {
            "illness_to_infection_ratio": pathogen_info.get("illness_to_infection_ratio", 1.0),
            "dalys_per_case": pathogen_info.get("dalys_per_case", 0.001),
            "pathogen_type": pathogen_info.get("pathogen_type", "unknown")
        }

    def validate_exposure_route(self, pathogen_name: str, exposure_route: str) -> bool:
        """
        Check if an exposure route is valid for a specific pathogen.

        Args:
            pathogen_name: Name of the pathogen
            exposure_route: Exposure route to validate

        Returns:
            True if exposure route is valid for the pathogen
        """
        pathogen_info = self.get_pathogen_info(pathogen_name)
        valid_routes = pathogen_info.get("exposure_routes", [])
        return exposure_route in valid_routes

    def get_typical_concentration(self, pathogen_name: str, matrix: str) -> Optional[float]:
        """
        Get typical pathogen concentration for a specific environmental matrix.

        Args:
            pathogen_name: Name of the pathogen
            matrix: Environmental matrix (e.g., "raw_wastewater", "treated_wastewater")

        Returns:
            Typical concentration in organisms per unit volume/mass, or None if not available
        """
        env_data = self.get_environmental_data(pathogen_name)
        concentrations = env_data.get("typical_concentrations", {})
        return concentrations.get(matrix)

    def add_custom_pathogen(self, pathogen_name: str, pathogen_data: Dict) -> None:
        """
        Add a custom pathogen to the database (runtime only, not saved to file).

        Args:
            pathogen_name: Name of the new pathogen
            pathogen_data: Dictionary containing pathogen data
        """
        required_fields = ["name", "pathogen_type", "dose_response_models"]
        for field in required_fields:
            if field not in pathogen_data:
                raise ValueError(f"Required field '{field}' missing from pathogen data")

        self.pathogen_data[pathogen_name.lower()] = pathogen_data

    def get_model_citation(self, pathogen_name: str, model_type: str = "beta_poisson") -> str:
        """
        Get citation for dose-response model.

        Args:
            pathogen_name: Name of the pathogen
            model_type: Type of dose-response model

        Returns:
            Citation string for the model
        """
        params = self.get_dose_response_parameters(pathogen_name, model_type)
        return params.get("source", "No citation available")

    def get_default_model_type(self, pathogen_name: str) -> str:
        """
        Get the default dose-response model type for a pathogen.

        Args:
            pathogen_name: Name of the pathogen

        Returns:
            String indicating the default model type

        Raises:
            ValueError: If pathogen not found
        """
        pathogen_info = self.get_pathogen_info(pathogen_name)
        if "dose_response_models" not in pathogen_info:
            raise ValueError(f"No dose-response models available for {pathogen_name}")

        available_models = list(pathogen_info["dose_response_models"].keys())

        # Prefer beta_poisson if available, otherwise use the first available
        if "beta_poisson" in available_models:
            return "beta_poisson"
        else:
            return available_models[0]


# Convenience function for common use case
def get_norovirus_parameters() -> Dict:
    """
    Get norovirus dose-response parameters using default Beta-Poisson model.

    Returns:
        Dictionary containing norovirus Beta-Poisson parameters
    """
    db = PathogenDatabase()
    return db.get_dose_response_parameters("norovirus", "beta_poisson")


if __name__ == "__main__":
    # Example usage
    db = PathogenDatabase()

    print("Available pathogens:", db.get_available_pathogens())

    # Get norovirus information
    norovirus_params = db.get_dose_response_parameters("norovirus")
    print(f"Norovirus Beta-Poisson parameters: {norovirus_params}")

    # Get environmental data
    env_data = db.get_environmental_data("norovirus")
    print(f"Norovirus environmental data: {env_data}")

    # Validate exposure route
    valid_route = db.validate_exposure_route("norovirus", "primary_contact")
    print(f"Primary contact valid for norovirus: {valid_route}")