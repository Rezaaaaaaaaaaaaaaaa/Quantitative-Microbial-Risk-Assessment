#' Estimate Shellfish Meal Size for Multiple Iterations
#'
#' This function estimates the shellfish meal size in grams for 100 people across 'n' iterations.
#' Each iteration represents a group of 100 people, and 'n' determines the number of such iterations.
#'
#' @param n Number of iterations determining the number of groups (each of 100 people).
#'
#' @return A matrix representing the estimated meal sizes for each group (100 people) across 'n' iterations.
#' @export
#'
#' @examples
#' # Estimate meal size for 500 iterations
#' meal_sizes <- mealSize(500)
#'
mealSize <- function(n){
  # Returns a matrix of meal sizes (in grams) for 100 people across 'n' iterations
  meals <- 100 * n  # Calculate the total number of people (100 * n iterations)
  mealSize <- rloglosisticTrunc(n = meals)  # Generate meal sizes using a function like rloglosisticTrunc()
  mealSize <- matrix(mealSize, ncol = n, byrow = TRUE)  # Reshape the output into a matrix format
  return(mealSize)
}

#' Convert Shellfish Meal Size to Water Volume Equivalent
#'
#' Estimates the equivalent volume of water in millilitres (ml) based on shellfish meal sizes for 100 people across 'n' iterations.
#' Each iteration represents a group of 100 people, exposed to the same Bioaccumulation Factor (BAF).
#' It assumes that BAF is described by truncate normal distribution with minimum and maximum values of 1 and 800g
#' mean = 49.9 and standard deviation = 20.03
#' It also assumes that meal size is described by a truncated log logistic (min 5g and maximum 800g) and
#' alpha = 	2.2046, beta = 75.072 and gamma =	-0.9032. These factors are hard coded
#'
#' @param n Number of iterations determining the number of groups (each of 100 people).
#'
#' @return A matrix representing the estimated water volume equivalents (in ml) for each group (100 people) across 'n' iterations.
#' @export
#'
#' @examples
#' # Estimate water volume equivalent for 500 iterations
#' water_equiv <- waterEquiv(500)
#'
waterEquiv <- function(n){
  # Calculate water volume equivalents based on shellfish meal sizes and Bioaccumulation Factor (BAF)
  meals <- mealSize(n)  # Estimate shellfish meal sizes for 'n' iterations
  BioAccumulation <- BAF(n)  # Get the Bioaccumulation Factor for 'n' iterations
  waterVolEquiv <- meals %*% diag(BioAccumulation)  # Calculate water volume equivalents each tranch of people gets the same BAF
  return(waterVolEquiv)
}
