"""
Advanced Dose-Response Models for QMRA
Ported from Charlotte Jones-Todd's R QMRA package
Implements 11 comprehensive dose-response models
"""

import numpy as np
from scipy import special, stats
from scipy.special import gamma, beta, erf, hyp2f1
from typing import Union, List, Dict, Optional, Tuple
import warnings


class DoseResponseModels:
    """Advanced dose-response models for QMRA analysis"""

    @staticmethod
    def exponential(r: float, dose: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Exponential dose-response model

        Args:
            r: Pathogen-host survival probability (0 < r < 1)
            dose: Dose or array of doses

        Returns:
            Probability of infection
        """
        if not 0 < r < 1:
            raise ValueError("r must be in the range (0, 1)")

        dose = np.asarray(dose)
        return 1 - np.exp(-r * dose)

    @staticmethod
    def fractional_poisson(p: float, mu: float, dose: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Fractional Poisson dose-response model (Messner et al 2014)

        Args:
            p: Parameter of the dose-response model
            mu: Mean aggregate size (set to 1 in strict case)
            dose: Dose or array of doses

        Returns:
            Probability of infection
        """
        dose = np.asarray(dose)
        return p * (1 - np.exp(-dose / mu))

    @staticmethod
    def beta_poisson(alpha: float, beta_param: float, dose: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Beta-Poisson dose-response model

        Args:
            alpha: Shape parameter of beta distribution (> 0)
            beta_param: Shape parameter of beta distribution (> 0)
            dose: Dose or array of doses

        Returns:
            Probability of infection
        """
        if alpha <= 0:
            raise ValueError("alpha must be positive")
        if beta_param <= 0:
            raise ValueError("beta must be positive")

        dose = np.asarray(dose)

        # Using hypergeometric function approximation
        # 1 - 2F1(alpha, alpha+beta; alpha+beta; -dose)
        result = np.zeros_like(dose, dtype=float)

        for i, d in enumerate(np.atleast_1d(dose)):
            if d == 0:
                result.flat[i] = 0
            else:
                # Use the approximation for computational efficiency
                # This is equivalent to the exact hypergeometric function for most practical cases
                try:
                    # Exact calculation using hypergeometric function
                    hyp_val = hyp2f1(alpha, alpha + beta_param, alpha + beta_param, -d)
                    result.flat[i] = 1 - hyp_val
                except:
                    # Fallback to approximation if exact calculation fails
                    result.flat[i] = 1 - (1 + d / beta_param) ** (-alpha)

        return result.item() if result.size == 1 else result

    @staticmethod
    def beta_poisson_approx(alpha: float, beta_param: float, dose: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Approximation to Beta-Poisson model (Furumoto and Mickey 1967)

        Args:
            alpha: Shape parameter of beta distribution (> 0)
            beta_param: Shape parameter of beta distribution (> 0)
            dose: Dose or array of doses

        Returns:
            Probability of infection
        """
        if alpha <= 0:
            raise ValueError("alpha must be positive")
        if beta_param <= 0:
            raise ValueError("beta must be positive")

        dose = np.asarray(dose)
        return 1 - (1 + dose / beta_param) ** (-alpha)

    @staticmethod
    def simple_threshold(kmin: float, r: float, dose: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Simple threshold model, extension of the exponential model

        Args:
            kmin: Minimum number of surviving organisms
            r: Pathogen-host survival probability (0 < r < 1)
            dose: Dose or array of doses

        Returns:
            Probability of infection
        """
        if not 0 < r < 1:
            raise ValueError("r must be in the range (0, 1)")

        dose = np.asarray(dose)
        # Using gamma CDF (equivalent to pgamma in R)
        return stats.gamma.cdf(dose * r, kmin)

    @staticmethod
    def log_logistic(q1: float, q2: float, dose: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Log-logistic dose-response model

        Args:
            q1: Parameter of the log-logistic model
            q2: Parameter of the log-logistic model
            dose: Dose or array of doses

        Returns:
            Probability of infection
        """
        dose = np.asarray(dose)
        # Avoid log(0) by adding small epsilon to zero doses
        safe_dose = np.where(dose > 0, dose, np.finfo(float).eps)
        return 1 / (1 + np.exp(q1 - q2 * np.log(safe_dose)))

    @staticmethod
    def log_probit(q1: float, q2: float, dose: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Log-probit dose-response model

        Args:
            q1: Parameter of the log-probit model
            q2: Parameter of the log-probit model
            dose: Dose or array of doses

        Returns:
            Probability of infection
        """
        dose = np.asarray(dose)
        # Avoid log(0) by adding small epsilon to zero doses
        safe_dose = np.where(dose > 0, dose, np.finfo(float).eps)
        arg = (1 / q2) * np.log(safe_dose / q1)

        # Phi function implementation
        return (1 + erf(arg / np.sqrt(2))) / 2

    @staticmethod
    def weibull(q1: float, q2: float, dose: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Weibull dose-response model

        Args:
            q1: Parameter of the Weibull model
            q2: Parameter of the Weibull model
            dose: Dose or array of doses

        Returns:
            Probability of infection
        """
        dose = np.asarray(dose)
        return 1 - np.exp(-q1 * dose ** q2)

    @staticmethod
    def simple_binomial(r: float, dose: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Simple binomial dose-response model

        Args:
            r: Pathogen-host survival probability (0 < r < 1)
            dose: Dose or array of doses

        Returns:
            Probability of infection
        """
        if not 0 < r < 1:
            raise ValueError("r must be in the range (0, 1)")

        dose = np.asarray(dose)
        return 1 - (1 - r) ** dose

    @staticmethod
    def beta_binomial(alpha: float, beta_param: float, dose: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Beta-binomial dose-response model

        Args:
            alpha: Shape parameter of beta distribution (> 0)
            beta_param: Shape parameter of beta distribution (> 0)
            dose: Dose or array of doses

        Returns:
            Probability of infection
        """
        if alpha <= 0:
            raise ValueError("alpha must be positive")
        if beta_param <= 0:
            raise ValueError("beta must be positive")

        dose = np.asarray(dose)
        # Using beta function ratio
        return 1 - beta(alpha, beta_param + dose) / beta(alpha, beta_param)

    @staticmethod
    def overdispersed_exponential(r: float, k: float, dose: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Overdispersed exponential dose-response model

        Args:
            r: Pathogen-host survival probability (0 < r < 1)
            k: Overdispersion parameter
            dose: Dose or array of doses

        Returns:
            Probability of infection
        """
        if not 0 < r < 1:
            raise ValueError("r must be in the range (0, 1)")

        dose = np.asarray(dose)
        return 1 - (1 + (r * dose) / k) ** (-k)

    @staticmethod
    def gauss_hypergeometric(alpha: float, beta_param: float, k: float,
                           dose: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Gauss hypergeometric form dose-response model

        Args:
            alpha: Shape parameter (> 0)
            beta_param: Shape parameter (> 0)
            k: Additional parameter
            dose: Dose or array of doses

        Returns:
            Probability of infection
        """
        if alpha <= 0:
            raise ValueError("alpha must be positive")
        if beta_param <= 0:
            raise ValueError("beta must be positive")

        dose = np.asarray(dose)
        result = np.zeros_like(dose, dtype=float)

        for i, d in enumerate(np.atleast_1d(dose)):
            if d == 0:
                result.flat[i] = 0
            else:
                try:
                    # Using hypergeometric function
                    hyp_val = hyp2f1(alpha, k, alpha + beta_param, -d / k)
                    result.flat[i] = 1 - hyp_val
                except:
                    # Fallback to approximation
                    result.flat[i] = np.nan
                    warnings.warn(f"Could not compute Gauss hypergeometric for dose {d}")

        return result.item() if result.size == 1 else result


class DoseResponseSelector:
    """Helper class for selecting and applying dose-response models"""

    # Model parameter requirements
    MODEL_PARAMS = {
        'exponential': ['r'],
        'fractional_poisson': ['p', 'mu'],
        'beta_poisson': ['alpha', 'beta'],
        'beta_poisson_approx': ['alpha', 'beta'],
        'simple_threshold': ['kmin', 'r'],
        'log_logistic': ['q1', 'q2'],
        'log_probit': ['q1', 'q2'],
        'weibull': ['q1', 'q2'],
        'simple_binomial': ['r'],
        'beta_binomial': ['alpha', 'beta'],
        'overdispersed_exponential': ['r', 'k'],
        'gauss_hypergeometric': ['alpha', 'beta', 'k']
    }

    def __init__(self):
        self.models = DoseResponseModels()
        self.model_map = {
            'exponential': self.models.exponential,
            'fractional_poisson': self.models.fractional_poisson,
            'beta_poisson': self.models.beta_poisson,
            'beta_poisson_approx': self.models.beta_poisson_approx,
            'simple_threshold': self.models.simple_threshold,
            'log_logistic': self.models.log_logistic,
            'log_probit': self.models.log_probit,
            'weibull': self.models.weibull,
            'simple_binomial': self.models.simple_binomial,
            'beta_binomial': self.models.beta_binomial,
            'overdispersed_exponential': self.models.overdispersed_exponential,
            'gauss_hypergeometric': self.models.gauss_hypergeometric
        }

    def get_model(self, model_name: str):
        """Get a dose-response model by name"""
        if model_name not in self.model_map:
            raise ValueError(f"Unknown model: {model_name}. Available models: {list(self.model_map.keys())}")
        return self.model_map[model_name]

    def calculate_risk(self, model_name: str, dose: Union[float, np.ndarray],
                       params: Dict[str, float]) -> Union[float, np.ndarray]:
        """
        Calculate infection risk using specified model

        Args:
            model_name: Name of the dose-response model
            dose: Dose or array of doses
            params: Dictionary of model parameters

        Returns:
            Probability of infection
        """
        # Validate parameters
        required_params = self.MODEL_PARAMS.get(model_name, [])
        missing_params = set(required_params) - set(params.keys())
        if missing_params:
            raise ValueError(f"Missing required parameters for {model_name}: {missing_params}")

        # Get model function
        model_func = self.get_model(model_name)

        # Prepare parameters in correct order
        param_values = [params[p] for p in required_params]

        # Calculate risk
        return model_func(*param_values, dose)

    def compare_models(self, dose: Union[float, np.ndarray],
                      models_params: Dict[str, Dict[str, float]]) -> Dict[str, np.ndarray]:
        """
        Compare multiple dose-response models

        Args:
            dose: Dose or array of doses
            models_params: Dictionary mapping model names to their parameters

        Returns:
            Dictionary mapping model names to calculated risks
        """
        results = {}

        for model_name, params in models_params.items():
            try:
                risk = self.calculate_risk(model_name, dose, params)
                results[model_name] = np.asarray(risk)
            except Exception as e:
                warnings.warn(f"Failed to calculate {model_name}: {e}")
                results[model_name] = np.full_like(dose, np.nan, dtype=float)

        return results


def calculate_n50(model_name: str, params: Dict[str, float]) -> float:
    """
    Calculate N50 (dose for 50% infection probability) for a given model

    Args:
        model_name: Name of the dose-response model
        params: Model parameters

    Returns:
        N50 value
    """
    from scipy.optimize import brentq

    selector = DoseResponseSelector()

    def objective(dose):
        return selector.calculate_risk(model_name, dose, params) - 0.5

    try:
        # Find N50 using Brent's method
        n50 = brentq(objective, 1e-10, 1e10)
        return n50
    except:
        return np.nan


def calculate_id50(model_name: str, params: Dict[str, float]) -> float:
    """
    Calculate ID50 (infectious dose for 50% of population)
    Alias for N50
    """
    return calculate_n50(model_name, params)