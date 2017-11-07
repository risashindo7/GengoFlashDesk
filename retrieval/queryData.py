import argparse
import nltk
import numpy as np
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import wordnet


def parse_args():
    parser = argparse.ArgumentParser(description="Run DeepFM.")
    parser.add_argument('--titles', nargs='?', default='retrieval/data/SETTITLES.ALL',
                        help='Path of the document file with titiles.')
    parser.add_argument('--wholesets', nargs='?', default='retrieval/data/WHOLESETS.ALL',
                        help='Path of the document file with set content.')
    parser.add_argument('--spanish_titles', nargs='?', default='retrieval/data/data_spanish/SETTITLES.ALL',
                        help='Path of the document file with titiles for spanish.')
    parser.add_argument('--spanish_wholesets', nargs='?', default='retrieval/data/data_spanish/WHOLESETS.ALL',
                        help='Path of the document file with set content for spanish.')
    parser.add_argument('--french_titles', nargs='?', default='retrieval/data/data_french/SETTITLES.ALL',
                        help='Path of the document file with titiles for french.')
    parser.add_argument('--french_wholesets', nargs='?', default='retrieval/data/data_french/WHOLESETS.ALL',
                        help='Path of the document file with set content for french.')

    return parser.parse_args()


def tokenize_text(docs):
    """
    custom tokenization function given a list of documents
    Parameters
        ----------
        docs : string
            a document

    Returns
    -------
    stems : list
        list of tokens
    """

    text = ''
    for d in docs:
        text += '' + d
    stemmer = PorterStemmer()
    tokens = nltk.word_tokenize(text)
    stems = []
    for item in tokens:
        stems.append(stemmer.stem(item))
    return stems


def load_docs(file):
    docs = []
    with open(file, 'r') as f:
        doc_split = f.read().replace('\n', ' ').replace('\r', ' ').split('.I')
    for l in doc_split[1:]:
        docs.append((''.join(re.sub(' +', ' ', l).split('.W')[1:])))
    return docs


def load_cardset(file, index):
    docs = []
    with open(file, 'r') as f:
        doc_split = f.read().replace('\n', ' ').replace('\r', ' ').split('.I')
    for l in doc_split[1:]:
        docs.append((''.join(re.sub(' +', ' ', l).split('.W')[1:])))
    listOfCardsWithHyphenAndSpaces = docs[index].split(';')
    listOfCardsAsTuplesWithSpaces = list(map(lambda x: x.split('-'), listOfCardsWithHyphenAndSpaces))
    listOfCardsAsTuples = list(map(lambda x: 
        list(map(lambda y: y.strip(), x)),
        listOfCardsAsTuplesWithSpaces))
    return listOfCardsAsTuples


def load_cardset_titles(file, indices):
    docs = []
    with open(file, 'r') as f:
        doc_split = f.read().replace('\n', ' ').replace('\r', ' ').split('.I')
    for l in doc_split[1:]:
        docs.append((''.join(re.sub(' +', ' ', l).split('.W')[1:])))
    return [ docs[i] for i in indices]


def load_data(docs_path):
    original_docs = load_docs(docs_path)
    return original_docs


def tf_idf(docs, queries, tokenizer):
    """
    performs TF-IDF vectorization for documents and queries
    Parameters
        ----------
        docs : list
            list of documents
        queries : list
            list of queries
        tokenizer : custom tokenizer function

    Returns
    -------
    tfs : sparse array,
        tfidf vectors for documents. Each row corresponds to a document.
    tfs_query: sparse array,
        tfidf vectors for queries. Each row corresponds to a query.
    dictionary: list
        sorted dictionary
    """

    processed_docs = [d.lower().translate(str.maketrans('','',string.punctuation)) for d in docs]
    tfidf = TfidfVectorizer(stop_words='english', tokenizer=tokenizer)
    tfs = tfidf.fit_transform(processed_docs)
    tfs_query = tfidf.transform(queries)
    return tfs, tfs_query


def performQuery(queries, cardQueries, language):
    titles = load_data(chooseLanguage(0, language))
    cards = load_data(chooseLanguage(1, language))
    
    #support synonyms
    def get_synonyms(word):
        synonyms = []
        for syn in wordnet.synsets(word.strip()):
            for l in syn.lemmas():
                synonyms.append(l.name())
        return (synonyms)
    
    titles_with_synonyms = map(lambda x: " ".join(get_synonyms(x) + ([x] * 15)) , titles)
    
    vec_titles, vec_queries = tf_idf(titles_with_synonyms, queries, tokenize_text)
    
    vec_cards, vec_card_queries = tf_idf(cards, cardQueries, tokenize_text)

    sim_matrix_titles = cosine_similarity(vec_titles, vec_queries)
    sim_matrix_content = cosine_similarity(vec_cards, vec_card_queries)
    
    sim_matrix = sim_matrix_titles + sim_matrix_content
    
    ranked_documents = np.argsort(-sim_matrix[:, 0])
    listed = [sim_matrix[i] for i in ranked_documents[:10]]
    
    flat_list = [item for sublist in listed for item in sublist]
    non_zero_vals = len(list(filter(lambda x: x > 0.3, flat_list)))
    
    return (ranked_documents[:non_zero_vals] + 1)


def retrieveCards(index, language):
    cardSet = load_cardset(chooseLanguage(1, language), index)
    return cardSet

def retrieveSetNames(indices, language):
    setTitles = load_cardset_titles(chooseLanguage(0, language), indices)
    return setTitles
    
def chooseLanguage(setsOrTitles, language): #titles = 0, sets = 1
    args =  parse_args()
    if (setsOrTitles == 0): #meaning titles
        if  (language == "Spanish"):
            return args.spanish_titles
        if (language == "French"):
            return args.french_titles
    elif (setsOrTitles == 1): #meaning sets
        if (language == "Spanish"):
            return args.spanish_wholesets
        if (language == "French"):
            return args.french_wholesets