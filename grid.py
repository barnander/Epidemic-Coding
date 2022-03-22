# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 13:11:22 2022

@author: Basil
"""

import numpy as np
import matplotlib.pyplot as plt

def original_grid(n):
    row = ["S" for i in range(n)]
    grid = np.array([row for i in range(n)])
    return grid
