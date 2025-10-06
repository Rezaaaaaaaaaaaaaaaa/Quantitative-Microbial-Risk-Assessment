#' exponential dose-response model
#' @param r pathogen-host survival probability 
#' @param dose vector of doses
#' @export
setGeneric("expon_dr",
           function(r,dose){
               standardGeneric("expon_dr")
           })

setMethod("expon_dr",
          c(r = "numeric", dose = "vector"),
          function(r, dose){
              if(r < 0 | r > 1) {stop("r must be in the range of (0,1)")}
              res = 1 - exp(-r*dose)
              res
          }
          )
#' dose-response model as per Messner et al 2014
#' @param P parameter of the dose-response model
#' @param mu parameter of the dose response model, set to 1 in strict case. Defined as
#' the mean aggregate size and is a function of alpha: -alpha/((1 - alpha)*ln(1 - alpha))
#' @param dose vector of doses
#' @export
setGeneric("fractional_pois_dr",
           function(p,mu,dose){
               standardGeneric("fractional_pois_dr")
           })

setMethod("fractional_pois_dr",
          c(p = "numeric",mu = "numeric", dose = "vector"),
          function(p, mu, dose){
              res = p*(1 - exp(-dose/mu))
              res
          }
          )
#' beta-poisson dose-response model
#' @inheritParams expon_dr
#' @param alpha shape parameter of the standard beta distribution
#' @param beta shape paramter of the standard beta distribution
#' @export
setGeneric("betapois_dr",
           function(alpha, beta, dose){
               standardGeneric("betapois_dr")
           })

setMethod("betapois_dr",
          c(alpha = "numeric", beta = "numeric", dose = "vector"),
          function(alpha, beta, dose){
              if(alpha < 0 ) {stop("alpha must be positive")}
              if(beta < 0 ) {stop("beta must be positive")}
              res = 1 - genhypergeo(alpha, alpha + beta, -dose)
              res
          }
          )

#' approximation to the beta-poisson dose-response model. derived by furomoto and Mickey 1967
#' @inheritParams betapois_dr
#' @export
setGeneric("betapois_dr_approx",
           function(alpha, beta, dose){
               standardGeneric("betapois_dr_approx")
           })

setMethod("betapois_dr_approx",
          c(alpha = "numeric", beta = "numeric", dose = "vector"),
          function(alpha, beta, dose){
              if(alpha < 0 ) {stop("alpha must be positive")}
              if(beta < 0 ) {stop("beta must be positive")}
              res = 1 - (1 + dose/beta)^(-alpha)
              res
          }
          )

#' simple threshold model, extension of the exponential model.
#' @param kmin parameter of the simple threshold model. Minimum number of surviving organisms
#' @inheritParams expon_dr
#' @export
setGeneric("s_thres_dr",
           function(kmin, r, dose){
               standardGeneric("s_thres_dr")
           })

setMethod("s_thres_dr",
          c(kmin = "numeric",r = "numeric", dose = "vector"),
          function(kmin, r, dose){
              if(r < 0 | r > 1) {stop("r must be in the range of (0,1)")}
              res = pgamma(dose*r, kmin)
              res
          }
          )

#' log logistic dose response model
#' @param q1 parameter of the log-logistic dose response model
#' @param q2 parameter of the log-logistic dose response model
#' @inheritParams expon_dr
#' @export
setGeneric("loglogistic_dr",
           function(q1, q2, dose){
               standardGeneric("loglogistic_dr")
           })

setMethod("loglogistic_dr",
          c(q1 = "numeric",q2 = "numeric", dose = "vector"),
          function(q1, q2, dose){
              res = 1/(1 + exp(q1 - q2*log(dose)))
              res
          }
          )

#' function for the log-probit dose response model
#' @param arg argument of this function
setGeneric("phi",
           function(arg){
               standardGeneric("phi")
           })

setMethod("phi",
          c(arg = "numeric"),
          function(arg){
              erf = function(x) 2 * pnorm(x * sqrt(2)) - 1
              (1/sqrt(2*pi))*sqrt(pi/2)*(erf(arg/sqrt(2)) + 1)
          })
#' log probit dose response model
#' @param q1 parameter of the log-probit dose response model
#' @param q2 parameter of the log-probit dose response model
#' @inheritParams expon_dr
#' @export
setGeneric("logprobit_dr",
           function(q1, q2, dose){
               standardGeneric("logprobit_dr")
           })

setMethod("logprobit_dr",
          c(q1 = "numeric",q2 = "numeric", dose = "vector"),
          function(q1, q2, dose){
              arg = (1/q2)* log(dose/q1)
              res = phi(arg)
              res
          }
          )
#' weibull dose-response model
#' @param q1 parameter of the Weibull dose response model
#' @param q2 parameter of the Weibull dose response model
#' @inheritParams expon_dr
#' @export
setGeneric("weibull_dr",
           function(q1, q2, dose){
               standardGeneric("weibull_dr")
           })

setMethod("weibull_dr",
          c(q1 = "numeric",q2 = "numeric", dose = "vector"),
          function(q1, q2, dose){
              res = 1 - exp(-q1*dose^q2)
              res
          }
          )
#' simple binomial dose-response model
#' @inheritParams expon_dr
#' @export
setGeneric("s_binom_dr",
           function(r, dose){
               standardGeneric("s_binom_dr")
           })

setMethod("s_binom_dr",
          c(r = "numeric", dose = "vector"),
          function(r, dose){
              if(r < 0 | r > 1) {stop("r must be in the range of (0,1)")}
              res = 1 - (1 - r)^dose
              res
          }
          )
#' Beta binomial dose-response model
#' @inheritParams betapois_dr
#' @export
setGeneric("beta_binom_dr",
           function(alpha, beta, dose){
               standardGeneric("beta_binom_dr")
           })

setMethod("beta_binom_dr",
          c(alpha = "numeric", beta = "numeric", dose = "vector"),
          function(alpha, beta, dose){
              if(alpha < 0 ) {stop("alpha must be positive")}
              if(beta < 0 ) {stop("beta must be positive")}
              res = 1 - beta(alpha, beta + dose)/beta(alpha,beta)
              res
          }
          )
#' overdispersed exponential dose-response model
#' @inheritParams expon_dr 
#' @param k overdispersion parameter
#' @export
setGeneric("od_expon_dr",
           function(r,k,dose){
               standardGeneric("od_expon_dr")
           })

setMethod("od_expon_dr",
          c(r = "numeric", k = "numeric",dose = "vector"),
          function(r,k, dose){
              if(r < 0 | r > 1) {stop("r must be in the range of (0,1)")}
              res = 1 - (1 + ((r*dose)/k))^-k
              res
          }
          )
#' Gaus hypergeometric form dose-response model
#' @inheritParams betapois_dr
#' @inheritParams od_expon_dr
#' @export
setGeneric("Ghyper_dr",
           function(alpha, beta,k, dose){
               standardGeneric("Ghyper_dr")
           })

setMethod("Ghyper_dr",
          c(alpha = "numeric", beta = "numeric",k = "numeric", dose = "vector"),
          function(alpha, beta, k,dose){
              if(alpha < 0 ) {stop("alpha must be positive")}
              if(beta < 0 ) {stop("beta must be positive")}
              res = 1 - hypergeo(alpha,k, alpha + beta, -dose/k)
              res
          }
          )
