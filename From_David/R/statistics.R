#' Estimate Mode of a Vector
#'
#' This function estimates the mode of a vector based on the most frequently occurring value.
#' It identifies the value that appears most frequently (mode) in the input vector.
#'
#' @param x A numeric or categorical vector to estimate the mode from.
#'
#' @return The mode of the input vector 'x'.
#'
#' @details
#' The function identifies the mode of the provided vector by finding the most frequently occurring value.
#' In cases where multiple values have the same maximum frequency, the function returns the first one encountered.
#' This implementation refers to the approach detailed at https://stackoverflow.com/questions/2547402/how-to-find-the-statistical-mode.
#'
#' @examples
#' vector <- c(1, 2, 2, 3, 4, 4, 4, 5)
#' Mode(vector)
#'
#' @references
#' See https://stackoverflow.com/questions/2547402/how-to-find-the-statistical-mode
#'
#' @export
#'
Mode <- function(x) {
  ux <- unique(x)
  ux[which.max(tabulate(match(x, ux)))]
}

#' Create Statistics DataFrame from isIllNoro Matrix
#'
#' This function takes the 'isIllNoro' matrix and generates a dataframe with statistics commonly used in risk reports.
#' The statistics include Minimum, Maximum, Mean, Mode, Median, Standard Deviation, and Variance .
#' (Kurtosis and Skewness is not currently included in the statistics)
#'
#' @param isIllNoro A matrix representing illness status data.
#'
#' @return A dataframe containing statistics named similarly to those found in risk assessment reports.
#'
#' @details
#' The function calculates various statistics (Minimum, Maximum, Mean, Mode, Median, Standard Deviation, Variance, Skewness, Kurtosis)
#' based on the provided 'isIllNoro' matrix and creates a dataframe with these statistics named accordingly.
#' The 'Mode' function used here refers to a custom function for estimating the mode of a vector.
#'
#' @seealso
#' \code{\link{Mode}}
#'
#' @examples
#' # Assuming isIllNoro is a matrix of illness status data
#' isIllNoro <- matrix(c(rep(c(0,1),50),rep(c(0,0,0,1),25)), ncol =2)
#' stats_df <- create_stats_df(isIllNoro)
#'
#' @export
#'
create_stats_df <- function(isIllNoro) {

  # e1071 library is laded to estimate skewness
  if (!requireNamespace("e1071", quietly = TRUE)) {
    # Load the package if it's not already loaded
    require("e1071")
  }

  my_vec <- colSums(isIllNoro)

  StatName <- c(
    "Minimum",
    "Maximum",
    "Mean",
    "Mode",
    "Median",
    "Std. Deviation",
    "Variance"
    #"Skewness",
    #"Kurtosis"
  )

  Val <- c(
    min(my_vec),
    max(my_vec),
    mean(my_vec),
    Mode(my_vec), # Assuming Mode() is a custom function estimating mode
    median(my_vec),
    sd(my_vec),
    var(my_vec)
    #skewness(my_vec),
    #kurtosis(my_vec)
  )

  df <- data.frame(StatName, Val)
  return(df)
}


#' Create Percentile DataFrame from isIllNoro Matrix
#'
#' This function takes the 'isIllNoro' matrix and generates a dataframe with percentiles commonly used in risk assessment reports.
#' The percentiles include values at 0.01, 0.025, 0.05, 0.1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.9, 0.95, 0.975, 0.99, 0.995, and 0.999.
#'
#' @param isIllNoro A matrix representing illness status data.
#'
#' @return A dataframe containing percentiles named similarly to those found in risk assessment reports.
#'
#' @details
#' The function calculates various percentiles based on the provided 'isIllNoro' matrix and creates a dataframe with these percentiles named accordingly.
#'
#' @examples
#' # Assuming isIllNoro is a matrix of illness status data
#' isIllNoro <- matrix(c(rep(c(0,1),50),rep(c(0,0,0,1),25)), ncol =2)
#' create_percentile_df(isIllNoro)
#' @export
#'
create_percentile_df <- function(isIllNoro) {
  my_vec <- colSums(isIllNoro)

  if (length(my_vec) < 1000) {
    warning("The number of iterations is less than 1000. Consider using a larger dataset for more accurate percentiles.")
  }

  Percentile <- c(
    0.010, 0.025, 0.050, 0.100, 0.200, 0.250, 0.300, 0.350, 0.400, 0.450, 0.500,
    0.550, 0.600, 0.650, 0.700, 0.750, 0.800, 0.900, 0.950, 0.975, 0.990, 0.995, 0.999
  )

  Val <- unname(quantile(my_vec, Percentile))

  df <- data.frame(Percentile, Val)
  return(df)
}

