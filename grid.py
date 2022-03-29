# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 13:11:22 2022

@author: Basil
"""

import numpy as np
import matplotlib.pyplot as plt
import random

def original_grid(n):
    row = ["S" for i in range(n)]
    grid = np.array([row for i in range(n)])
    i = random.randint(0,n-1)
    j = random.randint(0, n-1)
    grid[i,j] = 'I'
    return grid

def in_range(square, radius):
    affected_squares = []
    x = square[0]
    y = square[1]
    affected_squares = [[x+i,y+j] for i in range(-radius,radius+1) for j in range(-radius,radius+1)]
    affected_squares.remove(square)
    return affected_squares

def grid_search(grid, letter):
    n = len(grid)
    pos_letter = []
    for i in range(n):
        for j in range(n):
            if grid[i,j] == letter:
                pos_letter.append(f'[{i},{j}]')
    return pos_letter
      
        

def main(n):
    keys = [f'[{i},{j}]' for i in range(n) for j in range(n)]
    values = [-1 for i in range(n^2)]
    inf_track = {key:value for (key,value) in zip(keys,values)}
    grid = original_grid(n)
    
    
