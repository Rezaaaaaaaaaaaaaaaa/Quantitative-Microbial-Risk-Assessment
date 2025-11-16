#' Swim Risk Model
#'
#' This function calculates the risk of norovirus infection from #'swimming in water impacted by wastewater. It considers factors #'such as influent concentration, treattment (LRV), considering factors such as dilution, water consumption,
#' and dose-response for disagregated norovirus.
#'
#' @param n Number of simulations
#' @param X0 Parameter for effluent concentration calculation
#' @param X50 Parameter for effluent concentration calculation
#' @param X100 Parameter for effluent concentration calculation
#' @param LRV Log Removal Value for effluent concentration calculation
#' @param P Parameter for effluent concentration calculation
#' @param MHF Method harmonisation factor for norovirus
#' @param myCSVFile Path to the CSV file containing water quality data
#' @param mySite Name of the site for water quality data
#' @param min_duration Minimum duration of swimming (minutes)
#' @param mode_duration Mode duration of swimming (minutes)
#' @param max_duration Maximum duration of swimming (minutes)
#' @param min_ingestion_rate Minimum ingestion rate (volume per minute)
#' @param mean_ingestion_rate Mean ingestion rate (volume per minute)
#' @param sd_ingestion_rate Standard deviation of ingestion rate (volume per minute)
#' @param max_ingestion_rate Maximum ingestion rate (volume per minute)
#'
#' @return A vector containing the number of infected individuals in each simulation.
#'
#' @details The function calculates the risk by estimating effluent concentration, dilution
#' factor, ingested volume, dose, and applying dose-response modeling.
#'
#' @seealso
#' \code{\link{estEffluentConc}}, \code{\link{estDilution}},
#' \code{\link{volume_ingested_swim}}, \code{\link{doseResponseNoro}},
#' \code{\link{isInfected}}, \code{\link{isIllNoro}}, \code{\link{roundDose}}
#'
#' @export
swimRiskModel <- function(n,
                          X0,
                          X50,
                          X100,
                          LRV,
                          P,
                          MHF,
                          myCSVFile,
                          mySite,
                          min_duration,
                          mode_duration,
                          max_duration,
                          min_ingestion_rate,
                          mean_ingestion_rate,
                          sd_ingestion_rate,
                          max_ingestion_rate
){
  # effluent conc
  effluentConc <- estEffluentConc(n, X0, X50, X100, LRV, P, MHF)
  dilutionFactor <- estDilution(myCSVFile, mySite, n)
  dilutedEffluentConc <- effluentConc / dilutionFactor

  # injested vol
  volWaterConsumed <- volume_ingested_swim(n,
                                           min_duration,
                                           mode_duration,
                                           max_duration,
                                           min_ingestion_rate,
                                           mean_ingestion_rate,
                                           sd_ingestion_rate,
                                           max_ingestion_rate
  )

  # dose
  rawDose <-  volWaterConsumed %*% diag(dilutedEffluentConc) # not this is used to multiple each column by a single value
  roundedDose <- roundDose(rawDose)
  probInfection <- doseResponseNoro(roundedDose)
  isInfected <- isInfected(probInfection)
  isIllNoro <- isIllNoro(isInfected)
  results <- colSums(isIllNoro)
  return(results)
}
