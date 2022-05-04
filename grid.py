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
import argparse

parser=argparse.ArgumentParser(description='How each value changes the sim')
parser.add_argument('--Size',metavar='N',type=int,default=50,
                        help='Use a grid of size N x N')
parser.add_argument('--Start',metavar='N',type=int,default=1,
                    help='The number of initial infected at the start of the sim ')
parser.add_argument('--Inf',metavar='p',type=float,default=0.3,
                        help='Chance of infection each day when in range of an infected individual ')
parser.add_argument('--Range',metavar='N',type=int,default=2,
                        help='How far the virus can jump from person to person within the grid')
parser.add_argument('--Rec',metavar='p',type=float,default=0.3,
                        help='Chance to recover each day you are infected ')
parser.add_argument('--Death',metavar='p',type=float,default=0.005,
                        help='Chance of an infetced individual to die each day')
parser.add_argument('--Hosprate',metavar='p',type=float,default=0.1,
                    help='Chance for an infected individual to be hospitalised')
parser.add_argument('--Hospcap',metavar='%',type=float,default=0.3,
                    help='percentage of total population that can be hospitalised before capacity is reached')
parser.add_argument('--Demo',metavar='d',default='S',choices=['S','C','E'],
                    help='Choose what population demographic is simulated, stationary"s", constrictive"c", expansive"e')
parser.add_argument('--Vac',metavar='p',type=float,default=0.5,
                    help='The total proportion of the population that recieves a vaccine')
parser.add_argument('--Proc',metavar='p',type=float,default=1.5,
                    help='Set the factor at which the chance of infection is divided by after recieving the vaccine, must be greater than 1')
parser.add_argument('--Immune',metavar='p',type=int,default=5,
                    help='the ammount of days that a person remains immune from infection after recovery, after thsi period the become susceptible again')
parser.add_argument('--Duration',metavar='T',type=int,default=50,
                    help='set the duration of the sim to time T')


args=parser.parse_args()

import pandas as pd





class Individual:
    def __init__(self, inf_status, age, vacc_status):
        self.inf_status = inf_status
        self.age = age
        self.vacc_status = vacc_status

        
    def __str__(self):
        return self.inf_status
    
    def __repr__(self):
        return self.inf_status[0]
        
def original_grid(n, pop_structure, vacc_percentage, inf_start):
    """
    

    Parameters
    ----------
    n : Integer
    length of square population grid
    pop_structure : String
        describes the distribution of age within the population
    vacc_percentage : Float
        percent of the population which is vaccinated

    Returns
    -------
    grid : Nd array
        grid including  the desired amount of infected individuals, age distribution and vaccination percentage

    """
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
    for x in range(inf_start):
        i = random.randint(0,n-1)
        j = random.randint(0, n-1)
        grid[i,j].inf_status = 'I0'
    
    return grid


def in_range(square, radius,allowed_coords):
    """
    

    Parameters
    ----------
    square : List
        coordinates of (infected) Individual in grid
    radius : Integer
        distance the virus can jump in the grid
    allowed_coords : List
        list of all the coordinates of the grid

    Returns
    -------
    affected_squares : List
        list of the coordinates of all the squares in the grid within the radius of the infected square

    """
    affected_squares = []
    x = square[0]
    y = square[1]
    affected_squares = [[x+i,y+j] for i in range(-radius,radius+1) for j in range(-radius,radius+1)]
    affected_squares = [i for i in affected_squares if allowed_coords.count(i)]
    return affected_squares

def grid_search(grid, letter):
    """
    

    Parameters
    ----------
    grid : Nd array
        grid including all the individuals of the population
    letter : String
        infection status desired ("S","I","H", or "R")

    Returns
    -------
    pos_letter : List
        list of the coordinates of individuals that are the desired infected state

    """
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
    """
    

    Parameters
    ----------
    inf_rate : Float
        chance of infection from contact with infected person

    Returns
    -------
    bool
        true is returned at a rate equivalent to the infection rate

    """

    limit = int(10000*inf_rate)
    number = random.randint(1, 10000) 
    if number > limit :
       return False
    else:
       return True
    
    
def infect(susceptible, grid, inf_rate, vacc_protection):
    """
    

    Parameters
    ----------
    susceptible : List
        Coordinates of people in contact with infected people ()
    grid : TYPE
        DESCRIPTION.
    inf_rate : TYPE
        DESCRIPTION.
    vacc_protection : TYPE
        DESCRIPTION.

    Returns
    -------
    grid : TYPE
        DESCRIPTION.

    """
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


def main(n,inf_start, inf_rate, inf_range, rec_rate, death_rate, hosp_rate,percent_hosp_capacity,pop_structure,vacc_percentage, protection, immunity, duration):
    """
    

    Parameters
    ----------
    n : Integer
        side length of square grid
    inf_start : Integer
        Number of infected individuals on the first day
    inf_rate : Float
        Chance that a susceptible person gets infected 
    inf_range : Integer
        distance from infected person someone can get infected from
    rec_rate : Float
        DESCRIPTION.
    death_rate : TYPE
        DESCRIPTION.
    hosp_rate : TYPE
        DESCRIPTION.
    percent_hosp_capacity : TYPE
        DESCRIPTION.
    pop_structure : TYPE
        DESCRIPTION.
    vacc_percentage : TYPE
        DESCRIPTION.
    protection : TYPE
        DESCRIPTION.
    immunity : TYPE
        DESCRIPTION.
    duration : TYPE
        DESCRIPTION.

    Returns
    -------
    grid_list : TYPE
        DESCRIPTION.

    """
    grid = original_grid(n,pop_structure, vacc_percentage,inf_start)    
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
                        if len(grid_search(grid, "H")) >= hosp_capacity:
                            if prob(2*death_rates[grid[j,i].age]):
                                grid[j,i].inf_status = "D"
                                hod += 1
                                ho_death = True
                        else:
                            grid = age_change([j,i], grid, hosp_rates, "H")
                            grid = age_change([j,i], grid, rec_rates, "R0")
                    else:
                        person.inf_status = "I" + str(int(person.inf_status[1]) + 1)
                elif person.inf_status[0] == "H":
                    grid = age_change([j,i], grid, death_rates, "D")
                    grid = age_change([j,i], grid, rec_rates, "R0")
                
                
                elif person.inf_status[0] == "R":
                    if int(person.inf_status[1]) > immunity:
                        person.inf_status = "S"
                    
                    else:
                        person.inf_status = "R" + str(int(person.inf_status[1]) + 1)
                    
                   
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



if __name__ == "__main__":
    n = args.Size
    inf_start=args.Start
    inf_rate = args.Inf
    inf_range = args.Range
    rec_rate = args.Rec
    death_rate = args.Death
    hosp_rate = args.Hosprate
    percent_hosp_capacity = args.Hospcap
    pop_structure= args.Demo
    vacc_percentage = args.Vac
    protection = args.Proc
    immunity=args.Immune
    duration = args.Duration
    grid_list=main(n, inf_start,inf_rate,inf_range, rec_rate, death_rate, hosp_rate,percent_hosp_capacity,pop_structure,vacc_percentage, protection,immunity, duration)
    anim=grid_animation(grid_list)
    plot_show(grid_count_list(grid_list))



#grid_list = main(30,2, 0.3, 2, 0.2, 0.05, 0.15, 0.05, "E",0,1.5, 50)

anim=grid_animation(grid_list)
plot_show(grid_count_list(grid_list))
