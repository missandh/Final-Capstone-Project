"""Chunking utilities for policy and document retrieval."""

from __future__ import annotations

from typing import Iterable, List


def split_fixed_chunks(text: str, chunk_size: int = 200, overlap: int = 40) -> List[str]:
    """Split text into fixed-size chunks with optional overlap."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def split_sentence_chunks(text: str, sentence_delimiters: Iterable[str] = (".", "!", "?")) -> List[str]:
    """Split text by sentence-like delimiters while preserving content."""
    sentences = []
    current = ""
    for char in text:
        current += char
        if char in sentence_delimiters:
            sentence = current.strip()
            if sentence:
                sentences.append(sentence)
            current = ""
    if current.strip():
        sentences.append(current.strip())
    return sentences
