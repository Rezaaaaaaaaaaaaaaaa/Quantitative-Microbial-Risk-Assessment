#' PDF of a cumualative distribution
#' @param y vector of quantiles
#' @param x supplied vector of quantiles (x_1, ..., x_n)
#' @param p supplied vector of probabilities (p_1, ..., p_n) corresponding to elements of \code{x}  
#' @param min (optional) numeric minimum value of \code{x}, if supplied this is taken as the first
#'  element of \code{x} and the p_0 element of \code{p} is set to be 0
#' @param max  (optional) numeric maximum value of \code{x}, if supplied this is taken as the first
#'  element of \code{x} and the p_(n+1) element of \code{p} is set to be 1
#' @export
pcumulative <- function(y, x, p, min = NULL, max = NULL){
    if(length(y) == 1){
        fx = cumulative(y = y, x = x, p = p, min = min, max = max)
    }
    if(length(y) > 1){
        fx = sapply(y, function(y.n) cumulative(y = y.n, x = x, p = p, min = min, max = max))
        }
    return(fx)
}
#' PDF for cumulative distribution
setGeneric("cumulative",
           function(y, x, p, min, max){
               standardGeneric("cumulative")
               })
setMethod("cumulative",
          c(y = "numeric",x = "numeric", p = "numeric", min = "numeric", max = "numeric"),
          function(y, x, p, min, max){
            if(sum(p < 0) > 0 | sum(p > 1) > 0){stop("p should be between (0,1)")}
            if(sum(x < min) > 0 | sum(x > max) > 0){stop("x should be between ",min, " and ", max)}
            if(length(p) != length(x)){stop("x and p are do not have the same number of elements")}
            if(sum(y <= min) > 0 | sum(y >= max) > 0){stop("y should be greater than ",min,
                                                         " and less than ", max)}
            p = p[order(x)]
            x = sort(x)
            n = length(x)
            p = c(0,p,1)
            x = c(min,x,max)
            where.y = which(sort(c(y,x)) == y)[1]
            fx = (p[where.y] - p[where.y - 1])/(x[where.y] - x[where.y - 1])
            return(fx)
          }
)
setMethod("cumulative",
          c(y = "numeric",x = "numeric", p = "numeric", min = NULL, max = NULL),
          function(y, x, p, min, max){
            if(sum(p < 0) > 0 | sum(p > 1) > 0){stop("p should be between (0,1)")}
            if(length(p) != length(x)){stop("x and p are do not have the same number of elements")}
            p = p[order(x)]
            x = sort(x)
            n = length(x)
            if(sum(y <= x[1]) > 0 | sum(y >= x[n]) > 0){stop("y should be greater than ",x[1],
                                                         " and less than ", x[n])}
            where.y = which(sort(c(y,x)) == y)[1]
            fx = (p[where.y] - p[where.y - 1])/(x[where.y] - x[where.y - 1])
            return(fx)
          }
)
#' CDF of the cumulative distribution
#' @inheritParams pcumulative
#' @export
dcumulative <- function(y, x, p, min = NULL, max = NULL){
    if(length(y) == 1){
        Fx = cdfcumulative(y = y, x = x, p = p, min = min, max = max)
    }
    if(length(y) > 1){
        Fx = sapply(y, function(y.n) cdfcumulative(y = y.n, x = x, p = p, min = min, max = max))
        }
    return(Fx)
}
#' CDF cumulative
setGeneric("cdfcumulative",
           function(y, x, p, min, max){
             standardGeneric("cdfcumulative")
           })
setMethod("cdfcumulative",
          c(y = "numeric",x = "numeric", p = "numeric", min = "numeric", max = "numeric"),
          function(y, x, p, min, max){
            if(sum(p < 0) > 0 | sum(p > 1) > 0){stop("p should be between (0,1)")}
            if(sum(x < min) > 0 | sum(x > max) > 0){stop("x should be between ",min, " and ", max)}
            if(length(p) != length(x)){stop("x and p are do not have the same number of elements")}
            if(sum(y <= min) > 0 | sum(y >= max) > 0){stop("y should be greater than ",min,
                                                         " and less than ", max)}
            p = p[order(x)]
            x = sort(x)
            n = length(x)
            p = c(0,p,1)
            x = c(min,x,max)
            where.y = which(sort(c(y,x)) == y)[1]
            Fx = p[where.y - 1] + (p[where.y] - p[where.y - 1])*((y -
                                                          x[where.y - 1])/(x[where.y] -
                                                                           x[where.y - 1]))
            return(Fx)
          }
)
setMethod("cdfcumulative",
          c(y = "numeric",x = "numeric", p = "numeric", min = NULL, max = NULL),
          function(y, x, p, min, max){
            if(sum(p < 0) > 0 | sum(p > 1) > 0){stop("p should be between (0,1)")}
            if(length(p) != length(x)){stop("x and p are do not have the same number of elements")}
            p = p[order(x)]
            x = sort(x)
            n = length(x)
            if(sum(y <= x[1]) > 0 | sum(y >= x[n]) > 0){stop("y should be greater than ",x[1],
                                                         " and less than ", x[n])}
            where.y = which(sort(c(y,x)) == y)[1]
            Fx = p[where.y - 1] + (p[where.y] - p[where.y - 1])*((y - x[where.y - 1])/(x[where.y] -
                                                                                   x[where.y - 1]))
            return(Fx)
          }
)
#' Qualtile function of the cumulative distribution
#' @inheritParams pcumulative
#' @param P vector of probabilities
#' @export
qcumulative <- function(P, x, p, min = NULL, max = NULL){
    if(length(P) == 1){
        i.Fx = qucumulative(P = P, x = x, p = p, min = min, max = max)
    }
    if(length(P) > 1){
        i.Fx = sapply(P, function(P.n) qucumulative(P = P.n, x = x, p = p, min = min, max = max))
        }
    return(i.Fx)
}
#' CDF cumulative
setGeneric("qucumulative",
           function(P, x, p, min, max){
             standardGeneric("qucumulative")
           })
setMethod("qucumulative",
          c(P = "numeric",x = "numeric", p = "numeric", min = "numeric", max = "numeric"),
          function(P, x, p, min, max){
            if(sum(p < 0) > 0 | sum(p > 1) > 0){stop("p should be between (0,1)")}
            if(sum(x < min) > 0 | sum(x > max) > 0){stop("x should be between ",min, " and ", max)}
            if(length(p) != length(x)){stop("x and p are do not have the same number of elements")}
            if(sum(P <= 0) > 0 | sum(P >= 1) > 0){stop("P should be greater than 0 and less than 1")}
            p = p[order(x)]
            x = sort(x)
            n = length(x)
            p = c(0,p,1)
            x = c(min,x,max)
            where.P = which(sort(c(P,p)) == P)[1]
            i.Fx = (P - p[where.P - 1])/(p[where.P] - p[where.P - 1])*(x[where.P] - x[where.P - 1]) +
                x[where.P - 1]
            return(i.Fx)
          }
)
setMethod("qucumulative",
          c(P = "numeric",x = "numeric", p = "numeric", min = NULL, max = NULL),
          function(P, x, p, min, max){
            if(sum(p < 0) > 0 | sum(p > 1) > 0){stop("p should be between (0,1)")}
            if(length(p) != length(x)){stop("x and p are do not have the same number of elements")}
            p = p[order(x)]
            x = sort(x)
            n = length(x)
            if(sum(P <= 0) > 0 | sum(P >= 1) > 0){stop("P should be greater than 0 and less than 1")}
            where.P = which(sort(c(P,p)) == P)[1]
            i.Fx =  (P - p[where.P - 1])/(p[where.P] - p[where.P - 1])*(x[where.P] - x[where.P - 1]) +
                x[where.P - 1]
            return(i.Fx)
          }
)
#' Qualtile function of the cumulative distribution
#' @inheritParams pcumulative
#' @param n number of rvs to generate
#' @export
setGeneric("rcumulative",
           function(n, x, p, min, max){
             standardGeneric("rcumulative")
           })
setMethod("rcumulative",
          c(n = "numeric",x = "numeric", p = "numeric", min = "numeric", max = "numeric"),
          function(n, x, p, min, max){
            if(sum(p < 0) > 0 | sum(p > 1) > 0){stop("p should be between (0,1)")}
            if(sum(x < min) > 0 | sum(x > max) > 0){stop("x should be between ",min, " and ", max)}
            if(length(p) != length(x)){stop("x and p are do not have the same number of elements")}
            if (length(n) > 1) n <- length(n)
            if (n < 1 | is.na(n)) stop("please supply a valid n")
            n = floor(n)
            p = p[order(x)]
            x = sort(x)
            p = c(0,p,1)
            x = c(min,x,max)
            unf = runif(n)
            rx = qcumulative(P = unf, x = x, p = p, min = min, max = max)
            return(rx)
          }
)
setMethod("rcumulative",
          c(n = "numeric",x = "numeric", p = "numeric", min = NULL, max = NULL),
          function(n, x, p, min, max){
            if(sum(p < 0) > 0 | sum(p > 1) > 0){stop("p should be between (0,1)")}
            if(length(p) != length(x)){stop("x and p are do not have the same number of elements")}
            if (length(n) > 1) n <- length(n)
            if (n < 1 | is.na(n)) stop("please supply a valid n")
            n = floor(n)
            p = p[order(x)]
            x = sort(x)
            unf = runif(n)
            rx = qcumulative(P = unf, x = x, p = p)
            return(rx)
          }
)
