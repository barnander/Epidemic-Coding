# -*- coding: utf-8 -*-
"""
Created on Thu May  5 14:05:16 2022

@author: Basil
"""
import numpy as np
import random
from animation import integer_grid



class Individual:
    def __init__(self, inf_status, age, vacc_status):
        self.inf_status = inf_status
        self.age = age
        self.vacc_status = vacc_status

        
    def __str__(self):
        return self.inf_status
    
    def __repr__(self):
        return self.inf_status[0]
    

def original_grid(n, pop_structure, vacc_frac, inf_start):
    """
    Produces an original grid according to the number of intitial infections

    Parameters
    ----------
    n : Integer
    length of square population grid
    pop_structure : String
        describes the distribution of age within the population
    vacc_frac : Float
        fraction of the population which is vaccinated

    Returns
    -------
    grid : Nd array
        grid including  the desired amount of infected individuals, age distribution and vaccination percentage

    """
    ages = ['C','Y','M','O']
    vacc_statuses = [0, 1]
    if pop_structure == "E":
        grid = np.array([[Individual("S", random.choices(ages, [0.4,0.3,0.2,0.1]), random.choices(vacc_statuses, [1-vacc_frac, vacc_frac])[0]) for i in range(n)] for i in range(n)])
    elif pop_structure == "C":
        grid = np.array([[Individual("S", random.choices(ages, [0.1,0.2,0.3,0.4]), random.choices(vacc_statuses, [1-vacc_frac, vacc_frac])[0]) for i in range(n)] for i in range(n)])
    
    elif pop_structure == "S":
        grid = np.array([[Individual("S", random.choice(ages), random.choices(vacc_statuses, [1-vacc_frac, vacc_frac])[0]) for i in range(n)] for i in range(n)])
    for row in grid:
        for person in row:
            person.age = person.age[0]
    for initial_inf in range(inf_start):
        i = random.randint(0,n-1)
        j = random.randint(0, n-1)
        grid[i,j].inf_status = 'I0'
    
    return grid


def in_range(coords, radius,allowed_coords):
    """
    Goes through all of the squares in range of the infected individual, finds 
    those who are susceptible and returns a list of them

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
    x = coords[0]
    y = coords[1]
    affected_squares = [[x+x_range,y+y_range] for x_range in range(-radius,radius+1) for y_range in range(-radius,radius+1)]
    affected_squares = [square for square in affected_squares if allowed_coords.count(square)]
    return affected_squares

def grid_search(grid, letter):
    """
    Searches the grid on a given day for the desired infection status (eg. S, I,
    R, D, H)
    

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
    side_len = len(grid)
    pos_letter = []
    for i in range(side_len):
        for j in range(side_len):
            if grid[i,j].inf_status[0] == letter:
                pos_letter.append([i,j])
    return pos_letter

def prob(inf_rate):
    """
    Performs probability operations taking a float as an imput value and returning
    a True or False value based on whether the chosen condition has been satisfied
    

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
    
    
def infect(susceptible, grid, inf_rate, protection):
    """
    Iterates through the list of susceptible people in range and applies the 
    'inf_rate' probability to determine if they become infected

    Parameters
    ----------
    susceptible : List
        Coordinates of people in contact with infected people ()
    grid : Nd array
        Grid including all the individuals of the population
    inf_rate : float
        
    vacc_protection : float
        the factor that the infection and hospital rate is divided by given the 
        individual has been vaccinated

    Returns
    -------
    grid : Nd array
        grid including all the individuals of the population
        

    """
    ages = ["C", "Y", "M", "O"]
    inf_rates = [inf_rate * 2**num/4 for num in range(0,4)]   
    inf_rates = {key:value for (key,value) in zip(ages, inf_rates)}
    for sus in susceptible:
        age = grid[sus[0],sus[1]].age
        vacc_status = grid[sus[0],sus[1]].vacc_status
        status = grid[sus[0],sus[1]].inf_status
        if status == "S":
            if  vacc_status:
                if prob(inf_rates[age[0]]/protection):
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


def main(n,inf_start, inf_rate, inf_range, rec_rate, death_rate, hosp_rate,frac_hosp_capacity,pop_structure,vacc_frac, protection, immunity, duration):
    """
    The main function which runs our simulation. Calls all functions in the grid.py
    file, and uses them to iterate through the days in the duration, each day finding
    all the infected individuals, finding their contacts and applying the various 
    rate probabilities to them, before providing and updated grid for the next day. 
    It returns a list of integer grids for the duration of the simulation, one on
    each day

    Parameters
    ----------
    n : Int
        side length of square grid
    inf_start : Int
        Number of infected individuals on the first day
    inf_rate : Float
        Chance that a susceptible person gets infected each day
    inf_range : Integer
        Distance from infected person someone can get infected from
    rec_rate : Float
        Chance that an infected perosn will recover each day
    death_rate : Float
        Chance that an infected person will die each day
    hosp_rate : Float
        Chance that an infected person will have to be hospitalised
    frac_hosp_capacity : Float
        Fraction of the population that can be hospitalised at once without 
        overwhelming the hospitals
    pop_structure : Str
        Type of population in terms of dempographic distribution in the grid
    vacc_frac : Float
        Fraction of the population who have been vaccinated - the fraction
        is the fraction of individuals in the grid who have been vaccinated
    protection : Float
        The factor that the infection and hospital rate is divided by given the 
        individual has been vaccinated
    immunity : Int
        The number of days a person remains immune from being infected after they
        recover
    duration : Int
        The number of days the simulation lasts for

    Returns
    -------
    grid_list : List
        The list of integer grids produced - one for each day
        

    """
    grid = original_grid(n,pop_structure, vacc_frac,inf_start)
    grid_list=[integer_grid(grid)]
    hosp_capacity=frac_hosp_capacity*(n**2)
    hosp_overwhelm_days=0
    hod=0
    allowed_coords = [[i,j] for i in range(n) for j in range(n)]
    ages = ["C", "Y", "M", "O"]
    hosp_rates = [hosp_rate * 2**num/4 for num in range(0,4)]
    death_rates = [death_rate * 2**num/4 for num in range(0,4)]
    rec_rates = [rec_rate * 4/(2*num) for num in range(1,5)]
    rec_rates = {key:value for (key,value) in zip(ages, rec_rates)}
    death_rates = {key:value for (key,value) in zip(ages, death_rates)}
    hosp_rates = {key:value for (key,value) in zip(ages, hosp_rates)}
    for time in range(duration):
        ho_death = False
        row_no=0
        susceptible = []
        for row in grid:
            collumn_no = 0
            for person in row:
                if person.inf_status[0] == "I":
                    affected = in_range([row_no,collumn_no], inf_range, allowed_coords)
                    for sus in affected:
                        susceptible.append(sus)
                    if int(person.inf_status[1]) > 2:
                        if len(grid_search(grid, "H")) >= hosp_capacity:
                            if prob(2*death_rates[person.age]):
                                person.inf_status = "D"
                                hod += 1
                                ho_death = True
                        else:
                            new_statuses = [person.inf_status,"H", "R0"]
                            if person.vacc_status:
                                chance = [1-(hosp_rates[person.age] + rec_rates[person.age]),hosp_rates[person.age]/protection, rec_rates[person.age]]
                                
                            else:
                                chance = [1-(hosp_rates[person.age] + rec_rates[person.age]),hosp_rates[person.age], rec_rates[person.age]]

                            new_status = random.choices(new_statuses, chance )[0]
                            person.inf_status = new_status
                    else:
                        person.inf_status = "I" + str(int(person.inf_status[1]) + 1)
                elif person.inf_status[0] == "H":
                    new_statuses = [person.inf_status,"D", "R0"]
                    chance = [1-(death_rates[person.age] + rec_rates[person.age]),death_rates[person.age], rec_rates[person.age]]
                    new_status = random.choices(new_statuses, chance )[0]
                    person.inf_status = new_status

                
                elif person.inf_status[0] == "R":
                    if int(person.inf_status[1]) > immunity:
                        person.inf_status = "S"
                    
                    else:
                        person.inf_status = "R" + str(int(person.inf_status[1]) + 1)
                    
                   
                collumn_no += 1
            row_no += 1
        if ho_death:
            hosp_overwhelm_days +=1
        grid = infect(susceptible,grid, inf_rate, protection )
        grid_list.append(integer_grid(grid))
        
    print('Hospitals were overwhelmed for a total of', hosp_overwhelm_days,'days causing', hod, 'people to die because of lack of hospitalisation')
    return grid_list


