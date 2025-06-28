# INSTALL THESE FIRST (with pip)
# |____ sentence-transformers
# |____ scikit-learn
# |____ tf-keras

from sentence_transformers import SentenceTransformer  
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import sys
import numpy as np
import time
import os

ts = time.time()

os.environ["TOKENIZERS_PARALLELISM"] = "false" #got rid of dumb parallelism warning

model = SentenceTransformer('all-MiniLM-L6-v2') #no need for anything more powerful imo (plus this one is fast)

#this bit gets the categories from csv
j = pd.read_csv("JEOPARDY_CSV.csv")
j.columns = j.columns.str.strip()
jc = j["Category"]

#categories into list
categories = [i for i in jc.unique()]

print("encoding the ᓚᘏᗢegories...")

#get embeddings for minilm
embeddings = model.encode(categories)

ks = [8, 16, 32, 64, 128]
# i made a kmeans elbow curve and the optimal k seems to be well over 50
# but tbh i think 32 is a good sweet spot idk if i know what a realistic value would be

for k in ks:
    clustering_model = KMeans(n_clusters=k)
    clustering_model.fit(embeddings)
    labels = clustering_model.labels_

    print(f"splitting into {k} clusters...")

    #clustering
    clustered = {}
    for label, category in zip(labels, categories):
        clustered.setdefault(label, []).append(category)

    #this should give them normal names instead of stupid numbers!!!
    centroids = clustering_model.cluster_centers_
    names = [] 
    catlist = [] # for printing

    for id, list in clustered.items():
        cluster_centroid = centroids[id] # finds the "centre" of each cluster
        cossim = cosine_similarity([cluster_centroid], embeddings) #calc similarities of each category to centroid
        catname = categories[np.argmax(cossim)] #index to that category
        names.append((id, catname)) #add to category names
        catlist.append(catname)

    #store original output source (terminal) in variable  
    o = sys.stdout

    #print EVERYTHING!!!! (to text file)
    with open(f'{k}_clusters.txt', 'w') as f:
        sys.stdout = f #changes output to file from terminal 
        print(f"Cluster centroids: {catlist}")
        for id, list in clustered.items():
            category = next(name for cid, name in names if cid == id)
            print(f"\nCategory: {category}")  # voila
            for cat in list:
                print("  ", cat)

    # set output source back to terminal
    sys.stdout = o

te = time.time()
print("all done! ᕙ( •̀ ᗜ •́ )ᕗ ") 
print(f"elapsed time: {(te - ts):.2f} s") # approx. 25 sec