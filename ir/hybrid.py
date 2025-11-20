from ir.semantic import query as semantic_query
from ir.keyword import query as keyword_query

def query_with_stats(query_list, keyword_algorithm:str, k=3):
    results = {}
    for i, q in enumerate(query_list):
        hits = query(q, keyword_algorithm, k)
        results[str(i)] = [(hit['doc_id'], hit['score']) for hit in hits]
    return results

def query(query: str, keyword_algorithm:str, k=3):
    semantic_results = semantic_query(query, 5)
    keyword_results = keyword_query(query, keyword_algorithm)

    # goal is to find max in each, normalize each to a range between 0 and 1, add them together, and then return the top results
    max_sem = 0.0000001
    for res in semantic_results:  
        if res['score'] > max_sem:
            max_sem = res['score']

    max_kw = 0.0000001
    for res in keyword_results:
        if res['score'] > max_kw:
            max_kw = res['score']

    combined_list = {}

    for res in semantic_results:
        res['normalized_score'] = res['score'] / max_sem
        combined_list[res['doc_id']] = res


    for res in keyword_results:
        if res['doc_id'] in combined_list: 
            combined_list[res['doc_id']]['normalized_score'] += res['score'] / max_kw
        else:
            res['normalized_score'] = res['score'] / max_kw
            combined_list[res['doc_id']] = res

    ranked_results = sorted(
        combined_list.values(),
        key=lambda x: x['normalized_score'],
        reverse=True
    )

    print("\nHybrid Search Result\n")
    print(ranked_results)
    
    return ranked_results[:k]

    

    
    
