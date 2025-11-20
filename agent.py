# https://docs.langchain.com/oss/python/langchain/rag

import os
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from ir.semantic import query as semantic_query
from ir.keyword import query as keyword_query
from ir.hybrid import query as hybrid_query
from ir.semantic import query_with_stats as semantic_query_stats
from ir.keyword import query_with_stats as keyword_query_stats
from ir.hybrid import query_with_stats as hybrid_query_stats
from stats.stats import get_queries
from stats.stats import get_ndcg as get_ndcg_stats
from stats.stats import get_precision as get_precision_stats

api_key = os.getenv("API_KEY")
os.environ["OPENAI_API_KEY"] = api_key

model = init_chat_model("gpt-4.1")

@tool
def get_ndcg(query_results):
    """Computes ndcg for the supplied list of query results"""
    return get_ndcg_stats(query_results)

@tool
def get_precision(query_results):
    """Computes precision for the supplied list of query results"""
    return get_precision_stats(query_results)

@tool
def retrieve_semantic(query: str):
    """Retrieves gmail information using the semantic information retrieval method"""
    return semantic_query(query, 2)

@tool
def retrieve_semantic_stats(queries):
    """Runs a collection of queries against semantic search and returns the information of which docs were returned by which query"""
    return semantic_query_stats(queries, 2)

@tool
def retrieve_keyword(query: str, algorithm:str):
    """Retrieves gmail information using the keyword information retrieval method. The algorithem can be bm25, qld, or rm3"""
    return keyword_query(query, algorithm)

@tool
def retrieve_keyword_stats(queries, algorithm:str):
    """Runs a collection of queries against keyword search and returns the information of which docs were returned by which query"""
    return keyword_query_stats(queries, algorithm)

@tool
def retrieve_hybrid(query: str, keyword_algorithm:str):
    """Retrieves gmail information using the hybrid information retrieval method. The keyword_algorithm can be bm25, qld, or rm3"""
    return hybrid_query(query, keyword_algorithm)

@tool
def retrieve_hybrid_stats(queries, keyword_algorithm):
    """Runs a collection of queries against keyword search and returns the information of which docs were returned by which query"""
    return hybrid_query_stats(queries, keyword_algorithm)

@tool
def get_sample_query_list():
    """Gets the sample list of queries for analysis by any of the information retrieval accuracy mechanisms (ndcg, precision, etc.)"""
    return get_queries()

tools = [retrieve_semantic, retrieve_keyword, retrieve_hybrid, get_sample_query_list, retrieve_semantic_stats, retrieve_keyword_stats, retrieve_hybrid_stats, get_ndcg, get_precision]

def get_agent():
    return create_react_agent(model, tools, prompt='Your goal is to help with information retrieval tasks related to a gmail inbox. ' \
    'When asked to retrieve threads and summarize information, display the thread_id (for example TH-0001) and summarize each retrieved thread in a 2-3 bullet points. ' \
    'Do this for each returned thread. If asked to run tests, run the' \
    'test specified by the user and return the relevant metrics')