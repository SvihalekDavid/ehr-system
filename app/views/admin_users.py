from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db import get_db
from app.models.user import User
from app.models.organisation import Organisation
from uuid import uuid4

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/admin/users", response_class=HTMLResponse)
def list_users(request: Request, db: Session = Depends(get_db)):
    users = db.execute(select(User)).scalars().all()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@router.get("/admin/users/create", response_class=HTMLResponse)
def create_user_form(request: Request, db: Session = Depends(get_db)):
    orgs = db.execute(select(Organisation)).scalars().all()
    return templates.TemplateResponse("create_user.html", {"request": request, "orgs": orgs})

@router.post("/admin/users/create")
def create_user(
    name: str = Form(...),
    role: str = Form(...),
    organisation_id: str | None = Form(None),
    db: Session = Depends(get_db)
):
    user = User(id=str(uuid4()), name=name, role=role, organisation_id=organisation_id)
    db.add(user)
    db.commit()
    return RedirectResponse("/admin/users", status_code=303)

@router.get("/admin/users/{user_id}/edit", response_class=HTMLResponse)
def edit_user_form(user_id: str, request: Request, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    orgs = db.execute(select(Organisation)).scalars().all()
    return templates.TemplateResponse("edit_user.html", {"request": request, "user": user, "orgs": orgs})

@router.post("/admin/users/{user_id}/edit")
def update_user(
    user_id: str,
    name: str = Form(...),
    role: str = Form(...),
    organisation_id: str | None = Form(None),
    db: Session = Depends(get_db)
):
    user = db.get(User, user_id)
    user.name = name
    user.role = role
    user.organisation_id = organisation_id
    db.commit()
    return RedirectResponse("/admin/users", status_code=303)

@router.post("/admin/users/{user_id}/delete")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user:
        db.delete(user)
        db.commit()
    return RedirectResponse("/admin/users", status_code=303)
