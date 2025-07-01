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

model = SentenceTransformer("all-MiniLM-L6-v2") #no need for anything more powerful imo (plus this one is fast)

#this bit gets the categories from csv
j = pd.read_csv("data.tsv")
j.columns = j.columns.str.strip()
jc = j["category"]

#categories into list
categories = [i for i in jc.unique()]

print("encoding the ᓚᘏᗢegories...")

#get embeddings for minilm
embeddings = model.encode(categories)

k = 46 #from elbow.py

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

# make folder for outputs 
# !!! this will rewrite (erase) the contents of the clusters folder each time the code is run
if os.path.exists("clusters"):
    for filename in os.listdir("clusters"):
        file_path = os.path.join("clusters", filename)
        if os.path.isfile(file_path):
            os.unlink(file_path) 
else:
    os.makedirs("clusters")

print(f"exporting {k} clusters to 'clusters' folder...")

for id, catlist in clustered.items():

    catname = next(name for cid, name in names if cid == id) #get cluster name
    
    # this bit makes sure the file name doesnt have any weird characters (like \" or &)
    catsafe = "".join(c if c.isalnum() or c in (" ", "-", "_") else "" for c in catname)
    filename = f"clusters/{catsafe[:50]}.txt"  # [:50] makes sure the file names arent too long
    
    with open(filename, "w", encoding="utf-8") as f: #opens each txt file
        f.write(f"Category: {catname}\n") 
        f.write("-" * 50 + "\n") # hline 
        for cat in catlist:
            f.write(cat + "\n") # add category

# set output source back to terminal
sys.stdout = o

te = time.time()
print("all done! ᕙ( •̀ ᗜ •́ )ᕗ ") 
print(f"elapsed time: {(te - ts):.2f} s") # approx. 16 sec