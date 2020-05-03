#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 15:30:50 2020

@author: amith
"""

import traceback

from flask import Flask, jsonify, request
from generate_score import calc_summaries_scores

app = Flask(__name__)

@app.route("/get_results", methods=['POST'])
def get_results():
    """
    Input: A list ​ of​ queries ​ and​ number ​ of​ results to ​ return​ for​ each
    queries (list(string)): eg. [​ "is your problems"​ , ​ "achieve take book"​ ]
    K (integer): eg. ​ 3
    Output: A list ​ of​ lists ​ of​ books.
    books: eg. 
    [[
        {​ 'summary​ ':'​ The Book ​ in​ Three Sentences:
        Practicing meditation ​ and​ mindfulness will make you ​ at​ least ​ 10​ percent
        happier....', ​ 'id​ ':​ 0 ​ , ​ 'query​ ': ​ "is your problems"​ , ​ "author"​ : ​ "Dan
        Harris"​ },
        {​ 'summary​ ':'​ The Book ​ in​ Three Sentences: Finding
        something important ​ and​ meaningful ​ in​ your life ​ is​ the most productive
        use​ ​ of​ ...', ​ 'id​ ':​ 48​ , ​ 'query​ ': ​ "is your problems"​ , ​ "author"​ : ​ "Mark
        Manson"​ },
        {​ 'summary​ ':'​ The Book ​ in​ Three Sentences:
        Everything ​ in​ life ​ is​ an invention. ​ If​ you choose to look ​ at​ your life
        in​ a ​ new​ way...', ​ 'id​ ':​ 7 ​ , ​ 'query​ ': ​ "is your problems"​ , "
        author"​ :
        "Rosamund Zander and Benjamin Zander"​ }
        ], [
        {​ 'summary​ ':'​ The Book ​ in​ Three Sentences: The ​ 10​ X
        Rule says that ​ 1 ​ ) you should set targets ​ for​ yourself that are ​ 10​ X
        greater than what....', ​ 'id​ ':​ 1 ​ , ​ 'query​ ': ​ "achieve take book"​ , ​ "author"​ :
        "Grant Cardone"​ },
        {​ 'summary​ ':'​ The Book ​ in​ Three Sentences: Many ​ of
        our behaviors are driven by our desire to achieve a particular level ​ of
        status relative...', ​ 'id​ ':​ 20​ , ​ 'query​ ': ​ "achieve take book, "​ author​ ":
        "​ Keith Johnstone​ "},
        {'summary':'The Book in Three Sentences:
        Ultimately, profit is the only valid metric for guiding a company, and
        there are only three...', 'id':14, 'query': "​ achieve take book,
        "author"​ : ​ "Hermann Simon"​ }
    ]]
    """
    try:
        data = request.json
        print(f'Request data in /get_results route: {data}')
        queries_list = data.pop('queries')
        K = data.pop('K')
    except:
        traceback.print_exc()
        message = "One or both of the following parameters are missing - queries, K."
        return jsonify({"flag": False, "message" : message})
    
    result_list = []
    for query in queries_list:
        result_list.append(calc_summaries_scores(query, K))
    
    return jsonify(result_list)
     
if __name__ == '__main__':
    app.run()