from contextlib import contextmanager

import psycopg2

import numpy
from psycopg2.extensions import register_adapter, AsIs

register_adapter(numpy.float64, AsIs)
register_adapter(numpy.float32, AsIs)
register_adapter(numpy.int64, AsIs)
register_adapter(numpy.int32, AsIs)
register_adapter(numpy.int8, AsIs)
register_adapter(numpy.bool_, AsIs)


@contextmanager
def open_db_cursor(conn_str):
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()
    yield cur, conn
    conn.commit()
    conn.close()
