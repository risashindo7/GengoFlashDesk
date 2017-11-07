# -*- coding: utf-8 -*-
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import wordnet
from retrieval.queryData import tf_idf
from retrieval.queryData import tokenize_text
from image_logic.imageProcessor import load_image_list

def get_image_labels():
    image_labels = []
    with open('image_logic/image_labels.txt') as f:
        for line in f:
            image_labels.append(line.rstrip())
    return image_labels

def imageQuery(queries):
    
    #support synonyms
    def get_synonyms(word):
        synonyms = []
        for syn in wordnet.synsets(word.strip()):
            for l in syn.lemmas():
                synonyms.append(l.name())
        return (synonyms)
    
    queries_with_synonyms = map(lambda x: " ".join(get_synonyms(x) + ([x] * 15)) , queries)
    image_labels = get_image_labels()
    
    vec_images, vec_queries = tf_idf(image_labels, queries_with_synonyms, tokenize_text)

    sim_matrix = cosine_similarity(vec_images, vec_queries)
    
    ranked_images = np.argsort(-sim_matrix[:, 0])
    listed = [sim_matrix[i] for i in ranked_images[:4]]
    
    flat_list = [item for sublist in listed for item in sublist]
    non_zero_vals = len(list(filter(lambda x: x > 0.3, flat_list)))
    
    image_paths = []
    imageList = list(map(lambda x: x[1], load_image_list('image_logic/data/images')))
    for index in ranked_images[:non_zero_vals]:
        image_paths.append( imageList[index].replace("\\","/"))
    
    return image_paths

