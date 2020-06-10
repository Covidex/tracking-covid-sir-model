import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


class Sir:
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
        data = odeint(Sir.__deriv, y0, t, args=(self,))
        return np.array(data).T

    def plot(self):
        s, i, r = Sir.get_data(self)
        t = np.linspace(0, self.days, self.days)
        fig, ax = plt.subplots()
        ax.plot(t, s / 1000, 'b', alpha=0.5, lw=2, label='Susceptible')
        ax.plot(t, i / 1000, 'r', alpha=0.5, lw=2, label='Infected')
        ax.plot(t, r / 1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
        ax.set_xlabel('Time (days)')
        ax.set_ylabel('Number (1000s)')
        ax.grid(c='lightgray')
        ax.legend()
        plt.show()
