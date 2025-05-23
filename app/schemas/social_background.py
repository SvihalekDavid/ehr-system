from pydantic import BaseModel
from datetime import datetime

class SocialBackgroundCreate(BaseModel):
    patient_id: str
    user_id: str | None = None
    timestamp: datetime
    occupation: str | None = None
    lifestyle: str | None = None
    sleep_pattern: str | None = None
    sleep_duration: float | None = None
    version: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

class SocialBackgroundUpdate(SocialBackgroundCreate):
    pass
