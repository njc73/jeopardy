first create a venv (https://docs.python.org/3/library/venv.html) if you want, then install necessary packages:

    pip install matplotlib pandas numpy kneed sentence-transformers scikit-learn tf-keras

- elbow.py gives optimal k (# clusters)
- jeopardy.py uses optimal k from elbow.py (46) and splits data.tsv into k clusters, exporting each into a new (or existing) folder called "clusters"
    - data.tsv is a cleaned version of combined_season1-39.tsv
- subcat.py splits history.txt (example file, you can change the path and use a new txt file from clusters/) into 8 subclusters
- gooey.py lets you search data.tsv by category
