import os
from datetime import datetime

import peewee

database = peewee.PostgresqlDatabase(
    os.getenv('DB_NAME', 'thesis'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST', 'localhost'),
    port=os.getenv('DB_PORT', '5434'),
)


class BaseModel(peewee.Model):
    id = peewee.IdentityField(primary_key=True, generate_always=True)
    created = peewee.DateTimeField(default=datetime.now)

    class Meta:
        database = database
