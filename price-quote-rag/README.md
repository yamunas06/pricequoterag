# Price Quote RAG

## Introduction

Simple chatBOT which takes list of support runbooks as input and comes up with custom ChatBOT. Developed using RAG model. 


## Features

* ATM this project reads the support runBooks which are manually copied into resources/supportRunbooks
* Retrieves embedding from it. Stores it in a local Vector DB.
* ATM this project uses basic HuggingFaceEmbeddings, almost no hyper parameters
* Calls LLM running locally on Ollama with user's input query. 
* Application retrieves the runbooks for the user query from vector database. 
* Runbooks retrieved as embeddings is fed to LLM for generating response

## Installation

To get started, you'll need to:

1. Pyhon > 3.9. For some resaon Transformers were not getting insalled if python version was less than 3.9
2. pip3 install -r requirements.txt
3. pip3 install -U langchain-community # This is required because this project uses longchain

## Prerequisites
1. Install Ollama locally. https://ollama.com/library/llama3
2. Install and Run Llama3 locally "ollama run llama3"

## Usage

Here's how to use our project:

1. pip3 install -r requirements
2. python src/main.py
3. By default Llama3 LLM is used in this project. You can pass your own LLM to main.py. However make sure LLM is running locally using Ollama
4. ATM only 3 runBooks are loaded in project resources/supportRunBooks
5. Sample prompts
     - How can i fix price csv uploader
     - How can I fix Cancelled prices

## Improvements
1. Good runBooks
2. Ability to read confluence runBooks to build embedding rather than manually copy/pasting it in project
3. ATM embeddings are done when app starts. Ideally this should be separate process. It should also store the vectors of support runBooks in a VectorDB
4. Retrieval is not ranked. Ideally come up with config based ranking framework for retrieval
5. Retrieval to consider previous feedbacks ?
6. Lot of Hardwiring is done in this project, starting from embedding. Ideally we should be implementing these changes using Azure PromptFlow ?
7. Ability to evaluate the response of model
8. Tune Hyper parameters like Temperature etc. Check the response accuracy
9. Automated evaluation of response

## Contributing

* Contact prashanth.gundurao@tesco.com, if you would like to contribute to this project.
