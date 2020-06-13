import models

population = 10**6
days = 365
cont_rate = 1 / 4
recov_rate = 1 / 10
incub_time = 1 / 3
s0, e0, i0, r0 = (population - 1, 0, 1, 0)

# sir = models.SIR(s0, i0, r0, population, days, cont_rate, recov_rate)
# sir.plot2()

seir = models.SEIR(s0, e0, i0, r0, population, days, cont_rate, incub_time, recov_rate)
seir.plot2()
