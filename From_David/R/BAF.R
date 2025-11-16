#' Bioaccumulation Factor (BAF) Calculation for Shellfish
#'
#' BAF (Bioaccumulation Factor) represents the tendency of shellfish to accumulate pathogens in their flesh.
#'
#' @param n Number of iterations to generate BAF values.
#' @param mean_value Mean value for BAF (default = 44.9).
#' @param sd_value Standard deviation value for BAF (default = 20.93).
#' @param lower Lower bound for truncation in the distribution (default = 1).
#' @param upper Upper bound for truncation in the distribution (default = 100).
#'
#' @return A vector containing generated BAF values.
#' @export
#'
#' @examples
#' # Generate BAF values for 1000 iterations using default parameters
#' baf_values <- BAF(1000)
#'
BAF <- function(n,
                mean_value = 44.9,
                sd_value = 20.93,
                lower = 1,
                upper = 100){
  # Generate random samples from the truncated normal distribution
  require(truncnorm)

  BAF <- rtruncnorm(n = n, a = lower, b = upper, mean = mean_value, sd = sd_value)
  return(BAF)
}
