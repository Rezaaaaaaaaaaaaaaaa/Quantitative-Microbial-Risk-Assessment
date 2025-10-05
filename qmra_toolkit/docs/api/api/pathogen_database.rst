Pathogen Database Module
========================

.. automodule:: pathogen_database
   :members:
   :undoc-members:
   :show-inheritance:

The pathogen database module provides access to pathogen-specific parameters including dose-response relationships, illness ratios, and environmental data for quantitative microbial risk assessment.

Classes
-------

.. autoclass:: pathogen_database.PathogenDatabase
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from pathogen_database import PathogenDatabase

   # Initialize the database
   db = PathogenDatabase()

   # Get available pathogens
   pathogens = db.get_available_pathogens()
   print(f"Available pathogens: {pathogens}")

   # Get pathogen information
   norovirus_info = db.get_pathogen_info('norovirus')
   print(f"Pathogen type: {norovirus_info['pathogen_type']}")

   # Get dose-response parameters
   dr_params = db.get_dose_response_parameters('norovirus', 'beta_poisson')
   print(f"Alpha: {dr_params['alpha']}, Beta: {dr_params['beta']}")

Accessing Environmental Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Get environmental survival data
   env_data = db.get_environmental_data('norovirus')
   print(f"Survival time: {env_data['survival_time_days']} days")

   # Get typical concentrations
   concentration = db.get_typical_concentration('norovirus', 'raw_wastewater')
   print(f"Typical concentration in raw wastewater: {concentration} organisms/L")

Custom Pathogen Addition
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Add a custom pathogen
   custom_pathogen = {
       "name": "Custom Virus",
       "pathogen_type": "virus",
       "dose_response_models": {
           "exponential": {
               "r": 0.1,
               "source": "Custom study (2024)"
           }
       },
       "illness_to_infection_ratio": 0.8,
       "dalys_per_case": 0.001
   }

   db.add_custom_pathogen("custom_virus", custom_pathogen)

Data Structure
--------------

The pathogen database follows this JSON structure:

.. code-block:: json

   {
     "pathogen_name": {
       "name": "Human-readable name",
       "pathogen_type": "virus|bacteria|protozoa",
       "dose_response_models": {
         "beta_poisson": {
           "alpha": 0.04,
           "beta": 0.055,
           "source": "Citation",
           "notes": "Optional notes"
         },
         "exponential": {
           "r": 0.5,
           "source": "Citation"
         }
       },
       "illness_to_infection_ratio": 0.7,
       "dalys_per_case": 0.002,
       "exposure_routes": ["route1", "route2"],
       "environmental_data": {
         "survival_time_days": 60,
         "inactivation_rate_per_day": 0.1,
         "typical_concentrations": {
           "raw_wastewater": 1000000,
           "treated_wastewater": 1000
         }
       }
     }
   }