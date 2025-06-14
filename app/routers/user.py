from fastapi import Depends, HTTPException, status, Response, APIRouter

from app import models
from ..schemas import schemas
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.utils import *
from typing import List


router = APIRouter(
    prefix="/users",
    tags=['Users'] #Used to group user endpoint routes in one place
)

@router.get("/",response_model=List[schemas.UserResponse])
def get_users(db:Session = Depends(get_db)):
    users = db.query(models.users.User).all()
    return users


@router.get("/{id}",response_model= schemas.UserResponse)
def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.users.User).filter(models.users.User.user_id == id).first()
    if user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"user with id {id} doesn't exist ")
    return user


@router.post("/",status_code = status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    existing_user = db.query(models.users.User).filter(models.users.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
    user.password = password_hasher(user.password)
    new_user = models.users.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.delete("/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.users.User).filter(models.users.User.user_id == id)
    if user.first() is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"user with id {id} doesn't exist")
    user.delete(synchronize_session =False)
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.UserResponse)
def update_user(id:int, updated_user:schemas.UserUpdate, db:Session=Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id {id} doesn't exist")
    user_query.update(updated_user.dict(),synchronize_session=False)
    db.commit()
    return user_query.first() 
