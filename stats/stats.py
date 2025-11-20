import numpy as np

## baseline from assignment 1

query_file = './data/queries.txt'
qrels_file = './data/qrels.txt'

def get_queries():
    return load_queries(query_file);

def get_ndcg(results):
    return compute_ndcg(results, load_qrels(qrels_file))

def get_precision(results):
    return compute_precision(results, load_qrels(qrels_file))

def compute_ndcg(results, qrels, k=10):
    def dcg(relevances):
        # return sum((2 ** rel - 1) / np.log2(i + 2) for i, rel in enumerate(relevances[:k]))
        dcg_simple = sum(rel / np.log2(i + 2) for i, rel in enumerate(relevances[:k]))
        return dcg_simple

    ndcg_scores = []
    for qid, query_results in results.items():
        if qid not in qrels:
            # print(f"Query {qid} not found in qrels")
            continue
        relevances_current = [qrels[qid].get(docid, 0) for docid, _ in query_results]
        idcg = dcg(sorted(qrels[qid].values(), reverse=True))
        if idcg == 0:
            #print(f"IDCG is 0 for query {qid}")
            continue
        ndcg_scores.append(dcg(relevances_current) / idcg)

    if not ndcg_scores:
        print("No valid NDCG scores computed")
        return 0.0
    return np.mean(ndcg_scores)

def compute_precision(results, qrels, k=10, thresh=1):

    all_precisions = []

    for qid, query_results in results.items():
        if qid not in qrels:
            continue
        k_ranked_docs = []

        for query_res in query_results[:k]:
            k_ranked_docs.append(query_res[0])

        rel_count = 0

        for doc in k_ranked_docs:
            score = qrels[qid].get(doc, 0)
            if (score >= thresh):
                rel_count += 1

        all_precisions.append(rel_count / k)

    if all_precisions == []:
        return 0.0        

    return float(np.mean(all_precisions))

def load_queries(query_file):
    with open(query_file, 'r') as f:
        return [line.strip() for line in f]


def load_qrels(qrels_file):
    qrels = {}
    with open(qrels_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                qid, docid, rel = parts
            else:
                raise Exception(f"incorrect line: {line.strip()}")

            if qid not in qrels:
                qrels[qid] = {}
            qrels[qid][docid] = int(rel)
    return qrels