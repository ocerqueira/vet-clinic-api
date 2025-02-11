
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.config.database import get_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.services.auth import hash_password

router = APIRouter(prefix="/users")

# Rota protegida: Retorna os dados completos do usuário autenticado
@router.get("/me", response_model=UserRead)
def get_my_profile(
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    user = session.exec(select(User).where(User.username == current_user["sub"])).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return user  # Retorna os dados completos do usuário autenticado


# Criar um usuário
@router.post("/", response_model=UserRead)
def create_user(user_data: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="E-mail já está em uso")

    hashed_password = hash_password(user_data.hashed_password)
    user = User(
        name=user_data.name,
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_data.role
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Listar todos os usuários
@router.get("/", response_model=list[UserRead])
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

# Obter um usuário por ID
@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

# Atualizar um usuário por ID
@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_data: User, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user_data_dict = user_data.dict(exclude_unset=True)
    for key, value in user_data_dict.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Deletar um usuário por ID
@router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    session.delete(user)
    session.commit()
    return {"message": "Usuário deletado com sucesso"}

