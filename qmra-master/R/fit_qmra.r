#' The qmra class
#' @section Slots:
#' \describe{\item{\code{data}:}{a data frame which must contain the following named elements positive, total, and dose to be used with \code{fit.pcod}}
#' \item{\code{model}:}{a character of the chosen model based on arguments given to \code{fit.qmra}, set by user}
#' \item{\code{fit}:}{contains the model output}}
#' @name qmra
#' @rdname qmra
#' @aliases qmra-class
#' @exportClass qmra
qmra <- setClass("qmra",
                 slots = c(data = "data.frame",
                           model = "character",
                           parameters = "numeric",
                           fit = "list"),
                 validity = function(object){
                   if(sum(c("positive", "total","dose") %in% names(object@data))!=3) {
                     return("Data must contain elements named positive, total, and dose. Try ?fit.qmra")
                   }
                   return(TRUE)
                 })


#' log-likelihood to be minimised for ML estimate of dose-response parameters
#'@param data data frame of dose-respone study. Must contain named columns \code{positive},
#' number of positive subjects in at a specific dose;
#' \code{total}, total number of subjects; and \code{dose}, dose given.
#'@param params named vector of dose-response parameters
#'@param model character specifying assumed type of dose-response model
#'@export
setGeneric("qmra_ll",
           function(params, data, model){
             standardGeneric("qmra_ll")
           })

setMethod("qmra_ll",
          c(params = "vector", data = "data.frame", model = "character"),
          function(params, data, model){
            infected = data$positive
            total = data$total
            not.inf = total - infected
            dose.response = dr.mod(model = model, params = params, dose = data$dose)
            ll1 = sum(infected*log(dose.response),na.rm = TRUE)
            ll2 = sum(not.inf*log(1 - dose.response),na.rm = TRUE)
            ll = -2*(ll1 + ll2)
            ll
          })


#'  deviance statistic to be minimised for ML estimate of dose-response parameters
#' @inheritParams qmra_ll
#'@export
setGeneric("qmra_dev",
           function(params, data, model){
             standardGeneric("qmra_dev")
           })

setMethod("qmra_dev",
          c(params = "vector", data = "data.frame", model = "character"),
          function(params,data, model){
            infected = data$positive
            total = data$total
            not.inf = total - infected
            ratio = infected/total
            dose.response = dr.mod(model = model, params = params, dose = data$dose)
            arg1 = dose.response/ratio
            dev1 = numeric(length(infected)) ## initialise first bit
            for(i in 1:length(infected)){
              if(infected[i] == 0 | arg1[i] == 0){
                dev1[i] = 0
              }else{
                dev1[i] = infected[i] * log(arg1[i])
              }
            }
            d1 = sum(dev1)
            arg2 = ((1 - dose.response)/(1 - ratio))
            dev2 = numeric(length(infected)) ## initialise first bit
            for(i in 1:length(infected)){
              if(not.inf[i] == 0 | arg2[i] == 0){
                dev2[i] = 0
              }else{
                dev2[i] = not.inf[i] * log(arg2[i])
              }
            }
            d2 = sum(dev2)
            dev = -2*(d1 + d2)
            dev
          })

#' function to choose which dose-response model for use in qmra model fit
#' @inheritParams qmra_dev
#' @param dose vector of dose values 
setGeneric("dr.mod",
           function(model, params, dose){
             standardGeneric("dr.mod")
           })
setMethod("dr.mod",
          c(model = "character",params = "vector", dose = "numeric"),
          function(model,params,dose){
  pos = c("exponential", "betapoisson", "approx_betapoisson", "simple_binomial",
         "beta_binomial", "loglogistic", "logprobit", "weibull",
         "overdispersed_exponential","fractional_poisson","gauss_hypergeometric",
         "simple_threshold") ## vector or all possible dose-response functions
  if(!(model %in% pos)){stop("not a known dose-response model")}
  if(model == "exponential"){
    res = expon_dr(r = params['r'], dose = dose)
    res
  }
  if(model == "betapoisson"){
    res = betapois_dr(alpha = params['alpha'], beta = params['beta'], dose = dose)
    res
  }
  if(model == "approx_betapoisson"){
    res = betapois_dr_approx(alpha = params['alpha'], beta = params['beta'], dose = dose)
    res
  }
  if(model == "simple_binomial"){
   res = s_binom_dr(r = params['r'], dose = dose)
   res
  }
  if(model == "beta_binomial"){
   res = beta_binom_dr(alpha = params['alpha'],beta = params['beta'], dose = dose)
   res
  }
  if(model == "loglogistic"){
    res = loglogistic_dr(q1 = params['q1'], q2 = params['q2'], dose = dose)
    res
  }
  if(model == "logprobit"){
    res = logprobit_dr(q1 = params['q1'], q2 = params['q2'], dose = dose)
  }            
  if(model == "weibull"){
    res = weibull_dr(q1 = params['q1'], q2 = params['q2'], dose = dose)
    res
  }
  if(model == "overdispersed_exponential"){
      res = od_expon_dr(r = params['r'], k = params['k'], dose = dose)
      res
  }
  if(model == "fractional_poisson"){
      res = fractional_pois_dr(p = params['p'], mu = params['mu'], dose = dose)
      res
  }
  if(model == "gauss_hypergeometric"){
      res = Re(Ghyper_dr(alpha = params['alpha'], beta = params['beta'], k = params['k'], dose = dose))
      res
  }
  if(model == "simple_threshold"){
    res = s_thres_dr(kmin = params['kmin'], r = params['r'], dose = dose)
    res
  }
  return(res)
})

#' Function to fit dose-response model
#' fitting function for the various dose-response relationships 
#' parameter estimates obtained by minimization of the deviance \code{qmra_dev}
#' @inheritParams qmra_dev
#' @param upper vector of upper limits of the parameters to be estimated
#' @param lower vector of lower limits of parameters to be estimated
#' @param method to carry out minimisation
#' @export
setGeneric("fit.qmra",
           function(data, params, model, upper, lower, method){
             standardGeneric("fit.qmra")
           })

setMethod("fit.qmra",
          c(data = "data.frame", params = "vector", model = "character", upper = "numeric", 
            lower = "numeric", method = "character"),
          function(data, params, model,upper, lower, method){
            qmra = qmra(data = data, model = model, parameters = params)
            print(model)
            ll = optim(par = params, qmra_dev,data = data, model = model, 
                         method = method,upper = upper, lower = lower,hessian = TRUE)
            pars = ll$par
            fisher = solve(ll$hessian)
            ses = sqrt(diag(fisher))
            upper = pars + 1.96*ses
            lower = pars - 1.96*ses ## normal approximation
            res = cbind(pars,ses,lower,upper)
            rownames(res) = names(pars)
            colnames(res) = c("Estimate", "se","2.5%", "97.5%")
            qmra@fit$estimated_parameters = res
            qmra@fit$AIC = AIC(params = params, data = data, model = model)
            qmra@fit$BIC = BIC(params = params, data = data, model = model)
            qmra
          })


#'  maximum possible log-likelihood l_sup
#'@param data data frame of dose-respone study. Must contain named columns \code{positive},
#' number of positive subjects in at a specific dose;
#' \code{total}, total number of subjects; and \code{dose}, dose given.
#'@param params named vector of dose-response parameters
#'@param model character specifying assumed type of dose-response model
#'@export
setGeneric("qmra_ll_sup",
           function(data){
             standardGeneric("qmra_ll_sup")
           })

setMethod("qmra_ll_sup",
          c(data = "data.frame"),
          function(data){
            infected = data$positive
            total = data$total
            not.inf = total - infected
            ratio = infected/total
            ll_sup1 = sum(infected * log(ratio),na.rm = TRUE)
            ll_sup2 = sum(not.inf*log(not.inf/total), na.rm = TRUE)
            ll_sup = -2*(ll_sup1 + ll_sup2)
            ll_sup
          })

#' function to get fitted parameter estimates of a dose-response model
#' @param qmra a \code{qmra} fitted object
#' @export
setGeneric("pars.qmra", 
           function(fit){
             standardGeneric("pars.qmra")
           })

setMethod("pars.qmra",
          c(fit = "qmra"),
          function(fit){
            print(fit@fit$estimated_parameters)
          })
