from contextlib import contextmanager

import psycopg2

import numpy
from psycopg2.extensions import register_adapter, AsIs


def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)


def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)


def addapt_numpy_int32(numpy_int32):
    return AsIs(numpy_int32)


def addapt_numpy_int8(numpy_int8):
    return AsIs(numpy_int8)


def addapt_numpy_bool(bool_):
    return AsIs(bool_)


register_adapter(numpy.float64, addapt_numpy_float64)
register_adapter(numpy.int64, addapt_numpy_int64)
register_adapter(numpy.int32, addapt_numpy_int32)
register_adapter(numpy.int8, addapt_numpy_int8)
register_adapter(numpy.bool_, addapt_numpy_bool)


@contextmanager
def open_db_cursor(conn_str):
    conn = psycopg2.connect(conn_str)
    cursor = conn.cursor()
    yield cursor, conn
    conn.commit()
    conn.close()
