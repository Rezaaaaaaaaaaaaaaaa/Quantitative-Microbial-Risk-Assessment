#' treatment
#'
#' Estimate of how how the
#'
#' @param influent vector, concentration of bugs per L in influent
#' @param LRV numeric, treatment Log reduction value
#'
#' @return effluent concentration of bugs in effluent
#' @export
#'
#' @examples
#' treatment(1000,2)
treatment <- function(influent, LRV){
  # takes influent estimates the effluent based on the LRV
  treatment <- 10^LRV
  effluent <- influent/treatment
  return(effluent)
}


#' methodHarmonisationFactor
#'
#' Corrects concentration taking into account the measurement method
#' only used for norovirus
#'
#' @param effluent vector, concentration of bugs in treated wastewater
#' @param MHF number, correcting factor (only used for Norovirus)
#'
#' @return correctedEffluent
#' @export
#'
#' @examples
#' # Correct concentration of Norovirus in treated wastewater using MHF 1.5
#' effluent_concentration <- c(10, 15, 20, 25)
#' corrected_concentration <- methodHarmonisationFactor(effluent_concentration, 1.5)
#'
methodHarmonisationFactor <- function(effluent, MHF){
  #method correction
  correctedEffluent <-  effluent/MHF
  return(correctedEffluent)
}


#' convertConcInLiterToMililiters
#'
#' Deals with the fact that bug concentration is in L and we need it in mL
#'
#' @param effluent number, concentration per L
#'
#' @return effluent concentraion per mL
#' @export
#'
#' @examples
#' convertConcInLiterToMililiters(1000)
#'
convertConcInLiterToMililiters <- function(effluent){
  # convert concs from L to mL
  effluent <- effluent/1000
  return(effluent)
}

#' Estimates concentrtion of effluent at the end of the pipe
#'
#' Takes the estimate concentration of bugs in **influent** (per L) and returns the
#' concentration per ml in the **effluent** taking into account treatment and MHF.
#' This function is specifically for **norovirus** and assumes Xp = 0.95
#'
#' @param n number of iterations
#' @param X0 minimum conc
#' @param X50 median conc
#' @param X100 maximum conc
#' @param LRV Treatment
#' @param P probability value relating to Xp (default is normally 0.95)
#' @param MHF Method Harmonisation Factor (default is normally 18.5)
#'
#' @return vector
#' @export
#'
#' @examples
#' estEffluentConc(5, 10, 1000, 1e6, 2, 0.95, 18.5)
#'
estEffluentConc <- function(n, X0, X50, X100, LRV, P = 0.95, MHF = 18.5){
  # estimate the "effective concentration of pathogens being discharged
  # taking into account the concentration of pathogens per l.
  # Treatment the water. Correcting for method and converting to concentration per ml
  influent <- rhockey(n, X0, X50, X100, P)
  effluent <- treatment(influent, LRV)
  effluent <- methodHarmonisationFactor(effluent, MHF)
  effluent <- convertConcInLiterToMililiters(effluent)
  return(effluent)
}
