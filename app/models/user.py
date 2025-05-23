from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True)
    name = Column(String)
    role = Column(String)
    organisation_id = Column(String, ForeignKey("organisation.id"), nullable=True)

    organisation = relationship("Organisation", backref="users")
