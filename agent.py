# https://docs.langchain.com/oss/python/langchain/rag

import os
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from ir.semantic import query as semantic_query
from ir.keyword import query as keyword_query


api_key = os.getenv("API_KEY")
os.environ["OPENAI_API_KEY"] = api_key

model = init_chat_model("gpt-4.1")

@tool
def retrieve_semantic(query: str):
    """Retrieves gmail information using the semantic information retrieval method"""
    return semantic_query(query, 2)

@tool
def retrieve_keyword(query: str, algorithm:str):
    """Retrieves gmail information using the keyword information retrieval method. The algorithem can be bm25, qld, or rm3"""
    return keyword_query(query, algorithm)

tools = [retrieve_semantic, retrieve_keyword]

def get_agent():
    return create_react_agent(model, tools, prompt='Summarize each thread you receive by listing the id of the thread, and then the synthesizes information about the thread in 2-3 bullet points')