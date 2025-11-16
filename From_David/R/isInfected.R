#' Determine Infection Status based on Probabilities
#'
#' This function determines whether an individual is infected or not based on a matrix of probabilities ('probInfection').
#' It checks if the input probabilities are within the range [0, 1] inclusive, and if not, throws an error.
#' If the probabilities are within the valid range, the function generates a random seed-based comparison to determine infection status.
#'
#' @param probInfection A numeric matrix representing probabilities of infection for individuals.
#' @param mySeed An optional numeric seed for reproducibility in random number generation (default = 98).
#'
#' @return A numeric matrix indicating infection status (1 for infected, 0 for not infected).
#'
#' @details
#' This function evaluates whether individuals are infected based on the provided probabilities.
#' It checks if the input probabilities are within the acceptable range [0, 1].
#' If the input probabilities are outside this range, the function throws an error.
#' Otherwise, it generates a seed-based random comparison to determine the infection status.
#'
#' @examples
#' prob_matrix <- matrix(runif(25), nrow = 5)
#' isInfected(prob_matrix)
#' isInfected(prob_matrix, mySeed = 123)
#'
#' @seealso
#' \code{\link{runif}}
#'
#' @export
#'
isInfected <- function(probInfection, mySeed = 98) {
  # Check if values in probInfection matrix are in the range [0, 1]
  if (any(probInfection < 0) || any(probInfection > 1)) {
    stop("Input probabilities must be within the range [0, 1]")
  }

  set.seed(mySeed)

  isInfected <- ifelse(probInfection > runif(length(probInfection)), 1, 0)
  return(isInfected)
}
