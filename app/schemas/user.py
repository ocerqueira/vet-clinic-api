from sqlmodel import SQLModel
from typing import Optional

# Esquema para Criar Usuário (sem ID)
class UserCreate(SQLModel):
    name: str
    username: str
    email: str
    hashed_password: str

# Esquema para Retornar Usuário (com ID)
class UserRead(UserCreate):
    id: int
