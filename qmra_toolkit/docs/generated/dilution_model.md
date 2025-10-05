# Dilution Model Module

Dilution Modelling Integration Module for QMRA Toolkit

This module provides dilution modelling capabilities and integration with
engineer-provided log reduction values (LRVs), which is NIWA's key differentiator.

## Classes

### DilutionModel

Dilution modelling for QMRA - NIWA's key differentiator.

This class handles dilution calculations for various scenarios including:
- Point source discharge dilution
- Far-field dilution
- Natural die-off during transport
- Multiple treatment barriers

### DilutionScenario

Container for dilution scenario parameters.

### TreatmentBarrier

Container for treatment barrier information.

### TreatmentType

Types of treatment processes.

## Functions

### create_chlorination_barrier(log_reduction: float, variability: float = 0.3) -> dilution_model.TreatmentBarrier

Create chlorination barrier.

### create_membrane_barrier(log_reduction: float, variability: float = 0.1) -> dilution_model.TreatmentBarrier

Create membrane filtration barrier.

### create_uv_barrier(log_reduction: float, variability: float = 0.2) -> dilution_model.TreatmentBarrier

Create UV disinfection barrier.

### create_wastewater_treatment_train() -> dilution_model.DilutionModel

Create a typical wastewater treatment train.

Returns:
    Configured DilutionModel with typical wastewater treatment barriers

