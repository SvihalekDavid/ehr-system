from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db import get_db
from app.models.patient import Patient
from uuid import uuid4
from datetime import date
from app.models.eeg_record import EEGRecord
from app.models.alcohol_intake import AlcoholIntake
from app.models.neurological_symptoms import NeurologicalSymptoms
from app.models.clinical_exam import ClinicalExam
from app.models.vital_signs import VitalSigns
from app.models.social_background import SocialBackground

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/patients", response_class=HTMLResponse)
def patient_list(request: Request, db: Session = Depends(get_db)):
    patients = db.execute(select(Patient)).scalars().all()
    return templates.TemplateResponse("patients.html", {"request": request, "patients": patients})

@router.get("/patients/create", response_class=HTMLResponse)
def create_patient_form(request: Request):
    return templates.TemplateResponse("create_patient.html", {"request": request})

@router.post("/patients/create")
def create_patient(
    request: Request,
    name: str = Form(...),
    birth_date: date = Form(...),
    sex: str = Form(...),
    db: Session = Depends(get_db)
):
    patient = Patient(id=str(uuid4()), name=name, birth_date=birth_date, sex=sex)
    db.add(patient)
    db.commit()
    return RedirectResponse(url="/patients", status_code=303)

@router.get("/patients/{patient_id}/edit", response_class=HTMLResponse)
def edit_patient_form(patient_id: str, request: Request, db: Session = Depends(get_db)):
    patient = db.get(Patient, patient_id)
    if not patient:
        return HTMLResponse("Pacient nenalezen", status_code=404)
    return templates.TemplateResponse("edit_patient.html", {"request": request, "patient": patient})

@router.post("/patients/{patient_id}/edit")
def update_patient(
    patient_id: str,
    name: str = Form(...),
    birth_date: date = Form(...),
    sex: str = Form(...),
    db: Session = Depends(get_db)
):
    patient = db.get(Patient, patient_id)
    if not patient:
        return HTMLResponse("Pacient nenalezen", status_code=404)
    patient.name = name
    patient.birth_date = birth_date
    patient.sex = sex
    db.commit()
    return RedirectResponse(url="/patients", status_code=303)

@router.post("/patients/{patient_id}/delete")
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = db.get(Patient, patient_id)
    if patient:
        db.delete(patient)
        db.commit()
    return RedirectResponse(url="/patients", status_code=303)

@router.get("/patients/{patient_id}", response_class=HTMLResponse)
def patient_detail(patient_id: str, request: Request, db: Session = Depends(get_db)):
    patient = db.get(Patient, patient_id)
    if not patient:
        return HTMLResponse("Pacient nenalezen", status_code=404)

    eeg_records = db.execute(
        select(EEGRecord).where(EEGRecord.patient_id == patient_id)
    ).scalars().all()

    alcohol_records = db.execute(
        select(AlcoholIntake).where(AlcoholIntake.patient_id == patient_id)
    ).scalars().all()

    neurological_records = db.execute(
        select(NeurologicalSymptoms).where(NeurologicalSymptoms.patient_id == patient_id)
    ).scalars().all()

    clinical_records = db.execute(
        select(ClinicalExam).where(ClinicalExam.patient_id == patient_id)
    ).scalars().all()

    vital_records = db.execute(
        select(VitalSigns).where(VitalSigns.patient_id == patient_id)
    ).scalars().all()

    social_records = db.execute(
        select(SocialBackground).where(SocialBackground.patient_id == patient_id)
    ).scalars().all()

    return templates.TemplateResponse("patient_detail.html", {
        "request": request,
        "patient": patient,
        "eeg_records": eeg_records,
        "alcohol_records": alcohol_records,
        "neurological_records": neurological_records,
        "clinical_records": clinical_records,
        "vital_records": vital_records,
        "social_records": social_records
    })
