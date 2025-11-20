# cs-410-final-project

This project provides an agent to be able to query data synced from a gmail account. It is aimed at being a POC of intergrating gmail
(or other email servers) into an LLN to allow a sales managers to easily search and summarize their sales teams communications. 
It can query data using semantic search, keyword search, hybrid search, and can even run sample queries to report statistics on its information retrieval mechanisms using precision@10 and ndcg using provided sample queries.

## Setup

Instructions are for Mac OSX only

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

Then, run 

```python3 init.py```

Your gmail account will be populated with sample thread data, and the corpus/thread_data.csv will be deleted and recreated, or created if you deleted it manually.

### Setting up your agent

I am using OpenAI as my LLM to run this application. You can choose whatever LLM (running something locally for free with ollama for example) you wish, but know that this has been tested with OpenAI only. 

The OpenAI setup follows these instructions (you can stop before install the OpenAPI SDK and Run an API Call)

https://platform.openai.com/docs/quickstart

Once you have your key, add it to your .env file

API_KEY=sk-proj-the-rest-of-your-key

## Running the application

Now that setup is complete, we can run our application. You can start by running in your terminal:

```python3 main.py```

Ask the agent a question, and then hit "Enter"

There are 2 categories of questions:

First, you can ask questions about the gmail data. Anything that one might like to know as a sales manager should be available. Some examples:

 - Give me all of the email threads that have executive involvement. Use hybrid search to find them with bm25
 - Give me the most relevant email thread that is selling Google Gemini using keyword seach and qld
 - Find all threads that are selling product to banks. Give me only the first thread. Use semantic search

Second, you can ask the agent to evaluate its own performance. 

Some examples:

 - Compute ndcg for the sample queries using semantic search
 - Compute ndcg for the sample queries using hybrid search and rm3
 - Computer ndcg for the sample queries using keyword search and bm25
 - Compute precision for the sample queries using hybrid search with bm25
 - Compute precision for the sample queries using keyword search with qld

 Sample data exists in the data/qrels.txt and data/queries.txt file for computing these metrics. You are free to add your own examples as well. 