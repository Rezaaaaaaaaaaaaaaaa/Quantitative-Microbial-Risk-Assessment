## helper functions for the qmra Package


#' median infectious dose of the exponential dose-response model
#' @inheritParams expon_dr
#' @export
setGeneric("expon_N50",
           function(r){
             standardGeneric("expon_N50")
           })

setMethod("expon_N50",
          c(r = "numeric"),
          function(r){
            N50 = -log(0.5)/(r)
            N50
          }
)


#' median infectious dose of the approximate beta-poisson dose-response model
#' @inheritParams betapois_dr_approx
#' @export
setGeneric("betapois_N50_approx",
           function(alpha, beta){
             standardGeneric("betapois_N50_approx")
           })

setMethod("betapois_N50_approx",
          c(alpha = "numeric", beta = "numeric"),
          function(alpha, beta){
            N50 = beta*(2^(1/alpha) - 1)
            N50
          }
)

#' AIC
#' @inheritParams qmra_dev
#' @export

setGeneric("get.AIC",
           function(params, data, model){
             standardGeneric("get.AIC")
           })

setMethod("get.AIC",
          c(params = "vector", data = "data.frame", model = "character"),
          function(params, data, model){
            Y = qmra_dev(params = params, data = data, model = model)
            np = length(params)
            nobs = length(table(data$dose))
            res = Y + 2*np*(nobs/(nobs - np - 1))
            res
          })
#' BIC
#' @inheritParams qmra_dev
#' @export

setGeneric("get.BIC",
           function(params, data, model){
             standardGeneric("get.BIC")
           })

setMethod("get.BIC",
          c(params = "vector", data = "data.frame", model = "character"),
          function(params, data, model){
            Y = qmra_dev(params = params, data = data, model = model)
            np = length(params)
            nobs = length(table(data$dose))
            res = Y + np*log(nobs)
            res
          })

#' pathogens class
#' @exportClass microbes
#' @export pathogens
pathogens <- setClass("microbes",
                      slots = c(Campylobacter = "list",
                                Cryptosporidium = "list",
                                E.coli = "list",
                                Giardia = "list",
                                Salmonella = "list",
                                Adenovirus = "list",
                                Norovirus = "list",
                                Enterovirus = "list"))

#' Function to simulate from appropriate distribution (internal to qmra)
#' @param x a list with named components specifying the distribution andparameter values of that distribution
#' @param nsim number of simulations to carry out 
get.sim.value <- function(x, nsim){
  dist <- x$distribution
  if(sum(dist %in% c("triangular","hockey", "pert","lnorm","lnormTrunc")) != length(dist)) {
    stop("please ensure all distributions are supported (i.e., triangular, hockey, pert, lnorm,or lnormTrunc )")}
  if(dist == "triangular"){rs <- rhockey(n = nsim, a = x[["min"]], b = x[["mode"]],
                                                    c = x[["mode"]],
                                                    d = x[["max"]], h1 = 1/(x[["mode"]] - x[["min"]]))}
  if(dist == "hockey"){rs <- rhockey(n = nsim, a = x[["a"]], b = x[["b"]],
                                         c = x[["c"]],
                                         d = x[["d"]], h1 = x[["h1"]])}
  if(dist == "pert"){rs <- mc2d::rpert(nsim, min = x[['min']], max = x[['max']], mode = x[['mode']])}
  if(dist == "lnorm"){rs <- rlnorm(nsim, meanlog = x[['meanlog']], sdlog = x[['sdlog']])}
  if(dist == "lnormTrunc"){rs <- EnvStats:::rlnormTrunc(nsim, meanlog = x[['meanlog']], sdlog = x[['sdlog']],
                                                                   min = x[['min']], max = x[['max']])}
  return(rs)
}

#' functions imported from
#' @importFrom hypergeo genhypergeo
#' @importFrom optimx optimx
#' @importFrom rlnormTrunc EnvStats 
