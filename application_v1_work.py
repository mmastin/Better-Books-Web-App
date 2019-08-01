from flask import Flask
from flask import request
import numpy as np
import pandas as pd
# import requests
import _pickle as pickle
import spacy
from spacy.lang.en import English
import json


df = pd.read_pickle('/Users/mattmastin/Desktop/df_pickle.pkl')
# Maybe need to pickle model with 'wb' - write binary - or remove 'rb'
# Peyton's log regression opened as 'rb', Doc2Vec model not 'wb/rb'

application = app = Flask(__name__)
# AWS EBS expects name 'application'

nlp = spacy.load("en_core_web_lg")


def get_recs_from_desc(input_string, from_isbn=False):
    '''Takes a book description, converts to a spacy doc object and
    calculates the similarity score for all other books in the dataframe
    (variable called df), sorts and returns the top 10 as a json object
    containing title, author, avg rating and ISBN'''

    # convert input string of hypthetical book description into spacy doc object
    test_doc = nlp(input_string)

    # instantiate empty list of similarity scores:
    sims = []

    # iterate over the doc object for each book in the df to get the similarity score and append to list
    for doc in df.docs:
        sim = test_doc.similarity(doc)
        sims.append(sim)

    # sort the list and grab the top 10:
    if from_isbn:
        # skip the 0th ranked book which will be the bookused to get the input_string of the description:
        top10 = pd.Series(sims).sort_values(ascending=False).iloc[1:11]
    else:
        top10 = pd.Series(sims).sort_values(ascending=False).iloc[:10]

    # instantiate empty list to store the python dicts of each book
    books = []

    # iterate thru the top 10 ranked simlilar books and populate the book list w/ dictionaries for each book
    for i in top10.index:
        book = {}
        book['title'] = df.iloc[i]['book_title']
        book['author'] = df.iloc[i]['author']
        book['avg_rating'] = str(df.iloc[i]['avg_rating'])
        book['ISBN'] = str(df.iloc[i]['ISBN'])
        books.append(book)
    return json.dumps(books)


@app.route('/<desc>', methods=['GET'])
def describe(desc):
    try:
        input_desc = desc
    except:
        pass
    if input_desc:
        return get_recs_from_desc(input_desc)
    else:
        return sample

input_string = 'world war II lovers reunite in England'
sample = get_recs_from_desc(input_string)

if __name__ == '__main__':
    app.run(debug=True)