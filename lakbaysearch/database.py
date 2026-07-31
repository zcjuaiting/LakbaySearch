import sqlite3
import os
from datetime import datetime
from typing import Optional


DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "analytics.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            execution_time REAL NOT NULL,
            num_results INTEGER NOT NULL,
            top_result TEXT
        )
    """)
    conn.commit()
    conn.close()


def log_search(query: str, execution_time: float, num_results: int, top_result: Optional[str] = None) -> None:
    if not query or not query.strip():
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO analytics (query, timestamp, execution_time, num_results, top_result) VALUES (?, ?, ?, ?, ?)",
        (query.strip().lower(), datetime.now().isoformat(), execution_time, num_results, top_result)
    )
    conn.commit()
    conn.close()


def get_total_searches() -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM analytics")
    result = cursor.fetchone()[0]
    conn.close()
    return result


def get_zero_result_searches() -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM analytics WHERE num_results = 0")
    result = cursor.fetchone()[0]
    conn.close()
    return result


def get_average_search_time() -> float:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(execution_time) FROM analytics")
    result = cursor.fetchone()[0]
    conn.close()
    return round(result, 4) if result else 0.0


def get_most_searched_queries(limit: int = 10) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT query, COUNT(*) as count FROM analytics GROUP BY query ORDER BY count DESC LIMIT ?",
        (limit,)
    )
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def get_most_frequent_top_result(limit: int = 10) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT top_result, COUNT(*) as count FROM analytics WHERE top_result IS NOT NULL GROUP BY top_result ORDER BY count DESC LIMIT ?",
        (limit,)
    )
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def get_recent_searches(limit: int = 20) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT query, timestamp, num_results, execution_time, top_result FROM analytics ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results