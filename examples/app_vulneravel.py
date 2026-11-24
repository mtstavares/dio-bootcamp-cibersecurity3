"""AMOSTRA INTENCIONALMENTE VULNERÁVEL. Somente SQLite em memória."""

import sqlite3


def create_lab_database() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE users (username TEXT, password TEXT)")
    # Texto puro é uma segunda falha intencional, corrigida no app.py.
    connection.execute("INSERT INTO users VALUES (?, ?)", ("aluna", "senha-laboratorio"))
    connection.commit()
    return connection


def login(connection: sqlite3.Connection, username: str, password: str) -> bool:
    query = (
        "SELECT username FROM users WHERE username = '" + username
        + "' AND password = '" + password + "'"
    )
    return connection.execute(query).fetchone() is not None


if __name__ == "__main__":
    db = create_lab_database()
    try:
        print("Login legítimo:", login(db, "aluna", "senha-laboratorio"))
        print("Bypass por SQL Injection:", login(db, "' OR 1=1 -- ", "incorreta"))
    finally:
        db.close()
