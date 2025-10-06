#' Human dose-response study data from Ward et al 
#' @name dr_study
#' @format a data frame with 8 rows and 3 variables:
#' \describe{
#' \item{dose}{dose of infectious pathogen}
#' \item{positive}{number of positive subjects}
#' \item{total}{total number of subjects}
#' }
#' @docType data
#' @keywords datasets
#' @usage data(dr_study)
 
#' C.parvum(Iowa strain) infectivity in human volunteers by oral dosing.
#' Example from Table 8.7 in Haas, Rose & Gerba QMRA 2014 
#' @name parvum
#' @format a data frame with 8 rows and 3 variables:
#' \describe{
#' \item{dose}{dose of infectious pathogen}
#' \item{positive}{number of positive subjects}
#' \item{total}{total number of subjects}
#' }
#' @docType data
#' @keywords datasets
#' @usage data(parvum)
 
#' experimental data sets for ecoli.
#' Example from Table 8.8 in Haas, Rose & Gerba QMRA 2014 
#' @name ecoli
#' @format a data frame with 19 rows and 4 variables:
#' \describe{
#' \item{dose}{dose of infectious pathogen}
#' \item{positive}{number of positive subjects}
#' \item{total}{total number of subjects}
#' \item{strain}{character specifying the ecoli strain}
#' }
#' @docType data
#' @keywords datasets
#' @usage data(ecoli)
#' 
#' 
#' dose-response study data from Tenuis et al 1996 for Giardia 
#' lamblia in healthy volunteers
#' @name lamblia
#' @format a data frame with 8 rows and 3 variables:
#' \describe{
#' \item{dose}{dose of infectious pathogen}
#' \item{positive}{number of positive subjects}
#' \item{total}{total number of subjects}
#' }
#' @docType data
#' @keywords datasets
#' @usage data(lamblia)

#' experimental data sets for Rhinovirus dose-response experimants.
#' Data from http://qmrawiki.canr.msu.edu/experiments/rhinovirus
#' @name rhinovirus
#' @format a data frame with 47 rows and 4 variables:
#' \describe{
#' \item{dose}{dose of infectious pathogen}
#' \item{positive}{number of positive subjects}
#' \item{total}{total number of subjects}
#' \item{experiment}{character specifying the ecoli strain}
#' }
#' @docType data
#' @keywords datasets
#' @usage data(rhinovirus)
#' 
#' Estimated parameter values from dose-response studies found in the literature
#' @name pathogens
#' @format an object of class pathogens that contains named slots relating to each pathogen. Each
#' slot cotains a list of esimated parameters from dose-response studies found in the literature
#' @docType data
#' @keywords datasets
#' @usage data(pathogens)
#' 
#' @name Enterococci_concentration
#' @format a data frame with 18961 rows and 8 columns containing 
#' simulated concentration values (g/m3) from a hydrodynamic model
#' based on a constant input load of 1000 (MPN/m3). Each column represents
#' a costal site at Whanganui, NZ.
#' @docType data
#' @keywords datasets
#' @usage data(Enterococci_concentration)
#' 
#' @name Fecal_bacteria_concentration
#' @format a data frame with 18961 rows and 8 columns containing 
#' simulated concentration values (g/m3) from a hydrodynamic model
#' based on a constant input load of 1000 (MPN/m3). Each column represents
#' a costal site at Whanganui, NZ.
#' @docType data
#' @keywords datasets
#' @usage data(Fecal_bacteria_concentration)
#' 
#' @name Tracer_concentration
#' @format a data frame with 18961 rows and 8 columns containing 
#' simulated concentration values (g/m3) from a hydrodynamic model
#' based on a constant input load of 1000 (MPN/m3). Each column represents
#' a costal site at Whanganui, NZ.
#' @docType data
#' @keywords datasets
#' @usage data(Tracer_concentration)
#' 
#' @name Enterococci_dilution
#' @format a data frame with 18961 rows and 8 columns containing 
#' simulated dilution values for \link{Enterococci_concentration}. Each column represents
#' a costal site at Whanganui, NZ.
#' @docType data
#' @keywords datasets
#' @usage data(Enterococci_dilution)
#' 
#' @name Fecal_bacteria_dilution
#' @format a data frame with 18961 rows and 8 columns containing 
#' simulated dilution values for \link{Fecal_bacteria_concentration}. Each column represents
#' a costal site at Whanganui, NZ.
#' @docType data
#' @keywords datasets
#' @usage data(Fecal_bacteria_dilution)
#' 
#' @name Tracer_dilution
#' @format a data frame with 18961 rows and 8 columns containing 
#' simulated dilution values for \link{Tracer_concentration}. Each column represents
#' a costal site at Whanganui, NZ.
#' @docType data
#' @keywords datasets
#' @usage data(Tracer_dilution)
