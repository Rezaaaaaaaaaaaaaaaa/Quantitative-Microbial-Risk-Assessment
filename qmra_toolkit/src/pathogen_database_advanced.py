"""
Advanced Pathogen Database for QMRA
Ported from Charlotte Jones-Todd's R QMRA package
Includes comprehensive pathogen parameters from literature
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Union
import json


@dataclass
class PathogenParameters:
    """Container for pathogen dose-response parameters"""
    name: str
    model: str
    parameters: Dict[str, float]
    source: Optional[str] = None
    endpoint: Optional[str] = None
    host: Optional[str] = None
    route: Optional[str] = None
    n50: Optional[float] = None
    id50: Optional[float] = None


class PathogenDatabase:
    """
    Comprehensive pathogen database with dose-response parameters
    Based on Charlotte's R package and literature values
    """

    def __init__(self):
        self.pathogens = self._initialize_database()

    def _initialize_database(self) -> Dict[str, List[PathogenParameters]]:
        """Initialize the pathogen database with literature values"""

        database = {
            'campylobacter': [
                PathogenParameters(
                    name='Campylobacter jejuni',
                    model='beta_poisson',
                    parameters={'alpha': 0.145, 'beta': 7.59},
                    source='Medema et al 1996',
                    endpoint='infection',
                    host='human',
                    route='oral',
                    n50=896
                ),
                PathogenParameters(
                    name='Campylobacter jejuni',
                    model='beta_poisson_approx',
                    parameters={'alpha': 0.024, 'beta': 0.011},
                    source='Teunis et al 2005',
                    endpoint='infection',
                    host='human',
                    route='oral'
                ),
                PathogenParameters(
                    name='Campylobacter jejuni',
                    model='weibull',
                    parameters={'q1': 2.70e-5, 'q2': 0.51},
                    source='Alternative model',
                    endpoint='infection',
                    host='human',
                    route='oral'
                )
            ],

            'cryptosporidium': [
                PathogenParameters(
                    name='Cryptosporidium parvum (Iowa)',
                    model='exponential',
                    parameters={'r': 0.00419},
                    source='Haas et al 1996',
                    endpoint='infection',
                    host='human',
                    route='oral',
                    n50=165
                ),
                PathogenParameters(
                    name='Cryptosporidium parvum',
                    model='fractional_poisson',
                    parameters={'p': 0.1778, 'mu': 35.98},
                    source='Messner et al 2014',
                    endpoint='infection',
                    host='human',
                    route='oral'
                ),
                PathogenParameters(
                    name='Cryptosporidium hominis',
                    model='exponential',
                    parameters={'r': 0.0199},
                    source='DuPont et al 1995',
                    endpoint='infection with diarrhea',
                    host='human',
                    route='oral'
                ),
                PathogenParameters(
                    name='Cryptosporidium parvum',
                    model='beta_poisson',
                    parameters={'alpha': 0.115, 'beta': 1.11},
                    source='Teunis & Havelaar 2000',
                    endpoint='infection',
                    host='human',
                    route='oral'
                )
            ],

            'giardia': [
                PathogenParameters(
                    name='Giardia lamblia',
                    model='exponential',
                    parameters={'r': 0.01982},
                    source='Rose et al 1991',
                    endpoint='infection',
                    host='human',
                    route='oral',
                    n50=35
                ),
                PathogenParameters(
                    name='Giardia lamblia',
                    model='beta_poisson',
                    parameters={'alpha': 0.0489, 'beta': 5.472},
                    source='Regli et al 1991',
                    endpoint='infection',
                    host='human',
                    route='oral'
                )
            ],

            'ecoli': [
                PathogenParameters(
                    name='E. coli O157:H7',
                    model='beta_poisson',
                    parameters={'alpha': 0.0571, 'beta': 1.415},
                    source='Haas et al 2000',
                    endpoint='infection',
                    host='human',
                    route='oral'
                ),
                PathogenParameters(
                    name='Enteropathogenic E. coli',
                    model='beta_poisson',
                    parameters={'alpha': 0.1778, 'beta': 1.44e6},
                    source='Haas et al 1999',
                    endpoint='infection',
                    host='human',
                    route='oral',
                    n50=8.60e6
                ),
                PathogenParameters(
                    name='Enterotoxigenic E. coli',
                    model='beta_poisson',
                    parameters={'alpha': 0.3126, 'beta': 2.8844e8},
                    source='Haas et al 1999',
                    endpoint='positive response',
                    host='human',
                    route='oral'
                ),
                PathogenParameters(
                    name='Enteroinvasive E. coli',
                    model='beta_poisson',
                    parameters={'alpha': 0.2521, 'beta': 5.935e7},
                    source='Haas et al 1999',
                    endpoint='positive response',
                    host='human',
                    route='oral'
                )
            ],

            'norovirus': [
                PathogenParameters(
                    name='Norovirus (aggregate)',
                    model='fractional_poisson',
                    parameters={'p': 0.72, 'mu': 1106},
                    source='Messner et al 2014',
                    endpoint='infection',
                    host='human',
                    route='oral'
                ),
                PathogenParameters(
                    name='Norovirus GI.1',
                    model='beta_poisson_approx',
                    parameters={'alpha': 0.040, 'beta': 0.055},
                    source='Teunis et al 2008',
                    endpoint='infection',
                    host='human',
                    route='oral',
                    n50=1.5
                ),
                PathogenParameters(
                    name='Norwalk virus',
                    model='beta_poisson',
                    parameters={'alpha': 0.270, 'beta': 0.480},
                    source='Regli et al 1991',
                    endpoint='infection',
                    host='human',
                    route='oral'
                )
            ],

            'rotavirus': [
                PathogenParameters(
                    name='Rotavirus',
                    model='exponential',
                    parameters={'r': 0.0147},
                    source='Regli et al 1991',
                    endpoint='infection',
                    host='human',
                    route='oral',
                    n50=47.2
                ),
                PathogenParameters(
                    name='Rotavirus',
                    model='beta_poisson',
                    parameters={'alpha': 0.253, 'beta': 0.426},
                    source='Ward et al 1986',
                    endpoint='infection',
                    host='human',
                    route='oral',
                    n50=6.17
                ),
                PathogenParameters(
                    name='Rotavirus',
                    model='beta_poisson_approx',
                    parameters={'alpha': 0.167, 'beta': 0.191},
                    source='Haas et al 1993',
                    endpoint='infection',
                    host='human',
                    route='oral'
                )
            ],

            'salmonella': [
                PathogenParameters(
                    name='Salmonella typhi',
                    model='beta_poisson',
                    parameters={'alpha': 0.1086, 'beta': 1.125e7},
                    source='Hornick et al 1966',
                    endpoint='infection',
                    host='human',
                    route='oral'
                ),
                PathogenParameters(
                    name='Salmonella (nontyphoid)',
                    model='beta_poisson',
                    parameters={'alpha': 0.3126, 'beta': 2.884e3},
                    source='Haas et al 1999',
                    endpoint='infection',
                    host='human',
                    route='oral',
                    n50=2.36e4
                ),
                PathogenParameters(
                    name='Salmonella typhimurium',
                    model='weibull',
                    parameters={'q1': 0.00752, 'q2': 0.131},
                    source='Alternative model',
                    endpoint='infection',
                    host='human',
                    route='oral'
                )
            ],

            'shigella': [
                PathogenParameters(
                    name='Shigella dysenteriae',
                    model='beta_poisson',
                    parameters={'alpha': 0.2100, 'beta': 1.120e3},
                    source='Haas et al 1999',
                    endpoint='positive response',
                    host='human',
                    route='oral'
                ),
                PathogenParameters(
                    name='Shigella flexneri',
                    model='beta_poisson',
                    parameters={'alpha': 0.265, 'beta': 1.48e6},
                    source='DuPont et al 1989',
                    endpoint='positive response',
                    host='human',
                    route='oral'
                )
            ],

            'vibrio': [
                PathogenParameters(
                    name='Vibrio cholerae (Classical)',
                    model='beta_poisson',
                    parameters={'alpha': 0.250, 'beta': 2.43e2},
                    source='Cash et al 1974',
                    endpoint='infection',
                    host='human',
                    route='oral'
                ),
                PathogenParameters(
                    name='Vibrio cholerae (El Tor)',
                    model='beta_poisson',
                    parameters={'alpha': 0.170, 'beta': 1.05e7},
                    source='Hornick et al 1971',
                    endpoint='infection',
                    host='human',
                    route='oral'
                )
            ],

            'adenovirus': [
                PathogenParameters(
                    name='Adenovirus 4',
                    model='exponential',
                    parameters={'r': 0.0097},
                    source='Couch et al 1966',
                    endpoint='infection',
                    host='human',
                    route='inhalation',
                    n50=71
                ),
                PathogenParameters(
                    name='Adenovirus (oral)',
                    model='beta_poisson',
                    parameters={'alpha': 0.219, 'beta': 2.291},
                    source='Crabtree et al 1997',
                    endpoint='infection',
                    host='human',
                    route='oral'
                )
            ],

            'enterovirus': [
                PathogenParameters(
                    name='Echovirus 12',
                    model='beta_poisson',
                    parameters={'alpha': 0.374, 'beta': 1.86e2},
                    source='Schiff et al 1984',
                    endpoint='infection',
                    host='human',
                    route='oral'
                ),
                PathogenParameters(
                    name='Poliovirus 1',
                    model='exponential',
                    parameters={'r': 0.009102},
                    source='Minor et al 1981',
                    endpoint='infection',
                    host='human',
                    route='oral'
                ),
                PathogenParameters(
                    name='Poliovirus 3',
                    model='beta_poisson',
                    parameters={'alpha': 0.409, 'beta': 0.788},
                    source='Rose & Gerba 1991',
                    endpoint='infection',
                    host='human',
                    route='oral'
                )
            ],

            'hepatitis': [
                PathogenParameters(
                    name='Hepatitis A virus',
                    model='exponential',
                    parameters={'r': 0.0001},
                    source='Ward et al 1958',
                    endpoint='infection',
                    host='human',
                    route='oral'
                ),
                PathogenParameters(
                    name='Hepatitis A virus',
                    model='beta_poisson',
                    parameters={'alpha': 0.163, 'beta': 7.58e5},
                    source='Rose & Sobsey 1993',
                    endpoint='infection',
                    host='human',
                    route='oral'
                )
            ],

            'legionella': [
                PathogenParameters(
                    name='Legionella pneumophila',
                    model='exponential',
                    parameters={'r': 0.06},
                    source='Armstrong & Haas 2007',
                    endpoint='clinical severity (ICU)',
                    host='human',
                    route='inhalation'
                )
            ],

            'listeria': [
                PathogenParameters(
                    name='Listeria monocytogenes',
                    model='exponential',
                    parameters={'r': 5.6e-10},
                    source='Buchanan et al 1997',
                    endpoint='infection',
                    host='human (normal)',
                    route='oral'
                ),
                PathogenParameters(
                    name='Listeria monocytogenes',
                    model='exponential',
                    parameters={'r': 1.18e-7},
                    source='Buchanan et al 1997',
                    endpoint='infection',
                    host='human (susceptible)',
                    route='oral'
                )
            ]
        }

        return database

    def get_pathogen(self, pathogen_name: str) -> List[PathogenParameters]:
        """Get all parameter sets for a specific pathogen"""
        pathogen_name_lower = pathogen_name.lower()
        for key in self.pathogens:
            if key in pathogen_name_lower or pathogen_name_lower in key:
                return self.pathogens[key]
        raise ValueError(f"Pathogen '{pathogen_name}' not found in database")

    def get_all_pathogens(self) -> List[str]:
        """Get list of all available pathogens"""
        return list(self.pathogens.keys())

    def get_pathogen_by_model(self, pathogen_name: str, model_name: str) -> Optional[PathogenParameters]:
        """Get specific pathogen parameters by model type"""
        pathogen_list = self.get_pathogen(pathogen_name)
        for params in pathogen_list:
            if params.model == model_name:
                return params
        return None

    def get_best_fit_model(self, pathogen_name: str) -> PathogenParameters:
        """
        Get the recommended/best-fit model for a pathogen
        Priority: fractional_poisson > beta_poisson > exponential
        """
        pathogen_list = self.get_pathogen(pathogen_name)

        # Priority order for models
        model_priority = ['fractional_poisson', 'beta_poisson', 'beta_poisson_approx', 'exponential']

        for model in model_priority:
            for params in pathogen_list:
                if params.model == model:
                    return params

        # Return first available if no priority model found
        return pathogen_list[0]

    def export_to_json(self, filepath: str):
        """Export database to JSON file"""
        export_data = {}
        for pathogen_name, params_list in self.pathogens.items():
            export_data[pathogen_name] = [
                {
                    'name': p.name,
                    'model': p.model,
                    'parameters': p.parameters,
                    'source': p.source,
                    'endpoint': p.endpoint,
                    'host': p.host,
                    'route': p.route,
                    'n50': p.n50,
                    'id50': p.id50
                }
                for p in params_list
            ]

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)

    def summary(self) -> str:
        """Generate summary of database contents"""
        summary_lines = ["Pathogen Database Summary", "=" * 50]

        for pathogen_name, params_list in self.pathogens.items():
            summary_lines.append(f"\n{pathogen_name.title()}: {len(params_list)} model(s)")
            for params in params_list:
                summary_lines.append(f"  - {params.model}: {params.source or 'No source'}")

        summary_lines.append(f"\nTotal pathogens: {len(self.pathogens)}")
        total_models = sum(len(p) for p in self.pathogens.values())
        summary_lines.append(f"Total model parameterizations: {total_models}")

        return "\n".join(summary_lines)


# Bioaccumulation factors for shellfish
BIOACCUMULATION_FACTORS = {
    'norovirus': {
        'oysters': 100,
        'mussels': 100,
        'clams': 100,
        'default': 100
    },
    'hepatitis': {
        'oysters': 100,
        'mussels': 100,
        'clams': 100,
        'default': 100
    },
    'vibrio': {
        'oysters': 200,
        'mussels': 150,
        'clams': 150,
        'default': 150
    },
    'default': {
        'oysters': 100,
        'mussels': 100,
        'clams': 100,
        'default': 100
    }
}


# Morbidity ratios (infection to illness)
MORBIDITY_RATIOS = {
    'campylobacter': 0.33,
    'cryptosporidium': 0.39,
    'giardia': 0.5,
    'ecoli': 0.35,
    'norovirus': 0.7,
    'rotavirus': 0.88,
    'salmonella': 0.2,
    'shigella': 0.13,
    'vibrio': 0.36,
    'adenovirus': 0.5,
    'enterovirus': 0.5,
    'hepatitis': 0.7,
    'legionella': 1.0,
    'listeria': 1.0
}