from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from app.models.base import Base

class ClinicalExam(Base):
    __tablename__ = "clinical_exam"

    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patient.id"), nullable=False)
    user_id = Column(String, ForeignKey("user.id"), nullable=True)
    timestamp = Column(DateTime, nullable=False)
    gcs = Column(Integer)
    orientation = Column(Boolean)
    arm_strength = Column(String)
    leg_strength = Column(String)
    clinical_note = Column(String)
    version = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
