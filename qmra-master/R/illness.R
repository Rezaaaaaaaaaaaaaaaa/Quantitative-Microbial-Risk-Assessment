#' Function that takes a vector of individual dose values and calculates
#' for a supplied dose-response function with supplied parameter values
#' a list of with components 1) the probability of infection and two
#' indicator variables indicating if individual was 2) infected
#' and 3) conditional on 2) ill.
#' @inheritParams dr.mod
#' @param p.ill numeric values giving the probability of a person getting ill given they are infected
#'@export
setGeneric("illness.qmra",
           function(dose, model, params, p.ill){
               standardGeneric("illness.qmra")
               })

setMethod("illness.qmra",
          c(dose = "numeric", model = "character",params = "numeric", p.ill = "numeric"),
          function(dose,model,params,p.ill){
              p.inf = dr.mod(model = model, params = params, dose = dose)
              probability.ill = p.inf*p.ill
              inf = sapply(p.inf, function(x) sample(x = c(0,1), size = 1, prob = c(1 - x, x)))
              if(length(p.ill) == 1){
                  ill = ifelse(inf == 1, sample(c(0,1), size = length(inf[inf == 1]),
                                                prob = c(1 - p.ill, p.ill), replace = TRUE),0)
              }else{
                  if(length(p.ill) != length(inf)){
                      stop("If multiple probabilities are provided must be the same length as infection probability vector")
                  }
                  ill <- numeric(length(p.ill))
                  for(i in 1:length(p.ill)){
                      ill[i] <- ifelse(inf[i] == 1, sample(c(0,1), size = 1,
                                                           prob = c(1 - p.ill[i], p.ill[i]), replace = TRUE),0)
                  }
              }
              return(list(probability.infected = p.inf,probability.ill = probability.ill, infected = inf, ill = ill,
                          individual.infection.rate = mean(p.inf), individual.illness.rate = mean(probability.ill),
                          inputs = list(model = model, params = params,p.ill = p.ill)))
          })
#' function to run \code{illness.qmra} for multiple dose-response curves and return a list for each
#' dose-response model with named elements containing the sum (for each run) of each vector of indicator variables
#' indicating if individual was 1) infected and 2) conditional on 1) ill.
#' @inheritParams illness.qmra
#' @param mod.vec a character vector of dose-response model names
#' @param params.list a list of named parameter vectors for each dose-response model given in \link{mod.vec}
#' @export
setGeneric("multi.illness.qmra",
           function(dose, params.list, p.ill,mod.vec){
               standardGeneric("multi.illness.qmra")
               })
setMethod("multi.illness.qmra",
          c(dose = "numeric",params.list = "list", p.ill = "numeric",mod.vec = "character"),
          function(dose, params.list, p.ill,mod.vec){
              len <- length(mod.vec)
              illness <- list()
              for(i in 1:len){
                  ill.fun <- illness.qmra(dose = dose, model = mod.vec[i],params = params.list[[i]],p.ill = p.ill)
                  probability.infected <- ill.fun$probability.infected
                  probability.ill <- ill.fun$probability.ill
                  dist.of.num.infected <- ill.fun$infected
                  dist.of.num.ill <- ill.fun$ill
                  i.inf.r <- ill.fun$individual.infection.rate
                  i.ill.r <- ill.fun$individual.illness.rate
                  illness[[i]] <- list(probability.infected = probability.infected,probability.ill = probability.ill,
                                       dist.of.num.infected = dist.of.num.infected,dist.of.num.ill = dist.of.num.ill, i.inf.r = i.inf.r, i.ill.r = i.ill.r,
                                       inputs = list(model = mod.vec[i], params = params.list[[i]],p.ill = p.ill))
              }
              names(illness) <- mod.vec
              return(illness)
          })
setMethod("multi.illness.qmra",
          c(dose = "numeric",params.list = "list", p.ill = "matrix",mod.vec = "character"),
          function(dose, params.list, p.ill,mod.vec){
              len <- length(mod.vec)
              illness <- list()
              for(i in 1:len){
                  ill.fun <- apply(dose, 1, function(x) illness.qmra(dose = x, model = mod.vec[i],
                                                                     params = params.list[[i]],p.ill = p.ill[,i]))
                  probability.infected <- ill.fun$probability.infected
                  probability.ill <- ill.fun$probability.ill
                  dist.of.num.infected <- ill.fun$infected
                  dist.of.num.ill <- ill.fun$ill
                  i.inf.r <- ill.fun$individual.infection.rate
                  i.ill.r <- ill.fun$individual.illness.rate
                  illness[[i]] <- list(probability.infected = probability.infected,probability.ill = probability.ill,
                                       dist.of.num.infected = dist.of.num.infected,dist.of.num.ill = dist.of.num.ill, i.inf.r = i.inf.r, i.ill.r = i.ill.r,
                                       inputs = list(model = mod.vec[i], params = params.list[[i]],p.ill = p.ill))
              }
              names(illness) <- mod.vec
              return(illness)
          })
#' function to run \code{illness.qmra} for multiple dose-response curves and return a data frame
#' @inheritParams illness.qmra
#' @export
setGeneric("multi.qmra.dose",
           function(dose, params.list,mod.vec){
               standardGeneric("multi.qmra.dose")
               })
setMethod("multi.qmra.dose",
          c(dose = "numeric",params.list = "list",mod.vec = "character"),
          function(dose, params.list,mod.vec){
              len <- length(mod.vec)
              probs <- list()
              for(i in 1:len){
                  probs[[i]] <- dr.mod(model = mod.vec[i], params = params.list[[i]], dose = dose)
              }
              names(probs) <- mod.vec
              stk.probs <- stack(probs)
              stk.probs$Dose <- rep(dose,len)
              colnames(stk.probs) <- c("Probability of infection","Dose-response function","Dose")
              return(stk.probs)
          })
