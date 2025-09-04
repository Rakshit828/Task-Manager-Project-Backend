# Here, we write the form like schemas in the frontend

from pydantic import BaseModel, Field, EmailStr
from uuid import UUID
from datetime import datetime

class BanUserSchema(BaseModel):
    email: EmailStr