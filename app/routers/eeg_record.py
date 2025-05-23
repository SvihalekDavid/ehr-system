from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from app.db import get_db
from app.schemas.eeg_record import EEGRecordCreate, EEGRecordUpdate
from app.models.eeg_record import EEGRecord
from app.models.patient import Patient
from app.models.user import User
from sqlalchemy import select

router = APIRouter(prefix="/eeg_records", tags=["eeg_records"])

@router.get("/")
def get_all_records(db: Session = Depends(get_db)):
    return db.execute(select(EEGRecord)).scalars().all()

@router.get("/{record_id}")
def get_record(record_id: str, db: Session = Depends(get_db)):
    record = db.get(EEGRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="EEG záznam nenalezen")
    return record

@router.post("/")
def create_record(data: EEGRecordCreate, db: Session = Depends(get_db)):
    # validace existence FK
    if not db.get(Patient, data.patient_id):
        raise HTTPException(status_code=400, detail="Pacient neexistuje")
    if data.user_id and not db.get(User, data.user_id):
        raise HTTPException(status_code=400, detail="Uživatel neexistuje")

    record = EEGRecord(id=str(uuid4()), **data.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.put("/{record_id}")
def update_record(record_id: str, data: EEGRecordUpdate, db: Session = Depends(get_db)):
    record = db.get(EEGRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Záznam nenalezen")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(record, field, value)

    db.commit()
    db.refresh(record)
    return record

@router.delete("/{record_id}")
def delete_record(record_id: str, db: Session = Depends(get_db)):
    record = db.get(EEGRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Záznam nenalezen")
    db.delete(record)
    db.commit()
    return {"message": "Záznam smazán"}
