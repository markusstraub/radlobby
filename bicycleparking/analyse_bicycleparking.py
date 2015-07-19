# -*- coding: utf-8 -*-
"""
Analysis of bicycle parking for districts in Vienna, Austria
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_capacity(parking):
    return parking.groupby('bezirk')['anzahl'].sum()
    
def get_count(parking):
    return parking.groupby('bezirk')['anzahl'].count()

def replace_nan_with_0(series):
    print()

def plot_first_try():
    # todo balken nebeneinander...
    # pd.concat([x, x], axis=1).plot(kind='bar')
    
    get_count(parking_data_small).plot(kind='bar', stacked=True, title='Radabstellanlagen pro Bezirk')
    get_count(parking_data_big).plot(kind='bar')
    plt.figure()
    
    get_capacity(parking_data_small).plot(kind='bar', stacked=True, title='Gesamtkapazität der Radabstellanlagen pro Bezirk')
    get_capacity(parking_data_big).plot(kind='bar')
    #population.plot(kind='bar')
    plt.figure()
    
def plot(summary):
    fig, axes = plt.subplots(nrows=len(summary.columns), ncols=1)
    for i, c in enumerate(summary.columns):
        summary[c].plot(kind='bar', ax=axes[i], figsize=(7, 30), title=c)
    fig.subplots_adjust(hspace=0.3)
    fig.savefig('vienna_bicycleparking_analysed.png')

def print_biggest_stations():
    sorted = parking_data.sort(columns='anzahl', ascending=False)
    print(sorted.head(n=50))




# read data
population_data = pd.read_csv('vienna_population.csv', delimiter=',', quotechar='"', skipinitialspace=True)
population = population_data['2014']
population = population[1:]
population.name = 'population'

parking_data = pd.read_csv('vienna_bicycleparking.csv', delimiter=',', quotechar='"', skipinitialspace=True)
parking_data_small = parking_data[parking_data['anzahl']<50]
parking_data_big = parking_data[parking_data['anzahl']>=50]

# calculate capacity per district
parking_all_capacity = get_capacity(parking_data)
parking_all_capacity.name = 'total_capacity'
parking_big_capacity = get_capacity(parking_data_big)   
parking_big_capacity.name = 'big_station_capacity'

# put result in dataframe, calculate capacity per person
summary = pd.concat([population, parking_all_capacity, parking_big_capacity], axis=1)
summary.index.name = 'district'
summary['total_capacity_per_1000_inhabitants'] = np.round(1000*summary['total_capacity']/summary['population'], 0)
summary['big_station_capacity_per_1000_inhabitants'] = np.round(1000*summary['big_station_capacity']/summary['population'])
summary['percent_of_total_capacity'] = np.round(100*summary['total_capacity']/summary['total_capacity'].sum(), 2)


# export result (NaN=0)
summary.to_csv('vienna_bicycleparking_analysed.csv', na_rep='0', sep=',', encoding='utf-8')

print(summary)
plot(summary)
