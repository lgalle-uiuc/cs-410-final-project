import numpy as np
import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer

# https://medium.com/@mrcoffeeai/faiss-vector-database-be3a9725172f

def init():
    df = pd.read_csv('./corpus/thread_data.csv')
    model = SentenceTransformer('all-MiniLM-L6-v2')
    df['Embedding'] = df['chunk'].apply(model.encode)
    vector = model.encode(df['chunk'])
    dim = vector.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vector)   

    search_query = 'Google Gemini'
    encode_pre = model.encode(search_query)
    encode_pre.shape

    #FAISS expects 2d array, so next step we are converting encode_pre to a 2D array
    svec = np.array(encode_pre).reshape(1,-1)


    #We will get euclidean distance and index of the 2 nearest neighbours
    distance,pos = index.search(svec,k=1)

    print(df['chunk'].iloc[pos[0]])
