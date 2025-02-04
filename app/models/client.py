from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    lastname: str = Field(max_length=100)
    gender: Optional[str] = Field(max_length=10, nullable=True)
    document: str = Field(max_length=25, unique=True)
    birth_date: Optional[date] = Field(default=None, nullable=True)
    phone: str = Field(max_length=20)
    email: str = Field(max_length=150, unique=True)
    address: Optional[str] = Field(max_length=200, nullable=True)
    number: Optional[str] = Field(max_length=10, nullable=True)
    neighborhood: Optional[str] = Field(max_length=100, nullable=True)
    city: Optional[str] = Field(max_length=100, nullable=True)
    state: Optional[str] = Field(max_length=50, nullable=True)
    zip_code: Optional[str] = Field(max_length=20, nullable=True)