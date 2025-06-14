import flask
from psycopg2.extras import RealDictCursor
from db.connection import get_db  # FIXED: was get_connection


def get_cursor():
    db = get_db()
    return db.cursor(cursor_factory=RealDictCursor)

# Query execution helper


def execute_query(sql, params=None, fetchone=False, fetchall=False):
    cur = get_cursor()
    cur.execute(sql, params or [])
    db = get_db()
    db.commit()  # <- add this to persist inserts/updates
    if fetchone:
        return cur.fetchone()
    if fetchall:
        return cur.fetchall()
