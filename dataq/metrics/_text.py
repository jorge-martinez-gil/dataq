# -*- coding: utf-8 -*-
"""Tokenisation helpers for the text-based dimensions (similarity).

The original ``check_similarity.py`` relied on ``nltk`` resources downloaded at
runtime (``punkt``, ``stopwords``). That is a reproducibility hazard: any host
without network access to the NLTK servers cannot run the metric.

This module preserves the NLTK-backed path when its data is present, and
otherwise falls back to a self-contained tokenizer plus a vendored copy of the
standard NLTK English stop-word list, so the dimension always runs offline.
"""
from __future__ import annotations

import re
from typing import List, Set

# Standard NLTK English stop-word list (vendored for offline reproducibility).
ENGLISH_STOPWORDS: Set[str] = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you",
    "you're", "you've", "you'll", "you'd", "your", "yours", "yourself",
    "yourselves", "he", "him", "his", "himself", "she", "she's", "her",
    "hers", "herself", "it", "it's", "its", "itself", "they", "them",
    "their", "theirs", "themselves", "what", "which", "who", "whom", "this",
    "that", "that'll", "these", "those", "am", "is", "are", "was", "were",
    "be", "been", "being", "have", "has", "had", "having", "do", "does",
    "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because",
    "as", "until", "while", "of", "at", "by", "for", "with", "about",
    "against", "between", "into", "through", "during", "before", "after",
    "above", "below", "to", "from", "up", "down", "in", "out", "on", "off",
    "over", "under", "again", "further", "then", "once", "here", "there",
    "when", "where", "why", "how", "all", "any", "both", "each", "few",
    "more", "most", "other", "some", "such", "no", "nor", "not", "only",
    "own", "same", "so", "than", "too", "very", "s", "t", "can", "will",
    "just", "don", "don't", "should", "should've", "now", "d", "ll", "m",
    "o", "re", "ve", "y", "ain", "aren", "aren't", "couldn", "couldn't",
    "didn", "didn't", "doesn", "doesn't", "hadn", "hadn't", "hasn",
    "hasn't", "haven", "haven't", "isn", "isn't", "ma", "mightn",
    "mightn't", "mustn", "mustn't", "needn", "needn't", "shan", "shan't",
    "shouldn", "shouldn't", "wasn", "wasn't", "weren", "weren't", "won",
    "won't", "wouldn", "wouldn't",
}


def _nltk_tokens(text: str) -> Set[str]:
    """NLTK-backed preprocessing (raises if resources are unavailable)."""
    import nltk  # local import: optional dependency
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.corpus import stopwords

    stop_words = set(stopwords.words("english"))
    tokens: List[str] = []
    for sentence in sent_tokenize(text.lower()):
        tokens.extend(
            w for w in word_tokenize(sentence) if w not in stop_words
        )
    return set(tokens)


_TOKEN_RE = re.compile(r"\w+|[^\w\s]", re.UNICODE)


def _fallback_tokens(text: str) -> Set[str]:
    """Self-contained tokenizer used when NLTK data is unavailable."""
    tokens = _TOKEN_RE.findall(text.lower())
    return {t for t in tokens if t not in ENGLISH_STOPWORDS}


def preprocess_text(text: str, prefer_nltk: bool = True) -> Set[str]:
    """Return a set of meaningful, lower-cased tokens for ``text``."""
    if prefer_nltk:
        try:
            return _nltk_tokens(text)
        except Exception:
            pass
    return _fallback_tokens(text)


def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0.0
