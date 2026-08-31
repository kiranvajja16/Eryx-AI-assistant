import sqlite3
import os

DB_PATH="data/eryx.db"


def get_connection():
    os.makedirs("data",exist_ok=True)

    return sqlite3.connect(DB_PATH)

def initialize_database():
    connection=get_connection()

    cursor=connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        note TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            reminder_time TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()