from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4

from app.db import get_db
from app.models.neurological_symptoms import NeurologicalSymptoms
from app.models.user import User
from app.models.patient import Patient
from fastapi.responses import JSONResponse
from app.fhir.neurological_to_fhir import neurological_symptoms_to_fhir


templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/patients/{patient_id}/neuro/create", response_class=HTMLResponse)
def show_neuro_form(patient_id: str, request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("create_neurological_symptoms.html", {
        "request": request,
        "patient_id": patient_id,
        "users": users
    })

@router.post("/patients/{patient_id}/neuro/create")
def save_neuro_record(
    patient_id: str,
    timestamp: str = Form(...),
    user_id: str = Form(...),
    headache: bool = Form(...),
    headache_type: str = Form(None),
    intensity: int = Form(None),
    dizziness: bool = Form(...),
    balance_issues: bool = Form(...),
    consciousness_issues: bool = Form(...),
    drunk_feeling: bool = Form(...),
    version: int = Form(...),
    db: Session = Depends(get_db)
):
    record = NeurologicalSymptoms(
        id=str(uuid4()),
        patient_id=patient_id,
        user_id=user_id,
        timestamp=datetime.fromisoformat(timestamp),
        headache=headache,
        headache_type=headache_type,
        intensity=intensity,
        dizziness=dizziness,
        balance_issues=balance_issues,
        consciousness_issues=consciousness_issues,
        drunk_feeling=drunk_feeling,
        version=version,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(record)
    db.commit()
    return RedirectResponse(url=f"/patients/{patient_id}", status_code=303)

@router.get("/neuro/{record_id}/edit", response_class=HTMLResponse)
def edit_neuro_form(record_id: str, request: Request, db: Session = Depends(get_db)):
    record = db.get(NeurologicalSymptoms, record_id)
    users = db.query(User).all()
    return templates.TemplateResponse("edit_neurological_symptoms.html", {
        "request": request,
        "record": record,
        "users": users
    })

@router.post("/neuro/{record_id}/edit")
def update_neuro_record(
    record_id: str,
    timestamp: str = Form(...),
    user_id: str = Form(...),
    headache: bool = Form(...),
    headache_type: str = Form(None),
    intensity: int = Form(None),
    dizziness: bool = Form(...),
    balance_issues: bool = Form(...),
    consciousness_issues: bool = Form(...),
    drunk_feeling: bool = Form(...),
    version: int = Form(...),
    db: Session = Depends(get_db)
):
    record = db.get(NeurologicalSymptoms, record_id)
    record.timestamp = datetime.fromisoformat(timestamp)
    record.user_id = user_id
    record.headache = headache
    record.headache_type = headache_type
    record.intensity = intensity
    record.dizziness = dizziness
    record.balance_issues = balance_issues
    record.consciousness_issues = consciousness_issues
    record.drunk_feeling = drunk_feeling
    record.version = version
    record.updated_at = datetime.now()
    db.commit()
    return RedirectResponse(url=f"/patients/{record.patient_id}", status_code=303)

@router.post("/neuro/{record_id}/delete")
def delete_neuro_record(record_id: str, db: Session = Depends(get_db)):
    record = db.get(NeurologicalSymptoms, record_id)
    patient_id = record.patient_id
    db.delete(record)
    db.commit()
    return RedirectResponse(url=f"/patients/{patient_id}", status_code=303)

@router.get("/neuro/{record_id}", response_class=HTMLResponse)
def inspect_neuro_record(record_id: str, request: Request, db: Session = Depends(get_db)):
    record = db.get(NeurologicalSymptoms, record_id)

    patient = db.get(Patient, record.patient_id)
    user = db.get(User, record.user_id) if record.user_id else None

    return templates.TemplateResponse("inspect_neuro.html", {
        "request": request,
        "record": record,
        "patient_name": patient.name if patient else "Neznámý",
        "user_name": user.name if user else "Neznámý"
    })

@router.get("/neuro/{record_id}/fhir", response_class=JSONResponse)
def export_neuro_fhir(record_id: str, db: Session = Depends(get_db)):
    record = db.get(NeurologicalSymptoms, record_id)
    fhir_data = neurological_symptoms_to_fhir(record)
    return JSONResponse(content=fhir_data)


