from pydantic import BaseModel, PrivateAttr
from datetime import datetime, date
from uuid import UUID
from typing import Optional, Annotated

class BookResponseSchema(BaseModel):
    uuid: UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime 
    updated_at: datetime 

    class Config:
        orm_model=True


class BookCreateSchema(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str


class BookUpdateSchema(BaseModel):
    title: Optional[str]
    author: Optional[str]
    publisher: Optional[str]
    published_date: Optional[date]
    page_count: Optional[int]
    language: Optional[str]
