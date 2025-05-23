from fastapi import FastAPI
from app.routers import (
    patient, user, organisation, eeg_record, alcohol_intake,
    neurological_symptoms, clinical_exam, vital_signs, social_background
)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.views import (
    home, patients_gui, admin_users, admin_organisations,
    admin, eeg, alcohol_intake, neurological_symptoms, clinical_exam,
    vital_signs, social_background
)
import os
from app.db import engine
from app.models import Base

db_path = "data/ehr.db"
if not os.path.exists(db_path):
    print("📄 Vytvářím databázi...")
    Base.metadata.create_all(bind=engine)

app = FastAPI()

# GUI
app.include_router(home.router)
app.include_router(patients_gui.router)
app.include_router(admin_users.router)
app.include_router(admin_organisations.router)
app.include_router(admin.router)
app.include_router(eeg.router)
app.include_router(neurological_symptoms.router)
app.include_router(clinical_exam.router)
app.include_router(vital_signs.router)
app.include_router(social_background.router)


# API
app.include_router(patient.router)
app.include_router(user.router)
app.include_router(organisation.router)
app.include_router(eeg_record.router)
app.include_router(alcohol_intake.router)
app.include_router(neurological_symptoms.router)
app.include_router(clinical_exam.router)
app.include_router(vital_signs.router)
app.include_router(social_background.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
