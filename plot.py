#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 13:05:33 2022

@author: rr21338
"""

import numpy as np
import matplotlib.pyplot as plt

def grid_count(grid,grid_count_list,susceptible_list,state,starting_population):
    grid_count=len(grid[grid==state])
    if state=='I':
        susceptible=starting_population-grid_count
    grid_count_list.append(grid_count)
    susceptible_list.append(susceptible)
    return grid_count_list,susceptible_list

def plot_show(list_of_infections):
    x=np.arange(len(list_of_infections[0]))
    y=np.array(list_of_infections[0])
    z=np.array(list_of_infections[1])
    plt.xlabel('Day(D)')
    plt.ylabel('Number of People')
    plt.plot(x,y,label='Number of Infected') 
    plt.plot(x,z,label='Number of Susceptible')
    plt.title("Matplotlib Plot NumPy Array")
    plt.legend()
    return plt.show()
               
def original_grid(n):
    row = ["S" for i in range(n)]
    grid = np.array([row for i in range(n)])
    return grid
starting_population=100000
grid=original_grid(100)
grid[2,3]='I'
previous_infected=[20*np.exp(x) for x in range(0,9)]
previous_susceptible=[100000-x for x in previous_infected]
thing=grid_count(grid,previous_infected,previous_susceptible,'I',starting_population)
# print(thing[0])
plot_show(thing)

