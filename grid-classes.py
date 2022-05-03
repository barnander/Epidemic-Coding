#!usr/bin/env python
"""
Created on Tue Mar 22 13:11:22 2022
@author: Basil
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation
import matplotlib.colors as colors
# <<<<<<< HEAD
# import argparse

# def init(*args):
#     parser=argparse.ArgumentParser(description='create sim animation')
#     parser.add_argument('--size,',metavar='N',type=int,default=25,
#                        help='Use a grid of size N x N')
#     parser.add_argument('--Duration',metavar='T',type=int,default=50,
#                         help='Set the lenght of time simutlated')
#     parser.add_argument('--Rec',metavar='p',type=float,default=0.1,
#                         help='Chance of recovery per day')
#     parser.add_argument('--Inf',metavar='p',type=float,default=0.2,
#                         help='Chance for be infected when in range')
#     parser.add_argument('--Spread',metavar='D',type=int,default=2,
#                         help='infection can jump a distance of D away from a case')
#     parser.add_argument('--plot',action='store_true',
#                         help='provides a plot instead of animation')
#     parser.add_argument('--file',metavar='n',type=str,default=None,
#                         help='give the name to a file to save instead of display')
#     args=parser.parse_args(args)
#     anim=grid_animation(main(args.size,args.Inf,args.Spread,args.Rec,args.Duration))
    
    
    
# =======
import pandas as pd

# >>>>>>> 8833a6aa952a66e6ae755288be0a0a5a05e6a475

class Individual:
    def __init__(self, inf_status, age, vacc_status):
        self.inf_status = inf_status
        self.age = age
        self.vacc_status = vacc_status

        
    def __str__(self):
        return self.inf_status
    
    def __repr__(self):
        return self.inf_status[0]
        
def original_grid(n, pop_structure, vacc_percentage):
    ages = ['C','Y','M','O']
    vacc_statuses = [0, 1]
    if pop_structure == "E":
        grid = np.array([[Individual("S", random.choices(ages, [0.4,0.3,0.2,0.1]), random.choices(vacc_statuses, [1-vacc_percentage, vacc_percentage])[0]) for i in range(n)] for i in range(n)])
    elif pop_structure == "C":
        grid = np.array([[Individual("S", random.choices(ages, [0.1,0.2,0.3,0.4]), random.choices(vacc_statuses, [1-vacc_percentage, vacc_percentage])[0]) for i in range(n)] for i in range(n)])
    
    elif pop_structure == "S":
        grid = np.array([[Individual("S", random.choice(ages), random.choices(vacc_statuses, [1-vacc_percentage, vacc_percentage])[0]) for i in range(n)] for i in range(n)])
    for row in grid:
        for person in row:
            person.age = person.age[0]
    i = random.randint(0,n-1)
    j = random.randint(0, n-1)
    grid[i,j].inf_status = 'I0'
    
    return grid


def in_range(square, radius,allowed_coords):
    affected_squares = []
    x = square[0]
    y = square[1]
    affected_squares = [[x+i,y+j] for i in range(-radius,radius+1) for j in range(-radius,radius+1)]
    affected_squares = [i for i in affected_squares if allowed_coords.count(i)]
    # affected_squares.remove(square)
    return affected_squares

def grid_search(grid, letter):
    n = len(grid)
    pos_letter = []
    for i in range(n):
        for j in range(n):
            if grid[i,j].inf_status[0] == letter:
                pos_letter.append([i,j])
    return pos_letter
    


def integer_grid(grid):
    n = len(grid)
    intgrid=np.zeros((n,n),dtype=int)  
    for counter1,row in enumerate(grid):
        counter2 = 0
        for i in row: 
            if i.inf_status[0] =='I':
                intgrid[counter1,counter2]=1
            elif i.inf_status[0] =='R':
                intgrid[counter1,counter2]=2
            elif i.inf_status[0] == 'D':
                intgrid[counter1,counter2] = 3
            elif i.inf_status[0] =='H':
                intgrid[counter1,counter2]=4
            else:
                intgrid[counter1,counter2]=0
            counter2 += 1
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
    
    
def infect(susceptible, grid, inf_rate, vacc_protection):
    ages = ["C", "Y", "M", "O"]
    inf_rates = [inf_rate * 2**i/4 for i in range(0,4)]   
    inf_rates = {key:value for (key,value) in zip(ages, inf_rates)}
    for sus in susceptible:
        age = grid[sus[0],sus[1]].age
        vacc_status = grid[sus[0],sus[1]].vacc_status
        status = grid[sus[0],sus[1]].inf_status
        if status == "S":
            if  vacc_status:
                if prob(inf_rates[age[0]]/vacc_protection):
                    grid[sus[0],sus[1]].inf_status = "I0"
            else:
                if prob(inf_rates[age[0]]):
                    grid[sus[0],sus[1]].inf_status = "I0"
    return grid

def age_change(coord, grid, change_rates, resultant_change):
    age = grid[coord[0],coord[1]].age
    if prob(change_rates[age[0]]):
        grid[coord[0],coord[1]].inf_status = resultant_change
    return grid


def main(n, inf_rate, inf_range, rec_rate, death_rate, hosp_rate,percent_hosp_capacity,pop_structure, protection, duration):
    grid = original_grid(n,pop_structure, 0)    
    print(grid)
    print(grid[0][0].age)
    grid_list=[integer_grid(grid)]
    hosp_capacity=percent_hosp_capacity*(n**2)
    hosp_overwhelm_days=0
    hod=0
    allowed_coords = [[i,j] for i in range(n) for j in range(n)]
    ages = ["C", "Y", "M", "O"]
    hosp_rates = [hosp_rate * 2**i/4 for i in range(0,4)]
    death_rates = [death_rate * 2**i/4 for i in range(0,4)]
    rec_rates = [rec_rate * 4/(2*i) for i in range(1,5)]
    rec_rates = {key:value for (key,value) in zip(ages, rec_rates)}
    death_rates = {key:value for (key,value) in zip(ages, death_rates)}
    hosp_rates = {key:value for (key,value) in zip(ages, hosp_rates)}
    for time in range(duration):
        ho_death = False
        j=0
        susceptible = []
        for row in grid:
            i = 0
            for person in row:
                if person.inf_status[0] == "I":
                    affected = in_range([j,i], inf_range, allowed_coords)
                    #print(affected)
                    for sus in affected:
                        susceptible.append(sus)
                    if int(person.inf_status[1]) > 2:
                        print(len(grid_search(grid, "H")))
                        if len(grid_search(grid, "H")) >= hosp_capacity:
                            
                            
                            grid[j,i].inf_status = "D"
                            hod += 1
                            ho_death = True
                        else:
                            grid = age_change([j,i], grid, hosp_rates, "H")
                            grid = age_change([j,i], grid, rec_rates, "R")
                    else:
                        person.inf_status = "I" + str(int(person.inf_status[1]) + 1)
                elif person.inf_status[0] == "H":
                    grid = age_change([j,i], grid, death_rates, "D")
                    grid = age_change([j,i], grid, rec_rates, "R")
                   
                i += 1
            j += 1
        if ho_death:
            hosp_overwhelm_days +=1
        grid = infect(susceptible,grid, inf_rate, protection )
        grid_list.append(integer_grid(grid))
        
    print('Hospitals were overwhelmed for a total of', hosp_overwhelm_days,'days causing', hod, 'people to die because of lack of hospitalisation')
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
    list1=["A peak of " + str(peak_inf) +" infections", "occurred on day " + str(index)]
    joined="\n".join(list1)
    axs2=plt.annotate(joined,(index,peak_inf),(-1,(peak_inf + list_of_infections[1][1]/10)),arrowprops=dict(arrowstyle='->',relpos=(0.5,0.)),bbox=dict(boxstyle="round,pad=0.3", fc="w", ec="r", lw=1))
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



#if __name__ == "__main__":
    # n = int(input("Side length for square grid: "))
    # inf_rate = float(input('Infection Rate: '))
    # inf_range = int((input('Infection Range: ')))
    # rec_rate = float(input("Recovery Rate: "))
    # death_rate = float(input('Death Rate: '))
    # hosp_rate = float(input("Hospital Rate of Infected: "))
    # percent_hosp_capacity = float(input("Hospital Capacity as a percentage of total population: "))
    # hosp_rec_rate= float(input("Recovery rate of infected patients in hospital: "))
    # pop_structure= input("Population demographic ('stationary', 'constrictive' or 'expansive'): ")
    # duration= int(input("Time of simulation: "))
    # grid_list=main(n, inf_rate, inf_range, rec_rate, death_rate,hosp_rate,percent_hosp_capacity,hosp_rec_rate,pop_structure, duration)
    # anim=grid_animation(grid_list)
    # plot_show(grid_count_list(grid_list))

grid_list = main(30, 0.3, 2, 0.2, 0.05, 0.03, 0.1, "E",1.5, 50)
anim=grid_animation(grid_list)
plot_show(grid_count_list(grid_list))
