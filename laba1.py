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

C_values = np.unique(np.array(table))

C_probs = []

for c in C_values:
    c_prob = 0
    for j in range(n):
        for i in range(n):
            if table.loc[[f'k_{j}']][f'M_{i}'].values == c:
                c_prob += probs.loc[['P(M_j)']][j].values*probs.loc[['P(k_i)']][i].values
    C_probs.append(c_prob)
    
print(pd.DataFrame(np.matrix(C_probs).T, index = ['P(C_h)']))
                   
CM_probs = np.zeros((n, n))

for c in C_values:
    for i in range(n):
        for j in range(n):
            if table[f'M_{i}'].values[j] == c:
                index = list(C_values).index(c)
                CM_probs[index][i] += probs.loc[['P(M_j)']][i].values*probs.loc[['P(k_i)']][j].values
 
print('\nP(C, M):\n') 
print(pd.DataFrame(CM_probs, index = [f'C_{i}' for i in range(n)],
                   columns = [f'M_{j}' for j in range(n)]))


M_given_C_probs = np.divide(CM_probs, [C_probs for i in range(n)])[0]
print('\nP(M|C):\n')
print(pd.DataFrame(M_given_C_probs, index = [f'C_{i}' for i in range(n)],
                   columns = [f'M_{j}' for j in range(n)]))

delta_D = [f'M_{list(M_given_C_probs[i]).index(max(M_given_C_probs[i]))}'
           for i in range(n)]

print('\nDeterministic δ:\n')
print(pd.DataFrame(np.matrix(delta_D), index = [''],
                   columns = [f'C_{i}' for i in range(n)]))

delta_S = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        if M_given_C_probs[i][j] == max(M_given_C_probs[i]):
            delta_S[i][j] = 1
    suma = sum(delta_S[i])
    if suma > 1:
        delta_S[i] = [0. if delta_S[i][j] == 0. else round(1/suma, 4)
                      for j in range(n)]
        
print('\nStochastic δ:\n')
print(pd.DataFrame(delta_S, index = [f'C_{i}' for i in range(n)],
                   columns = [f'M_{j}' for j in range(n)]))

losses_D = sum(CM_probs[i][j]*(0 if delta_D[i] == f'M_{j}' else 1)
               for i in range(n) for j in range(n))

print('\nAverage losses for deterministic δ:\n')
print(losses_D)

losses_S = sum(CM_probs[i][j]*(1 - delta_S[i][j]) for i in range(n) 
               for j in range(n))

print('\nAverage losses for stochastic δ:\n')
print(losses_S)
