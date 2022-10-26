# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 12:47:22 2022

@author: Daria
"""
import re
import numpy as np
import pandas as pd


file = open('znedoleni.txt', 'r')

alphabet = 'абвгдеєжзиійклмнопрстуфхцчшщьюя'

text = ''
for line in file:
    text += line
text = text.replace('ґ', 'г')
clean_text = re.sub(f'[^{alphabet}]', '', text.lower())

L = len(clean_text)
alphabet = list(alphabet)

letter_freqs = [clean_text.count(i)/L for i in alphabet]
print(pd.DataFrame(np.matrix(letter_freqs), columns = alphabet, index = ['']))

bigrams = [f'{i}{j}' for i in alphabet for j in alphabet]
bigram_freqs = [clean_text.count(i)/(L - 1) for i in bigrams]

print(pd.DataFrame(np.array(bigram_freqs).reshape((31, 31)), 
                   columns = alphabet, index = alphabet))
