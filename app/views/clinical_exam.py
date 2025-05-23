from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4

from app.db import get_db
from app.models.clinical_exam import ClinicalExam
from app.models.user import User
from app.models.patient import Patient
from fastapi.responses import JSONResponse
from app.fhir.clinical_to_fhir import clinical_exam_to_fhir


templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/patients/{patient_id}/clinical/create", response_class=HTMLResponse)
def show_clinical_form(patient_id: str, request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("create_clinical.html", {
        "request": request,
        "patient_id": patient_id,
        "users": users
    })

@router.post("/patients/{patient_id}/clinical/create")
def save_clinical_record(
    patient_id: str,
    timestamp: str = Form(...),
    user_id: str = Form(...),
    gcs: int = Form(None),
    orientation: bool = Form(...),
    arm_strength: str = Form(None),
    leg_strength: str = Form(None),
    clinical_note: str = Form(None),
    version: int = Form(...),
    db: Session = Depends(get_db)
):
    record = ClinicalExam(
        id=str(uuid4()),
        patient_id=patient_id,
        user_id=user_id,
        timestamp=datetime.fromisoformat(timestamp),
        gcs=gcs,
        orientation=orientation,
        arm_strength=arm_strength,
        leg_strength=leg_strength,
        clinical_note=clinical_note,
        version=version,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(record)
    db.commit()
    return RedirectResponse(url=f"/patients/{patient_id}", status_code=303)

@router.get("/clinical/{record_id}/edit", response_class=HTMLResponse)
def edit_clinical_form(record_id: str, request: Request, db: Session = Depends(get_db)):
    record = db.get(ClinicalExam, record_id)
    users = db.query(User).all()
    return templates.TemplateResponse("edit_clinical.html", {
        "request": request,
        "record": record,
        "users": users
    })

@router.post("/clinical/{record_id}/edit")
def update_clinical_record(
    record_id: str,
    timestamp: str = Form(...),
    user_id: str = Form(...),
    gcs: int = Form(None),
    orientation: bool = Form(...),
    arm_strength: str = Form(None),
    leg_strength: str = Form(None),
    clinical_note: str = Form(None),
    version: int = Form(...),
    db: Session = Depends(get_db)
):
    record = db.get(ClinicalExam, record_id)
    record.timestamp = datetime.fromisoformat(timestamp)
    record.user_id = user_id
    record.gcs = gcs
    record.orientation = orientation
    record.arm_strength = arm_strength
    record.leg_strength = leg_strength
    record.clinical_note = clinical_note
    record.version = version
    record.updated_at = datetime.now()
    db.commit()
    return RedirectResponse(url=f"/patients/{record.patient_id}", status_code=303)

@router.post("/clinical/{record_id}/delete")
def delete_clinical_record(record_id: str, db: Session = Depends(get_db)):
    record = db.get(ClinicalExam, record_id)
    patient_id = record.patient_id
    db.delete(record)
    db.commit()
    return RedirectResponse(url=f"/patients/{patient_id}", status_code=303)

@router.get("/clinical/{record_id}", response_class=HTMLResponse)
def inspect_clinical_record(record_id: str, request: Request, db: Session = Depends(get_db)):
    record = db.get(ClinicalExam, record_id)

    patient = db.get(Patient, record.patient_id)
    user = db.get(User, record.user_id) if record.user_id else None

    return templates.TemplateResponse("inspect_clinical.html", {
        "request": request,
        "record": record,
        "patient_name": patient.name if patient else "Neznámý",
        "user_name": user.name if user else "Neznámý"
    })

@router.get("/clinical/{record_id}/fhir", response_class=JSONResponse)
def export_clinical_fhir(record_id: str, db: Session = Depends(get_db)):
    record = db.get(ClinicalExam, record_id)
    patient = db.get(Patient, record.patient_id)
    user = db.get(User, record.user_id) if record.user_id else None
    fhir_data = clinical_exam_to_fhir(record, patient=patient, user=user)
    return JSONResponse(content=fhir_data)
