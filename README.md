# README <!-- omit in toc -->

## Table of Contents <!--toc omit in  -->



## Overview

This repo contains a sample RAG based solution in promptflow using the SDK.

## Prerequisites

- Python 3.9 or Python 3.10
- promptflow sdk
- OpenAI API Key or Azure OpenAI APIP Key
- Azure Cognitive Search

## Getting Started

### Setup

To install the dependencies, run the following command:

```bash
pip install -r requirements.txt
```

You wll also need to create a `.env` file. To do so, copy the `.env.sample` file and rename it to `.env`. Then, fill in the values for the following variables:

- `AZURE_SEARCH_ENDPOINT` [Required]: The Azure Cognitive Search Endpoint
- `AZURE_SEARCH_ADMIN_KEY` [Required]: The Azure Cognitive Search Admin Key
- `INDEX_NAME` [Required]: The name of the index in Azure Cognitive Search
- `OPENAI_API_TYPE` [Required]: The OpenAI Type (either **azure** or **openai**)
- `OPENAI_API_BASE` [Optional]: The OpenAI base url
- `OPENAI_API_KEY` [Required]: The OpenAI API Key
- `OPENAI_API_VERSION` [Default=2023-05-15]: The version of OpenAI API

### Creating the Connections

Connection are ways for promptflow to interact with services in a secure way. Since this sample interfaces with `Azure Cognitive Search` and `OpenAI`, we need to establish safe and secure ways to use the services.

To create the Azure Cognitive Search connection run the following:

```bash
pf connection create --file src/connections/cognitive_search.yaml --set api_key="<your-api-key>" --set api_base="<your-search-endpoint>"
```

To create the Azure OpenAI connection run the following:

```bash
pf connection create --file src/connections/azure_openai.yaml --set api_key="<your-api-key>" --set api_base="<your-aoai-endpoint>"
```

**NOTE**: The process to create a OpenAI connection is very similar, but you will need to create a `openai` connection and reference it in the `flow.dag.yaml file`.

### Creating your Index

To create the index and populate the data in cognitive search, run the [script](./src/scripts/chunk_and_upload.py) with the following command:

```bash
python -m src.scripts.chunk_and_upload
```

This script will both create the index (based on the index file name in your .env file) and will upload the chunked data from the [langchain introduction file](./assets/langchain_introduction.html).

### Testing the Flow

To test the flow, run the following command:

```bash
pf flow test --flow src/flows/standard/promptflow-rag --inputs text="What is Langchain?"
```

### Running the Flow

To run the flow, run the following command:

```bash
pf run create --flow --flow src/flows/standard/promptflow-rag --data src/flows/standard/promptflow-rag/data.jsonl
```