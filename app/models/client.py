from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import date 

class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    lastname: str = Field(max_length=100)
    gender: str = Field(max_length=10)
    document: str = Field(max_length=25)
    birth_date: Optional[date] = Field(default=None, nullable=True)
    phone: str = Field(max_length=20)
    email: str = Field(max_length=150)
    address: str = Field(max_length=200)
    number: str = Field(max_length=10)
    neighborhood: str = Field(max_length=100)
    city: str = Field(max_length=100)
    state: str = Field(max_length=50)
    zip_code: str = Field(max_length=20)