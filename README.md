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

## Code Explanation

### Mocking and Retrieving Data from the gmail account

#### Mocking

The mocking of email data is done over the Gmail SMTP server via SSL. It uses the google app username and password to make a connection to the server to perform requests. To generate email threads, we are grabbing the email thread id from the email_threads.csv data, and stamping that into the message id in google to be able to reference the thread ids when we pull it back down into our local. We also use these same thread ids in the message id to be able to thread messages together in the references/reply-to headers

#### Syncing

We retrieve the email messages over IMAP and using the google app creds as in mocking. We pull all messages from the gmail server and reconstruct each of the threads from the message id headers, reference headers, and reply to headers that we referenced before. Once the threads are rebuilt, we save them into our corpus folder with the corresponding thread ids and content, all merged into a single row. 

### Semantic Search

Semantic seach is done using faiss. We read the thread_data.csv we save to the corpus file, create a pandas dataframe, encode it using our sentence transformers, and then store it into the faiss vector database with capabilities for cosine distance search. When searching, we first encode the query, find the nearest cosine distance neighbors, ensure it is over the threshold provided by the caller, and then return a dictionary with the results. 

### Keyword Search

Keyword search uses the same mechanisms used in assigment 1, with options of bm25, rm3, and qld. We've prepopulated the .jsonl document in the corpus folder, and then through the initial load we process these files and have lucene generate the documents into our index. We then run keyword search based off of the algorithm provided by the caller. 

### Hybrid Search

This calls both the semantic search and keyword search and combines them into a single result. We do this by normalizing each of the results from the semantic and the keyword search by dividing each of the scores by the max score of the group, adding the normalized scores from semantic and keyword seach together, and then returning the top k results for simplicity.

### Self Analysis

We have populated qrels and queries into the data folder with a collection of example queries and results for testing. Precision and ndcg are assuming that these queries have already been done against one of the IR mechanisms above, and the results are fed into these methods, and matched against the qrels. The result is populated and returned to the user. 

 ### The Agent
The agent is built using langchain. We have an agent file, which wraps all of the relevant functions needed to fulfill the goals of this project. Calls to our OpenAI model are then brokered by langchain, and the result of tools calls can be chained together by the agent to provide the desired result for the user. 
