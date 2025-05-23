from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4

from app.db import get_db
from app.models.social_background import SocialBackground
from app.models.user import User
from app.models.patient import Patient
from fastapi.responses import JSONResponse
from app.fhir.social_to_fhir import social_background_to_fhir

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/patients/{patient_id}/social/create", response_class=HTMLResponse)
def show_social_form(patient_id: str, request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("create_social.html", {
        "request": request,
        "patient_id": patient_id,
        "users": users
    })

@router.post("/patients/{patient_id}/social/create")
def save_social_record(
    patient_id: str,
    timestamp: str = Form(...),
    user_id: str = Form(...),
    occupation: str = Form(None),
    lifestyle: str = Form(None),
    sleep_pattern: str = Form(None),
    sleep_duration: float = Form(None),
    version: int = Form(...),
    db: Session = Depends(get_db)
):
    record = SocialBackground(
        id=str(uuid4()),
        patient_id=patient_id,
        user_id=user_id,
        timestamp=datetime.fromisoformat(timestamp),
        occupation=occupation,
        lifestyle=lifestyle,
        sleep_pattern=sleep_pattern,
        sleep_duration=sleep_duration,
        version=version,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(record)
    db.commit()
    return RedirectResponse(url=f"/patients/{patient_id}", status_code=303)

@router.get("/social/{record_id}/edit", response_class=HTMLResponse)
def edit_social_form(record_id: str, request: Request, db: Session = Depends(get_db)):
    record = db.get(SocialBackground, record_id)
    users = db.query(User).all()
    return templates.TemplateResponse("edit_social.html", {
        "request": request,
        "record": record,
        "users": users
    })

@router.post("/social/{record_id}/edit")
def update_social_record(
    record_id: str,
    timestamp: str = Form(...),
    user_id: str = Form(...),
    occupation: str = Form(None),
    lifestyle: str = Form(None),
    sleep_pattern: str = Form(None),
    sleep_duration: float = Form(None),
    version: int = Form(...),
    db: Session = Depends(get_db)
):
    record = db.get(SocialBackground, record_id)
    record.timestamp = datetime.fromisoformat(timestamp)
    record.user_id = user_id
    record.occupation = occupation
    record.lifestyle = lifestyle
    record.sleep_pattern = sleep_pattern
    record.sleep_duration = sleep_duration
    record.version = version
    record.updated_at = datetime.now()
    db.commit()
    return RedirectResponse(url=f"/patients/{record.patient_id}", status_code=303)

@router.post("/social/{record_id}/delete")
def delete_social_record(record_id: str, db: Session = Depends(get_db)):
    record = db.get(SocialBackground, record_id)
    patient_id = record.patient_id
    db.delete(record)
    db.commit()
    return RedirectResponse(url=f"/patients/{patient_id}", status_code=303)

@router.get("/social/{record_id}", response_class=HTMLResponse)
def inspect_social_record(record_id: str, request: Request, db: Session = Depends(get_db)):
    record = db.get(SocialBackground, record_id)

    patient = db.get(Patient, record.patient_id)
    user = db.get(User, record.user_id) if record.user_id else None

    return templates.TemplateResponse("inspect_social.html", {
        "request": request,
        "record": record,
        "patient_name": patient.name if patient else "Neznámý",
        "user_name": user.name if user else "Neznámý"
    })

@router.get("/social/{record_id}/fhir", response_class=JSONResponse)
def export_social_fhir(record_id: str, db: Session = Depends(get_db)):
    record = db.get(SocialBackground, record_id)
    patient = db.get(Patient, record.patient_id)
    user = db.get(User, record.user_id) if record.user_id else None
    fhir_data = social_background_to_fhir(record, patient=patient, user=user)
    return JSONResponse(content=fhir_data)


