import pandas as pd

def load_dataset():
    return pd.read_csv("data/finalclean_file.csv")

def get_unique_genre(df, min_count=10):
    genre_counts = df['Genre'].value_counts()

    frequent_genres = genre_counts[genre_counts > min_count].index.tolist()
    frequent_genres.sort()
    
    print(frequent_genres)
    return frequent_genres
