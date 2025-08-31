from typing import List, Optional, Annotated
from datetime import datetime, date, time
from pydantic import BaseModel, Field
from uuid import UUID


class ResponseTaskSchema(BaseModel):
    task_uid: UUID
    title: str 
    description: Optional[str]
    created_at: datetime 
    start_time: time
    deadline: time
    is_completed: bool = False
    progress_rate: int

    class Config:
        orm_mode = True


class CreateTaskSchema(BaseModel):
    title: str = Field(max_length=10)
    description: Optional[str] = Field(max_length=100)
    start_time: time
    deadline: time


class UpdateTaskSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=100)
    start_time: Optional[time] = None
    deadline: Optional[time] = None
    is_completed: Optional[bool] = None
    progress_rate: Optional[int] = None

