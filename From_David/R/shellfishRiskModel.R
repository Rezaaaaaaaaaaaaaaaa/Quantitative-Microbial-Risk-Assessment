#' Shellfish Consumption Risk Model
#'
#' This function calculates the risk of norovirus infection associated with shellfish consumption.
#' This model assumes norovirus is in a disagregated state
#'
#'
#' @param n Integer specifying the number of Monte Carlo simulations.
#' @param X0 Numeric specifying the minimum norovirus concentration in influent (gc/L).
#' @param X50 Numeric specifying the median norovirus concentration in influent (gc/L).
#' @param X100 Numeric specifying the maximum norovirus concentration in influent (gc/L).
#' @param LRV Numeric specifying the log reduction value for norovirus during sewage treatment.
#' @param P Numeric number (between 0 and 1) percentile for Xp (Our default values 0.95)
#' @param MHF Numeric Method Harmonisation Factor (Our default value is 18.5)
#' @param myCSVFile Character string specifying the name of the CSV file containing dilution data.
#' @param mySite Character string specifying the column name for site-specific dilution values.
#'
#' @return Numeric vector representing the total number of norovirus-infected cases in each simulation of 100 people.
#'
#' @details
#' This function combines various sub-functions to estimate the risk of norovirus infection
#' based on shellfish consumption. It involves estimating effluent concentration, dilution factor,
#' diluted effluent concentration, water equivalent consumed, raw dose, rounded dose, probability of infection,
#' infection status, and the total number of infected cases in each simulation.
#'
#' @examples
#' \dontrun{
#' # Example usage
#' results <- shellFishRiskModel(1000, 0.5, 1.5, 2.0, 1.0, 0.2, 2.5, "your_data.csv", "yourSiteColumn")
#' }
#'
#' @seealso
#' \code{\link{estEffluentConc}}, \code{\link{estDilution}}, \code{\link{waterEquiv}},
#' \code{\link{roundDose}}, \code{\link{doseResponseNoro}}, \code{\link{isInfected}},
#' \code{\link{isIllNoro}}
#'
#' @export
shellfishRiskModel <- function(n, X0, X50, X100, LRV, P, MHF, myCSVFile, mySite){

  effluentConc <- estEffluentConc(n, X0, X50, X100, LRV, P, MHF)
  dilutionFactor <- estDilution(myCSVFile, mySite, n)
  dilutedEffluentConc <- effluentConc / dilutionFactor

  waterEquivConsumed <- waterEquiv(n)
  rawDose <-  waterEquivConsumed %*% diag(dilutedEffluentConc) # not this is used to multiple each column by a single value
  roundedDose <- roundDose(rawDose)
  probInfection <- doseResponseNoro(roundedDose)
  isInfected <- isInfected(probInfection)
  isIllNoro <- isIllNoro(isInfected)
  results <- colSums(isIllNoro)
  return(results)
}
