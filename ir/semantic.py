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
index = faiss.IndexFlatIP(dim)
faiss.normalize_L2(vector)
index.add(vector)   

def query(search_query, results, threshold=.3):
    encoded = model.encode(search_query)
    vec = np.array(encoded).reshape(1, -1)
    faiss.normalize_L2(vec)
    similarity, pos = index.search(vec, results)
    chunks = df["chunk"].iloc[pos[0]]    

    docs = []
    for i, chunk in enumerate(chunks):
        if similarity[0][i] > threshold:
            doc = {
                "doc_id" : df.iloc[pos[0][i]].thread_id, 
                "score" : similarity[0][i],
                "page_content" : chunk
            }
            docs.append(doc)
    return docs