"""Precision and recall helpers for retrieval evaluation."""

from __future__ import annotations

from typing import Iterable, List, Sequence


def precision_at_k(retrieved: Sequence[str], relevant: Sequence[str], k: int | None = None) -> float:
    """Compute precision at k for a retrieved list."""
    if k is None:
        k = len(retrieved)
    k = min(k, len(retrieved))
    if k == 0:
        return 0.0
    relevant_set = set(relevant)
    retrieved_top_k = retrieved[:k]
    hits = sum(1 for item in retrieved_top_k if item in relevant_set)
    return hits / k


def recall_at_k(retrieved: Sequence[str], relevant: Sequence[str], k: int | None = None) -> float:
    """Compute recall at k for a retrieved list."""
    if k is None:
        k = len(retrieved)
    k = min(k, len(retrieved))
    if not relevant:
        return 0.0
    relevant_set = set(relevant)
    retrieved_top_k = retrieved[:k]
    hits = sum(1 for item in retrieved_top_k if item in relevant_set)
    return hits / len(relevant_set)


def average_precision(retrieved: Sequence[str], relevant: Sequence[str]) -> float:
    """Compute average precision for a ranked list."""
    if not retrieved:
        return 0.0
    relevant_set = set(relevant)
    precision_sum = 0.0
    hits = 0
    for idx, item in enumerate(retrieved, start=1):
        if item in relevant_set:
            hits += 1
            precision_sum += hits / idx
    if not relevant_set:
        return 0.0
    return precision_sum / len(relevant_set)
