#' dhockey
#'
#' Estimates the density of the hockey distribution at any value of bug
#' concentration, x. Does This change Text
#'
#'
#' @param x vector, bug concentration
#' @param X0 number, minimum bug concentration
#' @param X50 number, median big concentration
#' @param X100 number, maximum bug concentration
#' @param P number (between 0 and 1) percentile for Xp
#'
#' @return vector, of probability densities
#' @export
#'
#' @examples
#' dhockey(0,10,100,10000)
#'
dhockey <- function(x, X0, X50, X100, P = 0.95) {
  # These are user defined values for areas (same proposed by McBride),
  A <- 0.5 # area between X0 and X50
  B <- P - 0.5 # area X50 and X95 s by McBride
  C <- 1 - P # Xp to X100, called q by McBride

  # calculated parameters for McBride
  h1 <- (2 * A) / (X50 - X0)
  Xp <-
    (X50 + X100 + 1 / h1 - (((X100 - X50) ^ 2) + (1 / (h1 ^ 2)) + ((X50 / h1) *
                                                                     (2 - 8 * C)) + ((X100 / h1) * (2 - 8 * B))) ^ 0.5) / 2
  h2 <- (2 * C) / (X100 - Xp)
  ## checked they work like grahams, so that is good

  # calculates the slopes and intercepts of each section
  ## Section 1 (x <= X50)
  m1 <- (h1 - 0) / (X50 - X0)

  ## Section 2 (x50 < x <= X95)
  m2 <- (h2 - h1) / (Xp - X50)

  ## Section 3 (x> X95)
  m3 <- (0 - h2) / (X100 - Xp)

  h <- ifelse(x <= X0, 0,
              ifelse(x <= X50, m1 * (x - X0),
                     ifelse(
                       x <= Xp ,  (m2 * (x - X50) + h1),
                       ifelse(x <= X100, (m3 * (x - Xp) + h2),
                              ifelse(x > X100, 0, 0))
                     )))
  return(h)
}



#' phockey
#'
#' Returns the cumulate probability for any value of bug.
#'
#'
#' @param x vector, bug concentration
#' @param X0 number, minimum bug concentration
#' @param X50 number, median big concentration
#' @param X100 number, maximum bug concentration
#' @param P number (between 0 and 1) percentile for Xp
#'
#' @return vector, cumulative probaility
#' @export
#'
#' @examples
#' phockey(100, 10, 100, 1000)
#'
phockey <- function(x, X0, X50, X100, P = 0.95){
  # returns the cumulative probability for any given value of x (bug concentraion)

  # These are user defined values for areas (same proposed by McBride),
  A <- 0.5 # area between X0 and X50
  B <- P-0.5 # area X50 and X95 s by McBride
  C <- 1-P # Xp to X100, called q by McBride

  # calculated parameters for McBride
  h1 <- (2*A)/(X50-X0)
  Xp <- (X50 + X100 + 1/h1 -(((X100-X50)^2) + (1/(h1^2)) + ((X50/h1)*(2-8*C)) + ((X100/h1)*(2-8*B)))^0.5)/2
  h2 <- (2*C)/(X100 - Xp)
  ## checked they work like grahams, so that is good

  # calculates the slopes and intercepts of each section
  ## Section 1 (x <= X50)
  m1 <- (h1-0)/(X50-X0)

  ## Section 2 (x50 < x <= X95)
  m2 <- (h2-h1)/(Xp-X50)

  ## Section 3 (x> X95)
  m3 <- (0-h2)/(X100-Xp)

  p <- ifelse(x <= X0,0,
              ifelse(x <= X50, (m1*(x-X0)^2)/2,
                     ifelse(x <=Xp , (0.5 +(((2*h1)+(m2*(x-X50)))/2)*(x-X50)),
                            ifelse(x <=X100, (P +(((2*h2)+(m3*(x-Xp)))/2)*(x-Xp)),
                                              1)

                            )))
  return(p)
}


#' qhockey
#'
#' Estimate bug concentration for any value of cumulative probability for the hockey stick distribution
#'
#' @param p vector, probability for the value of x to be calculated
#' @param X0 number, minimum bug concentration
#' @param X50 number, median big concentration
#' @param X100 number, maximum bug concentration
#' @param P number (between 0 and 1) percentile for Xp
#'
#' @return vector of bug concentrations
#' @export
#'
#' @examples
#' qhockey(0.5, 10, 100, 1000)
#'
qhockey <- function(p, X0, X50, X100, P = 0.95){
  # This function calculates the quantiles for the hockeystick distribution
  # Takes a vector of probabilities, p, and the key parameters for the hockey stick
  # distribution X0, X50 and X100 and returns the virus concentration at those values
  # assumes breakpoint is 0.95

  ## Data checks
  if(min(p)<0|max(p)>1) {stop("Probablity is less than 0 or greater than 1, please check probabilities")}
  if(X0 > X50 |X50 > X100 | X50-X0 > X100 -X50 ) {stop("There is a problem with the virus conc data")}

  # These are user defined values for areas (same proposed by McBride),
  A <- 0.5 # area between X0 and X50
  B <- P-0.5 # area X50 and X95 s by McBride
  C <- 1-P # Xp to X100, called q by McBride

  # calculated parameters for McBride
  h1 <- (2*A)/(X50-X0)
  Xp <- (X50 + X100 + 1/h1 -(((X100-X50)^2) + (1/(h1^2)) + ((X50/h1)*(2-8*C)) + ((X100/h1)*(2-8*B)))^0.5)/2
  h2 <- (2*C)/(X100 - Xp)
  ## checked they work like Grahams, so that is good

  # calculates the slopes and intercepts of each section
  ## Section 1 (x <= X50)
  m1 <- h1/(X50-X0)
  c1 <- 0 # as the height is zero for X0

  ## Section 2 (x50 < x <= X95)
  m2 <- (h2-h1)/(Xp-X50)
  c2 <- h1

  ## Section 3 (x> X95)
  m3 <- -(h2)/(X100-Xp)
  c3 <- h2

  my_x <-  ifelse(p <= 0.5,
                  solve_x(m1, c1, p) + X0,
                  ifelse(p <= P,
                         solve_x(m2, c2, p-0.5) + X50,
                         ifelse(p == 1,
                                X100,
                                solve_x(m3, c3, p-P) + Xp)
                  )
  )
  return(my_x)
}



#' rhockey
#'
#' Draws a random (and reproducible) sample from the hockey stick distribution
#'
#' @param n number, sample size
#' @param X0 number, minimum bug concentration
#' @param X50 number, median big concentration
#' @param X100 number, maximum bug concentration
#' @param P number (between 0 and 1) percentile for Xp
#' @param mySeed number, random seed
#'
#' @return vector, bug concentrations
#' @export
#'
#' @examples
#' rhockey(10, 10, 100, 1000, P = 0.95, mySeed = 123)
rhockey <- function(n, X0, X50, X100, P = 0.95, mySeed = 123){
  # This function draws a random sample from the calculates the hockey stick distribution probabilities, n, is the number of samples and
  # the key parameters for the hockey stick distribution X0, X50 and X100 and returns the virus concentration at those values
  # assumes breakpoint is 0.95

  set.seed(mySeed) # makes the code reproducible

  U <- stats::runif(n)

  x <- qhockey(U, X0, X50, X100, P = P)
  return(x)
}
