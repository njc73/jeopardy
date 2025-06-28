#ok i lied i made a k-means graph

from sentence_transformers import SentenceTransformer  #use sentence instead of tf-idf, we want to vectorise whole sentences
from sklearn.cluster import KMeans
import pandas as pd
from matplotlib import pyplot as plt
import os
import time
from kneed import KneeLocator

ts = time.time()

os.environ["TOKENIZERS_PARALLELISM"] = "false"

print("determining optimal k value...")

model = SentenceTransformer('all-MiniLM-L6-v2') 

#this bit gets the categories from csv
j = pd.read_csv("JEOPARDY_CSV.csv")
j.columns = j.columns.str.strip()
jc = j["Category"]

#categories into list
categories = [i for i in jc.unique()]

#get embeddings for minilm
embeddings = model.encode(categories)

inertias = []
kmax = 200
ks = range(1, kmax, 5)  

for k in ks:
    kmeans = KMeans(n_clusters = k, random_state = 1234567890)
    kmeans.fit(embeddings)
    inertias.append(kmeans.inertia_)

knee = KneeLocator(ks, inertias, curve='convex', direction='decreasing')

plt.figure(figsize=(8, 6))
plt.plot(ks, inertias, marker = 'o', color = 'pink', linestyle = '--')
plt.title('elbow :D')
plt.xlabel('N_clusters (k)')
plt.ylabel('Inertia')
plt.xticks(ks)
plt.grid(True)

te = time.time()

def mintosec(x):
    min = (x // 60)
    sec = (x - (60 * min))
    return f"{(min):.0f} min, {(sec):.2f} sec"

print(f"Optimal k: {knee.elbow}") #46

print(f"Time elapsed; {mintosec(te - ts)}") #about two minutes

plt.show()