from pydantic import BaseModel
from sqlmodel import SQLModel


# Schema para login (entrada de dados)
class LoginData(SQLModel):
    username: str
    password: str

# Schema para resposta do token JWT
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token: str
