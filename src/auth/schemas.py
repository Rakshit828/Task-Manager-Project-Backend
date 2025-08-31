# Here, we write the form like schemas in the frontend

from pydantic import BaseModel, Field, EmailStr
from uuid import UUID
from datetime import datetime

class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    username: str = Field(max_length=10)
    email: EmailStr = Field(max_length=40)
    password: str = Field(min_length=8)


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(max_length=40)
    password: str = Field(min_length=8)


class UserResponseSchema(BaseModel):
    user_uid: UUID 
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    is_verified: bool 
    created_at: datetime 
    updated_at: datetime 

    class Config:
        orm_model = True