#' solve_x
#'
#' helper function, solves the quadratic equation
#'
#' @param slope number
#' @param height number
#' @param area number
#'
#' @return number
#' @export
#'
#' @examples
#' solve_x(1,0,0.5)
solve_x <- function(slope, height, area){
  # Takes slope intercept and area under curve and returns x
  # Used the quadratic equation
  a = slope/2 # slope of segment
  b = height # height at point i
  c = -area # area under curve at point i (sum of areas = p)
  discriminant <- (b^2) - (4*a*c)
  discriminant <- pmax(0, discriminant) # ensures discriminant does not result in <0

  x <- (-b + sqrt(discriminant)) / (2*a)
  return(x)
}
