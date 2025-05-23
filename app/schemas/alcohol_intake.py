from pydantic import BaseModel
from datetime import datetime

class AlcoholIntakeCreate(BaseModel):
    patient_id: str
    user_id: str | None = None
    timestamp: datetime
    alcohol_type: str | None = None
    amount_units: float | None = None
    frequency: str | None = None
    audit_score: int | None = None
    version: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

class AlcoholIntakeUpdate(AlcoholIntakeCreate):
    pass
