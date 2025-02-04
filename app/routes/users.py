from  fastapi import APIRouter, Depends
from sqlmodel import Session
from app.config.database import get_session
from app.models.user import User

router = APIRouter()

@router.post("/users/")
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/users/")
def get_users(session: Session = Depends(get_session)):
    return session.exec(User).all()