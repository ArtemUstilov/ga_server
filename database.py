from contextlib import contextmanager

import psycopg2
from sqlalchemy import create_engine

import numpy
from psycopg2.extensions import register_adapter, AsIs


def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)


def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)


def addapt_numpy_int32(numpy_int32):
    return AsIs(numpy_int32)


register_adapter(numpy.float64, addapt_numpy_float64)
register_adapter(numpy.int64, addapt_numpy_int64)
register_adapter(numpy.int32, addapt_numpy_int32)

CONN_STR = 'postgresql://thesis:thesis@localhost:5432/thesis'

engine = create_engine(CONN_STR)


@contextmanager
def open_db_cursor():
    conn = psycopg2.connect(CONN_STR)
    cursor = conn.cursor()
    yield cursor, conn
    conn.commit()
    conn.close()
