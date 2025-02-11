
from sqlmodel import SQLModel


# Esquema para Criar Usuário (sem ID)
class UserCreate(SQLModel):
    name: str
    username: str
    email: str
    hashed_password: str
    role: str | None = "user"

# Esquema para Retornar Usuário (com ID)
class UserRead(UserCreate):
    id: int
    password: str | None = None
