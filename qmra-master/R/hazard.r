#' hazard model for probability of illness given infection
#' @param gamma shape parameter
#' @param eta location parameter
#' @param dose vector of doses
#' @param increase logical is the model an increasing hazard model or a decreasing model
#' @export
setGeneric("hazard",
           function(gamma, eta, dose, increase){
               standardGeneric("hazard")
           })

setMethod("hazard",
          c(gamma = "numeric", eta = "numeric", dose = "vector", increase = "logical"),
          function(gamma, eta, dose, increase){
              if(increase == FALSE){
                  haz = 1 - (1 + eta/dose)^-gamma
              }else{
                  haz = 1 - (1 + eta*dose)^-gamma
              }
              return(haz)
          }
          )
