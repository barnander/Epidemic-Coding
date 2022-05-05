import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors



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

def inst_anim(grid_list,time):
    fig = plt.figure(3)
    cols=len(grid_list[0][0])
    rows=len(grid_list[0][1])
    brg=colors.ListedColormap(['blue','red','green','black','cyan'])
    bounds=[0,1,2,3,4,5]
    norm = colors.BoundaryNorm(bounds, brg.N)
    im = plt.imshow(grid_list[0],cmap=brg,aspect='auto',interpolation='nearest',extent=[0.5, 0.5+cols, 0.5, 0.5+rows], norm=norm)
    plt.axis('off')
    im.set_array(grid_list[time])
    return
    
inst_anim(grid_list,8)