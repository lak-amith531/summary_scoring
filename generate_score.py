#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 18:15:03 2020

@author: amith
"""

import traceback
import json
import requests

from nltk.corpus import stopwords
from cleaning_utils import (fix_encoding,
                            clean_text,
                            remove_redundant_phrases)
from fuzzywuzzy import fuzz
from partial_matching import PartialMatch
from functools import lru_cache

# This is static currently, look if it can be progressively increased accoring 
# to our requirement
MAX_SIZE = 60
        

def genarate_relevance_score(query, summary):
    pm = PartialMatch(query, summary)
    return pm.calculate_partial_ratio()


def calc_summaries_scores(query, K):
    """
    Input: The input should be a user query ​ of​ ​ type​ ​ string ​ and​ number ​ of
    items to ​ return
    query (string): eg. ​ 'is​ your problems'
    K (integer): eg. ​ 3
    
    Output: [
        {​ 'summary​ ':'​ The Book ​ in​ Three Sentences: Practicing
        meditation ​ and​ mindfulness will make you ​ at​ least ​ 10​ percent
        happier....', ​ 'id​ ':​ 0 ​ },
        {​ 'summary​ ':'​ The Book ​ in​ Three Sentences: Finding
        something important ​ and​ meaningful ​ in​ your life ​ is​ the most productive
        use​ ​ of​ ...', ​ 'id​ ':​ 48​ },
        {​ 'summary​ ':'​ The Book ​ in​ Three Sentences: Everything ​ in
        life ​ is​ an invention. ​ If​ you choose to look ​ at​ your life ​ in​ a ​ new
        way...', ​ 'id​ ':​ 7 ​ }
        ]
    """
    phrases = ['The Book in Three Sentences:']
    path = 'data.json'
    text_input = load_json(path).get('summaries', [])
    scores_list = []
    for _, row in enumerate(text_input):
        book_id = row['id']
        summary = remove_redundant_phrases(phrases, row['summary'])
        cleaned_summary_string = clean_text(summary)
        cleaned_query_string = clean_text(query)
        score = genarate_relevance_score(cleaned_query_string, cleaned_summary_string)
        scores_list.append({'id': row['id'], 
                            'query' : query, 
                            'summary' : row['summary'], 
                            'score': score,
                            'author': get_author_name(book_id)})
    return sorted(scores_list, key = lambda x: (x['score'],x['id']), reverse= True)[:K]
    
def load_json(path):
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except:
        traceback.print_exc()
        data = {}
    return data

@lru_cache(maxsize= MAX_SIZE)
def get_author_name(book_id):
    """
    Input json - {"book_id": 1}
    Output json - {"author": "Amith Lakkakula"}
    """
    try:
        book_id = int(book_id)
    except:
        return "Invalid input for the api call"
    
    url = "https://ie4djxzt8j.execute-api.eu-west-1.amazonaws.com/coding" 
    response = requests.post(url, json= {"book_id": book_id})  

    # can handle this better if there is access to the api code
    if response.status_code == 200:
        try:
            return response.json()['author']
        except:
            return "Invalid output json received"
    else:
        return f"Error code - {response.status_code}. Error message - {response.reason}"


