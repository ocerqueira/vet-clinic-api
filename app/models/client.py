
from sqlmodel import Field, SQLModel


class Client(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(max_length=100)
    lastname: str = Field(max_length=100)
    gender: str | None = Field(max_length=10, nullable=True)
    document: str = Field(max_length=25, unique=True)
    phone: str = Field(max_length=20)
    email: str = Field(max_length=150, unique=True)
    address: str | None = Field(max_length=200, nullable=True)
    number: str | None = Field(max_length=10, nullable=True)
    neighborhood: str | None = Field(max_length=100, nullable=True)
    city: str | None = Field(max_length=100, nullable=True)
    state: str | None = Field(max_length=50, nullable=True)
    zip_code: str | None = Field(max_length=20, nullable=True)
