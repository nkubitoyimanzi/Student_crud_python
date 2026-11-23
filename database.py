import sqlite3
from pathlib import Path
from contextlib import contextmanager

BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = BASE_DIR / "students.db"


@contextmanager
def get_connection():
    "Create and manage database connection"

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    try:
        yield connection
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def initialize_database():
    "Create database table if it doesn't exist"

    with get_connection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL CHECK(age > 0),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
