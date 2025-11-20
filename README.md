# cs-410-final-project

This project provides an agent to be able to query data synced from a gmail account. It can query data using semantic search, keyword search, 
hybrid search, and can even run sample queries to report statistics on its information retrieval mechanisms using precision@10 and ndcg


## Setup

### Local Environment

Follow instructions listed here to set up a pyserini environment in conda:

https://github.com/castorini/pyserini/blob/master/docs/installation.md#pypi-installation-walkthrough

Run the following commands:

```pip install -r requirements.txt```
```conda install -c conda-forge langgraph```
```pip install langchain langchain-text-splitters langchain-community bs4```

Create a .env file in the root of the project. It will be populated with data at a later point. 

### Syncing Data to/from the Gmail account

You can skip this step if you wish, as the corpus/thread_data.csv is already sitting in the repository, which is the synced from the google account. 

Create a new gmail account (this is critical, this integration reads EVERYTHING from the gmail account) and create an app password. 

Follow the steps below to create your app password:

https://support.google.com/mail/answer/185833?hl=en

In your .env file, set the following properties:

GMAIL_EMAIL=your-email
GMAIL_APP_PASSWORD=your-password

1. Compute ndcg for the sample queries using semantic search
2. Compute ndcg for the sample queries using hybrid search and bm25
3. Computer ndcg for the sample queries using keyword search and rm3
2. Compute precision for the sample queries using hybrid search with bm25
Compute precision for the sample queries using keyword search with qld