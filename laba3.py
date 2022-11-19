# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 11:56:19 2022

@author: Daria
"""
import gmpy2
import numpy as np

file = open('SE_15.txt', 'r')
data = []
for line in file:
    data.append(line[5:])
file.close()

C = [int(data[i], 16) for i in range(0, len(data), 2)]
N = [int(data[i], 16) for i in range(1, len(data), 2)]
t = len(C)
e = 5

def Chinese_remainder_theorem(values, modulus):
    n = np.prod(modulus)
    N = [n//n_i for n_i in modulus]
    return sum(values[i]*N[i]*gmpy2.invert(N[i], modulus[i]) for i in range(t))%n
 
 

def SE_attack():
    x = Chinese_remainder_theorem(C, N)
    M = gmpy2.iroot(x, e)
    assert M[1]
    return hex(M[0]).upper()

        
print(SE_attack())
