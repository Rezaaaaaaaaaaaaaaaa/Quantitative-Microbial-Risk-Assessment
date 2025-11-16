#' cdf log logistic fucntion
#'
#' estimates the cdf for the loglogistic
#'
#' @param x number
#' @param alpha number
#' @param beta number
#' @param gamm number
#'
#' @return number
#' @export
#'
#' @examples
ploglosistic <-  function(x, alpha, beta, gamm) {
  # cdf of the log logistic distribution
  # returns the cumulative probability of a log logistic distribution

  t <- (x-gamm)/beta
  cdf <-1/(1 + ((1/t)^alpha))
  return(cdf)
  #
}


#' cdf log logistic function
#'
#' Estimates the cdf for the truncated loglogistic function, which is used to
#' estimate n meal sizes.
#'
#' @param n number the sample size
#' @param alpha number = 2.2046
#' @param beta number = 75.072
#' @param gamm number = -0.9032
#' @param minX number minimum value for the truncated value = 5g
#' @param maxX number maximum value for the truncated value = 800g
#' @return number
#' @export
#'
#' @examples
rloglosisticTrunc <- function(n, alpha = 2.2046, beta = 75.072, gamm = -0.9032, minX = 5, maxX = 800, mySeed = 234){

  # draws random and reproducible sample from the truncated, loglogistic function
  # minX and maxX is set as default of 5 and 800g in accordance with the
  # QMRA assumptions of McBride,
  #

  set.seed(mySeed)

  step <- (maxX - minX)/10000 # by default splits x range into 10,000 steps
  x <- seq(minX,maxX, step)

  #estimates the cumulative probability
  cumProb <- ploglosistic(x, alpha, beta, gamm)

  #draws a uniform random sample
  U <- runif(n, min = min(cumProb), max = max(cumProb))

  # plots an empirical curve through the cdf
  estX <- approx(cumProb, x, U)
  sample <- estX$y
  return(sample)
}

