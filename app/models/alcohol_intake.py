from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime
from app.models.base import Base

class AlcoholIntake(Base):
    __tablename__ = "alcohol_intake"

    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patient.id"), nullable=False)
    user_id = Column(String, ForeignKey("user.id"), nullable=True)
    timestamp = Column(DateTime, nullable=False)
    alcohol_type = Column(String)
    amount_units = Column(Float)
    frequency = Column(String)
    audit_score = Column(Integer)
    version = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
