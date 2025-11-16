
#' Rounds a matrix of dose values to the nearest integers in a stochastic manner.
#'
#' This function performs stochastic rounding on a matrix of 'rawDose' values, providing a matrix of rounded doses based on randomness.
#'
#' @param rawDose A numeric matrix representing the raw doses to be rounded.
#' @param mySeed An optional numeric seed for reproducibility in random number generation.
#'
#' @return A numeric matrix representing the rounded doses based on stochastic rounding.
#'
#' @examples
#' matrix_input <- matrix(c(3.6, 7.2, 5.4, 6.7), nrow = 2)
#' roundDose(matrix_input)
#' roundDose(matrix_input, mySeed = 123)
#'
#' @export
#'
roundDose <- function(rawDose, mySeed= 245){

  set.seed(mySeed)

  floorDose <- floor(rawDose)
  remander <- rawDose-floorDose

  random <- runif(length(remander))
  random <- matrix(random, nrow = nrow(remander))

  oneOrZero <- ifelse(remander > random, 1, 0)
  roundedDose <- floorDose + oneOrZero
  return(roundedDose)
}
