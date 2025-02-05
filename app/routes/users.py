from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.config.database import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead 

router = APIRouter()

# Criar um usuário (Usamos UserCreate para entrada e UserRead para saída)
@router.post("/users/", response_model=UserRead)
def create_user(user_data: UserCreate, session: Session = Depends(get_session)):
    user = User(**user_data.dict())  # Criamos o objeto sem ID
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Listar todos os usuários
@router.get("/users/", response_model=List[UserRead])
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()  
    return users

# Obter um usuário por ID
@router.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

# Atualizar um usuário por ID
@router.put("/users/{user_id}", response_model=User)
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
@router.delete("/users/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    session.delete(user)
    session.commit()
    return {"message": "Usuário deletado com sucesso"}
