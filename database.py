import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        plan TEXT DEFAULT 'free',
        daily_usage INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def create_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    try:
        c.execute(
            "INSERT INTO users (username, password, plan, daily_usage) VALUES (?, ?, 'free', 0)",
            (username, password)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def get_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = c.fetchone()
    conn.close()
    return user


def update_usage(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        "UPDATE users SET daily_usage = daily_usage + 1 WHERE id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()


def get_usage(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        "SELECT daily_usage FROM users WHERE id=?",
        (user_id,)
    )

    usage = c.fetchone()[0]
    conn.close()
    return usage