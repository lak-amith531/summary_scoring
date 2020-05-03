#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 05:10:49 2020

@author: amith
"""

import unicodedata
import traceback
import re

from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words('english'))

def fix_encoding(text_input):
    if isinstance(text_input, list):
        for idx, text in enumerate(text_input):
            # Replace all compatibility characters with their equivalents
            text_input[idx] = unicodedata.normalize("NFKD", text)
        return text_input
    if isinstance(text_input, str):
        text_input = unicodedata.normalize("NFKD", text_input)
        return text_input

def clean_text(text):
    text = fix_encoding(text)
    
    words = []
    # Split based on characters other than alphabets and numbers
    for word in re.split('[^A-Za-z0-9]+',text):
        word = word.lower()
        if word not in STOPWORDS:
            words.append(word)
    # Remove duplicates and return the string
    return ' '.join(list(dict.fromkeys(words))).strip()  

def remove_redundant_phrases(phrases, text):
    for phrase in phrases:
        text = text.replace(phrase, '')
    return text





