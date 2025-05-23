from pydantic import BaseModel
from datetime import datetime

class VitalSignsCreate(BaseModel):
    patient_id: str
    user_id: str | None = None
    timestamp: datetime
    temperature: float | None = None
    bp_systolic: int | None = None
    bp_diastolic: int | None = None
    heart_rate: int | None = None
    version: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

class VitalSignsUpdate(VitalSignsCreate):
    pass
