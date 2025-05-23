from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from app.models.base import Base

class SocialBackground(Base):
    __tablename__ = "social_background"

    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patient.id"), nullable=False)
    user_id = Column(String, ForeignKey("user.id"), nullable=True)
    timestamp = Column(DateTime, nullable=False)
    occupation = Column(String)
    lifestyle = Column(String)
    sleep_pattern = Column(String)
    sleep_duration = Column(Float)
    version = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
