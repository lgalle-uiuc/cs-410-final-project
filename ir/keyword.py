import os
import json
from tqdm import tqdm
from pyserini.search.lucene import LuceneSearcher
import numpy as np
import subprocess
import matplotlib.pyplot as plt
import pandas as pd

# code borrowed from mp1

def preprocess_corpus(input_file, output_dir):
    df = pd.read_csv(input_file)
    os.makedirs(output_dir, exist_ok=True)
    jsonl_path = os.path.join(output_dir, "docs.jsonl")
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            doc = {
                "id": str(row["thread_id"]),
                "contents": str(row["chunk"]),
            }
            f.write(json.dumps(doc) + "\n")

def build_index(input_dir, index_dir):
    if os.path.exists(index_dir) and os.listdir(index_dir):
        #print(f"Index already exists at {index_dir}. Skipping index building.")
        return

    cmd = [
        "python", "-m", "pyserini.index.lucene",
        "--collection", "JsonCollection",
        "--input", input_dir,
        "--index", index_dir,
        "--generator", "DefaultLuceneDocumentGenerator",
        "--threads", "1",
        "--storePositions", "--storeDocvectors", "--storeRaw"
    ]
    subprocess.run(cmd, check=True)

directory = 'corpus/keyword'

if not os.path.exists(directory) or not os.listdir(directory):
    preprocess_corpus('./corpus/thread_data.csv', directory)

build_index(directory, 'corpus/keyword/index')

searcher = LuceneSearcher(os.path.join(directory, 'index'))

def query(query, algorithm, bm25_k1=3.15, bm25_b=1, top_k=3):
    if 'bm25' == algorithm:
        print(f"\nRunning bm25 with k1:{bm25_k1} and b:{bm25_b}")
        searcher.set_bm25(k1=bm25_k1, b=bm25_b)
    elif 'qld' == algorithm:
        print(f"\nRunning qld")
        searcher.set_qld()
    elif 'rm3' == algorithm:
        print(f"\nRunning bm25 with rm3 pseudo-relevance feedback")
        searcher.set_bm25(k1=bm25_k1, b=bm25_b)
        searcher.set_rm3(20, 10, 0.5)

    hits = searcher.search(query, k=top_k)
    print(hits[0].lucene_document)
    return [(hit.docid, hit.score, hit.lucene_document.get('raw')) for hit in hits]