import streamlit as st
from oraculo.functions.data import get_collections
from tqdm import tqdm
import chromadb
from chromadb.config import Settings
import hashlib
import logging
from typing import List
import pandas as pd
from chromadb.api.types import QueryResult


def init_db():
    client = chromadb.Client(
        Settings(persist_directory=".chromadb", chroma_db_impl="duckdb+parquet")
    )
    collections = client.list_collections()
    del client
    return collections


def query_db(collection_name, query_texts, n_results):
    client = chromadb.Client(
        Settings(persist_directory=".chromadb", chroma_db_impl="duckdb+parquet")
    )
    collection = client.get_collection(collection_name)
    result = collection.query(query_texts=query_texts, n_results=n_results)
    logging.info(result)

    del client
    del collection
    return result


def convert_json_to_records(json_data: QueryResult) -> List[dict]:
    ids = json_data["ids"]
    embeddings = json_data["embeddings"]
    documents = json_data["documents"]
    metadatas = json_data["metadatas"]
    distances = json_data["distances"]

    num_records = len(ids[0])
    records = []

    for i in range(num_records):
        record = {
            "ids": ids[0][i],
            "embeddings": None if embeddings is None else embeddings[0][i],
            "documents": documents[0][i],
            "metadatas": metadatas[0][i],
            "distances": distances[0][i],
        }
        records.append(record)

    return records


def create_streamlit_card(json_data):
    for key, value in json_data.items():
        if isinstance(value, dict):
            st.write(f"{key.capitalize()}:")
            for sub_key, sub_value in value.items():
                st.write(f"  - {sub_key.capitalize()}: {sub_value}")
        else:
            st.write(f"{key.capitalize()}: {value}")
    st.write("---")


# create a dropdown menu with all the collections
collection_name = st.sidebar.selectbox(
    "Select a collection",
    get_collections(),
)

# create a search box
search_query = st.text_input("Search", "")

# add a slider to select the number of results
n_results = st.slider("Number of results", 1, 20, 5)

# create a button to search and query the database
if st.button("Search"):
    result = query_db(collection_name, [search_query], n_results)
    results = convert_json_to_records(result)

    for result in results:
        create_streamlit_card(result)