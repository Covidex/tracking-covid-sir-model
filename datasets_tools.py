import numpy as np
import csv


def load_owid_data(filename='datasets/owid-covid-data.csv', continent=None, country=None):
    reader = csv.reader(open(filename))
    data = list(reader)[1:]
    if continent:
        data = [row for row in data if row[1] == continent]
    if country:
        data = [row for row in data if row[2] == country]
    data = [row for row in data if row[4] != '0']
    total_cases = []
    new_cases = []
    for row in data:
        total_cases.append(row[4])
        new_cases.append(row[5])
    return np.array((total_cases, new_cases), dtype=np.int32)


def load_data(filename='datasets/covid_19_clean_complete.csv', cols=None):
    reader = csv.reader(open(filename))
    data = list(reader)[1:]
    cs = []
    for i in range(len(cols)):
        cs.append([row[cols[i]] for row in data])
    return np.array(cs, dtype=np.float)


cov = load_data(cols=(5, 6, 7, 8))
print(cov)
