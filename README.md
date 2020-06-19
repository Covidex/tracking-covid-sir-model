#### Dev Notes:
  Events have the form *[(day, lambda)]* meaning that on a given day, the
  value of R becomes the output of *lambda(R)*. The following equations
  might prove useful:
  
  * `R = R0 * s` Value of R with respect to R0 and s
  * `R0 -> lambda(R0 * s) / s` New value of R0 after applying the
    lambda function to R
  * `cont -> lambda(cont * s / recov) * recov / s` New value of cont after
  applying the lambda function to R