import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


class SIR:
    def __init__(self, s0, i0, r0, population, days, cont_rate, recov_rate):
        self.s0 = s0
        self.i0 = i0
        self.r0 = r0
        self.population = population
        self.days = days
        self.cont_rate = cont_rate
        self.recov_rate = recov_rate

    @staticmethod
    def __deriv(y, t, model):
        s, i, r = y
        ds_dt = -model.cont_rate * s * i / model.population
        di_dt = model.cont_rate * s * i / model.population - model.recov_rate * i
        dr_dt = model.recov_rate * i
        return ds_dt, di_dt, dr_dt

    def get_data(self):
        y0 = self.s0, self.i0, self.r0
        t = np.linspace(0, self.days, self.days)
        data = odeint(SIR.__deriv, y0, t, args=(self,))
        return np.array(data).T

    def plot(self):
        s, i, r = SIR.get_data(self) / 1000
        t = np.linspace(0, self.days, self.days)
        fig, ax = plt.subplots()
        ax.plot(t, s, 'b', alpha=0.5, lw=2, label='Susceptible')
        ax.plot(t, i, 'r', alpha=0.5, lw=2, label='Infected')
        ax.plot(t, r, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
        ax.set_xlabel('Time (days)')
        ax.set_ylabel('Number (1000s)')
        ax.grid(c='lightgray')
        ax.legend()
        plt.show()

    def plot2(self):
        s, i, r = SIR.get_data(self) / 1000
        t = np.linspace(0, self.days, self.days)
        fig = plt.figure()
        ax = fig.add_subplot(facecolor=(.9, .9, .9), xmargin=0, ymargin=0)
        ax.fill_between(t, i, 0, facecolor=(1, .3, .3))
        ax.fill_between(t, r + i, i, facecolor=(.7, .7, .7))
        ax.set_xlabel('Time (days)')
        ax.set_ylabel('Number (1000s)')
        plt.show()


# class SEIR(SIR): TODO
#     def __init__(self, s0, e0, i0, r0, population, days, cont_rate, recov_rate):
#         self.e0 = e0
#         super().__init__(s0, i0, r0, population, days, cont_rate, recov_rate)