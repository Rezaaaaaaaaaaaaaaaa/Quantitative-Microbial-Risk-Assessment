context("Testing deviances")

test_that(
  "deviance beta poisson",
  {
    ## Testing beta poisson deviance 
    model <- "betapoisson"
    params <- c(alpha = 0.265,N50 = 5.597)
    data <- dr_study
    dev.bp <- qmra_dev(data = data, params = params, model = model)
    expect_equal(dev.bp, expected = 6.81592,
                 tolerance = 0.01)
  }
)
test_that(
  "deviance logprobit",
  {
    ## Testing log probit deviance to data 
    model <- "logprobit"
    params <- c(q1 = 10.504,q2 = 4.137)
    data <- dr_study
    dev.lp <- qmra_dev(data = data, params = params, model = model)
    expect_equal(dev.lp, expected = 11.87489,
                 tolerance = 0.01)
  }
)