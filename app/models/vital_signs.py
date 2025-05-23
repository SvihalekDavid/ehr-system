from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from app.models.base import Base

class VitalSigns(Base):
    __tablename__ = "vital_signs"

    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patient.id"), nullable=False)
    user_id = Column(String, ForeignKey("user.id"), nullable=True)
    timestamp = Column(DateTime, nullable=False)
    temperature = Column(Float)
    bp_systolic = Column(Integer)
    bp_diastolic = Column(Integer)
    heart_rate = Column(Integer)
    version = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
