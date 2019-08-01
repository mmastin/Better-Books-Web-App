import json
import os
import tarfile
import warnings

import numpy as np
import pandas as pd
import requests
import spacy
import wget
# from elevate import elevate
from spacy.lang.en import English

import _pickle as pickle
from flask import Flask

print(wget.__version__)
warnings.filterwarnings('ignore')
# sm_url = 'https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.1.0/en_core_web_sm-2.1.0.tar.gz'
# lg_url = "https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-2.1.0/en_core_web_lg-2.1.0.tar.gz"
# Using pickled model here? Peyton had this import in his flask
# Add other imports needed for model

df = pd.read_csv('small df.csv').truncate(before=0, after=100)
df = df[['book_title', 'description']].reset_index()

sm_url = 'https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.1.0/en_core_web_sm-2.1.0.tar.gz'
sm_path = './manual/sp_sm.tar.gz'
# elevate()
try:
    os.mkdir('manual')
except:
    pass
wget.download(sm_url, sm_path)
current_dir = os.getcwd()
unzip_path = current_dir + '/manual'

tar = tarfile.open(unzip_path + '/sp_sm.tar.gz', "r:gz")
tar.extractall(unzip_path)
tar.close()

# sm_path = 
# Works:
# nlp = spacy.load(".\en_core_web_sm-2.1.0\en_core_web_sm\en_core_web_sm-2.1.0")
nlp = spacy.load(".\manual\en_core_web_sm-2.1.0\en_core_web_sm\en_core_web_sm-2.1.0")
docs = list(nlp.pipe(df.description))
df['docs'] = docs

# df = pd.read_pickle('df_pickle.pkl')

def get_recs_from_desc(input_string, from_isbn=False):
    '''Takes a book description, converts to a spacy doc object and 
    calculates the similarity score for all other books in the dataframe 
    (variable called df), sorts and returns the top 10 as a json object
    containing title, author, avg rating and ISBN'''
    
    #convert input string of hypthetical book description into spacy doc object
    test_doc = nlp(input_string)
    
    #instantiate empty list of similarity scores:
    sims = []
    
    #iterate over the doc object for each book in the df to get the similarity score and append to list
    for doc in df.docs:
        sim = test_doc.similarity(doc)
        sims.append(sim)
    
    #sort the list and grab the top 10:
    if from_isbn:
        #skip the 0th ranked book which will be the bookused to get the input_string of the description:
        top10 = pd.Series(sims).sort_values(ascending=False).iloc[1:11]
    else:
        top10 = pd.Series(sims).sort_values(ascending=False).iloc[:10]
    
    #instantiate empty list to store the python dicts of each book
    books = []
    
    #iterate thru the top 10 ranked simlilar books and populate the book list w/ dictionaries for each book
    for i in top10.index:
        book = {}
        book['title'] = df.iloc[i]['book_title']
        # book['author'] = df.iloc[i]['author']
        # book['avg_rating'] = df.iloc[i]['avg_rating']
        # book['ISBN'] = df.iloc[i]['ISBN']
        books.append(book)
    return json.dumps(books)


application = app = Flask(__name__)
# AWS EBS expects name 'application'

@app.route('/<desc>', methods = ['GET'])
def describe(desc):
    try:
        input_desc = desc
    except:
        pass
    if input_desc:
        return get_recs_from_desc(input_desc)
    else:
        return sample


if __name__ == '__main__':
    app.run(debug=True)
