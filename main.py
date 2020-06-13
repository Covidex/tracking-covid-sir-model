import models

population = 10**6
days = 365
cont_rate = 1. / 4
recov_rate = 1. / 10
s0, i0, r0 = (population - 1, 1, 0)

model = models.SIR(s0, i0, r0, population, days, cont_rate, recov_rate)
model.plot2()
