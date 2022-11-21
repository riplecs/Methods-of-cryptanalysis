# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 11:56:19 2022

@author: Daria
"""
import time
import gmpy2
import numpy as np

file = open('SE_15.txt', 'r')
data = file.readlines()
file.close()

t = len(data)//2
C = [int(data[i][5:], 16) for i in range(0, 2*t, 2)]
N = [int(data[i][5:], 16) for i in range(1, 2*t, 2)]

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

start_time = time.time()     
print(SE_attack())
print(time.time() - start_time)

file = open('MitM_15.txt', 'r')
data = file.readlines()
file.close()

C, N = int(data[0][4:], 16), int(data[1][4:], 16)

e = 65537
l = 20

def MitM_attack():
    T = range(1, 2**(l//2) + 1)
    T_pow_e = [gmpy2.powmod(T_i, e, N) for T_i in T]
    for T_pow_e_i in T_pow_e:
        C_s = C*gmpy2.invert(T_pow_e_i, N)%N
        if C_s in T_pow_e:
            return hex(T[T_pow_e.index(C_s)]*T[T_pow_e.index(T_pow_e_i)]).upper()
    return 'Відкритий текст не було визначено'

def brute_force():
    for i in range(1, 2**l):
        if C - gmpy2.powmod(i, e, N) == 0:
            return hex(i).upper()


start_time = time.time()
print(MitM_attack())
print(time.time() - start_time)

start_time = time.time()
print(brute_force())
print(time.time() - start_time)