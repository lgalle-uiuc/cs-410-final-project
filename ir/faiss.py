import numpy as np
import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer

# https://medium.com/@mrcoffeeai/faiss-vector-database-be3a9725172f

df = pd.read_csv('./corpus/thread_data.csv')
model = SentenceTransformer('all-MiniLM-L6-v2')
df['embedding'] = df['chunk'].apply(model.encode)
vector = model.encode(df['chunk'])
dim = vector.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(vector)   

def query(search_query, results):
    encoded = model.encode(search_query)
    vec = np.array(encoded).reshape(1, -1)
    distance, pos = index.search(vec, results)
    return df["chunk"].iloc[pos[0]]