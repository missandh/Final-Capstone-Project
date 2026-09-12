"""Empirical retrieval utilities with cosine-thresholded scoring."""

from __future__ import annotations

from typing import Iterable, List, Sequence

import numpy as np


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    """Compute cosine similarity between two vectors."""
    a_arr = np.asarray(a, dtype=float)
    b_arr = np.asarray(b, dtype=float)
    denom = np.linalg.norm(a_arr) * np.linalg.norm(b_arr)
    if np.isclose(denom, 0.0):
        return 0.0
    return float(np.dot(a_arr, b_arr) / denom)


def filter_by_threshold(results: Iterable[tuple[str, float]], threshold: float = 0.25) -> List[tuple[str, float]]:
    """Keep only results whose similarity exceeds the selected threshold."""
    return [(doc, score) for doc, score in results if score >= threshold]


def score_candidates(query_vector: Sequence[float], candidate_vectors: Sequence[Sequence[float]]) -> List[tuple[str, float]]:
    """Return scored candidate texts in ranking order."""
    scores = []
    for idx, vector in enumerate(candidate_vectors):
        score = cosine_similarity(query_vector, vector)
        scores.append((f"doc_{idx}", score))
    return sorted(scores, key=lambda item: item[1], reverse=True)
