#!usr/bin/env python
"""
Created on Tue Mar 22 13:11:22 2022
@author: Basil
"""
from grid import main
from plot import plot_show
from animation import grid_animation
import argparse
from plot import arg


parser=argparse.ArgumentParser(description='How each value changes the sim')
args=arg(parser)

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
    frac_hosp_capacity = args.Hospcap
    while frac_hosp_capacity>1:
        print('please give a value between 0 and 1')
        frac_hosp_capacity=float(input('please give a value for what proportion of the popualation can be hospitilised = '))
    while frac_hosp_capacity<0:
        print('please give a value between 0 and 1')
        frac_hosp_capacity=float(input('please give a value for what proportion of the popualation can be hospitilised = '))
    pop_structure= args.Demo
    vacc_frac = args.Vac
    while vacc_frac>1:
        print('please give a value between 0 and 1')
        vacc_frac=float(input('please give a value for the proportion of population vaccinated = '))
    while vacc_frac<0:
        print('please give a value between 0 and 1')
        vacc_frac=float(input('please give a value for the proportion of population vaccinated = '))
    protection = args.Proc
    while protection<1:
        print('please give a value greater than 1')
        protection=float(input('please give a value for the factor that infection rate is reduced by when vaccinated = '))
    immunity=args.Immune
    duration = args.Duration
    grid_list=main(n, inf_start,inf_rate,inf_range, rec_rate, death_rate, hosp_rate,frac_hosp_capacity,pop_structure,vacc_frac, protection,immunity, duration)
    anim=grid_animation(grid_list)
    plot_show(grid_list)





