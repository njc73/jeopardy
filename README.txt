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
- jeopardy.py splits JEOPARDY_CSV.csv into 8, 16, 32, 64, and 128 clusters
- subcat.py splits history.txt into 8 subclusters
    ! i'd like to modify jeopardy.py to automatically output each cluster to a text file in a folder ... watch this space
- gooey.py is ugly af but lets you search data.tsv by category
    - data.tsv is a cleaned version of combined_season1-39.tsv

feel free to contribute :P# jeopardy
