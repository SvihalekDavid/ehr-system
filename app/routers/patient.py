from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from app.db import get_db
from app.schemas.patient import PatientCreate, PatientUpdate
from app.models.patient import Patient

from sqlalchemy import select

router = APIRouter(prefix="/patients", tags=["patients"])

@router.get("/")
def get_all_patients(db: Session = Depends(get_db)):
    return db.execute(select(Patient)).scalars().all()

@router.get("/{patient_id}")
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Pacient nebyl nalezen")
    return patient

@router.post("/")
def create_patient(data: PatientCreate, db: Session = Depends(get_db)):
    patient = Patient(id=str(uuid4()), **data.dict())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

@router.put("/{patient_id}")
def update_patient(patient_id: str, data: PatientUpdate, db: Session = Depends(get_db)):
    patient = db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Pacient nebyl nalezen")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)
    return patient

@router.delete("/{patient_id}")
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Pacient nebyl nalezen")
    db.delete(patient)
    db.commit()
    return {"message": "Pacient byl smazán"}
