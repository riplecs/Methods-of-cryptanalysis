# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 12:47:22 2022

@author: Daria
"""
import re
import math
import random
import numpy as np
import pandas as pd


file = open('znedoleni.txt', 'r')

alphabet = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
m = len(alphabet)

text = ''
for line in file:
    text += line
text = text.replace('ґ', 'г')
clean_text = re.sub(f'[^{alphabet}]', '', text.lower())

L_text = len(clean_text)
alph = list(alphabet)

letter_freqs = [clean_text.count(i)/L_text for i in alph]
print(pd.DataFrame(np.matrix(letter_freqs), columns = alph, index = ['']))

bigrams = [f'{i}{j}' for i in alph for j in alph]
bigram_freqs = [clean_text.count(i)/(L_text - 1) for i in bigrams]

print(pd.DataFrame(np.array(bigram_freqs).reshape((m, m)), 
                   columns = alph, index = alph))

entropy_per_letter = sum(-f*math.log2(f) for f in letter_freqs)
print(entropy_per_letter)
entropy_per_bigram = sum((-f*math.log2(f) if f > 0 else 0) 
                         for f in bigram_freqs)/2
print(entropy_per_bigram)
compl_index =  sum(clean_text.count(bi)*(clean_text.count(bi) - 1)
                   for bi in bigrams)/(L_text*(L_text - 1))
print(compl_index)


def gen_texts(text, l, n):
    texts = []
    for i in range(n):
        start = random.randint(0, L_text - l - 1)
        texts.append(text[start : start + l])
    return texts

    
def  Vigenere(key, text):
    text = [alph.index(t) for t in text]
    cipher_text = [(t + key[text.index(t)%len(key)])%m for t in text]
    return ''.join([alph[c] for c in cipher_text])

    
def gen_affine_keys(l):
    a = random.randint(1, m**l - 1)
    while math.gcd(a, m) != 1:
        a = random.randint(1, m**l - 1)
    b = random.randint(0, m**l - 1)
    return a, b

def Affine(text, l):
    a, b = gen_affine_keys(l)
    text = [alph.index(t) for t in text]
    if l == 2:
        text = [(text[i]*m + text[i + 1])%m**l
                for i in range(0, len(text) - 1, l)]
    cipher_text = [(a*t+b)%m**l for t in text]
    if l == 2:
        new_cipher_text = []
        for c in cipher_text:
            new_cipher_text.append(c//m)
            new_cipher_text.append(c%m)
        cipher_text = new_cipher_text
    return ''.join(alph[c] for c in cipher_text)
    
#for L in (10, 100, 1000, 10000):
#    texts = gen_texts(clean_text, L, (10000 if L != 10000 else 1000))
    


