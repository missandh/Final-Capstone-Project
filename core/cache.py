"""Normalized query cache."""

from __future__ import annotations

import hashlib
from typing import Any, Dict


class QueryCache:
    """Small normalized cache for repeated retrieval queries."""

    def __init__(self):
        self._cache: Dict[str, Any] = {}

    def normalize(self, query: str) -> str:
        return " ".join(query.lower().split())

    def get(self, query: str):
        return self._cache.get(self.normalize(query))

    def set(self, query: str, value: Any) -> None:
        self._cache[self.normalize(query)] = value


class NormalizedResponseCache:
    """Hash-based cache for normalized responses."""

    def __init__(self):
        self.cache: Dict[str, str] = {}
        self.hits = 0
        self.misses = 0

    def _normalize_key(self, query: str) -> str:
        clean = " ".join(query.strip().lower().split())
        return hashlib.sha256(clean.encode()).hexdigest()

    def get(self, query: str):
        key = self._normalize_key(query)
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None

    def set(self, query: str, response: str):
        key = self._normalize_key(query)
        self.cache[key] = response
