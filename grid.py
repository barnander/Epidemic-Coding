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
import pandas as pd

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
            elif letter=='H':
                intgrid[counter1,counter2]=4
            else:
                intgrid[counter1,counter2]=0
    return intgrid


def animate_func(i,grid_list,first_grid):
    fig = plt.figure(2)
    cols=len(first_grid[0])
    rows=len(first_grid[1])
    brg=colors.ListedColormap(['blue','red','green','black','cyan'])
    bounds=[0,1,2,3,4,5]
    norm = colors.BoundaryNorm(bounds, brg.N)
    im = plt.imshow(first_grid,cmap=brg,aspect='auto',interpolation='nearest',extent=[0.5, 0.5+cols, 0.5, 0.5+rows], norm=norm)
    plt.axis('off')
    im.set_array(grid_list[i])
    return [im]

def grid_animation(grid_list):
    fig = plt.figure(2)
    anim = animation.FuncAnimation(fig, animate_func, frames = len(grid_list),fargs=(grid_list,grid_list[0],), interval = 600,repeat=False)
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

def main(n, inf_rate, inf_range, rec_rate, death_rate,hosp_rate,percent_hosp_capacity,hosp_rec_rate, duration):
    keys = [f'[{i}, {j}]' for i in range(n) for j in range(n)]
    values = [-1 for i in range(n**2)]
    inf_track = {key:value for (key,value) in zip(keys,values)}
    grid = original_grid(n)
    # print(grid)
    grid_list=[integer_grid(grid)]
    hosp_capacity=percent_hosp_capacity*(n**2)
    hosp_overwhelm_days=0
    hod=0
    for i in range(duration):
        
        infected_list = grid_search(grid, 'I')  
        hosp_list = grid_search(grid, 'H')
        if len(hosp_list)>hosp_capacity:
            hosp_overwhelm_days+=1
            print('Hospitals were Overwhelmed on day ',i, ' with ',len(hosp_list), 'requiring hospitalisation')
            
        for infected_pos in infected_list:
            
        #     if inf_track[str(infected_pos)] == -1:
        #         inf_time = random.randint(inf_min, inf_max)
        #         inf_track[str(infected_pos)] = inf_time~
            
        #     elif inf_track[str(infected_pos)] == 0:
        #         grid[infected_pos[0],infected_pos[1]] = 'R' 
        #         infected_list.remove(infected_pos)
        #     else:
        #         inf_track[str(infected_pos)] -= 1
        # print(inf_track)
            if prob(rec_rate):
                grid[infected_pos[0],infected_pos[1]] = 'R' 
            elif prob(hosp_rate):
                grid[infected_pos[0],infected_pos[1]] = 'H' 
            # elif prob(death_rate):
            #     grid[infected_pos[0],infected_pos[1]] = 'D' 
        for counter,hosp_pos in enumerate(hosp_list):
            if (counter+1)>(hosp_capacity):
                # print(counter, 'counter')
                # print(hops)
                # print('Hospitals were overwhelmed on day',i, 'with ', len(hosp_list), 'requiring hospitalisation')
                grid[hosp_pos[0],hosp_pos[1]] = 'D' 
                hod+=1
            else:
                if prob(death_rate):
                    grid[hosp_pos[0],hosp_pos[1]] = 'D'
                elif prob(hosp_rec_rate):
                    grid[hosp_pos[0],hosp_pos[1]] = 'R'
                    
                
                
        infected_list = grid_search(grid, 'I')
        grid = infect(grid, inf_rate, inf_range, infected_list)
        numbergrid=integer_grid(grid)
        grid_list.append(numbergrid)
        # print(grid)
        # print(grid)
    print('Hospitals were overwhelmed for a total of', hosp_overwhelm_days,'days causing', hod, 'people to die because of lack of hospitalisation')
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
    grid_count_hos_list=grid_count(4,grid_list)
    return grid_count_inf_list,grid_count_sus_list, grid_count_rec_list, grid_count_dea_list,grid_count_hos_list

def grid_count(state,grid_list):
    grid_count_list=[]
    for grid in grid_list:
        grid_count_state=len(grid[grid==state])
        grid_count_list.append(grid_count_state)
    return grid_count_list

def plot_show(list_of_infections):
    x=np.arange(len(list_of_infections[0]))
    y=np.array(list_of_infections[0])
    z=np.array(list_of_infections[1])
    a=np.array(list_of_infections[2])
    b=np.array(list_of_infections[3])
    c=np.array(list_of_infections[4])
    fig, (axs1,axs2) =plt.subplots(1,2,figsize = (15,5),num=1)
    peak_inf=max(list_of_infections[0])
    index=list_of_infections[0].index(peak_inf)
    print('The peak number of infections was', peak_inf, 'and occured on day', index)
    axs2=plt.xlabel('Day(D)')
    axs2=plt.ylabel('Number of People')
    axs2=plt.plot(x,y,label='Number of Infected',color='r') 
    axs2=plt.plot(x,z,label='Number of Susceptible',color='b')
    axs2=plt.plot(x,a,label='Number of Recovered',color='g')
    axs2=plt.plot(x,b, label='Number of Dead',color='k')
    axs2=plt.plot(x,c, label='Number of Hospitalised', color='c')
    axs2=plt.plot()
    axs2=plt.title("Population Statistics from Simulation")
    axs2=plt.legend()
    axs1.axis('off')
    stats=np.zeros((5,4),dtype=int)
    for counter,i in enumerate(list_of_infections):
        stats[(counter),0]=i[int((len(i)-1)/4)]
        stats[(counter),1]=i[int((len(i)-1)/2)]
        stats[(counter),2]=i[int((len(i)-1)*(3/4))]
        stats[(counter),3]=i[int(len(i)-1)]
    df = pd.DataFrame(stats, 
                      columns=['Day '+ str(int((len(list_of_infections[0])-1)/4)),'Day '+ str(int((len(list_of_infections[0])-1)/2)),'Day '+ str(int((len(list_of_infections[0])-1)*(3/4))),'Day '+ str((len(list_of_infections[0])-1))], 
                      index = [ 'Number of Infected', 'Number of Susceptible', 'Number of Recovered', 'Number of Dead','Number of Hospitalised'])
    table = axs1.table(cellText=df.values, cellLoc='center',colLabels = df.columns, rowLabels = df.index,  loc='center',colWidths=[0.15,0.15,0.15,0.15])
    
    
    return plt.show()


grid_list=main(50,0.5,2,0.2,0.005,0.05,0.1,0.05,50)
anim=grid_animation(grid_list)
plot_show(grid_count_list(grid_list))

