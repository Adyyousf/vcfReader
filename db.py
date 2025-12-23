import sqlite3
from datetime import datetime
import sys
from pathlib import Path
    

db_name = Path(__file__).resolve().parent 
# print(f"Database directory: {db_name}")

def init_db():
    with sqlite3.connect(db_name / "SQLiteDatabases/users.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_login_info (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                user_name TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
    return "table created"

def save_log(original, cleaned, db="SQLiteDatabases/api_requests.db"):
    #1 timestamp of the request
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(db_name / db) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO api_request_logs (request_time, original_contacts, cleaned_contacts)
            VALUES (?, ?, ?)
        ''', (timestamp, original, cleaned))
        conn.commit()
    response = cursor.lastrowid
    return response


# save user login info
def save_user(name, user_name, password):
    with sqlite3.connect(db_name / "SQLiteDatabases/users.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO user_login_info (Name, user_name, password)
            VALUES (?, ?, ?)
        ''', (name, user_name, password))
        conn.commit()
    response = cursor.lastrowid
    return response

# check user credentials
def check_user(user_name, password):
    with sqlite3.connect(db_name / "SQLiteDatabases/users.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM user_login_info
            WHERE user_name = ? AND password = ?
        ''', (user_name, password))
        user = cursor.fetchone()

        # status = None

        if user:
            status = "success"
            print("User authenticated successfully.")
        else:
            status = "failure"
            print("Authentication failed. Invalid username or password.")

    return status



def fetch_logs(db):
    with sqlite3.connect(db_name / db) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM api_request_logs')
        logs = cursor.fetchall()
        # print(logs)
    return logs

# logs = fetch_logs()
# print(f"Fetched {len(logs)} logs from the database.")
# for log in logs:
#     print(log)

# try:
# init_db()
# db_name = db_name / "users.db"
# conn = sqlite3.connect(db_name)
# cursor = conn.cursor()
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# tables = cursor.fetchall()
# print("Tables in database:", tables)