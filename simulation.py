#!usr/bin/env python
"""
Created on Tue Mar 22 13:11:22 2022
@author: Basil
"""
from grid import main
from plot import plot_show
from animation import grid_animation
import argparse

parser=argparse.ArgumentParser(description='How each value changes the sim')
parser.add_argument('--Size',metavar='N',type=int,default=30,
                        help='Use a grid of size N x N')
parser.add_argument('--Start',metavar='N',type=int,default=3,
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
parser.add_argument('--Immune',metavar='p',type=int,default=10000,
                    help='the ammount of days that a person remains immune from infection after recovery, after thsi period the become susceptible again')
parser.add_argument('--Duration',metavar='T',type=int,default=50,
                    help='set the duration of the sim to time T')


args=parser.parse_args()

import pandas as pd



if __name__ == "__main__":
    n = args.Size
    inf_start=args.Start
    inf_rate = args.Inf
    while inf_rate>1:
        print('please give a value between 0 and 1')
        inf_rate=float(input('please give an infection rate = '))
    while inf_rate<0:
        print('please give a value between 0 and 1')
        inf_rate=float(input('please give an infection rate = '))
    inf_range = args.Range
    rec_rate = args.Rec
    while rec_rate>1:
        print('please give a value between 0 and 1')
        rec_rate=float(input('please give a recovery rate = ' ))
    while rec_rate<0:
        print('please give a value between 0 and 1')
        rec_rate=float(input('please give a recovery rate = ' ))
    death_rate = args.Death
    while death_rate>1:
        print('please give a value between 0 and 1')
        death_rate=float(input('please give a value for the death rate = '))
    while death_rate<0:
        print('please give a value between 0 and 1')
        death_rate=float(input('please give a value for the death rate = '))
    hosp_rate = args.Hosprate
    while hosp_rate>1:
        print('please give a value between 0 and 1')
        hosp_rate=float(input('please give a value for chance of hospitilisation = '))
    while hosp_rate<0:
        print('please give a value between 0 and 1')
        hosp_rate=float(input('please give a value for chance of hospitilisation = '))
    percent_hosp_capacity = args.Hospcap
    while percent_hosp_capacity>1:
        print('please give a value between 0 and 1')
        percent_hosp_capacity=float(input('please give a value for what proportion of the popualation can be hospitilised = '))
    while percent_hosp_capacity<0:
        print('please give a value between 0 and 1')
        percent_hosp_capacity=float(input('please give a value for what proportion of the popualation can be hospitilised = '))
    pop_structure= args.Demo
    vacc_percentage = args.Vac
    while vacc_percentage>1:
        print('please give a value between 0 and 1')
        vacc_percentage=float(input('please give a value for the proportion of population vaccinated = '))
    while vacc_percentage<0:
        print('please give a value between 0 and 1')
        vacc_percentage=float(input('please give a value for the proportion of population vaccinated = '))
    protection = args.Proc
    while protection<1:
        print('please give a value greater than 1')
        protection=float(input('please give a value for the factor that infection rate is reduced by when vaccinated = '))
    immunity=args.Immune
    duration = args.Duration
    grid_list=main(n, inf_start,inf_rate,inf_range, rec_rate, death_rate, hosp_rate,percent_hosp_capacity,pop_structure,vacc_percentage, protection,immunity, duration)
    anim=grid_animation(grid_list)
    plot_show(grid_list)



