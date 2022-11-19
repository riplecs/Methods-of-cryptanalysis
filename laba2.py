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
file.close()
text = text.replace('ґ', 'г')
clean_text = re.sub(f'[^{alphabet}]', '', text.lower())

L_i = [10, 100, 1000, 10000]
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

bigram_freqs = [count_enters(clean_text, i)/(L_text - 1) for i in bigrams]

print(pd.DataFrame(np.array(bigram_freqs).reshape((m, m)),  columns = alph, 
                   index = alph))

entropy_per_letter = sum(-f*math.log2(f) for f in letter_freqs)
print(entropy_per_letter)
entropy_per_bigram = sum((-f*math.log2(f) if f > 0 else 0) for f in bigram_freqs)/2
print(entropy_per_bigram)

def culc_index(Zm, text):
    ind = 0
    for i in Zm:
        c = count_enters(text, i)
        ind += c*(c - 1)
    return ind/(len(text)*(len(text) - 1))

letter_index =  culc_index(alph, clean_text)
print(letter_index)
bi_index =  culc_index(bigrams, clean_text)
print(bi_index)

letter_freqs_threshold = sorted(letter_freqs, reverse = True)[math.ceil(m*0.2)]
letter_freqs_threshold2 = sorted(letter_freqs)[math.ceil(m*0.2)]

bigram_freqs_s, bigrams_s = zip(*sorted(zip(bigram_freqs, bigrams)))

Afrqs = ([alph[letter_freqs.index(i)] for i in letter_freqs 
          if i > letter_freqs_threshold], bigrams_s[-math.ceil(m*m*0.1):])

Bprhs = ([alph[letter_freqs.index(i)] for i in letter_freqs 
          if i < letter_freqs_threshold2], bigrams_s[:math.ceil(m*m*0.1)])

Afrq_alph_freqs = ([letter_freqs[alph.index(el)] for el in Afrqs[0]], 
                   [bigram_freqs[bigrams.index(el)] for el in Afrqs[1]])


threshold2_1_i = [[2, 6, 6, 6],
                [2, 20, 80, 80]]

threshold5_i = [[6, 3, 0, 5],
                [102, 100, 100, 97]]

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
    a, b = a_i[l - 1], b_i[l - 1]
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
    return ''.join(random.choices(Zm, k = length))
    

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
    text =  [text[i:i + l] for i in range(L - l + 1)]
    return all(elem in text for elem in Afrq)
        

def criterion2_1(text):
    text = [text[i:i + l] for i in range(L - l + 1)]
    return len(list(set(Afrq)&set(text))) > threshold2_1
    

def criterion2_2(text):
    Afrq_text_freqs = [count_enters(text, i)/(L - l + 1) for i in Afrq]
    return all([Afrq_text_freqs >= Afrq_alph_freq])
    

def criterion2_3(text):
    Afrq_text_freqs = [count_enters(text, i)/(L - l + 1) for i in Afrq]
    return sum(Afrq_text_freqs) >= sum(Afrq_alph_freq)


def criterion4(text):
    threshold = 0.01*0.1**(l - 1)
    Zm = alph if l == 1 else bigrams
    index = culc_index(Zm, text)
    true_index = letter_index if l == 1 else bi_index
    return abs(index - true_index) <= threshold


def criterion5(text):
    text_nums = [count_enters(text, i) for i in Bprh]
    return text_nums.count(0) > threshold5


criterions = {criterion2_0 : '\n__Criterion 2.0__\n',
              criterion2_1 : '\n__Criterion 2.1__\n',
              criterion2_2 : '\n__Criterion 2.2__\n',
              criterion2_3 : '\n__Criterion 2.3__\n',
              criterion4 : '\n__Criterion 4.0__\n',
              criterion5 : '\n__Criterion 5.0__\n'}

distortions = {Vigenere : '\n__Vigenere__\n',
               Affine : '\n__Affine substitution__\n',
               uniform_text : '\n__Uniformly distributed sequence__\n',
               fibonacci_text : '\n__Fibonacci sequence__\n'}


results = open('result.txt', 'w')


key = gen_Vigenere_key()
results.write(f'Vigenere key: r = {"".join([alph[k] for k in key])}\n')
l = 1
a1, b1 = gen_affine_keys()
results.write(f'Affine substitution key: a = {a1}, b = {b1}\n')
l = 2
a2, b2 = gen_affine_keys()
results.write(f'Affine bigram substitution key: a = {a2}, b = {b2}\n')
a_i, b_i = [a1, a2], [b1, b2]


for L in L_i:
    N = (10000 if L != 10000 else 1000)
    texts = gen_texts()
    for distort in distortions:
        results.write(distortions[distort])
        for criterion in criterions:
            results.write(criterions[criterion])
            for l in (1, 2):
                Afrq = Afrqs[l - 1]
                Bprh = Bprhs[l - 1]
                Afrq_alph_freq = Afrq_alph_freqs[l - 1]
                threshold2_1 = threshold2_1_i[l - 1][L_i.index(L)]
                threshold5 = threshold5_i[l - 1][L_i.index(L)]
                alpha, beta = 0, 0
                for text in texts:
                    alpha += (1 - int(criterion(text)))
                    cipher_text = distort()
                    beta += int(criterion(cipher_text))
                results.write(f'\nL = {L}, l = {l}\n')
                results.write(f'False positive = {alpha/(2*N)}\n')
                results.write(f'False negative =  {beta/(2*N)}\n')
                

results.close()        

#################################

def BWT(text):
    rotations = [text[i:] + text[:i] for i in range(len(text))]
    indexes = [alph.index(r[0]) for r in rotations]
    indexes, rotations = zip(*sorted(zip(indexes, rotations)))
    return [r[-1] for r in rotations]

def BWTcriterion(text):
    text = BWT(text)
    compressed_text = [text[0]]
    nums = 0
    j = 0
    for i in range(len(text) - 1):
        if text[i + 1] != compressed_text[-1]:
            if j > 1:
                compressed_text.append(str(j))
                nums += 1
            compressed_text.append(text[i + 1])
            j = 0
        j += 1
    if j > 1:
        compressed_text.append(str(j))
        nums += 1
    return nums

L, l = 1000, 1
text = clean_text[:L]

print(BWTcriterion(text))
print(BWTcriterion(Affine()))
print(BWTcriterion(Vigenere()))
print(BWTcriterion(uniform_text()))
print(BWTcriterion(fibonacci_text()))
