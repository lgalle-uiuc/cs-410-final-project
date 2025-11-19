from ir.semantic import query as semantic_query
from ir.keyword import query as keyword_query

def query(query: str, keyword_algorithm:str, results=3):
    semantic_results = semantic_query(query, 5)
    keyword_restuls = keyword_query(query, keyword_algorithm)

    # goal is to find max in each, normalize each to a range between 0 and 1, add them together, and then return the top results
    
    
