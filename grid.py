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
            elif letter == 'D':
                intgrid[counter1,counter2] = 3
            else:
                intgrid[counter1,counter2]=0
    return intgrid

def grid_animation(grid_list):
    fig = plt.figure(2)
    first_grid = grid_list[0]
    cols=len(first_grid[0])
    rows=len(first_grid[1])
    brg=colors.ListedColormap(['blue','red','green','black'])
    bounds=[0,1,2,3,4]
    norm = colors.BoundaryNorm(bounds, brg.N)
    im = plt.imshow(first_grid,cmap=brg,aspect='auto',interpolation='nearest',extent=[0.5, 0.5+cols, 0.5, 0.5+rows], norm=norm)
    plt.axis('off')
    # plt.gca().cla()
    #plt.gca().cla()

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
        contacts = [i for i in contacts if grid[i[0],i[1]] == 'S']
        for i in contacts:
            if prob(inf_rate):
                grid[i[0],i[1]] = 'I'
    return grid  

def main(n, inf_rate, inf_range, rec_rate, death_rate, duration):
    keys = [f'[{i}, {j}]' for i in range(n) for j in range(n)]
    values = [-1 for i in range(n**2)]
    inf_track = {key:value for (key,value) in zip(keys,values)}
    grid = original_grid(n)
    # print(grid)
    grid_list=[integer_grid(grid)]
    for i in range(duration):
        
        infected_list = grid_search(grid, 'I')        
        for infected_pos in infected_list:
            
        #     if inf_track[str(infected_pos)] == -1:
        #         inf_time = random.randint(inf_min, inf_max)
        #         inf_track[str(infected_pos)] = inf_time
            
        #     elif inf_track[str(infected_pos)] == 0:
        #         grid[infected_pos[0],infected_pos[1]] = 'R' 
        #         infected_list.remove(infected_pos)
        #     else:
        #         inf_track[str(infected_pos)] -= 1
        # print(inf_track)
            if prob(rec_rate):
                grid[infected_pos[0],infected_pos[1]] = 'R' 
            elif prob(death_rate):
                grid[infected_pos[0],infected_pos[1]] = 'D' 
        
        infected_list = grid_search(grid, 'I')
        grid = infect(grid, inf_rate, inf_range, infected_list)
        numbergrid=integer_grid(grid)
        grid_list.append(numbergrid)
        # print(grid)
        print(grid)
    
    inf_data=[]
    rec_data=[]
    suc_data=[]
    for grid in grid_list:
        inf_data.append(len(grid_search(grid, 'I')))
        rec_data.append(len(grid_search(grid, 'R')))
        suc_data.append(len(grid_search(grid, 'S')))
    return grid_list

def grid_count_list(grid_list):
    grid_count_inf_list=grid_count(1,grid_list)
    grid_count_sus_list=grid_count(0,grid_list)
    grid_count_rec_list=grid_count(2,grid_list)
    grid_count_dea_list=grid_count(3,grid_list)
    return grid_count_inf_list,grid_count_sus_list, grid_count_rec_list, grid_count_dea_list

def grid_count(state,grid_list):
    grid_count_list=[]
    for grid in grid_list:
        grid_count_state=len(grid[grid==state])
        grid_count_list.append(grid_count_state)
    return grid_count_list

def plot_show(list_of_infections):
    print(list_of_infections)
    x=np.arange(len(list_of_infections[0]))
    y=np.array(list_of_infections[0])
    z=np.array(list_of_infections[1])
    a=np.array(list_of_infections[2])
    b=np.array(list_of_infections[3])
    line_graph=plt.figure(1)
    plt.gca().cla()
    plt.xlabel('Day(D)')
    plt.ylabel('Number of People')
    plt.plot(x,y,label='Number of Infected') 
    plt.plot(x,z,label='Number of Susceptible')
    plt.plot(x,a,label='Number of Recovered')
    plt.plot(x,b, label='Number of Dead')
    plt.plot()
    plt.title("Population Statistics from Simulation")
    plt.legend()
    return plt.show()



grid_list=main(30,0.5,2,0.2,0.05, 50)
anim=grid_animation(grid_list)
plot_show(grid_count_list(grid_list))
# subplot(plot_show(grid_count_list(grid_list)),anim=grid_animation(grid_list))


