#' Estimate Illness Status based on Infection Status
#'
#' This function estimates illness status based on a matrix of infection status ('isInfected') where 1 represents infected and 0 represents not infected.
#' The estimation relies on the conditional probability of illness given infection (P(ill|inf)). Note the default value used here differs from comes from
#' table A1.2 of the WHO guidance on "Quantitative Microbial Risk Assessment: Application for Water Safety Management", originating from Teunis et al. 2008.
#' The function also accounts for suseptability which is set at 0.74 of the population being suseptible to norovirus
#'
#' @param isInfected A numeric matrix representing infection status (1 for infected, 0 for not infected).
#' @param probIll A numeric value representing the conditional probability of illness given infection status (default = 0.6).
#' @param propSuseptable A numeric value representing the propotion of population suseptiable to norovirus (default = 0.74)
#' @param mySeed An optional numeric seed for reproducibility in random number generation (default = 87).
#'
#' @return A numeric matrix representing the estimated illness status based on infection status and conditional probability.
#'
#' @details
#' This function estimates illness status based on the provided infection status matrix ('isInfected') and the given conditional probability of illness given infection.
#' It checks if the input infection status values are either 0 (not infected) or 1 (infected). If not, it throws an error.
#' The estimation relies on a random comparison using the conditional probability to determine illness status.
#'
#' @examples
#' infection_status <- matrix(c(1, 0, 1, 1, 0, 1), nrow = 2)
#' isIllNoro(infection_status)
#' isIllNoro(infection_status, probIll = 0.75, mySeed = 123)
#'
#' @seealso
#' \code{\link{runif}}
#'
#' @references
#' McBride (various spreadsheets),
#' Cressey (2021) SCREENING QUANTITATIVE MICROBIAL RISK ASSESSMENT (QMRA): KAIKOHE WASTEWATER TREATMENT PLANT,
#' Teunis et al. (2008). Add citation/reference details.
#'
#' @export
#'
isIllNoro <- function(isInfected, probIll = 0.60, propSuseptable = 0.74, mySeed = 87){
  set.seed(mySeed)

  # Check if values in isInfected matrix are either 0 or 1
  if (any(isInfected != 0 & isInfected != 1)) {
    stop("isInfected must be either 0 (not infected) or 1 (infected)")
  }

  adjProbIll <- probIll * propSuseptable

  isIll <- ifelse(adjProbIll > runif(length(isInfected)), 1, 0) * isInfected
  return(isIll)
}
