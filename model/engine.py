import pickle
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PKL_DIR = os.path.join(BASE_DIR, 'pkl')

def load_pickle(filename):
    path = os.path.join(PKL_DIR, filename)
    with open(path, 'rb') as f:
        return pickle.load(f)

tfidf = load_pickle('tfidf_vectorizer.pkl')
tfidf_matrix = load_pickle('tfidf_matrix.pkl')
cosine_sin = load_pickle('cosine_similarity.pkl')
df_1 = load_pickle('processed_books.pkl')
indices = load_pickle('title_indices.pkl')

def recommend_books(title, cosine_sim=cosine_sin, top_n=5):
    title = title.lower().strip()
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[0:top_n+1]
    book_indices = [i[0] for i in sim_scores]
    return df_1['ISBN'].iloc[book_indices].tolist()
