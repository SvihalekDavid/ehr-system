from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from app.db import get_db
from app.schemas.vital_signs import VitalSignsCreate, VitalSignsUpdate
from app.models.vital_signs import VitalSigns
from app.models.patient import Patient
from app.models.user import User
from sqlalchemy import select

router = APIRouter(prefix="/vital_signs", tags=["vital_signs"])

@router.get("/")
def get_all_vital_signs(db: Session = Depends(get_db)):
    return db.execute(select(VitalSigns)).scalars().all()

@router.get("/{vs_id}")
def get_vital_sign(vs_id: str, db: Session = Depends(get_db)):
    vs = db.get(VitalSigns, vs_id)
    if not vs:
        raise HTTPException(status_code=404, detail="Záznam nenalezen")
    return vs

@router.post("/")
def create_vital_sign(data: VitalSignsCreate, db: Session = Depends(get_db)):
    if not db.get(Patient, data.patient_id):
        raise HTTPException(status_code=400, detail="Pacient neexistuje")
    if data.user_id and not db.get(User, data.user_id):
        raise HTTPException(status_code=400, detail="Uživatel neexistuje")

    vs = VitalSigns(id=str(uuid4()), **data.dict())
    db.add(vs)
    db.commit()
    db.refresh(vs)
    return vs

@router.put("/{vs_id}")
def update_vital_sign(vs_id: str, data: VitalSignsUpdate, db: Session = Depends(get_db)):
    vs = db.get(VitalSigns, vs_id)
    if not vs:
        raise HTTPException(status_code=404, detail="Záznam nenalezen")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(vs, field, value)

    db.commit()
    db.refresh(vs)
    return vs

@router.delete("/{vs_id}")
def delete_vital_sign(vs_id: str, db: Session = Depends(get_db)):
    vs = db.get(VitalSigns, vs_id)
    if not vs:
        raise HTTPException(status_code=404, detail="Záznam nenalezen")
    db.delete(vs)
    db.commit()
    return {"message": "Záznam smazán"}
