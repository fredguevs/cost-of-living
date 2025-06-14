import psycopg2
from psycopg2.extras import RealDictCursor
import flask


def get_db():
    if 'db' not in flask.g:
        flask.g.db = psycopg2.connect(
            dbname="cost_of_living",
            user="frederick",
            password="",
            host="localhost",
            port="5432"
        )
    return flask.g.db


def get_cursor():
    db = get_db()
    return db.cursor(cursor_factory=RealDictCursor)


def close_db(error=None):
    db = flask.g.pop('db', None)
    if db is not None:
        db.close()
