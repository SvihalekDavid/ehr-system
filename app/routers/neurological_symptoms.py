from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from app.db import get_db
from app.schemas.neurological_symptoms import NeuroSymptomsCreate, NeuroSymptomsUpdate
from app.models.neurological_symptoms import NeurologicalSymptoms
from app.models.patient import Patient
from app.models.user import User
from sqlalchemy import select

router = APIRouter(prefix="/neurological", tags=["neurological_symptoms"])

@router.get("/")
def get_all_symptoms(db: Session = Depends(get_db)):
    return db.execute(select(NeurologicalSymptoms)).scalars().all()

@router.get("/{symptom_id}")
def get_symptom(symptom_id: str, db: Session = Depends(get_db)):
    symptom = db.get(NeurologicalSymptoms, symptom_id)
    if not symptom:
        raise HTTPException(status_code=404, detail="Záznam nenalezen")
    return symptom

@router.post("/")
def create_symptom(data: NeuroSymptomsCreate, db: Session = Depends(get_db)):
    if not db.get(Patient, data.patient_id):
        raise HTTPException(status_code=400, detail="Pacient neexistuje")
    if data.user_id and not db.get(User, data.user_id):
        raise HTTPException(status_code=400, detail="Uživatel neexistuje")

    symptom = NeurologicalSymptoms(id=str(uuid4()), **data.dict())
    db.add(symptom)
    db.commit()
    db.refresh(symptom)
    return symptom

@router.put("/{symptom_id}")
def update_symptom(symptom_id: str, data: NeuroSymptomsUpdate, db: Session = Depends(get_db)):
    symptom = db.get(NeurologicalSymptoms, symptom_id)
    if not symptom:
        raise HTTPException(status_code=404, detail="Záznam nenalezen")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(symptom, field, value)

    db.commit()
    db.refresh(symptom)
    return symptom

@router.delete("/{symptom_id}")
def delete_symptom(symptom_id: str, db: Session = Depends(get_db)):
    symptom = db.get(NeurologicalSymptoms, symptom_id)
    if not symptom:
        raise HTTPException(status_code=404, detail="Záznam nenalezen")
    db.delete(symptom)
    db.commit()
    return {"message": "Záznam smazán"}
