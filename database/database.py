import sqlite3
import os

# Database Path
DB_PATH = os.path.join("database", "student_management.db")


def get_connection():
    """
    Returns SQLite Connection
    """
    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

