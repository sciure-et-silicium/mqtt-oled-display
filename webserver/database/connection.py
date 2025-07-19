# database/connection.py
import sqlite3
from flask import current_app

def get_db_connection():
    """Connexion SQLite brute (pour les cas où SQLAlchemy n'est pas adapté)"""
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def execute_raw_query(query, params=None):
    """Exécute une requête SQL brute"""
    conn = get_db_connection()
    try:
        if params:
            result = conn.execute(query, params)
        else:
            result = conn.execute(query)
        conn.commit()
        return result.fetchall()
    finally:
        conn.close()
