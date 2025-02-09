from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.config.database import get_session
from app.models.client import Client
from app.dependencies.auth import get_current_user, is_admin

router = APIRouter(prefix="/clients")

# Criar um cliente
@router.post("/", response_model=Client)
def create_client(client: Client, session: Session = Depends(get_session), current_user: dict = Depends(is_admin)):
    session.add(client)
    session.commit()
    session.refresh(client)
    return client

# Listar todos os clientes
@router.get("/", response_model=List[Client])
def get_clients(session: Session = Depends(get_session)):
    clients = session.exec(select(Client)).all()
    return clients

# Obter um cliente por ID
@router.get("/{client_id}", response_model=Client)
def get_client(client_id: int, session: Session = Depends(get_session), current_user: dict = Depends(get_current_user)):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client

# Atualizar um cliente por ID
@router.put("/{client_id}", response_model=Client)
def delete_client(client_id: int, session: Session = Depends(get_session), current_user: dict = Depends(get_current_user)):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    client_data_dict = client_data.dict(exclude_unset=True)
    for key, value in client_data_dict.items():
        setattr(client, key, value)

    session.add(client)
    session.commit()
    session.refresh(client)
    return client

# Deletar um cliente por ID
@router.delete("/{client_id}")
def delete_client(client_id: int, session: Session = Depends(get_session)):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    session.delete(client)
    session.commit()
    return {"message": "Cliente deletado com sucesso"}
