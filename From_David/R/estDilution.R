#' Estimate Dilution Values
#'
#' This function reads in a CSV file, extracts specified columns, and returns n estimates
#' of dilutions drawn from the empirical cumulative distribution function (CDF) of dilution.
#'
#' @param csv_file_name Character string specifying the name of the CSV file.
#' @param mySite Character string specifying the column name for the site dilution values.
#' @param n Integer specifying the number of dilution estimates to generate.
#' @param mySeed Integer specifying the seed for reproducibility in random sampling.
#'
#' @return Numeric vector containing n estimates of dilution values.
#'
#' @details
#' The function reads the CSV file, extracts the specified columns, and checks for validity
#' in the 'cumProb' and 'siteDilution' columns. It then samples from the empirical distribution
#' based on the estimated CDF of dilution.
#'
#' @examples
#' \dontrun{
#' # Example usage
#' result <- estDilution("your_data.csv", "yourSiteColumn", 100, mySeed = 1234)
#' }
#'
#' @seealso
#' \code{\link{read.csv}}, \code{\link{approx}}
#'
#' @importFrom stats runif approx
#'
#' @export
estDilution <- function(csv_file_name, mySite, n, mySeed = 4321) {
  # reads in file and takes returns n estimates of dilutions  drawn from the estimated
  # (empirical) cdf of dilution

  set.seed(mySeed)
  p <- runif(n)

  # read in data an rename columns
  df <-  read.csv(csv_file_name)
  df <- df[, c("cumProb", mySite)]
  colnames(df) <-  c("cumProb", "siteDilution")

  # Check if 'cumProb' column has values outside the valid range
  if (any(df$cumProb < 0 | df$cumProb > 1)) {
    stop("Error: 'cumProb' column has values outside the valid range [0, 1].")
  }

  # Check if 'siteDilution' column has values outside the valid range
  if (min(df$siteDilution < 0)) {
    stop("Error: 'the dilution values are negative, please check the values in the csv file")
  }

  # sample from empirical distribution
  interpolated_value <- approx(x = df$cumProb, y = df$siteDilution, xout = p)
  interpolated_value <- interpolated_value$y
  return(interpolated_value)
}
