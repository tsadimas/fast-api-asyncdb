import os
from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,
                        create_engine)
from sqlalchemy.sql import func
from databases import Database
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from app.api.models import UserDB

from settings import DATABASE_URL


# engine = create_engine(
#             DATABASE_URL, connect_args={"check_same_thread": False}
#             )
engine = create_engine(DATABASE_URL)

# SQLAlchemy

metadata = MetaData()
notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)


# databases query builder
database = Database(DATABASE_URL)


Base: DeclarativeMeta = declarative_base()


class UserTable(Base, SQLAlchemyBaseUserTable):
    pass

Base.metadata.create_all(engine)

users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users)
