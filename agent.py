# https://docs.langchain.com/oss/python/langchain/rag

import os
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from ir.faiss import query as faiss_query


api_key = os.getenv("API_KEY")
print(api_key)
os.environ["OPENAI_API_KEY"] = api_key

model = init_chat_model("gpt-4.1")

@tool
def retrieve_faiss(query: str):
    """Retrieve information to help answer a query."""
    retrieved_docs = faiss_query(query, 2)

    return retrieved_docs

tools = [retrieve_faiss]

def get_agent():
    return create_react_agent(model, tools)