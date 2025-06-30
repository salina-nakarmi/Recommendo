import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import os

os.makedirs("./pkl", exist_ok=True)

df = pd.read_csv("../data/final_processed.csv")

df.drop_duplicates(subset =["Book-Title"], inplace=True)

df["Book-Title"]=df["Book-Title"].str.split(r'[./(:]').str[0]

wanted_columns = ["ISBN","Book-Title","Book-Author", "Year-Of-Publication","Publisher", "Genre" , "Description"]
df_1 = df[wanted_columns].copy()
df_1.dropna(inplace=True)

books_we_have = df_1["ISBN"].unique()

df_1["Book-Title"] = df_1["Book-Title"].str.lower().str.strip()
df_1 = df_1.drop_duplicates(subset =["Book-Title"])
df_1 = df_1.reset_index(drop=True)

df_1["Combined_feature"] = df_1["Book-Title"] + " " + df_1["Book-Author"] + " " + df_1["Publisher"] + " " + df_1["Genre"] + " " +df_1["Description"]

tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(df_1["Combined_feature"])

sparse_size = (
    tfidf_matrix.data.nbytes +
    tfidf_matrix.indices.nbytes +
    tfidf_matrix.indptr.nbytes
)

cosine_sin = cosine_similarity(tfidf_matrix, tfidf_matrix)

indices = pd.Series(df_1.index,index= df_1["Book-Title"]).drop_duplicates()

with open("./pkl/tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(tfidf, f)

with open("./pkl/tfidf_matrix.pkl", "wb") as f:
    pickle.dump(tfidf_matrix, f)

with open("./pkl/cosine_similarity.pkl", "wb") as f:
    pickle.dump(cosine_sin, f)

with open("./pkl/processed_books.pkl", "wb") as f:
    pickle.dump(df_1, f)

with open("./pkl/title_indices.pkl", "wb") as f:
    pickle.dump(indices, f)
