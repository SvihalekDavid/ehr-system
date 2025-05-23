from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from app.db import get_db
from app.schemas.social_background import SocialBackgroundCreate, SocialBackgroundUpdate
from app.models.social_background import SocialBackground
from app.models.patient import Patient
from app.models.user import User
from sqlalchemy import select

router = APIRouter(prefix="/social_background", tags=["social_background"])

@router.get("/")
def get_all_social_records(db: Session = Depends(get_db)):
    return db.execute(select(SocialBackground)).scalars().all()

@router.get("/{record_id}")
def get_social_record(record_id: str, db: Session = Depends(get_db)):
    record = db.get(SocialBackground, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Záznam nenalezen")
    return record

@router.post("/")
def create_social_record(data: SocialBackgroundCreate, db: Session = Depends(get_db)):
    if not db.get(Patient, data.patient_id):
        raise HTTPException(status_code=400, detail="Pacient neexistuje")
    if data.user_id and not db.get(User, data.user_id):
        raise HTTPException(status_code=400, detail="Uživatel neexistuje")

    record = SocialBackground(id=str(uuid4()), **data.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.put("/{record_id}")
def update_social_record(record_id: str, data: SocialBackgroundUpdate, db: Session = Depends(get_db)):
    record = db.get(SocialBackground, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Záznam nenalezen")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(record, field, value)

    db.commit()
    db.refresh(record)
    return record

@router.delete("/{record_id}")
def delete_social_record(record_id: str, db: Session = Depends(get_db)):
    record = db.get(SocialBackground, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Záznam nenalezen")
    db.delete(record)
    db.commit()
    return {"message": "Záznam smazán"}
