from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db import get_db
from app.models.organisation import Organisation
from uuid import uuid4

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/admin/organisations", response_class=HTMLResponse)
def list_organisations(request: Request, db: Session = Depends(get_db)):
    orgs = db.execute(select(Organisation)).scalars().all()
    return templates.TemplateResponse("organisations.html", {"request": request, "orgs": orgs})

@router.get("/admin/organisations/create", response_class=HTMLResponse)
def create_organisation_form(request: Request):
    return templates.TemplateResponse("create_organisation.html", {"request": request})

@router.post("/admin/organisations/create")
def create_organisation(name: str = Form(...), address: str = Form(...), db: Session = Depends(get_db)):
    org = Organisation(id=str(uuid4()), name=name, address=address)
    db.add(org)
    db.commit()
    return RedirectResponse("/admin/organisations", status_code=303)

@router.get("/admin/organisations/{org_id}/edit", response_class=HTMLResponse)
def edit_organisation_form(org_id: str, request: Request, db: Session = Depends(get_db)):
    org = db.get(Organisation, org_id)
    return templates.TemplateResponse("edit_organisation.html", {"request": request, "org": org})

@router.post("/admin/organisations/{org_id}/edit")
def update_organisation(org_id: str, name: str = Form(...), address: str = Form(...), db: Session = Depends(get_db)):
    org = db.get(Organisation, org_id)
    org.name = name
    org.address = address
    db.commit()
    return RedirectResponse("/admin/organisations", status_code=303)

@router.post("/admin/organisations/{org_id}/delete")
def delete_organisation(org_id: str, db: Session = Depends(get_db)):
    org = db.get(Organisation, org_id)
    if org:
        db.delete(org)
        db.commit()
    return RedirectResponse("/admin/organisations", status_code=303)
