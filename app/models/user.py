from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(max_length=200)
    username: str = Field(max_length=200, index=True, unique=True)
    email: str = Field(max_length=255, unique=True)
    hashed_password: str
    role: str = Field(default="user", nullable=False, max_length=20)
