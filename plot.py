#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 13:05:33 2022

@author: rr21338
"""
import grid as gr
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
               



print(gr.original_grid(10))