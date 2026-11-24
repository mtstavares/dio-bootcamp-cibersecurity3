"""Login corrigido para laboratório local. Não fornece servidor HTTP."""

import hashlib
import hmac
import secrets
import sqlite3

ITERATIONS = 600_000


def password_hash(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)


def create_lab_database() -> sqlite3.Connection:
    """Cria dados fictícios em memória; a credencial é pública e didática."""
    connection = sqlite3.connect(":memory:")
    connection.execute(
        "CREATE TABLE users (username TEXT PRIMARY KEY, salt BLOB, password_hash BLOB)"
    )
    salt = secrets.token_bytes(16)
    connection.execute(
        "INSERT INTO users VALUES (?, ?, ?)",
        ("aluna", salt, password_hash("senha-laboratorio", salt)),
    )
    connection.commit()
    return connection


def login(connection: sqlite3.Connection, username: str, password: str) -> bool:
    user = connection.execute(
        "SELECT salt, password_hash FROM users WHERE username = ?", (username,)
    ).fetchone()
    if user is None:
        return False
    salt, stored_hash = user
    return hmac.compare_digest(password_hash(password, salt), stored_hash)


if __name__ == "__main__":
    db = create_lab_database()
    try:
        print("Login legítimo:", login(db, "aluna", "senha-laboratorio"))
        print("Bypass por SQL Injection:", login(db, "' OR 1=1 -- ", "incorreta"))
    finally:
        db.close()
