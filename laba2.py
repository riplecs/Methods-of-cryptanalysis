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
import matplotlib.pyplot as plt

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

def count_enters(text, bigram):
    count, start = 0, 0
    while start < len(text):
        pos = text.find(bigram, start)
        if pos != -1:
            start = pos + 1
            count += 1
        else:
            break
    return count

bigram_freqs = [count_enters(clean_text, i)/(L_text - 1) 
                for i in bigrams]

print(pd.DataFrame(np.array(bigram_freqs).reshape((m, m)), 
                   columns = alph, index = alph))

entropy_per_letter = sum(-f*math.log2(f) for f in letter_freqs)
print(entropy_per_letter)
entropy_per_bigram = sum((-f*math.log2(f) if f > 0 else 0) 
                         for f in bigram_freqs)/2
print(entropy_per_bigram)
letter_index =  sum(clean_text.count(i)*(clean_text.count(i) - 1)
                   for i in alph)/(L_text*(L_text - 1))
print(letter_index)
bi_index =  sum(count_enters(clean_text, i)*(count_enters(clean_text, i) - 1)
                for i in bigrams)/(L_text*(L_text - 1))
print(bi_index)


def gen_texts():
    texts = []
    for i in range(N):
        start = random.randint(0, L_text - L - 1)
        texts.append(clean_text[start : start + L])
    return texts

def gen_Vigenere_key():
    r = random.choice([1, 5, 10])
    return random.choices(range(m), k = r)

def  Vigenere():
    text_ = [alph.index(t) for t in text]
    cipher_text = [(t + key[text_.index(t)%len(key)])%m for t in text_]
    return ''.join([alph[c] for c in cipher_text])

    
def gen_affine_keys():
    a = random.randint(1, m**l - 1)
    while math.gcd(a, m) != 1:
        a = random.randint(1, m**l - 1)
    b = random.randint(0, m**l - 1)
    return a, b

def convert_bigrams(text):
    return [(text[i]*m + text[i + 1])%m**2 
            for i in range(0, len(text) - 1, 2)]


def deconvert_bigrams(cipher_text):
    new_cipher_text = []
    for c in cipher_text:
        new_cipher_text.append(c//m)
        new_cipher_text.append(c%m)
    return new_cipher_text
    

def Affine():
    text_ = [alph.index(t) for t in text]
    if l == 2:
        text_ = convert_bigrams(text_)
    cipher_text = [(a*t+b)%m**l for t in text_]
    if l == 2:
        cipher_text = deconvert_bigrams(cipher_text)
    return ''.join(alph[c] for c in cipher_text)


def uniform_text():
    Zm = alph if l == 1 else bigrams
    length = L//l
    return ''.join([random.choice(Zm) for i in range(length)])
    

def fibonacci_text():
    Zm = range(m) if l == 1 else convert_bigrams([alph.index(t) 
                                 for t in ''.join([b for b in bigrams])])
    length = L//l
    s0, s1 = random.choices(Zm, k = 2)
    y = [s0, s1]
    for i in range(length - 2):
        y.append((y[i] + y[i + 1])%m**l)
    if l == 2:
        y = deconvert_bigrams(y)
    return ''.join([alph[y_i] for y_i in y])
    

def criterion2_0(text):
    if l == 2:
        text = [text[i:i + 2] for i in range(L - 1)]
    return all(elem in np.unique(text) for elem in Afrq)
        

def criterion2_1(text, threshold = 0.9):
    if l == 2:
        text = [text[i:i + 2] for i in range(L - 1)]
    Aaf = [elem for elem in np.unique(text) if elem in Afrq]
    return len(list(set(Afrq)&set(Aaf))) > len(Afrq)*threshold
    

def criterion2_2(text):
    Afrq_text_freqs = [count_enters(text, i)/(L - l + 1) for i in Afrq]
    return all([Afrq_text_freqs >= Afrq_alph_freq])
    

def criterion2_3(text):
    Afrq_text_freqs = [count_enters(text, i)/(L - l + 1) for i in Afrq]
    return sum(Afrq_text_freqs) >= sum(Afrq_alph_freq)


def criterion4(text):
    threshold = 0.006 if l == 1 else 0.002
    Zm = alph if l == 1 else bigrams
    text_nums = [count_enters(text, i) for i in Zm]
    index = sum(i*(i - 1) for i in text_nums)/(L*(L - 1))
    true_index = letter_index if l == 1 else bi_index
    return abs(index - true_index) <= threshold

'''
N = 100
L = 1000
texts = gen_texts()

plt.plot(range(N), [sum(count_enters(j, i)*(count_enters(j, i) - 1)
         for i in alph)/(L*(L - 1)) - letter_index for j in texts],
         label = 'for l = 1')

plt.plot(range(N), [sum(count_enters(j, i)*(count_enters(j, i) - 1)
         for i in bigrams)/(L*(L - 1)) - bi_index for j in texts],
         label = 'for l = 2')

plt.legend()
'''

def criterion5(text, threshold = 0.9):
    text_nums = [count_enters(text, i) for i in Bprh]
    return text_nums.count(0) > m**l*threshold


criterions = {criterion2_0 : '__Criterion 2.0__\n',
              criterion2_1 : '__Criterion 2.1__\n',
              criterion2_2 : '__Criterion 2.2__\n',
              criterion2_3 : '__Criterion 2.3__\n',
              criterion4 : '__Criterion 4.0__\n',
              criterion5 : '__Criterion 5.0__\n'}

distortions = {Vigenere : 'Vigenere',
               Affine : 'Affine substitution',
               uniform_text : 'Uniformly distributed sequence',
               fibonacci_text : 'Fibonacci sequence'}


letter_freqs_threshold = sorted(letter_freqs, reverse = True)[math.ceil(m*0.1)]
bigram_freqs_threshold = sorted(bigram_freqs, reverse = True)[math.ceil(m*m*0.1)]

letter_freqs_threshold2 = sorted(letter_freqs)[math.ceil(m*0.1)]
bigram_freqs_threshold2 = sorted(bigram_freqs)[math.ceil(m*m*0.1)]

Afrqs = ([alph[letter_freqs.index(i)] for i in letter_freqs 
          if i > letter_freqs_threshold], 
        [bigrams[bigram_freqs.index(i)] for i in bigram_freqs 
          if i > bigram_freqs_threshold])

Bprhs = ([alph[letter_freqs.index(i)] for i in letter_freqs 
          if i < letter_freqs_threshold2], 
        [bigrams[bigram_freqs.index(i)] for i in bigram_freqs 
          if i < bigram_freqs_threshold2])

Afrq_alph_freqs = ([letter_freqs[alph.index(el)] for el in Afrqs[0]], 
                   [bigram_freqs[bigrams.index(el)] for el in Afrqs[1]])



results = open('results.txt', 'w')

for L in (10, 100, 1000, 10000):
    N = (10000 if L != 10000 else 1000)
    texts = gen_texts()
    for distort in distortions:
        results.write(distortions[distort])
        if distortions[distort] == 'Vigenere':
            key = gen_Vigenere_key()
            results.write(f'(r = {"".join([alph[k] for k in key])})\n')
        if distortions[distort] == 'Affine substitution':
            a, b = gen_affine_keys()
            results.write(f'(a = {a}, b = {b})\n')
        for criterion in criterions:
            print(criterions[criterion])
            results.write(criterions[criterion])
            for l in (1, 2):
                Afrq = Afrqs[l - 1]
                Bprh = Bprhs[l - 1]
                Afrq_alph_freq = Afrq_alph_freqs[l - 1]
                alpha, beta = 0, 0
                for text in texts:
                    alpha += (1 - int(criterion(text)))
                    cipher_text = distort()
                    beta += int(criterion(cipher_text))
                results.write(f'\nL = {L}, l = {l}\n')
                results.write(f'False positive = {alpha/(2*N)}\n')
                results.write(f'False negative =  {beta/(2*N)}\n')
            
results.close()        
        

