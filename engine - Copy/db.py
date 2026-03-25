import sqlite3
import csv

con = sqlite3.connect("voca.db")
cursor = con.cursor()

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS sys_command (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT UNIQUE,
#     path TEXT
# )
# """)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS web_command (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT UNIQUE,
#     url TEXT
# )
# """)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS contacts (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT,
#     mobile_no TEXT,
#     email TEXT
# )
# """)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS chat_history (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     user_text TEXT,
#     assistant_reply TEXT,
#     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
# )
# """)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS system_settings (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     command_name TEXT,
#     action TEXT,
#     value INTEGER
# )
# """)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS user_profile (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT,
#     email TEXT,
#     city TEXT,
#     designation TEXT
# )
# """)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS command_logs (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     command_text TEXT,
#     action_taken TEXT,
#     status TEXT,
#     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
# )
# """)

# cursor.execute("DROP TABLE IF EXISTS command_logs")

# cursor.execute("DROP TABLE IF EXISTS chat_history")

# ===============================
# # Insert system app
# cursor.execute(
#     "INSERT OR IGNORE INTO sys_command VALUES (null, ?, ?)",
#     ("notepad", "C:\\Windows\\System32\\notepad.exe")
# )

# # Insert website
# cursor.execute(
#     # "INSERT INTO web_command VALUES (null, ?, ?)",
#     # ("amazon", "https://www.amazon.in/")
#      "INSERT INTO web_command VALUES (null, ?, ?)",
#      ("whatsapp", "https://web.whatsapp.com/")
# )

# # Insert contact
# cursor.execute(
#     "INSERT OR IGNORE INTO contacts VALUES (null, ?, ?, ?)",
#     ("kevin", "+91 91382 14118", "rahul@gmail.com")
# )

# ---- SYSTEM SETTINGS
# cursor.execute(
#     "INSERT INTO system_settings VALUES (null, ?, ?, ?)",
#     ("volume_down", "decrease", 20)
# )

# cursor.execute(
#     "INSERT INTO system_settings VALUES (null, ?, ?, ?)",
#     ("brightness_up", "increase", 30)
# )

# galat app entry remove
# cursor.execute(
#     "DELETE FROM web_command WHERE name = ?",
#     ("youtube",)
# )


# # Insert user profile (one time)
# cursor.execute(
#     "INSERT OR IGNORE INTO user_profile VALUES (null, ?, ?, ?, ?)",
#     ("Ashwini", "ashwinirathore@email.com", "India", "Engineering Student")
# )

# COMMIT & CLOSE
con.commit()
con.close()

print("VOCA database ready with all required tables")
