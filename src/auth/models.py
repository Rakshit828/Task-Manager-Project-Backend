from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import text

from datetime import datetime
import uuid
from typing import Literal


class User(SQLModel, table=True):
    __tablename__="users"

    user_uid: uuid.UUID = Field(
        sa_column= Column(
            pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4
        )
    )
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(sa_column=Column(pg.VARCHAR, server_default="user"))
    is_verified: bool = Field(default=False)
    is_legal: bool = Field(
        sa_column=Column(pg.BOOLEAN, nullable=False, server_default="true")
    )
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, nullable=False))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))


    def __repr__(self):
        return f"<class 'User' {self.username}>"
