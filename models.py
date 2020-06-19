import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


# Class for the SIR model
class SIR:
    def __init__(self, s0, i0, r0, population, days, cont_rate, recov_rate, events=None):
        if events is None:
            events = []
        self.s0 = s0
        self.i0 = i0
        self.r0 = r0
        self.population = population
        self.days = days
        self.cont_rate = cont_rate
        self.recov_rate = recov_rate
        self.__events = events

    # Add events to the model
    def add_events(self, events):
        self.__events = self.__events + events

    # Remove all events
    def clear_events(self):
        self.__events = []

    # Returns the value of the next contact rate, after events are applied
    def __next_cont_rate(self, s, day, cont_rate):
        if not self.__events:
            return cont_rate
        t, func = self.__events[0]
        if t != day:
            return cont_rate
        self.__events = self.__events[1:]
        s = s / self.population
        return func(cont_rate * s / self.recov_rate) * self.recov_rate / s

    @staticmethod
    def __deriv(sir, t, model, cont_rate):
        s, i, r = sir
        ds_dt = -cont_rate * s * i / model.population
        di_dt = cont_rate * s * i / model.population - model.recov_rate * i
        dr_dt = model.recov_rate * i
        return ds_dt, di_dt, dr_dt

    def get_data(self):
        self.__events.sort(key=lambda e: e[0])
        events_backup = self.__events.copy()
        data = np.zeros((self.days, 3), dtype=np.float)
        data[0] = self.s0, self.i0, self.r0
        cont_rate = self.__next_cont_rate(self.s0, 0, self.cont_rate)
        for day in range(1, self.days):
            t = np.linspace(day - 1, day, 2)
            data[day] = odeint(SIR.__deriv, data[day - 1], t, args=(self, cont_rate))[-1]
            cont_rate = self.__next_cont_rate(data[day][0], day, cont_rate)
        self.__events = events_backup
        return np.array(data).T

    def plot(self):
        s, i, r = self.get_data() / 1000
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
        ax.fill_between(t, self.population / 1000, r + i, facecolor=(.9, .9, .9))
        ax.set_xlabel('Time (days)')
        ax.set_ylabel('Number (1000s)')
        plt.show()


# Class for the SEIR model
class SEIR:
    def __init__(self, s0, e0, i0, r0, population, days, cont_rate, incub_time, recov_rate, events=None):
        if events is None:
            events = []
        self.s0 = s0
        self.e0 = e0
        self.i0 = i0
        self.r0 = r0
        self.population = population
        self.days = days
        # cont_rates elements will have format [(start_time, value)]
        self.cont_rate = cont_rate
        self.incub_time = incub_time
        self.recov_rate = recov_rate
        # events should be be a list of format [(time, lambda)]
        self.__events = events

    # Add events to the model
    def add_events(self, events):
        self.__events = self.__events + events

    # Remove all events
    def clear_events(self):
        self.__events = []

    # Returns the value of the next contact rate, after events are applied
    def __next_cont_rate(self, s, day, cont_rate):
        if not self.__events:
            return cont_rate
        t, func = self.__events[0]
        if t != day:
            return cont_rate
        self.__events = self.__events[1:]
        s = s / self.population
        return func(cont_rate * s / self.recov_rate) * self.recov_rate / s

    # Does the calculations for the 4 categories in the model
    @staticmethod
    def __deriv(seir, t, model, cont_rate):
        s, e, i, r = seir
        ds_dt = -cont_rate * s * i / model.population
        de_dt = cont_rate * s * i / model.population - model.incub_time * e
        di_dt = model.incub_time * e - model.recov_rate * i
        dr_dt = model.recov_rate * i
        return ds_dt, de_dt, di_dt, dr_dt

    # Returns a 4 x t array of values corresponding to S, E, I, R
    def get_data(self):
        self.__events.sort(key=lambda e: e[0])
        events_backup = self.__events.copy()
        data = np.zeros((self.days, 4), dtype=np.float)
        data[0] = self.s0, self.e0, self.i0, self.r0
        cont_rate = self.__next_cont_rate(self.s0, 0, self.cont_rate)
        for day in range(1, self.days):
            t = np.linspace(day - 1, day, 2)
            data[day] = odeint(SEIR.__deriv, data[day - 1], t, args=(self, cont_rate))[-1]
            cont_rate = self.__next_cont_rate(data[day][0], day, cont_rate)
        self.__events = events_backup
        return np.array(data).T

    # Plots the data outputted by the model
    def plot(self):
        s, e, i, r = self.get_data() / 1000
        t = np.linspace(0, self.days, self.days)
        fig, ax = plt.subplots()
        ax.plot(t, s, 'b', alpha=0.5, lw=2, label='Susceptible')
        ax.plot(t, e, 'y', alpha=0.5, lw=2, label='Exposed')
        ax.plot(t, i, 'r', alpha=0.5, lw=2, label='Infected')
        ax.plot(t, r, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
        ax.set_xlabel('Time (days)')
        ax.set_ylabel('Number (1000s)')
        ax.legend()
        ax.grid(c='lightgray')
        plt.show()

    # Plots the data outputted by the model, but prettier
    def plot2(self):
        s, e, i, r = SEIR.get_data(self) / 1000
        t = np.linspace(0, self.days, self.days)
        fig = plt.figure()
        ax = fig.add_subplot(facecolor=(.9, .9, .9), xmargin=0, ymargin=0)
        ax.fill_between(t, i, 0, facecolor=(1, .3, .3))
        ax.fill_between(t, e + i, i, facecolor=(1, .6, .6))
        ax.fill_between(t, r + i, e + i, facecolor=(.7, .7, .7))
        ax.fill_between(t, self.population / 1000, e + i + r, facecolor=(.9, .9, .9))
        ax.set_xlabel('Time (days)')
        ax.set_ylabel('Number (1000s)')
        plt.show()
