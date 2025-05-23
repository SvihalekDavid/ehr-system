from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime
from app.models.base import Base

class NeurologicalSymptoms(Base):
    __tablename__ = "neurological_symptoms"

    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patient.id"), nullable=False)
    user_id = Column(String, ForeignKey("user.id"), nullable=True)
    timestamp = Column(DateTime, nullable=False)
    headache = Column(Boolean)
    headache_type = Column(String)
    intensity = Column(Integer)
    dizziness = Column(Boolean)
    balance_issues = Column(Boolean)
    consciousness_issues = Column(Boolean)
    drunk_feeling = Column(Boolean)
    version = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
