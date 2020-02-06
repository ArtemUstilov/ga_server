from contextlib import contextmanager

import psycopg2
from sqlalchemy import create_engine

CONN_STR = 'postgresql://thesis:thesis@localhost:5432/thesis'

engine = create_engine(CONN_STR)


@contextmanager
def open_db_cursor():
    conn = psycopg2.connect(CONN_STR)
    cursor = conn.cursor()
    yield cursor, conn
    conn.commit()
    conn.close()
