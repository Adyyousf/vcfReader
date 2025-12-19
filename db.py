import sqlite3
from datetime import datetime

db_name = "api_requests.db"

def init_db():
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_request_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_time TEXT NOT NULL,
                original_contacts INTEGER NOT NULL,
                cleaned_contacts INTEGER NOT NULL
            )
        ''')

def save_log(original, cleaned):
    #1 timestamp of the request
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO api_request_logs (request_time, original_contacts, cleaned_contacts)
            VALUES (?, ?, ?)
        ''', (timestamp, original, cleaned))
        conn.commit()
    response = cursor.lastrowid
    return response


def fetch_logs():
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM api_request_logs')
        logs = cursor.fetchall()
    return logs