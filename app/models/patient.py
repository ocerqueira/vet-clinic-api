from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(max_length=100)
    species: str = Field(max_length=50)
    breed: Optional[str] = Field(max_length=100, default=None)
    birth_date: Optional[date] = Field(default=None, nullable=True)
    
    owner_id: int = Field(foreign_key="client.id")