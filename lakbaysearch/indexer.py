import json
import os
from typing import Dict, List, Tuple, Any

from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix

from preprocessing import preprocess

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DOCUMENTS_PATH = os.path.join(DATA_DIR, "documents.json")


def load_documents() -> List[Dict[str, Any]]:
    if not os.path.exists(DOCUMENTS_PATH):
        print(f"Error: {DOCUMENTS_PATH} not found. Run crawler.py first.")
        return []
    with open(DOCUMENTS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def prepare_document_texts(documents: List[Dict[str, Any]]) -> List[str]:
    texts = []
    for doc in documents:
        combined = (
            (doc.get("title", "") + " ") * 3 +
            (doc.get("heading", "") + " ") * 2 +
            doc.get("content", "")
        )
        preprocessed = preprocess(combined)
        texts.append(preprocessed)
    return texts


def build_index(documents: List[Dict[str, Any]]) -> Tuple[TfidfVectorizer, csr_matrix, List[Dict[str, Any]]]:
    if not documents:
        print("Warning: No documents to index.")
        empty_vectorizer = TfidfVectorizer()
        empty_matrix = csr_matrix((0, 0))
        return empty_vectorizer, empty_matrix, []

    print(f"Building TF-IDF index for {len(documents)} documents...")

    texts = prepare_document_texts(documents)

    metadata = []
    for doc in documents:
        metadata.append({
            "id": doc.get("id"),
            "title": doc.get("title", ""),
            "heading": doc.get("heading", ""),
            "url": doc.get("url", ""),
            "source": doc.get("source", ""),
            "category": doc.get("category", ""),
            "content": doc.get("content", ""),
        })

    vectorizer = TfidfVectorizer(
        max_features=10000,
        sublinear_tf=True,
        analyzer='word',
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.85,
    )

    document_matrix = vectorizer.fit_transform(texts)

    print(f"Index built successfully.")
    print(f"  Vocabulary size: {len(vectorizer.get_feature_names_out())}")
    print(f"  Matrix shape: {document_matrix.shape}")

    return vectorizer, document_matrix, metadata