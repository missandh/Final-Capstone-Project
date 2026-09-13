"""PII masking and prompt injection checks."""

from __future__ import annotations

import re
from typing import List

PHONE_REGEX = r"(?:\+91[\-\s]?)?[6-9]\d{9}\b"
INJECTION_KEYWORDS = [
    "ignore previous instructions",
    "system prompt",
    "drop table",
    "you are now evil",
    "bypass security",
    "jailbreak",
]


def mask_pii_contact(text: str) -> str:
    """Masks Indian phone numbers to preserve privacy in logs and agent contexts."""
    return re.sub(PHONE_REGEX, "[PHONE]", text)


def detect_prompt_injection(text: str) -> bool:
    """Checks for obvious prompt-injection attempts."""
    lowered = text.lower()
    return any(kw in lowered for kw in INJECTION_KEYWORDS)


def check_groundedness(response: str, context: str) -> bool:
    """Ensures terms presented in response are grounded within retrieved context."""
    if not context or "I apologize, but I do not have verified policy information" in response:
        return True
    resp_words = set(re.findall(r"\w{5,}", response.lower()))
    context_words = set(re.findall(r"\w{5,}", context.lower()))
    overlap = resp_words.intersection(context_words)
    return len(overlap) >= 2


def mask_pii(text: str) -> str:
    """Backward-compatible generic PII masking helper."""
    masked = mask_pii_contact(text)
    masked = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "[EMAIL]", masked)
    masked = re.sub(r"\b\d{12,19}\b", "[ID]", masked)
    return masked


def detect_injection_attempts(text: str) -> List[str]:
    """Very lightweight prompt injection detection heuristics."""
    suspicious = []
    patterns = [
        "ignore previous instructions",
        "system prompt",
        "developer override",
        "act as",
        "bypass policy",
        "ignore all rules",
        "jailbreak",
    ]
    lower = text.lower()
    for pattern in patterns:
        if pattern in lower:
            suspicious.append(pattern)
    return suspicious
