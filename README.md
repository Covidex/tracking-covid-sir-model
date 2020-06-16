#### TO DO:
* Rewrite SEIR to support events. It is probably impossible to do this
  using *scipy*'s *odeint* or such functions, so the good old
  step-by-step method might be the best we've got. That would mean
  calculating *s, e, i, r* for each day using the numbers from
  the previous days and the events.
  
  Events have the form *[(day, lambda)]* meaning that on a given day, the
  value of R becomes the output of *lambda(R)*. The following equations
  might prove useful:
  
  * `R = R0 * s` Value of R with respect to R0 and s
  * `R0 -> lambda(R0 * s) / s` New value of R0 after applying the
    lambda function to R