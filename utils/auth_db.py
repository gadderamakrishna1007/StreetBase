# utils/auth_db.py
import sqlite3
import hashlib

DB_PATH = "login/users.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    hashed_pw = hash_password(password)
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    hashed_pw = hash_password(password)
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
    data = c.fetchone()
    conn.close()
    return data is not None
