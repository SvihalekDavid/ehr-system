from pydantic import BaseModel

class OrganisationCreate(BaseModel):
    name: str
    address: str | None = None

class OrganisationUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
