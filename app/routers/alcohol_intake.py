from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from app.db import get_db
from app.schemas.alcohol_intake import AlcoholIntakeCreate, AlcoholIntakeUpdate
from app.models.alcohol_intake import AlcoholIntake
from app.models.patient import Patient
from app.models.user import User
from sqlalchemy import select

router = APIRouter(prefix="/alcohol", tags=["alcohol_intake"])

@router.get("/")
def get_all_alcohol_intake(db: Session = Depends(get_db)):
    return db.execute(select(AlcoholIntake)).scalars().all()

@router.get("/{intake_id}")
def get_alcohol_intake(intake_id: str, db: Session = Depends(get_db)):
    record = db.get(AlcoholIntake, intake_id)
    if not record:
        raise HTTPException(status_code=404, detail="Záznam nenalezen")
    return record

@router.post("/")
def create_alcohol_intake(data: AlcoholIntakeCreate, db: Session = Depends(get_db)):
    if not db.get(Patient, data.patient_id):
        raise HTTPException(status_code=400, detail="Pacient neexistuje")
    if data.user_id and not db.get(User, data.user_id):
        raise HTTPException(status_code=400, detail="Uživatel neexistuje")

    record = AlcoholIntake(id=str(uuid4()), **data.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.put("/{intake_id}")
def update_alcohol_intake(intake_id: str, data: AlcoholIntakeUpdate, db: Session = Depends(get_db)):
    record = db.get(AlcoholIntake, intake_id)
    if not record:
        raise HTTPException(status_code=404, detail="Záznam nenalezen")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(record, field, value)

    db.commit()
    db.refresh(record)
    return record

@router.delete("/{intake_id}")
def delete_alcohol_intake(intake_id: str, db: Session = Depends(get_db)):
    record = db.get(AlcoholIntake, intake_id)
    if not record:
        raise HTTPException(status_code=404, detail="Záznam nenalezen")
    db.delete(record)
    db.commit()
    return {"message": "Záznam smazán"}
