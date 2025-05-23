from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4

from app.db import get_db
from app.models.vital_signs import VitalSigns
from app.models.user import User
from app.models.patient import Patient
from fastapi.responses import JSONResponse
from app.fhir.vital_to_fhir import vital_signs_to_fhir

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/patients/{patient_id}/vital/create", response_class=HTMLResponse)
def show_vital_form(patient_id: str, request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("create_vital.html", {
        "request": request,
        "patient_id": patient_id,
        "users": users
    })

@router.post("/patients/{patient_id}/vital/create")
def save_vital_record(
    patient_id: str,
    timestamp: str = Form(...),
    user_id: str = Form(...),
    temperature: float = Form(None),
    bp_systolic: int = Form(None),
    bp_diastolic: int = Form(None),
    heart_rate: int = Form(None),
    version: int = Form(...),
    db: Session = Depends(get_db)
):
    record = VitalSigns(
        id=str(uuid4()),
        patient_id=patient_id,
        user_id=user_id,
        timestamp=datetime.fromisoformat(timestamp),
        temperature=temperature,
        bp_systolic=bp_systolic,
        bp_diastolic=bp_diastolic,
        heart_rate=heart_rate,
        version=version,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(record)
    db.commit()
    return RedirectResponse(url=f"/patients/{patient_id}", status_code=303)

@router.get("/vital/{record_id}/edit", response_class=HTMLResponse)
def edit_vital_form(record_id: str, request: Request, db: Session = Depends(get_db)):
    record = db.get(VitalSigns, record_id)
    users = db.query(User).all()
    return templates.TemplateResponse("edit_vital.html", {
        "request": request,
        "record": record,
        "users": users
    })

@router.post("/vital/{record_id}/edit")
def update_vital_record(
    record_id: str,
    timestamp: str = Form(...),
    user_id: str = Form(...),
    temperature: float = Form(None),
    bp_systolic: int = Form(None),
    bp_diastolic: int = Form(None),
    heart_rate: int = Form(None),
    version: int = Form(...),
    db: Session = Depends(get_db)
):
    record = db.get(VitalSigns, record_id)
    record.timestamp = datetime.fromisoformat(timestamp)
    record.user_id = user_id
    record.temperature = temperature
    record.bp_systolic = bp_systolic
    record.bp_diastolic = bp_diastolic
    record.heart_rate = heart_rate
    record.version = version
    record.updated_at = datetime.now()
    db.commit()
    return RedirectResponse(url=f"/patients/{record.patient_id}", status_code=303)

@router.post("/vital/{record_id}/delete")
def delete_vital_record(record_id: str, db: Session = Depends(get_db)):
    record = db.get(VitalSigns, record_id)
    patient_id = record.patient_id
    db.delete(record)
    db.commit()
    return RedirectResponse(url=f"/patients/{patient_id}", status_code=303)

@router.get("/vital/{record_id}", response_class=HTMLResponse)
def inspect_vital_record(record_id: str, request: Request, db: Session = Depends(get_db)):
    record = db.get(VitalSigns, record_id)

    patient = db.get(Patient, record.patient_id)
    user = db.get(User, record.user_id) if record.user_id else None

    return templates.TemplateResponse("inspect_vital.html", {
        "request": request,
        "record": record,
        "patient_name": patient.name if patient else "Neznámý",
        "user_name": user.name if user else "Neznámý"
    })

@router.get("/vital/{record_id}/fhir", response_class=JSONResponse)
def export_vital_fhir(record_id: str, db: Session = Depends(get_db)):
    record = db.get(VitalSigns, record_id)
    patient = db.get(Patient, record.patient_id)
    user = db.get(User, record.user_id) if record.user_id else None
    fhir_data = vital_signs_to_fhir(record, patient=patient, user=user)
    return JSONResponse(content=fhir_data)
