from sqlalchemy import Column, String, Date
from app.models.base import Base

class Patient(Base):
    __tablename__ = "patient"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    sex = Column(String, nullable=False)
