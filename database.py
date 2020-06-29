import os
from contextlib import contextmanager

import numpy
import psycopg2

from psycopg2.extensions import register_adapter, AsIs
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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


DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@localhost:5432/thesis')


Base = declarative_base()


class AggrRecord(Base):
    __tablename__ = 'records'
    id = Column(Integer, autoincrement=True, primary_key=True)

    L = Column(Integer)
    N = Column(Integer)
    init = Column(String(32))
    estim = Column(String(32))
    type = Column(String(32))
    try_id = Column(Integer)
    params = Column(JSON, server_default='{}')

    cur_px = Column(Float)
    runs_final = Column(ARRAY(Integer))
    count_succ = Column(Integer)
    is_final = Column(Boolean, default=False)
    chosen_for_test = Column(Boolean, default=False)
    note = Column(String(50), nullable=True)


class AggrRecordTest(Base):
    __tablename__ = 'records_tests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer,
                       ForeignKey('records.id'),
                       nullable=True)
    L = Column(Integer)
    N = Column(Integer)
    init = Column(String(32))
    estim = Column(String(32))
    type = Column(String(32))

    test_px = Column(Float)
    runs_final = Column(ARRAY(Integer))
    count_succ = Column(Integer)

    test_px_120 = Column(Float)
    runs_final_120 = Column(ARRAY(Integer))
    count_succ_120 = Column(Integer)

    test_px_80 = Column(Float)
    runs_final_80 = Column(ARRAY(Integer))
    count_succ_80 = Column(Integer)
    note = Column(String(50), nullable=True)


class AggrTestDetails(Base):
    __tablename__ = 'test_details'

    id = Column(Integer, autoincrement=True, primary_key=True)
    test_record_id = Column(Integer,
                            ForeignKey('records_tests.id'),
                            nullable=False)
    run_number = Column(Integer)
    percent = Column(Integer)

    mean_health = Column(ARRAY(Float))
    polymorphous1_p = Column(ARRAY(Float))
    note = Column(String(50), nullable=True)


class TestQueueRecord(Base):
    __tablename__ = 'test_queue_record'

    id = Column(Integer, autoincrement=True, primary_key=True)
    record_id = Column(Integer, ForeignKey('records_tests.id'))
    coef = Column(Float, default=1)


Session = sessionmaker(bind=engine)


def pop_one_row(model):
    sql = f"""
    DELETE FROM {model.__tablename__}
    WHERE id IN (SELECT id FROM {model.__tablename__} LIMIT 1)
    RETURNING {','.join([f'"{a.name}"' for a in model.__table__.columns])};
    """

    res = engine.execute(sql)
    instance_dict = res.fetchone()
    return model(**instance_dict)
