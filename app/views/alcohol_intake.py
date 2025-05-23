from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4

from app.db import get_db
from app.models.alcohol_intake import AlcoholIntake
from app.models.user import User
from app.models.patient import Patient
from fastapi.responses import JSONResponse
from app.fhir.alcohol_to_fhir import alcohol_intake_to_fhir

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/patients/{patient_id}/alcohol/create", response_class=HTMLResponse)
def show_alcohol_form(patient_id: str, request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("create_alcohol.html", {"request": request, "patient_id": patient_id, "users": users})

@router.post("/patients/{patient_id}/alcohol/create")
def save_alcohol_record(
    patient_id: str,
    timestamp: str = Form(...),
    user_id: str = Form(...),
    alcohol_type: str = Form(...),
    amount_units: float = Form(...),
    frequency: str = Form(...),
    audit_score: int = Form(None),
    version: int = Form(...),
    db: Session = Depends(get_db)
):
    record = AlcoholIntake(
        id=str(uuid4()),
        patient_id=patient_id,
        user_id=user_id,
        timestamp=datetime.fromisoformat(timestamp),
        alcohol_type=alcohol_type,
        amount_units=amount_units,
        frequency=frequency,
        audit_score=audit_score,
        version=version,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(record)
    db.commit()
    return RedirectResponse(url=f"/patients/{patient_id}", status_code=303)

@router.get("/alcohol/{record_id}/edit", response_class=HTMLResponse)
def edit_alcohol_form(record_id: str, request: Request, db: Session = Depends(get_db)):
    record = db.get(AlcoholIntake, record_id)
    users = db.query(User).all()
    return templates.TemplateResponse("edit_alcohol.html", {"request": request, "record": record, "users": users})

@router.post("/alcohol/{record_id}/edit")
def update_alcohol_record(
    record_id: str,
    timestamp: str = Form(...),
    user_id: str = Form(...),
    alcohol_type: str = Form(...),
    amount_units: float = Form(...),
    frequency: str = Form(...),
    audit_score: int = Form(None),
    version: int = Form(...),
    db: Session = Depends(get_db)
):
    record = db.get(AlcoholIntake, record_id)
    record.timestamp = datetime.fromisoformat(timestamp)
    record.user_id = user_id
    record.alcohol_type = alcohol_type
    record.amount_units = amount_units
    record.frequency = frequency
    record.audit_score = audit_score
    record.version = version
    record.updated_at = datetime.now()
    db.commit()
    return RedirectResponse(url=f"/patients/{record.patient_id}", status_code=303)

@router.post("/alcohol/{record_id}/delete")
def delete_alcohol_record(record_id: str, db: Session = Depends(get_db)):
    record = db.get(AlcoholIntake, record_id)
    patient_id = record.patient_id
    db.delete(record)
    db.commit()
    return RedirectResponse(url=f"/patients/{patient_id}", status_code=303)

@router.get("/alcohol/{record_id}", response_class=HTMLResponse)
def inspect_alcohol_record(record_id: str, request: Request, db: Session = Depends(get_db)):
    record = db.get(AlcoholIntake, record_id)

    patient = db.get(Patient, record.patient_id)
    user = db.get(User, record.user_id) if record.user_id else None

    return templates.TemplateResponse("inspect_alcohol.html", {
        "request": request,
        "record": record,
        "patient_name": patient.name if patient else "Neznámý",
        "user_name": user.name if user else "Neznámý"
    })

@router.get("/alcohol/{record_id}/fhir", response_class=JSONResponse)
def export_alcohol_fhir(record_id: str, db: Session = Depends(get_db)):
    record = db.get(AlcoholIntake, record_id)
    patient = db.get(Patient, record.patient_id)
    user = db.get(User, record.user_id) if record.user_id else None
    fhir_data = alcohol_intake_to_fhir(record, patient=patient, user=user)
    return JSONResponse(content=fhir_data)