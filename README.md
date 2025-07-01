hi thomas

i didnt feel like sending a bunch of updated files and stuff so i put everything in a github repository

things you need to have installed (all via pip)
!!! i recommend setting up a virtual envionment (https://docs.python.org/3/library/venv.html) but you don't Have to
|____ matplotlib
|____ pandas
|____ numpy
|____ kneed
|____ sentence-transformers
|____ scikit-learn
|____ tf-keras

- elbow.py gives optimal k (# clusters)
- jeopardy.py uses optimal k from elbow.py (46) and splits data.tsv into k clusters, exporting each into a new (or existing) folder called "clusters"
    - data.tsv is a cleaned version of combined_season1-39.tsv
- subcat.py splits history.txt (example file, you can change the path and use a new txt file from clusters/) into 8 subclusters
- gooey.py lets you search data.tsv by category

feel free to contribute :P