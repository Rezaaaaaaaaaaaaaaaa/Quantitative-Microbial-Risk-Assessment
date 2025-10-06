#' functions for the concentration/ duration distributions

#' returns the negative log-likelihood of a Poisson distribution
#' @param lambda the mean density of the poisson distribution
#' @param count a vector of pathogen counts
#' @param volume a vector of volumes within which the counts \code{count} were recorded
setGeneric("poisson_neg_ll",
           function(lambda, count, volume){
             standardGeneric("poisson_neg_ll")
           })
setMethod("poisson_neg_ll",
          c(lambda = "numeric", count = "integer", volume = "numeric"),
          function(lambda, count, volume){
            ll = sum(count*log(lambda*volume)) - sum(log(factorial(count))) - sum(lambda*volume)
            -ll
          })
#' first derivative of the poisson log-likelihood
#' @inheritParams poisson_neg_ll
setGeneric("poisson_gr",
           function(lambda, count, volume){
             standardGeneric("poisson_gr")
           })
setMethod("poisson_gr",
          c(lambda = "numeric", count = "integer", volume = "numeric"),
          function(lambda,count,volume){
            g = sum(volume) - (1/lambda)*sum(count)
          })
#' returns the negative log-likelihood of the binomial distribution for MPN
#' @inheritParams poisson_neg_ll
#' @param ni number of replicates in the set
#' @param pi vector of positive replicates
#' @param volume volume per assay replicate
setGeneric("mpn_neg_ll",
           function(lambda, ni, pi, volume){
             standardGeneric("mpn_neg_ll")
           })
setMethod("mpn_neg_ll",
          c(lambda = "numeric", ni = "numeric", pi = "numeric", volume = "numeric"),
          function(lambda, ni,pi, volume){
            ll1 = sum(log(factorial(ni)) - log(factorial(pi)*factorial(ni - pi)))
            ll2 = sum(pi * log(1 - exp(-lambda*volume)))
            ll3 = -sum((ni - pi)*lambda*volume)
            ll = ll1 + ll2 + ll3
            nll = -ll
            nll
          })
