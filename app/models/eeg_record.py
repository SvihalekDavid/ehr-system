from sqlalchemy import Column, String, ForeignKey, DateTime, Float, Boolean
from app.models.base import Base

class EEGRecord(Base):
    __tablename__ = "eeg_record"

    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patient.id"), nullable=False)
    user_id = Column(String, ForeignKey("user.id"), nullable=True)
    timestamp = Column(DateTime, nullable=False)
    eeg_type = Column(String)
    dominant_frequency = Column(Float)
    abnormal_rhythms = Column(Boolean)
    abnormal_rhythm_type = Column(String)
    technician_comment = Column(String)
    version = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
