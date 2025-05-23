from sqlalchemy import Column, String
from app.models.base import Base

class Organisation(Base):
    __tablename__ = "organisation"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String)
