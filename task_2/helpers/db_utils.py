import os
from datetime import datetime

import numpy
import peewee

from psycopg2.extensions import register_adapter, AsIs

register_adapter(numpy.float64, AsIs)
register_adapter(numpy.float32, AsIs)
register_adapter(numpy.int64, AsIs)
register_adapter(numpy.int32, AsIs)
register_adapter(numpy.int8, AsIs)
register_adapter(numpy.bool_, AsIs)

database = peewee.PostgresqlDatabase(
    os.getenv('DB_NAME', 'thesis'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST', 'localhost'),
    port=os.getenv('DB_PORT', '5432'),
)


class BaseModel(peewee.Model):
    id = peewee.IdentityField(primary_key=True, generate_always=True)
    created = peewee.DateTimeField(default=datetime.now)

    class Meta:
        database = database
