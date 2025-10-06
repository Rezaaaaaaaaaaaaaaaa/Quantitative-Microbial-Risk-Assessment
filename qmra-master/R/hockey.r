#' Pdf of the hockey distribution (McBride, 2018)
#'@param x numeric input
#'@param a minimum value
#'@param b central measure, if traditional Hockey stick distribution then 50% of mass either side of b
#' (i.e., Median)
#'@param c right tie of distribution
#'@param d maximum value
#'@param h1 height of distribution at b, only required if h2 is NULL
#'@param h2 height of distribution at c, only required if h1 is NULL, if
#'both h1 and h2 are supplied then h2 will be ignored.
#'@export
phockey <- function(x, a, b, c, d, h1, h2 = NULL){
    if(length(x) == 1){
        fx = hockey(x = x, a = a, b = b, c = c, d = d, h1 = h1, h2 = h2)
    }
    if(length(x) > 1){
        fx = sapply(x, function(y) hockey(x = y, a = a, b = b, c = c, d = d, h1 = h1, h2 = h2))
        }
    return(fx)
}

#' Pdf for phockey 
setGeneric("hockey",
           function(x, a, b, c, d, h1, h2){
               standardGeneric("hockey")
               })
setMethod("hockey",
          c(x = "numeric", a = "numeric", b= "numeric", c= "numeric", d = "numeric", h1= "numeric", h2 = NULL),
          function(x, a, b, c, d, h1, h2 = NULL){
              if(h1  > 2/(c - a)){stop("h1 muxt be less than or equal to 2/(c - a)")}
              h2 = (2 - h1*(c - a))/(d - b)
              if(h1 < h2){stop("h1 must be greater than h2")}
              if(a > b | b > c | c > d){stop("a < b < c < d")}
              if(x > a & x <= b){
                  fx = (h1 * (x - a))/(b - a)
              }else{
                  if(x > b & x < c){
                      fx = (((h1 - h2)*(c - x))/(c - b)) + h2
                  }else{
                      if(x >= c & x < d){
                          fx = (h2 * (d - x))/(d - c)
                      }else{
                          fx = 0
                      }
                  }
              }
              return(fx)
          }
          )
setMethod("hockey",
          c(x = "numeric", a = "numeric", b= "numeric", c= "numeric", d = "numeric", h1= NULL, h2 = "numeric"),
          function(x, a, b, c, d, h1 = NULL, h2){
              if(h2  > 2/(d - b)){stop("h2 must be less than or equal to 2/(d - b)")}
              h1 = (2 - h2*(d - b))/(c - a)
              if(h1 < h2){stop("h1 must be greater than h2")}
              if(a > b | b > c | c > d){stop("a < b < c < d")}
              if(x > a & x <= b){
                  fx = (h1 * (x - a))/(b - a)
              }else{
                  if(x > b & x < c){
                      fx = (((h1 - h2)*(c - x))/(c - b)) + h2
                  }else{
                      if(x >= c & x < d){
                          fx = (h2 * (d - x))/(d - c)
                      }else{
                          fx = 0
                      }
                  }
              }
              return(fx)
          }
          )


#' Density of the Hockey stick distribution
#' @inheritParams phockey
#'@export
dhockey <- function(x, a, b, c, d, h1, h2 = NULL){
    if(length(x) == 1){
        Fx = cdfhockey(x = x, a = a, b = b, c = c, d = d, h1 = h1, h2 = h2)
    }
    if(length(x) > 1){
        Fx = sapply(x, function(y) cdfhockey(x = y, a = a, b = b, c = c, d = d, h1 = h1, h2 = h2))
        }
    return(Fx)
}
#' Cdf for dhockey 
setGeneric("cdfhockey",
           function(x, a, b, c, d, h1, h2){
               standardGeneric("cdfhockey")
               })
setMethod("cdfhockey",
          c(x = "numeric", a = "numeric", b= "numeric", c= "numeric", d = "numeric", h1= "numeric", h2 = NULL),
          function(x, a, b, c, d, h1, h2 = NULL){
              if(h1  > 2/(c - a)){stop("h1 muxt be less than or equal to 2/(c - a)")}
              h2 = (2 - h1*(c - a))/(d - b)
              if(h1 < h2){stop("h1 must be greater than h2")}
              if(a > b | b > c | c > d){stop("a < b < c < d")}
              if(x > a & x <= b){
                  Fx = -(h1*(a - x)^2)/(2 * (a - b))
              }else{
                  if(x > b & x < c){
                      Fx =  h1*(b - a)*(1/2) - ((b - x)*(b*(h1 + h2) - 2*c*h1 + x*(h1 - h2)))/(2*(b - c))
                  }else{
                      if(x >= c & x < d){
                          Fx = h1*(b - a)*(1/2) - (1/2)*(b - c)*(h1 + h2) -
                              (h2*(c - x) * (c - 2*d + x))/(2* (c - d))
                      }else{
                          if(x >= d){
                              Fx = 1
                          }else{
                              Fx = 0
                          }
                      }
                  }
              }
              return(Fx)
          }
          )
setMethod("cdfhockey",
          c(x = "numeric", a = "numeric", b= "numeric", c= "numeric", d = "numeric", h1= NULL, h2 = "numeric"),
          function(x, a, b, c, d, h1 = NULL, h2){
              if(h2  > 2/(d - b)){stop("h2 muxt be less than or equal to 2/(d - b)")}
              h1 = (2 - h2*(d - b))/(c - a)
              if(h1 < h2){stop("h1 must be greater than h2")}
              if(a > b | b > c | c > d){stop("a < b < c < d")}
               if(x > a & x <= b){
                  Fx = -(h1*(a - x)^2)/(2 * (a - b))
              }else{
                  if(x > b & x < c){
                      Fx = h1*(b - a)*(1/2) - ((b - x)*(b*(h1 + h2) - 2*c*h1 + x*(h1 - h2)))/(2*(b - c))
                  }else{
                      if(x >= c & x < d){
                          Fx = h1*(b - a)*(1/2) - (1/2)*(b - c)*(h1 + h2) -
                              (h2*(c - x) * (c - 2*d + x))/(2* (c - d))
                      }else{
                          if(x >= d){
                              Fx = 1
                          }else{
                              Fx = 0
                          }
                      }
                  }
              }
              return(Fx)
          }
          )

#' random number generator Hockey stick distribution
#' @inheritParams phockey
#' @param n number of rvs to generate
#'@export

setGeneric("rhockey",
           function(n, a, b, c, d, h1, h2){
             standardGeneric("rhockey")
           })
setMethod("rhockey",
          c(n = "numeric", a = "missing", b= "missing", c= "missing", d = "missing",
            h1= "missing", h2 = NULL),
          function(n, a, b, c, d, h1, h2 = NULL){
            rhockey(n = n, a = 0, b = 1, c = 1.82918 , d = 3, h1 = 1)
          }
          )
setMethod("rhockey",
          c(n = "numeric", a = "numeric", b= "numeric", c= "numeric", d = "numeric",
            h1= "numeric", h2 = NULL),
          function(n, a, b, c, d, h1, h2 = NULL){
              if (length(n) > 1) n <- length(n)
              if (n < 1 | is.na(n)) stop("please supply a valid n")
              n <- floor(n)
              if(h1  >= 2/(c - a)){stop("h1 must be less than  2/(c - a)")}
              h2 = (2 - h1*(c - a))/(d - b)
              if(h1 < h2){stop("h1 must be greater than h2")}
              if(a > b | b > c | c > d){stop("a < b < c < d")}
              pars = c(a,b,c,d)
              inv.pars = dhockey(x = pars, a, b, c, d, h1)
              unf = runif(n)
              rx = rep(NA,n)
              idx1 = which(unf > inv.pars[1] & unf < inv.pars[2])
              idx2 = which(unf > inv.pars[2] & unf < inv.pars[3])
              idx3 = which(unf >= inv.pars[3] & unf < inv.pars[4])
              if(length(idx1) > 0){
                  rx[idx1] <- sqrt(2*(b - a)*unf[idx1]/h1) + a
              }
              if(length(idx2) > 0){
                  p = (c - b)*(-a*h1^2 + a*h1*h2 - b*h1*h2 + c*h1^2 - 2*h1*unf[idx2] + 2*h2*unf[idx2])
                  den = h1 - h2
                  rx[idx2] <- (c*h1 - b*h2 - sqrt(p))/den
              }
              if(length(idx3) > 0){
                  rx[idx3] <- d - (sqrt(h2*(d - c)*(-a*h1 - b*h2 + c*h1 + d*h2 - 2*unf[idx3])))/h2
              }
              return(rx)
          }
          )
setMethod("rhockey",
          c(n = "numeric", a = "numeric", b= "numeric", c= "numeric", d = "numeric",
            h1= NULL, h2 = "numeric"),
          function(n, a, b, c, d, h1 = NULL, h2){
              if (length(n) > 1) n <- length(n)
              if (n < 1 | is.na(n)) stop("please supply a valid n")
              n <- floor(n)
              if(h2  >= 2/(d - b)){stop("h2 must be less 2/(d - b)")}
              h1 = (2 - h2*(d - b))/(c - a)
              if(h1 < h2){stop("h1 must be greater than h2")}
              if(a > b | b > c | c > d){stop("a < b < c < d")}
              pars = c(a,b,c,d)
              inv.pars = dhockey(x = pars, a, b, c, d, h1)
              unf = runif(n)
              rx = rep(NA,n)
              idx1 = which(unf > inv.pars[1] & unf < inv.pars[2])
              idx2 = which(unf > inv.pars[2] & unf < inv.pars[3])
              idx3 = which(unf >= inv.pars[3] & unf < inv.pars[4])
              if(length(idx1) > 0){
                  rx[idx1] <- sqrt(2*(b - a)*unf[idx1]/h1) + a
              }
              if(length(idx2) > 0){
                  p = (c - b)*(-a*h1^2 + a*h1*h2 - b*h1*h2 + c*h1^2 - 2*h1*unf[idx2] + 2*h2*unf[idx2])
                  den = h1 - h2
                  rx[idx2] <- (c*h1 - b*h2 - sqrt(p))/den
              }
              if(length(idx3) > 0){
                  rx[idx3] <- d - (sqrt(h2*(d - c)*(-a*h1 - b*h2 + c*h1 + d*h2 - 2*unf[idx3])))/h2
              }
              return(rx)
          }
          )
#' quantile function for the Hockey stick distribution
#' @inheritParams phockey
#' @param p vector of probabilties
#'@export

setGeneric("qhockey",
           function(p, a, b, c, d, h1, h2){
             standardGeneric("qhockey")
           })
setMethod("qhockey",
          c(p = "numeric", a = "numeric", b= "numeric", c= "numeric", d = "numeric",
            h1= "numeric", h2 = NULL),
          function(p, a, b, c, d, h1, h2 = NULL){
              if(length(which(p < 0 | p > 1)) > 0)stop("p must be a probability")
              if(h1  >= 2/(c - a)){stop("h1 must be less than  2/(c - a)")}
              if(length(which(p > h1)) > 0)stop(paste("p of",p[which(p > h1)],"not observed"))
              h2 = (2 - h1*(c - a))/(d - b)
              if(h1 < h2){stop("h1 must be greater than h2")}
              if(a > b | b > c | c > d){stop("a < b < c < d")}
              pars = c(a,b,c,d)
              inv.pars = dhockey(x = pars, a, b, c, d, h1)
              qx = rep(NA,length(p))
              idx1 = which(p >= inv.pars[1] & p < inv.pars[2])
              idx2 = which(p >= inv.pars[2] & p < inv.pars[3])
              idx3 = which(p >= inv.pars[3] & p <= inv.pars[4])
              if(length(idx1) > 0){
                  qx[idx1] <- ((b - a)/h1)*p[idx1] + a
              }
              if(length(idx2) > 0){
                  qx[idx2] <- c - (p[idx2] - h2)*(c - b)/(h1 - h2)
              }
              if(length(idx3) > 0){
                  qx[idx3] <- d - (p[idx3]*(d - c))/h2
              }
              return(qx)
          }
          )

setMethod("qhockey",
          c(p = "numeric", a = "numeric", b= "numeric", c= "numeric", d = "numeric",
            h1 = NULL, h2 = "numeric"),
          function(p, a, b, c, d, h1 = NULL, h2){
              if(length(which(p < 0 | p > 1)) > 0)stop("p must be a probability")
              if(h2  > 2/(d - b)){stop("h2 must be less than or equal to 2/(d - b)")}
              h1 = (2 - h2*(d - b))/(c - a)
              if(h1 < h2){stop("h1 must be greater than h2")}
              if(length(which(p > h1)) > 0)stop(paste("p of", p[which(p > h1)],"not observed"))
              if(a > b | b > c | c > d){stop("a < b < c < d")}
              pars = c(a,b,c,d)
              inv.pars = dhockey(x = pars, a, b, c, d, h1)
              qx = rep(NA,length(p))
              idx1 = which(p >= inv.pars[1] & p < inv.pars[2])
              idx2 = which(p >= inv.pars[2] & p < inv.pars[3])
              idx3 = which(p >= inv.pars[3] & p <= inv.pars[4])
              if(length(idx1) > 0){
                  qx[idx1] <- ((b - a)/h1)*p[idx1] + a
              }
              if(length(idx2) > 0){
                  qx[idx2] <- c - (p[idx2] - h2)*(c - b)/(h1 - h2)
              }
              if(length(idx3) > 0){
                  qx[idx3] <- d - (p[idx3]*(d - c))/h2
              }
              return(qx)
          }
          )
#' Finding the "hinge" point (c parameter) for the hockey stick distribution at the pth percentile
#' @inheritParams phockey
#' @param q = 1 - p (percentile) by default is 1 - 0.95 = 0.05
#' @param s = p - 0.5 (for Median b) by default is 0.95 - 0.5 = 0.45
Xp <- function(b,d,h1,q = 0.05,s = 0.45){
    1/2*(b + d + 1/h1 - sqrt((d - b)^2 + (b*(2-8*q) + d*(2 - 8*s))/(h1) + 1/h1^2))
}
