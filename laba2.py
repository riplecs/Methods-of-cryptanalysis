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
letters_freqs = [clean_text.count(i)/L for i in alphabet]
print(pd.DataFrame(np.matrix(letters_freqs), columns = alphabet, index = ['']))
