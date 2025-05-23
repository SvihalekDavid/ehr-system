from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4

from app.db import get_db
from app.models.eeg_record import EEGRecord
from app.models.user import User
from app.models.patient import Patient
from fastapi.responses import JSONResponse
from app.fhir.eeg_to_fhir import eeg_record_to_fhir

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/patients/{patient_id}/eeg/create", response_class=HTMLResponse)
def show_eeg_form(patient_id: str, request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("create_eeg.html", {
        "request": request,
        "patient_id": patient_id,
        "users": users
    })

@router.post("/patients/{patient_id}/eeg/create")
def save_eeg_record(
    patient_id: str,
    timestamp: str = Form(...),
    user_id: str = Form(...),
    eeg_type: str = Form(None),
    dominant_frequency: float = Form(None),
    abnormal_rhythms: str = Form(None),
    abnormal_rhythm_type: str = Form(None),
    technician_comment: str = Form(None),
    version: int = Form(...),
    db: Session = Depends(get_db)
):
    record = EEGRecord(
        id=str(uuid4()),
        patient_id=patient_id,
        user_id=user_id,
        timestamp=datetime.fromisoformat(timestamp),
        eeg_type=eeg_type,
        dominant_frequency=dominant_frequency,
        abnormal_rhythms=(abnormal_rhythms == "True"),
        abnormal_rhythm_type=abnormal_rhythm_type,
        technician_comment=technician_comment,
        version=version,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(record)
    db.commit()
    return RedirectResponse(url=f"/patients/{patient_id}", status_code=303)

@router.get("/eeg/{eeg_id}/edit", response_class=HTMLResponse)
def edit_eeg_form(eeg_id: str, request: Request, db: Session = Depends(get_db)):
    record = db.get(EEGRecord, eeg_id)
    users = db.query(User).all()
    return templates.TemplateResponse("edit_eeg.html", {
        "request": request,
        "record": record,
        "users": users
    })

@router.post("/eeg/{eeg_id}/edit")
def update_eeg_record(
    eeg_id: str,
    timestamp: str = Form(...),
    user_id: str = Form(...),
    eeg_type: str = Form(None),
    dominant_frequency: float = Form(None),
    abnormal_rhythms: str = Form(None),
    abnormal_rhythm_type: str = Form(None),
    technician_comment: str = Form(None),
    version: int = Form(...),
    db: Session = Depends(get_db)
):
    record = db.get(EEGRecord, eeg_id)
    record.timestamp = datetime.fromisoformat(timestamp)
    record.user_id = user_id
    record.eeg_type = eeg_type
    record.dominant_frequency = dominant_frequency
    record.abnormal_rhythms = (abnormal_rhythms == "True")
    record.abnormal_rhythm_type = abnormal_rhythm_type
    record.technician_comment = technician_comment
    record.version = version
    record.updated_at = datetime.now()
    db.commit()
    return RedirectResponse(url=f"/patients/{record.patient_id}", status_code=303)

@router.post("/eeg/{eeg_id}/delete")
def delete_eeg_record(eeg_id: str, db: Session = Depends(get_db)):
    record = db.get(EEGRecord, eeg_id)
    patient_id = record.patient_id
    db.delete(record)
    db.commit()
    return RedirectResponse(url=f"/patients/{patient_id}", status_code=303)

@router.get("/eeg/{eeg_id}", response_class=HTMLResponse)
def inspect_eeg_record(eeg_id: str, request: Request, db: Session = Depends(get_db)):
    record = db.get(EEGRecord, eeg_id)

    # načteme jméno pacienta a uživatele
    patient = db.get(Patient, record.patient_id)
    user = db.get(User, record.user_id) if record.user_id else None

    return templates.TemplateResponse("inspect_eeg.html", {
        "request": request,
        "record": record,
        "patient_name": patient.name if patient else "Neznámý",
        "user_name": user.name if user else "Neznámý"
    })

@router.get("/eeg/{eeg_id}/fhir", response_class=JSONResponse)
def export_eeg_to_fhir(eeg_id: str, db: Session = Depends(get_db)):
    record = db.get(EEGRecord, eeg_id)
    fhir_data = eeg_record_to_fhir(record)
    return JSONResponse(content=fhir_data)