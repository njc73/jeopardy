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

#easy list
h = open("history.txt").readlines() #open text file of single cluster in same directory

hist = [i[:-1] for i in h] #trim \n

print("encoding the ᓚᘏᗢegories...")
#get embeddings for minilm
model = SentenceTransformer('all-MiniLM-L6-v2') 
embeddings = model.encode(hist)

k = 8

clustering_model = KMeans(n_clusters=k)
clustering_model.fit(embeddings)
labels = clustering_model.labels_

print(f"splitting into {k} subclusters...")

#clustering
clustered = {}
for label, category in zip(labels, hist):
    clustered.setdefault(label, []).append(category)

#this should give them normal names instead of stupid numbers!!!
centroids = clustering_model.cluster_centers_
names = [] 
catlist = [] # for printing

for id, list in clustered.items():
    cluster_centroid = centroids[id] # finds the "centre" of each cluster
    cossim = cosine_similarity([cluster_centroid], embeddings) #calc similarities of each category to centroid
    catname = hist[np.argmax(cossim)] #index to that category
    names.append((id, catname)) #add to category names
    catlist.append(catname)

#store original output source (terminal) in variable  
o = sys.stdout

#print EVERYTHING!!!! (to text file)
with open(f'{k}_subclusters.txt', 'w') as f:
    sys.stdout = f #changes output to file from terminal 
    print(f"Subcluster centroids: {catlist}")
    for id, list in clustered.items():
        subcategory = next(name for cid, name in names if cid == id)
        print(f"\nSubcategory: {subcategory}")  # voila
        for cat in list:
            print("  ", cat)

# set output source back to terminal
sys.stdout = o

te = time.time()

print("all done! ଘ(੭*ˊᵕˋ)੭* ੈ♡‧₊˚") 
print(f"elapsed time: {(te - ts):.2f} s") # approx. 8 sec