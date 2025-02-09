from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session
from app.config.database import get_session
from app.services.auth import SECRET_KEY, ALGORITHM, is_token_revoked, verify_access_token

# Configuração do esquema OAuth2 para receber tokens via "Bearer"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Dependência para validar e autenticar usuários
def get_current_user(token: str = Security(oauth2_scheme), session: Session = Depends(get_session)):
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    
    if is_token_revoked(token, session):
        raise HTTPException(status_code=401, detail="Token revogado. Faça login novamente.")
    return payload  # Retorna os dados do usuário autenticado


def is_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Permissão negada")
    return current_user