
from sqlmodel import Field, SQLModel


class Patient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(max_length=100)
    species: str = Field(max_length=50)
    breed: str | None = Field(max_length=100, default=None)

    owner_id: int = Field(foreign_key="client.id")
