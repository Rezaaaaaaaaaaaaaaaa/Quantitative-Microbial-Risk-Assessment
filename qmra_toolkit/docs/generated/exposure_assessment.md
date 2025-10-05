# Exposure Assessment Module

Exposure Assessment Module for QMRA Toolkit

This module provides exposure assessment capabilities for different pathways
including primary contact (recreational water) and shellfish consumption.

## Classes

### AerosolInhalationExposure

Aerosol inhalation exposure assessment.

Models exposure through inhalation of contaminated aerosols
(e.g., from wastewater treatment plants, spray irrigation).

### DrinkingWaterExposure

Drinking water exposure assessment.

Models exposure through consumption of treated or untreated drinking water.

### ExposureAssessment

Abstract base class for exposure assessment models.

### ExposureParameters

Container for exposure scenario parameters.

### ExposureResult

Container for exposure assessment results.

### ExposureRoute

Supported exposure routes.

### PrimaryContactExposure

Primary contact exposure assessment (recreational water activities).

Models exposure through inadvertent water ingestion during swimming,
surfing, or other recreational water activities.

### ShellfishConsumptionExposure

Shellfish consumption exposure assessment.

Models exposure through consumption of shellfish (oysters, mussels, clams)
that may have bioaccumulated pathogens from contaminated water.

## Functions

### create_exposure_assessment(route: exposure_assessment.ExposureRoute, parameters: Dict[str, Union[float, int]], **kwargs) -> exposure_assessment.ExposureAssessment

Factory function to create exposure assessment objects.

Args:
    route: Exposure route
    parameters: Exposure parameters
    **kwargs: Additional route-specific parameters

Returns:
    Appropriate exposure assessment object

Raises:
    ValueError: If exposure route is not supported

### run_exposure_assessment(exposure_model: exposure_assessment.ExposureAssessment, n_samples: int = 1000) -> exposure_assessment.ExposureResult

Run complete exposure assessment with statistics.

Args:
    exposure_model: Configured exposure assessment model
    n_samples: Number of samples for uncertainty analysis

Returns:
    ExposureResult with doses and statistics

