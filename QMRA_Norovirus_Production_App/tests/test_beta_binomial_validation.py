"""
Validation Test for Beta-Binomial vs Beta-Poisson Dose-Response Models

This test validates the Beta-Binomial implementation against David's betaBinomial.xlsx
spreadsheet data. It demonstrates the critical difference between the two models
for norovirus parameters (alpha=0.04, beta=0.055).

Reference: David's email Nov 12, 2025 and betaBinomial.xlsx
"""

import numpy as np
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from qmra_core.dose_response import BetaPoissonModel
from scipy.special import gammaln


def beta_binomial_infection_probability(dose, alpha, beta):
    """
    Calculate infection probability using Beta-Binomial model (CORRECT for norovirus).

    This is the EXACT model that should be used for norovirus.
    Reference: Bell Island QMRA Appendix B, Equation 5, page 34
               McBride (2017), NIWA Client Report 2017350HN

    Formula: P(inf) = 1 - B(α, β+i) / B(α, β)

    Where B is the beta function: B(α,β) = Γ(α)Γ(β)/Γ(α+β)

    Excel equivalent:
    = 1 - EXP(GAMMALN(β+i) + GAMMALN(α+β) - GAMMALN(α+β+i) - GAMMALN(β))

    Args:
        dose: Pathogen dose (organisms/virions)
        alpha: Shape parameter (for norovirus: 0.04)
        beta: Scale parameter (for norovirus: 0.055)

    Returns:
        Probability of infection (0-1)
    """
    dose = np.asarray(dose)

    # Beta-Binomial formula using log-gamma functions
    # This avoids numerical overflow/underflow issues
    log_prob_complement = (
        gammaln(beta + dose) +
        gammaln(alpha + beta) -
        gammaln(alpha + beta + dose) -
        gammaln(beta)
    )

    prob = 1.0 - np.exp(log_prob_complement)
    return np.clip(prob, 0, 1)


def beta_poisson_approximation(dose, alpha, beta):
    """
    Calculate infection probability using Beta-Poisson approximation (INVALID for norovirus).

    This is what the current code incorrectly uses.

    Formula: P(inf) = 1 - (1 + dose/β)^(-α)

    Validity criteria:
    - β >> 1 (beta must be much greater than 1)
    - α << β (alpha must be much less than beta)

    For norovirus (α=0.04, β=0.055):
    - β is NOT >> 1 (it's 0.055, much less than 1) ❌
    - Therefore this approximation is INVALID ❌

    Args:
        dose: Pathogen dose (organisms/virions)
        alpha: Shape parameter
        beta: Scale parameter

    Returns:
        Probability of infection (0-1)
    """
    dose = np.asarray(dose)
    prob = 1 - np.power(1 + dose / beta, -alpha)
    return np.clip(prob, 0, 1)


def test_against_david_excel():
    """
    Test against David's betaBinomial.xlsx data.

    Expected values from David's spreadsheet:
    Dose    Beta-Binomial (CORRECT)    Beta-Poisson (CURRENT/WRONG)
    1       0.421053 (42.1%)            0.111445 (11.1%)
    10      0.480735 (48.1%)            0.188069 (18.8%)
    30      0.503631 (50.4%)            0.222863 (22.3%)
    100     0.527157 (52.7%)            0.259364 (25.9%)
    1000    0.568829 (56.9%)            0.324518 (32.5%)
    """

    # Norovirus parameters (Teunis et al. 2008)
    alpha = 0.04
    beta = 0.055

    # Test doses from David's spreadsheet
    test_doses = np.array([1, 10, 30, 100, 1000])

    # Expected values from David's betaBinomial.xlsx
    expected_beta_binomial = np.array([0.421053, 0.480735, 0.503631, 0.527157, 0.568829])
    expected_beta_poisson = np.array([0.111445, 0.188069, 0.222863, 0.259364, 0.324518])

    # Calculate using both models
    calculated_beta_binomial = beta_binomial_infection_probability(test_doses, alpha, beta)
    calculated_beta_poisson = beta_poisson_approximation(test_doses, alpha, beta)

    # Display results
    print("=" * 100)
    print("VALIDATION TEST: Beta-Binomial vs Beta-Poisson for Norovirus")
    print("=" * 100)
    print(f"\nNorovirus Parameters: alpha = {alpha}, beta = {beta}")
    print("\nReference: David's betaBinomial.xlsx (Nov 12, 2025)")
    print("-" * 100)

    print(f"\n{'Dose':<8} | {'Beta-Binomial (CORRECT)':<25} | {'Beta-Poisson (WRONG)':<25} | {'Underestimation':<15}")
    print(f"{'':8} | {'Expected':<12} {'Calculated':<12} | {'Expected':<12} {'Calculated':<12} | {'Factor':<15}")
    print("-" * 100)

    all_pass = True
    tolerance = 0.001  # 0.1% tolerance

    for i, dose in enumerate(test_doses):
        bb_expected = expected_beta_binomial[i]
        bb_calc = calculated_beta_binomial[i]
        bp_expected = expected_beta_poisson[i]
        bp_calc = calculated_beta_poisson[i]

        underestimation_factor = bb_expected / bp_expected

        # Check if Beta-Binomial matches expected
        bb_match = abs(bb_calc - bb_expected) < tolerance
        bp_match = abs(bp_calc - bp_expected) < tolerance

        bb_status = "[OK]" if bb_match else "[X] FAIL"
        bp_status = "[OK]" if bp_match else "[X] FAIL"

        print(f"{dose:<8} | {bb_expected:.6f} {bb_status:<3} {bb_calc:.6f} {bb_status:<3} | "
              f"{bp_expected:.6f} {bp_status:<3} {bp_calc:.6f} {bp_status:<3} | "
              f"{underestimation_factor:.2f}x")

        if not (bb_match and bp_match):
            all_pass = False

    print("-" * 100)

    # Summary statistics
    print("\n" + "=" * 100)
    print("CRITICAL FINDINGS:")
    print("=" * 100)

    print("\n1. BETA-BINOMIAL vs BETA-POISSON COMPARISON:")
    for i, dose in enumerate(test_doses):
        bb = expected_beta_binomial[i]
        bp = expected_beta_poisson[i]
        diff = bb - bp
        factor = bb / bp
        print(f"   Dose {dose:>4}: Beta-Binomial = {bb:.1%}, Beta-Poisson = {bp:.1%}, "
              f"Difference = {diff:.1%}, Factor = {factor:.2f}x")

    print("\n2. RISK UNDERESTIMATION:")
    print(f"   At dose = 1 virion:  {expected_beta_binomial[0]:.1%} vs {expected_beta_poisson[0]:.1%} "
          f"= {expected_beta_binomial[0]/expected_beta_poisson[0]:.1f}x UNDERESTIMATION [WARNING]")
    print(f"   At dose = 10 virions: {expected_beta_binomial[1]:.1%} vs {expected_beta_poisson[1]:.1%} "
          f"= {expected_beta_binomial[1]/expected_beta_poisson[1]:.1f}x UNDERESTIMATION [WARNING]")
    print(f"   At dose = 30 virions: {expected_beta_binomial[2]:.1%} vs {expected_beta_poisson[2]:.1%} "
          f"= {expected_beta_binomial[2]/expected_beta_poisson[2]:.1f}x UNDERESTIMATION [WARNING]")

    print("\n3. BETA-POISSON VALIDITY CHECK:")
    print(f"   Required: beta >> 1 (beta much greater than 1)")
    print(f"   Actual:   beta = {beta} [X] INVALID")
    print(f"   Required: alpha << beta (alpha much less than beta)")
    print(f"   Actual:   alpha = {alpha}, beta = {beta} [OK] Valid")
    print(f"   CONCLUSION: Beta-Poisson approximation is INVALID for norovirus")

    print("\n4. RECOMMENDATION:")
    print("   [OK] MUST use Beta-Binomial model for norovirus")
    print("   [X] DO NOT use Beta-Poisson approximation for norovirus")
    print("   Reference: Bell Island QMRA (McBride 2017), Appendix B, page 33")

    print("\n" + "=" * 100)

    if all_pass:
        print("[OK] ALL TESTS PASSED - Calculations match David's Excel spreadsheet")
    else:
        print("[X] SOME TESTS FAILED - Check calculations")

    print("=" * 100 + "\n")

    return all_pass


def test_current_code_beta_poisson():
    """
    Test the CURRENT (incorrect) Beta-Poisson implementation in dose_response.py
    """
    print("\n" + "=" * 100)
    print("TESTING CURRENT CODE: BetaPoissonModel class")
    print("=" * 100)

    # Norovirus parameters
    params = {
        "alpha": 0.04,
        "beta": 0.055,
        "source": "Teunis et al. (2008)"
    }

    model = BetaPoissonModel(params)

    test_doses = np.array([1, 10, 30, 100, 1000])

    # Calculate using current code
    current_results = model.calculate_infection_probability(test_doses)

    # Expected Beta-Binomial (correct)
    expected_correct = beta_binomial_infection_probability(test_doses, params["alpha"], params["beta"])

    print(f"\nDose | Current Code (Beta-Poisson) | Correct (Beta-Binomial) | Error")
    print("-" * 80)

    for i, dose in enumerate(test_doses):
        current = current_results[i] if isinstance(current_results, np.ndarray) else current_results
        correct = expected_correct[i]
        error = ((current - correct) / correct) * 100

        print(f"{dose:<5} | {current:.6f} ({current:.1%}) | {correct:.6f} ({correct:.1%}) | {error:+.1f}%")

    print("\n[WARNING] CURRENT CODE IS USING BETA-POISSON (INVALID FOR NOROVIRUS)")
    print("[OK] MUST BE CHANGED TO BETA-BINOMIAL")
    print("=" * 100 + "\n")


if __name__ == "__main__":
    print("\n" + "=" * 100)
    print("CRITICAL QMRA VALIDATION TEST")
    print("Beta-Binomial vs Beta-Poisson Dose-Response Models for Norovirus")
    print("=" * 100 + "\n")

    # Run validation against David's Excel
    test_against_david_excel()

    # Test current code
    test_current_code_beta_poisson()

    print("\n" + "=" * 100)
    print("NEXT STEPS:")
    print("1. Implement BetaBinomialModel class in dose_response.py")
    print("2. Update pathogen_database.py to use beta_binomial for norovirus")
    print("3. Rerun all QMRA calculations with correct model")
    print("4. Schedule call with David to review findings")
    print("=" * 100 + "\n")
