import re
import time
from typing import Dict, List, Optional, Tuple, Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

from preprocessing import preprocess


SNIPPET_LENGTH = 200
SNIPPET_CONTEXT = 100


def generate_snippet(content: str, query_terms: List[str]) -> str:
    if not content or not query_terms:
        return content[:SNIPPET_LENGTH] + "..." if len(content) > SNIPPET_LENGTH else content

    content_lower = content.lower()
    best_pos = -1
    best_term = ""

    for term in query_terms:
        pos = content_lower.find(term.lower())
        if pos != -1 and (best_pos == -1 or pos < best_pos):
            best_pos = pos
            best_term = term

    if best_pos == -1:
        return content[:SNIPPET_LENGTH] + "..." if len(content) > SNIPPET_LENGTH else content

    start = max(0, best_pos - SNIPPET_CONTEXT)
    end = min(len(content), best_pos + SNIPPET_CONTEXT)

    snippet = content[start:end]

    if start > 0:
        snippet = "..." + snippet
    if end < len(content):
        snippet = snippet + "..."

    for term in query_terms:
        if not term.strip():
            continue
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        snippet = pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", snippet)

    return snippet


def search(
    query: str,
    vectorizer: TfidfVectorizer,
    document_matrix: csr_matrix,
    metadata: List[Dict[str, Any]],
    category_filter: Optional[str] = None,
    source_filter: Optional[str] = None,
) -> Tuple[List[Dict[str, Any]], float]:
    start_time = time.time()

    if not query or not query.strip():
        return [], time.time() - start_time

    processed_query = preprocess(query)

    if not processed_query.strip():
        return [], time.time() - start_time

    query_vector = vectorizer.transform([processed_query])
    similarities = cosine_similarity(query_vector, document_matrix).flatten()

    query_terms = preprocess(query).split()
    original_query_terms = query.lower().split()

    results = []
    for idx, score in enumerate(similarities):
        if score == 0:
            continue

        doc_meta = metadata[idx]

        if category_filter and category_filter != "all":
            if doc_meta.get("category", "").lower() != category_filter.lower():
                continue

        if source_filter and source_filter != "all":
            if doc_meta.get("source", "").lower() != source_filter.lower():
                continue

        content = doc_meta.get("content", "")
        snippet = generate_snippet(content, original_query_terms)

        similarity_pct = round(float(score) * 100, 2)

        result = {
            "title": doc_meta.get("title", ""),
            "url": doc_meta.get("url", ""),
            "category": doc_meta.get("category", ""),
            "source": doc_meta.get("source", ""),
            "snippet": snippet,
            "similarity": similarity_pct,
        }
        results.append(result)

    results.sort(key=lambda r: r["similarity"], reverse=True)

    execution_time = time.time() - start_time

    return results, execution_time