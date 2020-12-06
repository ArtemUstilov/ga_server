from datetime import datetime

import peewee

database = peewee.PostgresqlDatabase(
    'thesis',
    # user='postgres',
    # password='postgres',
    host='localhost',
    port=5434,
)


class BaseModel(peewee.Model):

    id = peewee.IdentityField(primary_key=True, generate_always=True)
    created = peewee.DateTimeField(default=datetime.now)

    class Meta:
        database = database

