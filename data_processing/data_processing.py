#!/usr/bin/env python
# coding: utf-8

###
# Python function to generate processed text given raw text input.
###

import nltk
from nltk.corpus import treebank 
from nltk.tree import Tree
import string
import re
import os
import argparse

def remove_punct(text):
    text  = "".join([char for char in text if char not in string.punctuation])
    text = re.sub('[0-9]+', '', text)
    return text

def tokenization(text):
    text = text.strip()
    text = re.split('\W+', text)
    return text

def remove_stopwords(text):
    stopword = nltk.corpus.stopwords.words('english')
    text = [word for word in text if word not in stopword]
    return text

def lemmatizer(text):
    wn = nltk.WordNetLemmatizer()
    text = [wn.lemmatize(word) for word in text]
    return text

def clean_text(text):
    text = remove_punct(text)
    text = tokenization(text)
    text = remove_stopwords(text)
    text = lemmatizer(text)
    return text

def clean_text_wrapper(args):
    infile = args.infile
    outfile = args.outfile
    with open(infile) as f:
        text = f.read()
    text = clean_text(text)
    text = ",".join(text)
    out_dest = open(outfile, "a")
    out_dest.write(text)
    out_dest.close()
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', type=str, default="sample_input.txt", help='input file')
    parser.add_argument('--outfile', type=str, default="sample_output.csv", help='output file')
    args = parser.parse_args()
    nltk.download('stopwords')
    nltk.download('wordnet')
    clean_text_wrapper(args)

