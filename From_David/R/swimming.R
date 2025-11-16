#' Estimate Swim Duration
#'
#' The \code{swim_duration} function estimates swim duration based on provided parameters.
#'
#' @param n Number of swim durations to generate.
#' @param min_duration Minimum duration of a swim (typical values 0.2 hour).
#' @param mode_duration Mode duration of a swim (typical values 1 hour).
#' @param max_duration Maximum duration of a swim (typical value 4 hour).
#'
#' @return A matrix containing \code{n} swim durations.
#'
#' @details
#' This function uses the rpert function from the mc2d package to generate swim durations.
#' The rpert function generates random samples from the truncated triangular distribution.
#' The parameters \code{min_duration}, \code{mode_duration}, and \code{max_duration} define
#' the shape of the distribution.
#'
#' @seealso
#' \code{\link[=rpert]{rpert}} function from the mc2d package.
#'
#' @examples
#' \dontrun{
#' # Generate swim durations with default parameters
#' swim_durations <- swim_duration(10)
#'
#' # Generate swim durations with custom parameters
#' custom_durations <- swim_duration(10, min_duration = 0.5, mode_duration = 1.5, max_duration = 3.0)
#' }
#'
#' @export
swim_duration <- function(n, min_duration, mode_duration, max_duration, mySeed = 876){

  require(mc2d) # for the rpert distribution
  set.seed(mySeed)

  iter <- n * 100
  duration <- rpert(iter, min = min_duration, mode = mode_duration, max = max_duration, shape = 4)
  duration <- matrix(duration, ncol = n, byrow = TRUE)
  return(duration)
}


#' Ingestion rate (Swimmers primary contact)
#'
#' Ingestion rate (mL/h) of water from primary contact with water. Takes the form of a truncated lognormal distribution
#'
#' @param n Number of iterations to generate BAF values.
#' @param mean_ingestion_rate (typical default value = 53)
#' @param sd_ingestion_rate (typical default value = 75)
#' @param min_ingestion_rate (typical default value= 5)
#' @param max_ingestion_rate (typical default value= 250).
#'
#' @return A vector containing generated BAF values.
#' @export
#'
#' @examples
#' # Generate BAF values for 1000 iterations using default parameters
#' baf_values <- BAF(1000)
#'
swim_ingestion_rate <- function(n,
                                min_ingestion_rate,
                                max_ingestion_rate,
                                mean_ingestion_rate,
                                sd_ingestion_rate,
                                mySeed = 521){
  # Generate random samples from the truncated normal distribution
  require(truncnorm)
  set.seed(mySeed)

  iter <- n * 100

  primary_ingestion_rate <- rtruncnorm(iter,
                                       a = min_ingestion_rate,
                                       b = max_ingestion_rate,
                                       mean = mean_ingestion_rate,
                                       sd = sd_ingestion_rate
  )

  primary_ingestion_rate <- matrix(primary_ingestion_rate,
                                   ncol = n,
                                   byrow = TRUE
  )

  return(primary_ingestion_rate)
}


#' Calculate Volume Ingested during Swim
#'
#' The \code{volume_ingested_swim} function calculates the volume ingested during a swim
#' based on swim duration and ingestion rate parameters.
#'
#' @param n Number of swims to simulate.
#' @param min_duration Minimum duration of a swim (default = 0.2 h).
#' @param mode_duration Mode duration of a swim (default = 1 h).
#' @param max_duration Maximum duration of a swim (default = 4 h).
#' @param min_ingestion_rate Minimum ingestion rate during a swim (5 mL/h).
#' @param max_ingestion_rate Maximum ingestion rate during a swim (250 mL/h).
#' @param mean_ingestion_rate Mean ingestion rate during a swim (53 mL/h).
#' @param sd_ingestion_rate Standard deviation of ingestion rate during a swim (75 mL/h).
#'
#' @return A matrix containing the volume ingested during each of the \code{n} swims.
#'
#' @details
#' This function utilizes the \code{swim_duration} and \code{swim_ingestion_rate} functions
#' to generate swim durations and ingestion rates, respectively, and calculates the volume ingested
#' during each swim by multiplying the corresponding duration and ingestion rate.
#'
#' @seealso
#' \code{\link[=swim_duration]{swim_duration}} function for generating swim durations.
#' \code{\link[=swim_ingestion_rate]{swim_ingestion_rate}} function for generating ingestion rates.
#'
#' @examples
#' \dontrun{
#' # Calculate volume ingested during swims with default parameters
#' volume_data <- volume_ingested_swim(10)
#'
#' # Calculate volume ingested during swims with custom parameters
#' custom_volume_data <- volume_ingested_swim(10, min_duration = 0.5, mode_duration = 1.5,
#'                                            max_duration = 3.0, min_ingestion_rate = 10,
#'                                            max_ingestion_rate = 200, mean_ingestion_rate = 60,
#'                                            sd_ingestion_rate = 80)
#' }
#'
#' @export
volume_ingested_swim <- function(n,
                                 min_duration = 0.2,
                                 mode_duration = 1,
                                 max_duration = 4,
                                 min_ingestion_rate = 5,
                                 max_ingestion_rate = 250,
                                 mean_ingestion_rate = 53,
                                 sd_ingestion_rate = 75){
  duration <- swim_duration(n, min_duration, mode_duration, max_duration)
  ingestion_rate <- swim_ingestion_rate(n, min_ingestion_rate, max_ingestion_rate, mean_ingestion_rate, sd_ingestion_rate)
  vol <- duration * ingestion_rate
  return(vol)
}

