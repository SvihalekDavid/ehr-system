from pydantic import BaseModel
from datetime import datetime

class NeuroSymptomsCreate(BaseModel):
    patient_id: str
    user_id: str | None = None
    timestamp: datetime
    headache: bool | None = None
    headache_type: str | None = None
    intensity: int | None = None
    dizziness: bool | None = None
    balance_issues: bool | None = None
    consciousness_issues: bool | None = None
    drunk_feeling: bool | None = None
    version: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

class NeuroSymptomsUpdate(NeuroSymptomsCreate):
    pass
