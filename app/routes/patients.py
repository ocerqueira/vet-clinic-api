from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.config.database import get_session
from app.models.patient import Patient

router = APIRouter()

# Criar um paciente
@router.post("/patients/", response_model=Patient)
def create_patient(patient: Patient, session: Session = Depends(get_session)):
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient

# Listar todos os pacientes
@router.get("/patients/", response_model=List[Patient])
def get_patients(session: Session = Depends(get_session)):
    patients = session.exec(select(Patient)).all()
    return patients

# Obter um paciente por ID
@router.get("/patients/{patient_id}", response_model=Patient)
def get_patient(patient_id: int, session: Session = Depends(get_session)):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return patient

# Atualizar um paciente por ID
@router.put("/patients/{patient_id}", response_model=Patient)
def update_patient(patient_id: int, patient_data: Patient, session: Session = Depends(get_session)):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    patient_data_dict = patient_data.dict(exclude_unset=True)
    for key, value in patient_data_dict.items():
        setattr(patient, key, value)

    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient

# Deletar um paciente por ID
@router.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, session: Session = Depends(get_session)):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    session.delete(patient)
    session.commit()
    return {"message": "Paciente deletado com sucesso"}
