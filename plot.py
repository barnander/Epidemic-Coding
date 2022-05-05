#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 13:05:33 2022

@author: rr21338
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse

parser=argparse.ArgumentParser(description='How each value changes the sim')
parser.add_argument('--File',metavar='n',type=str,default=None,
                    help='Give a name for the plot and save it instead of displaying')
args=parser.parse_args()

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

def plot_show(grid_list):
    list_of_infections = grid_count_list(grid_list)
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
    axs2=plt.legend(loc = "center right")
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
    
    if args.File is None:
        return plt.show()
    else:
        plt.savefig(args.File)
        
    
    
