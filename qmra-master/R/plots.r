#' Function to plot either a fitted dose-response model
#' or the raw data
#' @param x a \code{qmra} fitted object or a data frame with named columns dose, positive, total
#' @export
setGeneric("show.qmra", 
           function(x){
             standardGeneric("show.qmra")
             })

setMethod("show.qmra",
          c(x = "qmra"),
          function(x){
            dose = x@data$dose
            risk = x@data$positive/x@data$total
            plot(dose,risk,pch = 20, xlab = "Dose", ylab = "Risk",ylim = c(0,1))
            pars = x@fit$estimated_parameters
            mod = x@model
            est = dr.mod(model = mod, params = pars, dose = dose)
            lines(dose,est,lwd = 2,lty = 2)
            legend("bottomright",bty = "n", lwd = 2, lty = 2, legend = "Estimated fit")
          })

setMethod("show.qmra",
          c(x = "data.frame"),
          function(x){
            dose = x$dose
            risk = x$positive/x$total
            plot(dose,risk,pch = 20, xlab = "Dose", ylab = "Risk",ylim = c(0,1))
          })
#' Function to show historgarms of dose components
#' @export
show.components <- function(x){
   n <- length(x)
   nms <- names(x)
   pltList <- lapply(1:n, function(i){
     tmp <- data.frame(x[[i]])
     names(tmp) <- nms[i]
     ggplot2::ggplot(data = tmp, aes(x = tmp)) + 
       ggplot2::geom_histogram(bins = 30) +
       xlab(nms[i]) + ylab("Frequency") +
       theme_bw() + theme( plot.background = element_blank(),panel.grid.major = element_blank(),
                           panel.grid.minor = element_blank())
   })
   do.call(gridExtra::grid.arrange,pltList)
}
#' Internal rug plot function
#' @param x vector of numeric values to show in a rug plot
#' @param ... other arguments to pass into plot
my.rug <- function(x,...){
  plot(x,rep(1,length(x)),
       pch = "|",ylim = c(0.9,1.1), ylab = "",yaxt = "n",xlab = "", xaxt = "n")
  exponent <- floor(log10(max(x)))
  base <- round(max(x)/ 10^exponent, 2)
  axis(1,at = range(x),labels = c(round(min(x),1),
                                  as.expression(substitute(base%*%10^exponent))))
  points(mean(x),1,pch = 18, col = "red",cex = 2)
}
#' Tornado (sensitivity) qmra plot
#' @param mc_qmra output from \code{mc_qmra}
#' @param illness.qmra output from \code{illness.qmra} 
#' @export
setGeneric("tornado.qmra", 
           function(mc_qmra, illness.qmra){
             standardGeneric("tornado.qmra")
           })

setMethod("tornado.qmra",
          c(mc_qmra = "list", illness.qmra = "list"),
          function(mc_qmra, illness.qmra){
            if(length(illness.qmra)!= 6) stop("Not yet implemented for multiple dose response models")
            means = c(influent = mean(mc_qmra$inputs$sim.influent),efficacy = mean(mc_qmra$inputs$sim.efficacy),
                          dilution = mean(mc_qmra$inputs$sim.dilution), vol = mean(mc_qmra$inputs$sim.vol),
                          dur = mean(mc_qmra$inputs$sim.dur))
            mins = c(influent = min(mc_qmra$inputs$sim.influent),efficacy = min(mc_qmra$inputs$sim.efficacy),
                        dilution = min(mc_qmra$inputs$sim.dilution), vol = min(mc_qmra$inputs$sim.vol),
                        dur = min(mc_qmra$inputs$sim.dur))
            maxs = c(influent = max(mc_qmra$inputs$sim.influent),efficacy = max(mc_qmra$inputs$sim.efficacy),
                        dilution = max(mc_qmra$inputs$sim.dilution), vol = max(mc_qmra$inputs$sim.vol),
                        dur = max(mc_qmra$inputs$sim.dur))
            tornado.dat <- list()
            for(i in 1:length(means)){
              tornado.dat[[i]] <- list(min = NULL,max = NULL)
              if(i <= 3){
                conc.min <- prod(means[1:3][-i]) * mins[i]
                conc.max <- prod(means[1:3][-i]) * maxs[i]
                conc <- as.numeric(c(min = conc.min, max = conc.max))
              }else{
                conc <- as.numeric(means[1]*means[2]*means[3])
              }
              if(i > 3){
                exp.min <- means[4:5][-(i-3)] * mins[i]
                exp.max <- means[4:5][-(i-3)] * maxs[i]
                exp <- as.numeric(c(min = exp.min, max = exp.max))
              }else{
                exp <- as.numeric(means[4]*means[5])
              }
              dose.tmp <- exp*conc
              d_r =  dr.mod(model = illness.qmra$inputs$model, params = illness.qmra$inputs$params, dose = dose.tmp)
              tornado.dat[[i]] <- d_r
            }
            names(tornado.dat) <- names(means)
            dat <- stack(tornado.dat)
            dat <- rbind(dat,data.frame(values = c(1,1),ind = c("p.inf","p.inf")))
            dat$level <- rep(c("Low","High"),length(tornado.dat) + 1)
            dat$values <- dat$values + 1
            dat$values <- c(-1,1)*dat$values
            ggplot(dat, aes(ind, values, fill = level)) +
              geom_bar(stat = "identity",position = "identity",show.legend = FALSE) + 
              ylim(-3,3) +
              coord_flip() + 
              scale_y_continuous(breaks = c(-2,2),labels = c( "-100%", "100%")) + ylab("") + xlab("") +
              scale_x_discrete(labels = c("Microbes in influent","Efficacy","Dilution","Volume","Duration","Prob. ill")) + 
              theme(axis.ticks.y=element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
                    panel.background = element_blank()) 
            
            
          })