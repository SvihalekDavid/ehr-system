from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    role: str
    organisation_id: str | None = None

class UserUpdate(BaseModel):
    name: str | None = None
    role: str | None = None
    organisation_id: str | None = None
