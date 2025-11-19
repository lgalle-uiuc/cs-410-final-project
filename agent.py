# https://docs.langchain.com/oss/python/langchain/rag

import bs4
from langchain.agents import create_agent
from langchain.tools import tool
from ir.faiss import query as faiss_query

model = init_chat_model("gpt-4.1")

@tool(response_format="content_and_artifact")
def retrieve_faiss(query: str):
    """Retrieve information to help answer a query."""
    retrieved_docs = faiss_query(query, 2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

tools = [retrieve_faiss]

prompt = (
    "Your job is to take actions on behalf of a user who is attempting to retrieve information from a gmail server. This information is sales threads"
)

def get_agent():
    return create_agent(model, tools, system_prompt=prompt)