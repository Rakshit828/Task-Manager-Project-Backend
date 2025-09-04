from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from typing import List, Optional, Annotated, Literal
from datetime import datetime, date, time



class Tasks(SQLModel, table=True):
    __tablename__="tasks"
    task_uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4
        )
    )
    title: str = Field(max_length=50)
    description: Optional[str] = Field(max_length=100)

    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP, default=datetime.now, nullable=False
        )
    )

    start_time: time
    deadline: time
    # priority: Literal['high', 'medium', 'low']
    is_completed: bool = False


    progress_rate: Annotated[
        Optional[int], 
        Field(
            default= 100 if is_completed else 0, 
            description="This indicates the progress in task", 
            ge=0, 
            le=100
        )
    ] 

    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.user_uid")
    # This is a foreign key that refrences to the userId of the Users table

# The start time and deadline will recive the time in 24-hour format
