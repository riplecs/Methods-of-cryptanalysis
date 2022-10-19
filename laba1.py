# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 15:03:10 2022

@author: Daria
"""

import pandas as pd
import numpy as np

n = 20

probs = pd.read_csv('prob_15.csv', header = None)
probs[''] = ['P(M_j)', 'P(k_i)']
probs = probs.set_index('')
print(probs)


table = pd.read_csv('table_15.csv',  names = [f'M_{j}' for j in range(n)])
table[''] = [f'k_{i}' for i in range(n)]
table = table.set_index('')
print(table)

C_probs = []
C_values = np.unique(np.array(table))

for c in C_values:
    c_prob = 0
    for j in range(n):
        for i in range(n):
            if table.loc[[f'k_{j}']][f'M_{i}'].values == c:
                c_prob += probs.loc[['P(M_j)']][j].values*probs.loc[['P(k_i)']][i].values
    C_probs.append(c_prob)
    
print(pd.DataFrame(np.matrix(C_probs).T, index = ['P(C_h)']))
                      
