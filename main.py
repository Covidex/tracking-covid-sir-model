import sir

population = 1000
days = 365
cont_rate = .2
recov_rate = 1. / 10
s0, i0, r0 = (1, 0, population - 1)

model = sir.Sir(s0, i0, r0, population, days, cont_rate, recov_rate)
model.plot()
