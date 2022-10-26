# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 12:47:22 2022

@author: Daria
"""
import re
import math
import numpy as np
import pandas as pd


file = open('znedoleni.txt', 'r')

alphabet = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'

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

print(pd.DataFrame(np.array(bigram_freqs).reshape((32, 32)), 
                   columns = alphabet, index = alphabet))

entropy_per_letter = sum(-f*math.log2(f) for f in letter_freqs)
print(entropy_per_letter)
entropy_per_bigram = sum((-f*math.log2(f) if f > 0 else 0) 
                         for f in bigram_freqs)/2
print(entropy_per_bigram)
compl_index =  sum(clean_text.count(bi)*(clean_text.count(bi) - 1)
                   for bi in bigrams)/(L*(L - 1))
print(compl_index)