"""Chroma indexing utilities for the clinical knowledge base."""

from __future__ import annotations

import json
import re

import chromadb
from chromadb.utils import embedding_functions

EMBED_MODEL = "all-MiniLM-L6-v2"
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)


def fixed_size_chunking(text, chunk_size=180, overlap=40):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end].strip())
        if end == len(text):
            break
        start += (chunk_size - overlap)
    return chunks


def sentence_chunking(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]


def index_collections():
    client = chromadb.Client()

    col_fixed = client.get_or_create_collection(name="kb_fixed", embedding_function=ef)
    col_sentence = client.get_or_create_collection(name="kb_sentence", embedding_function=ef)

    with open("data/knowledge_base.json", "r", encoding="utf-8") as handle:
        kb = json.load(handle)

    for doc in kb:
        fixed_chunks = fixed_size_chunking(doc["content"])
        for i, chunk in enumerate(fixed_chunks):
            col_fixed.upsert(
                ids=[f"{doc['doc_id']}_f_{i}"],
                documents=[chunk],
                metadatas=[{"doc_id": doc["doc_id"], "topic": doc["topic"]}],
            )

        sent_chunks = sentence_chunking(doc["content"])
        for j, sentence in enumerate(sent_chunks):
            col_sentence.upsert(
                ids=[f"{doc['doc_id']}_s_{j}"],
                documents=[sentence],
                metadatas=[{"doc_id": doc["doc_id"], "topic": doc["topic"]}],
            )

    return client, col_fixed, col_sentence
