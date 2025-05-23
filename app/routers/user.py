from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from app.db import get_db
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from sqlalchemy import select

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def get_all_users(db: Session = Depends(get_db)):
    return db.execute(select(User)).scalars().all()

@router.get("/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Uživatel nenalezen")
    return user

@router.post("/")
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    user = User(id=str(uuid4()), **data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.put("/{user_id}")
def update_user(user_id: str, data: UserUpdate, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Uživatel nenalezen")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Uživatel nenalezen")
    db.delete(user)
    db.commit()
    return {"message": "Uživatel smazán"}
