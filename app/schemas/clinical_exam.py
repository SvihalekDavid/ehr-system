from pydantic import BaseModel
from datetime import datetime

class ClinicalExamCreate(BaseModel):
    patient_id: str
    user_id: str | None = None
    timestamp: datetime
    gcs: int | None = None
    orientation: bool | None = None
    arm_strength: str | None = None
    leg_strength: str | None = None
    clinical_note: str | None = None
    version: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

class ClinicalExamUpdate(ClinicalExamCreate):
    pass
