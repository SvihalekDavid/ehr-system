from pydantic import BaseModel
from datetime import date

class PatientCreate(BaseModel):
    name: str
    birth_date: date
    sex: str

class PatientUpdate(BaseModel):
    name: str | None = None
    birth_date: date | None = None
    sex: str | None = None
