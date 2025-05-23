from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from app.db import get_db
from app.schemas.clinical_exam import ClinicalExamCreate, ClinicalExamUpdate
from app.models.clinical_exam import ClinicalExam
from app.models.patient import Patient
from app.models.user import User
from sqlalchemy import select

router = APIRouter(prefix="/clinical_exam", tags=["clinical_exam"])

@router.get("/")
def get_all_exams(db: Session = Depends(get_db)):
    return db.execute(select(ClinicalExam)).scalars().all()

@router.get("/{exam_id}")
def get_exam(exam_id: str, db: Session = Depends(get_db)):
    exam = db.get(ClinicalExam, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Záznam nenalezen")
    return exam

@router.post("/")
def create_exam(data: ClinicalExamCreate, db: Session = Depends(get_db)):
    if not db.get(Patient, data.patient_id):
        raise HTTPException(status_code=400, detail="Pacient neexistuje")
    if data.user_id and not db.get(User, data.user_id):
        raise HTTPException(status_code=400, detail="Uživatel neexistuje")

    exam = ClinicalExam(id=str(uuid4()), **data.dict())
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam

@router.put("/{exam_id}")
def update_exam(exam_id: str, data: ClinicalExamUpdate, db: Session = Depends(get_db)):
    exam = db.get(ClinicalExam, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Záznam nenalezen")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(exam, field, value)

    db.commit()
    db.refresh(exam)
    return exam

@router.delete("/{exam_id}")
def delete_exam(exam_id: str, db: Session = Depends(get_db)):
    exam = db.get(ClinicalExam, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Záznam nenalezen")
    db.delete(exam)
    db.commit()
    return {"message": "Záznam smazán"}
