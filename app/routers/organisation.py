from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from app.db import get_db
from app.schemas.organisation import OrganisationCreate, OrganisationUpdate
from app.models.organisation import Organisation
from sqlalchemy import select

router = APIRouter(prefix="/organisations", tags=["organisations"])

@router.get("/")
def get_all_organisations(db: Session = Depends(get_db)):
    return db.execute(select(Organisation)).scalars().all()

@router.get("/{organisation_id}")
def get_organisation(organisation_id: str, db: Session = Depends(get_db)):
    organisation = db.get(Organisation, organisation_id)
    if not organisation:
        raise HTTPException(status_code=404, detail="Organizace nenalezena")
    return organisation

@router.post("/")
def create_organisation(data: OrganisationCreate, db: Session = Depends(get_db)):
    organisation = Organisation(id=str(uuid4()), **data.dict())
    db.add(organisation)
    db.commit()
    db.refresh(organisation)
    return organisation

@router.put("/{organisation_id}")
def update_organisation(organisation_id: str, data: OrganisationUpdate, db: Session = Depends(get_db)):
    organisation = db.get(Organisation, organisation_id)
    if not organisation:
        raise HTTPException(status_code=404, detail="Organizace nenalezena")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(organisation, field, value)

    db.commit()
    db.refresh(organisation)
    return organisation

@router.delete("/{organisation_id}")
def delete_organisation(organisation_id: str, db: Session = Depends(get_db)):
    organisation = db.get(Organisation, organisation_id)
    if not organisation:
        raise HTTPException(status_code=404, detail="Organizace nenalezena")
    db.delete(organisation)
    db.commit()
    return {"message": "Organizace smazána"}
