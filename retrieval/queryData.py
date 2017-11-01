import argparse
import nltk
import numpy as np
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity


def parse_args():
    parser = argparse.ArgumentParser(description="Run DeepFM.")
    parser.add_argument('--docs', nargs='?', default='retrieval/data/med/MED.ALL',
                        help='Path of the document file.')

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


def performQuery(queries):
    args = parse_args()
    docs = load_data(args.docs)
    vec_docs, vec_queries = tf_idf(docs, queries, tokenize_text)

    sim_matrix = cosine_similarity(vec_docs, vec_queries)
    
    ranked_documents = np.argsort(-sim_matrix[:, 0])
    return (ranked_documents[:10] + 1)


