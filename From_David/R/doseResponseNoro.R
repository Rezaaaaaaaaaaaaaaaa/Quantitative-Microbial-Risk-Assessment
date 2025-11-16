#' Calculate Probability of Infection based on Dose-Response Model
#'
#' This function computes the probability of infection based on a dose-response model.
#' It takes parameters 'alpha' and 'beta', along with the actual rounded dose, and returns the probability of infection.
#' The dose-response model used is based on the formula:
#' \deqn{1 - \exp \left( \text{lgamma}(\beta + \text{roundedDose}) + \text{lgamma}(\alpha + \beta) - \text{lgamma}(\alpha + \beta + \text{roundedDose}) - \text{lgamma}(\beta) \right)}
#' The R equivalent of \code{GAMMALN(x)} is \code{lgamma(x)}.
#' Default values for 'alpha' and 'beta' are taken from Tunis et al. (2008).
#'
#' @param roundedDose A numeric value representing the rounded dose for dose-response calculation.
#' @param alpha A numeric parameter representing the alpha value in the dose-response function (default = 0.04).
#' @param beta A numeric parameter representing the beta value in the dose-response function (default = 0.055).
#'
#' @return A numeric value representing the probability of infection based on the dose-response model.
#'
#' @references
#' Teunis et al. (2008). [Add citation/reference details].
#'
#' @examples
#' doseResponseNoro(5)
#' doseResponseNoro(10, alpha = 0.03, beta = 0.06)
#'
#' @seealso
#' \code{\link{lgamma}}
#'
#' @export
#'
doseResponseNoro <- function(roundedDose, alpha = 0.04, beta = 0.055) {
  Pinf <- 1 - exp((lgamma(beta + roundedDose) + lgamma(alpha + beta) - lgamma(alpha + beta + roundedDose) - lgamma(beta)))
  Pinf <- ifelse(Pinf < 0, 0, Pinf)
  return(Pinf)
}
