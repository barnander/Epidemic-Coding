# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 13:11:22 2022

@author: Basil
"""

import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation
import matplotlib.colors as colors

def original_grid(n):
    row = ["S" for i in range(n)]
    grid = np.array([row for i in range(n)])
    i = random.randint(0,n-1)
    j = random.randint(0, n-1)
    grid[i,j] = 'I'
    intgrid=np.zeros((n,n),dtype=int)
    return grid#,intgrid
def in_range(square, radius,allowed_coords):
    affected_squares = []
    x = square[0]
    y = square[1]
    affected_squares = [[x+i,y+j] for i in range(-radius,radius+1) for j in range(-radius,radius+1)]
    affected_squares = [i for i in affected_squares if allowed_coords.count(i)]
    affected_squares.remove(square)
    return affected_squares

def grid_search(grid, letter):
    n = len(grid)
    pos_letter = []
    for i in range(n):
        for j in range(n):
            if grid[i,j] == letter:
                pos_letter.append([i,j])
    return pos_letter
    


def integer_grid(grid):
    n = len(grid)
    intgrid=np.zeros((n,n),dtype=int)  
    for counter1,row in enumerate(grid):
        for counter2,letter in enumerate(row):
           
            if letter=='I':
                intgrid[counter1,counter2]=1
            elif letter=='R':
                intgrid[counter1,counter2]=2
            else:
                intgrid[counter1,counter2]=0
    return intgrid

def grid_animation(grid_list):
    fig = plt.figure( figsize=(8,8) )
    first_grid = grid_list[0]
    cols=len(first_grid[0])
    rows=len(first_grid[1])
    brg=colors.ListedColormap(['blue','red','green'])
    bounds=[0,1,2,3]
    norm = colors.BoundaryNorm(bounds, brg.N)
    im = plt.imshow(first_grid,cmap=brg,aspect='auto',interpolation='nearest',extent=[0.5, 0.5+cols, 0.5, 0.5+rows], norm=norm)
    plt.axis('off')
    def animate_func(i):
        im.set_array(grid_list[i])
        return [im]
    anim = animation.FuncAnimation(fig, animate_func, frames = len(grid_list), interval = 600,repeat=False)
    return anim
    
def prob(inf_rate):
   limit = int(1000 * inf_rate)
   number = random.randint(1, 1000) 
   if number > limit :
       return False
   else:
       return True
    
def infect(grid, inf_rate, inf_range, infected_list):
    n = len(grid)
    allowed_coords = [[i,j] for i in range(n) for j in range(n)]
    for infected in infected_list:
        contacts = in_range(infected, inf_range, allowed_coords)
        contacts = [i for i in contacts if grid[i[0],i[1]] != 'R']
        for i in contacts:
            if prob(inf_rate):
                grid[i[0],i[1]] = 'I'
    return grid  

def main(n, inf_rate, inf_range, inf_min, inf_max):
    keys = [f'[{i}, {j}]' for i in range(n) for j in range(n)]
    values = [-1 for i in range(n**2)]
    inf_track = {key:value for (key,value) in zip(keys,values)}
    grid = original_grid(n)
    print(grid)
    grid_list=[]
    for i in range(10):
        
        infected_list = grid_search(grid, 'I')        
        for infected_pos in infected_list:
            
            if inf_track[str(infected_pos)] == -1:
                inf_time = random.randint(inf_min, inf_max)
                inf_track[str(infected_pos)] = inf_time
            
            elif inf_track[str(infected_pos)] == 0:
                grid[infected_pos[0],infected_pos[1]] = 'R' 
                infected_list.remove(infected_pos)
            else:
                inf_track[str(infected_pos)] -= 1
        print(inf_track)
        numbergrid=integer_grid(grid)
        grid_list.append(numbergrid)
        infected_list = grid_search(grid, 'I')
        grid = infect(grid, inf_rate, inf_range, infected_list)
        numbergrid=integer_grid(grid)
        print(grid)
    return grid_list
                



#testing that it works
# main(5,0.5,2,3,5)
anim=grid_animation(main(5,0.5,2,3,5))




