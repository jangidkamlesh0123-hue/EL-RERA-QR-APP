import sqlite3

DATABASE_NAME = "database.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS company (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT,
            contact TEXT,
            manager TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            certificate_id TEXT UNIQUE NOT NULL,
            intern_name TEXT NOT NULL,
            college_name TEXT NOT NULL,
            internship_role TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            total_hours INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()