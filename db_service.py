import sqlite3
from pathlib import Path


DB_PATH = Path("data/library.db")


def get_connection():

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            book_code TEXT UNIQUE NOT NULL,

            title TEXT NOT NULL,

            author TEXT NOT NULL,

            genre TEXT,

            price REAL,

            available_copies INTEGER,

            format TEXT
        )
    """)

    books = [

        (
            "BK101",
            "The Silent Orchard",
            "Meera Kapoor",
            "Fiction",
            399,
            3,
            "Paperback + eBook"
        ),

        (
            "BK102",
            "Data Structures Simplified",
            "R. Anand",
            "Computer Science",
            599,
            5,
            "Paperback"
        ),

        (
            "BK103",
            "Modern Machine Learning",
            "Priya Sharma",
            "Computer Science",
            799,
            2,
            "Hardcover + eBook"
        ),

        (
            "BK104",
            "Whispers of the Deccan",
            "Farah Iqbal",
            "History",
            449,
            4,
            "Paperback"
        )

    ]

    for book in books:

        cursor.execute(
            """
            INSERT OR IGNORE INTO books
            (
                book_code,
                title,
                author,
                genre,
                price,
                available_copies,
                format
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            book
        )

    connection.commit()

    connection.close()


def get_all_books():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM books
        ORDER BY title
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


def search_books(keyword):

    connection = get_connection()

    cursor = connection.cursor()

    keyword = f"%{keyword}%"

    cursor.execute(
        """
        SELECT *
        FROM books

        WHERE book_code LIKE ?
        OR title LIKE ?
        OR author LIKE ?
        OR genre LIKE ?
        """,
        (
            keyword,
            keyword,
            keyword,
            keyword
        )
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]
