#' Function to carry out Monte Carlo based simulation
#' for QMRA procedure
#' @param efficacy either a named list with elements \code{min} and \code{max} specifying the
#' minimum and maximum respectively of the log10 redction expected or a sinlge numeric value.
#' @param microbe.influent  \code{distribution} and \code{params}
#' specifying the distribution as a character and the parameters as a named list respectively
#' of the dilution distribution. 
#' @param dilution.exposure a named list eith elements
#' specifying the parameters of a cumulative distribution from which to draw the dilution value: 
#' \code{min}, \code{max}, and the vectors \code{x} and \code{p}
#' where \code{min} < \code{x} < \code{max} and 0 <= \code{p} <= 1
#' @return a simulated microbe value at exposure site
#' @export
setGeneric("conc_qmra",
           function(efficacy, microbe.influent, dilution.exposure){
               standardGeneric("conc_qmra")
           })
setMethod("conc_qmra",
          c(efficacy = "list", microbe.influent = "list",dilution.exposure = "list"),
          function(efficacy, microbe.influent,dilution.exposure){
              ## simulate microde at influent
              influent <- get.sim.value(x = microbe.influent, nsim = 1)
              ## efficacy
              eff.val <- runif(n = 1, efficacy[["min"]], efficacy[["max"]])
              microbe.effluent <- 10^(log10(influent) - eff.val)
              ## simulate dilution
              dilution = rcumulative(n = 1,x = dilution.exposure[["x"]],
                                     p = dilution.exposure[["p"]], 
                                     min = dilution.exposure[["min"]],
                                     max = dilution.exposure[["max"]])
              
              
              microbe.exposure = microbe.effluent*dilution
              return(list(microbe.exposure = microbe.exposure,sim = list(influent.val = influent, efficacy.val = eff.val, dilution = dilution)))
          })
setMethod("conc_qmra",
          c(efficacy = "numeric", microbe.influent = "list",
            dilution.exposure = "list"),
          function(efficacy, microbe.influent, dilution.exposure){
            ## efficacy
            eff.val <- efficacy
            ## simulate microde at influent
            influent <- get.sim.value(x = microbe.influent, nsim = 1)
            ## simulate dilution
            dilution = rcumulative(n = 1,x = dilution.exposure[["x"]],
                                   p = dilution.exposure[["p"]], 
                                   min = dilution.exposure[["min"]],
                                   max = dilution.exposure[["max"]])
            
            microbe.effluent <- 10^(log10(influent) - eff.val)
            microbe.exposure = microbe.effluent*dilution
            return(list(microbe.exposure = microbe.exposure,sim = list(influent.val = influent, efficacy.val = eff.val, dilution = dilution)))
          })
#' Function to simulate ingested volume for QMRA models
#' @param duration a named list with elements \code{distribution} (character), \code{min} (numeric),
#' \code{mode} (numeric), and \code{max} (numeric) specifying the assumed duration distribution and
#' associated parameters
#' @param vol.rate a named list with elements \code{distribution} (character), \code{min} (numeric),
#' \code{mode} (numeric), and \code{max} (numeric) specifying the assumed volume rate distribution and
#' associated parameters
setGeneric("ingested_qmra",
           function(duration, vol.rate){
               standardGeneric("ingested_qmra")
           })
setMethod("ingested_qmra",
          c(duration = "list", vol.rate = "list"),
          function(duration, vol.rate){
            vol <- get.sim.value(x = vol.rate, nsim = 1)
            dur <- get.sim.value(x = duration, nsim = 1)
            ## return volume ingested
            vol.ingested = dur*vol
            return(list(vol.ingested = vol.ingested,sim = list(volume = vol, duration = dur)))
            }
          )
#' Function to carry out Monte Carlo based simulations using both
#' \link{conc_qmra} and \link{ingested_qmra}
#' @param nsim either a numeric value specifying the number of Monte Carlo simulations to carry out for
#' both concentration and exposure, else a named vector of length two specifying the number of simulations seperatly.
#' for the \code{nsim.conc} and \code{nsim.exposure}.
#' @inheritParams conc_qmra
#' @inheritParams ingested_qmra
#' @export
setGeneric("mc_qmra",
           function(nsim, efficacy, microbe.influent,
                    dilution.exposure, duration, vol.rate){
               standardGeneric("mc_qmra")
           })
setMethod("mc_qmra",
          c(nsim = "numeric",efficacy = "list", microbe.influent = "list",
            dilution.exposure = "list",
            duration = "list", vol.rate = "list"),
          function(nsim , efficacy, microbe.influent, 
                    dilution.exposure, duration, vol.rate){
              if(length(nsim) == 2){
                  conc = sim.influent = sim.dilution = sim.efficacy = numeric(nsim['nsim.conc'])
                  expos = sim.vol = sim.dur = numeric(nsim['nsim.exposure'])
                  for(i in 1:nsim[1]){
                      tmp = conc_qmra(efficacy = efficacy, microbe.influent = microbe.influent,
                                          dilution.exposure = dilution.exposure)
                      conc[i] = tmp$microbe.exposure
                      sim.influent[i] = tmp$sim$influent.val
                      sim.efficacy[i] = tmp$sim$efficacy.val
                      sim.dilution[i] = tmp$sim$dilution
                  }
                  for(j in 1:nsim[2]){
                     tmp2 = ingested_qmra(duration = duration, vol.rate = vol.rate)
                     expos[j] = tmp2$vol.ingested
                     sim.vol[j] = tmp2$sim$volume
                     sim.dur[j] = tmp2$sim$duration
                  }
              }
              if(length(nsim) == 1){
                  conc = sim.influent = sim.dilution = sim.efficacy = sim.vol = sim.dur = expos = numeric(nsim)
                  for(i in 1:nsim){
                    tmp = conc_qmra(efficacy = efficacy, microbe.influent = microbe.influent,
                                    dilution.exposure = dilution.exposure)
                    conc[i] = tmp$microbe.exposure
                    sim.influent[i] = tmp$sim$influent.val
                    sim.efficacy[i] = tmp$sim$efficacy.val
                    sim.dilution[i] = tmp$sim$dilution
                    tmp2 = ingested_qmra(duration = duration, vol.rate = vol.rate)
                    expos[i] = tmp2$vol.ingested
                    sim.vol[i] = tmp2$sim$volume
                    sim.dur[i] = tmp2$sim$duration
                  }
              }
              dose.list = list(concentrations = conc, exposure = expos, dose = outer(conc,expos), 
                               inputs = list(nsim = nsim, efficacy = efficacy, microbe.influent = microbe.influent,
                                             dilution.exposure = dilution.exposure, duration = duration, vol.rate = vol.rate,
                                             sim.influent = sim.influent, sim.efficacy = sim.efficacy,
                                             sim.dilution = sim.dilution, sim.vol = sim.vol, sim.dur = sim.dur))
              return(dose.list)
          })

setMethod("mc_qmra",
          c(nsim = "numeric",efficacy = "numeric", microbe.influent = "list",
            dilution.exposure = "list",
            duration = "list", vol.rate = "list"),
          function(nsim , efficacy, microbe.influent, 
                    dilution.exposure, duration, vol.rate){
            if(length(nsim) == 2){
              conc = sim.influent = sim.dilution = sim.efficacy = numeric(nsim['nsim.conc'])
              expos = sim.vol = sim.dur = numeric(nsim['nsim.exposure'])
              for(i in 1:nsim[1]){
                tmp = conc_qmra(efficacy = efficacy, microbe.influent = microbe.influent,
                                dilution.exposure = dilution.exposure)
                conc[i] = tmp$microbe.exposure
                sim.influent[i] = tmp$sim$influent.val
                sim.efficacy[i] = tmp$sim$efficacy.val
                sim.dilution[i] = tmp$sim$dilution
              }
              for(j in 1:nsim[2]){
                tmp2 = ingested_qmra(duration = duration, vol.rate = vol.rate)
                expos[j] = tmp2$vol.ingested
                sim.vol[j] = tmp2$sim$volume
                sim.dur[j] = tmp2$sim$duration
              }
            }
            if(length(nsim) == 1){
              conc = sim.influent = sim.dilution = sim.efficacy = sim.vol = sim.dur = expos = numeric(nsim)
              for(i in 1:nsim){
                tmp = conc_qmra(efficacy = efficacy, microbe.influent = microbe.influent,
                                dilution.exposure = dilution.exposure)
                conc[i] = tmp$microbe.exposure
                sim.influent[i] = tmp$sim$influent.val
                sim.efficacy[i] = tmp$sim$efficacy.val
                sim.dilution[i] = tmp$sim$dilution
                tmp2 = ingested_qmra(duration = duration, vol.rate = vol.rate)
                expos[i] = tmp2$vol.ingested
                sim.vol[i] = tmp2$sim$volume
                sim.dur[i] = tmp2$sim$duration
              }
            }
            dose.list = list(concentrations = conc, exposure = expos, dose = outer(conc,expos), 
                             inputs = list(nsim = nsim, efficacy = efficacy, microbe.influent = microbe.influent,
                                           dilution.exposure = dilution.exposure, duration = duration, vol.rate = vol.rate,
                                           sim.influent = sim.influent, sim.efficacy = sim.efficacy,
                                           sim.dilution = sim.dilution, sim.vol = sim.vol, sim.dur = sim.dur))
            return(dose.list)
          })
