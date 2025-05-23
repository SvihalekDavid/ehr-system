from pydantic import BaseModel
from datetime import datetime

class EEGRecordCreate(BaseModel):
    patient_id: str
    user_id: str | None = None
    timestamp: datetime
    eeg_type: str | None = None
    dominant_frequency: float | None = None
    abnormal_rhythms: bool | None = None
    abnormal_rhythm_type: str | None = None
    technician_comment: str | None = None
    version: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

class EEGRecordUpdate(EEGRecordCreate):
    pass
