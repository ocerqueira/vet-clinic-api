from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import timedelta
from app.config.database import get_session
from app.models.user import User
from app.schemas.auth import LoginData, Token
from app.services.auth import hash_password, verify_password, create_access_token

router = APIRouter()

# Rota de Login
@router.post("/login", response_model=Token)
def login(login_data: LoginData, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == login_data.username)).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")

    # Gera o token JWT
    access_token = create_access_token(data={"sub": user.username, "role": user.role}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}
