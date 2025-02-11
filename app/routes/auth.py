from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from app.config.database import get_session
from app.models.user import User
from app.schemas.auth import LoginData, RefreshTokenRequest, Token
from app.services.auth import (
    create_access_token,
    create_refresh_token,
    is_token_revoked,
    revoke_token,
    verify_password,
    verify_refresh_token,
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Rota de Login
@router.post("/login", response_model=dict)
def login(login_data: LoginData, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == login_data.username)).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")

    # Gera o token JWT
    access_token = create_access_token(data={"sub": user.username, "role": user.role}, expires_delta=timedelta(minutes=30))
    refresh_token = create_refresh_token(data={"sub": user.username})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# LOGOUT - Revoga o Token
@router.post("/logout")
def logout(token: str = Security(oauth2_scheme), session: Session = Depends(get_session)):
    revoke_token(token, session)
    return {"message": "Logout realizado com sucesso!"}

# REFRESH TOKEN - Gera um novo Access Token
@router.post("/refresh", response_model=Token)
def refresh_token(refresh_request: RefreshTokenRequest, session: Session = Depends(get_session)):
    refresh_token = refresh_request.refresh_token  # 🔥 Agora capturamos corretamente o token

    payload = verify_refresh_token(refresh_token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Refresh Token inválido")

    # 🔥 Verifica se o Refresh Token foi revogado (se o usuário fez logout)
    if is_token_revoked(refresh_token, session):
        raise HTTPException(status_code=401, detail="Refresh Token revogado")

    new_access_token = create_access_token(data={"sub": payload["sub"], "role": payload.get("role", "user")}, expires_delta=timedelta(minutes=30))

    return {"access_token": new_access_token, "token_type": "bearer"}
