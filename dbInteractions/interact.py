import sqlite3
from pathlib import Path
import sys
import pandas as pd


root_path = Path(__file__).resolve().parent.parent

sys.path.append(str(root_path))


from db import init_db, save_log, fetch_logs


print ("............................................")


# init_db()
db_name = root_path / "SQLiteDatabases/users.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()
cursor.execute("SELECT * FROM user_login_info;")
tables = cursor.fetchall()
print(tables)

# query = "INSERT INTO user_login_info (Name, user_name, password) VALUES (?, ?, ?);"
# values = ("Test User", "testuser", "password123")
# cursor.execute(query, values)
# conn.commit()

# cursor.execute("SELECT * FROM user_login_info;")
# tables = cursor.fetchall()
# print(tables)


# logs = fetch_logs("users.db")
# print (logs)

# logs = pd.DataFrame(logs, columns=['id', 'request_time', 'original_contacts', 'cleaned_contacts'])

# print (logs)


# # if __name__ == "__main__":
# #     fetch_logs()

# # # Navigate two levels up from current file to reach root directory
# # db_path = Path(__file__).resolve().parent.parent / "api_requests.db"

# # print(f"Connecting to: {db_path}")

# # try:
# #     conn = sqlite3.connect(db_path)
# #     cursor = conn.cursor()
# #     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# #     tables = cursor.fetchall()
# #     print("Tables in database:", tables)
# #     conn.close()
# # except Exception as e:
# #     print("Connection failed:", e)