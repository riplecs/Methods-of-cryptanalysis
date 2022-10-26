# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 12:47:22 2022

@author: Daria
"""
import re

file = open('znedoleni.txt', 'r')

text = ''
for line in file:
    text += line
clean_text = re.sub(r'[^a-щьюяєії]', '', text.lower())


