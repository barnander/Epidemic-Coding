#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 13:05:33 2022

@author: rr21338
"""

import numpy as np
import matplotlib.pyplot as plt

def grid_count(grid,grid_count_list,state):
    grid_count=len(grid[grid==state])
    grid_count_list.append(grid_count)
    return grid_count_list

def plot_show(list_of_infections):
    x=np.arange(len(list_of_infections))
    y=np.array(list_of_infections)
    plt.xlabel('Days(D)')
    plt.ylabel('Number of infected (S)')
    plt.plot(x,y,label='Number Infected') 
    plt.title("Matplotlib Plot NumPy Array")
    plt.legend()
    return plt.show()
               
def original_grid(n):
    row = ["S" for i in range(n)]
    grid = np.array([row for i in range(n)])
    return grid
grid=original_grid(5)
grid[2,3]='I'
thing=grid_count(grid,[20,14,8,6],'I')
plot_show(thing)

