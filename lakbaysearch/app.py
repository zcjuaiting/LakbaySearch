import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify

from database import init_db, log_search
from database import (
    get_total_searches,
    get_zero_result_searches,
    get_average_search_time,
    get_most_searched_queries,
    get_most_frequent_top_result,
    get_recent_searches,
)
from indexer import load_documents, build_index
from search_engine import search

app = Flask(__name__)

# Global variables
vectorizer = None
document_matrix = None
metadata = None


def initialize_index():
    global vectorizer, document_matrix, metadata

    # Prevent rebuilding if already initialized
    if vectorizer is not None:
        return

    print("=" * 60)
    print("LakbaySearch - Philippine Tourism Search Engine")
    print("=" * 60)

    print("\n[1/4] Initializing database...")
    init_db()
    print("Database ready.")

    print("\n[2/4] Loading documents...")
    documents = load_documents()
    print(f"{len(documents)} documents loaded.")

    print("\n[3/4] Building TF-IDF index...")
    vectorizer, document_matrix, metadata = build_index(documents)

    print("Index built successfully.")

    print("\n[4/4] Application ready!")
    print("=" * 60)


# IMPORTANT:
# Build the database and TF-IDF index immediately when the app is imported.
# Gunicorn imports app.py and DOES NOT execute the __main__ block.
initialize_index()


def get_categories():
    if not metadata:
        return []
    return sorted(
        {
            doc["category"]
            for doc in metadata
            if doc.get("category")
        }
    )


def get_sources():
    if not metadata:
        return []
    return sorted(
        {
            doc["source"]
            for doc in metadata
            if doc.get("source")
        }
    )


@app.route("/")
def index():
    return render_template(
        "index.html",
        categories=get_categories(),
        sources=get_sources(),
    )


@app.route("/search")
def search_results():
    global vectorizer, document_matrix, metadata

    # Safety check
    if vectorizer is None or document_matrix is None or metadata is None:
        initialize_index()

    query = request.args.get("q", "").strip()
    category_filter = request.args.get("category", "all")
    source_filter = request.args.get("source", "all")

    if not query:
        return render_template(
            "index.html",
            error="Please enter a search query.",
            categories=get_categories(),
            sources=get_sources(),
        )

    results, execution_time = search(
        query=query,
        vectorizer=vectorizer,
        document_matrix=document_matrix,
        metadata=metadata,
        category_filter=category_filter if category_filter != "all" else None,
        source_filter=source_filter if source_filter != "all" else None,
    )

    top_result = results[0]["title"] if results else None

    log_search(
        query=query,
        execution_time=execution_time,
        num_results=len(results),
        top_result=top_result,
    )

    return render_template(
        "results.html",
        query=query,
        results=results,
        execution_time=round(execution_time, 3),
        total_results=len(results),
        category_filter=category_filter,
        source_filter=source_filter,
        categories=get_categories(),
        sources=get_sources(),
    )


@app.route("/analytics")
def analytics():
    return render_template(
        "analytics.html",
        total_searches=get_total_searches(),
        zero_result_searches=get_zero_result_searches(),
        avg_search_time=get_average_search_time(),
        most_searched_queries=get_most_searched_queries(),
        most_frequent_top_results=get_most_frequent_top_result(),
        recent_searches=get_recent_searches(),
    )


@app.route("/api/categories")
def api_categories():
    return jsonify(get_categories())


@app.route("/api/sources")
def api_sources():
    return jsonify(get_sources())


@app.errorhandler(404)
def not_found(error):
    return (
        render_template(
            "index.html",
            error="Page not found.",
            categories=get_categories(),
            sources=get_sources(),
        ),
        404,
    )


@app.errorhandler(500)
def internal_error(error):
    return (
        render_template(
            "index.html",
            error="Internal server error. Please try again.",
            categories=get_categories(),
            sources=get_sources(),
        ),
        500,
    )


if __name__ == "__main__":
    app.run(debug=True)
