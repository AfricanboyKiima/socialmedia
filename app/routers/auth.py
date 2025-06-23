from fastapi import APIRouter, Depends, HTTPException, status, Response

from app.schemas import schemas

from app.database import database

from app import models
from .. import utils
from sqlalchemy.orm import Session


router = APIRouter(
   tags=['Authentication']
)


@router.post("/login")
def login(user_credential:schemas.UserLogin, db:Session = Depends(database.get_db)):

    user = db.query(models.users.User).filter(models.users.User.email == user_credential.email).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid credentials")
    
    if not utils.verify(user_credential.password, user.password):

        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    return {"token":"We have a user with such credentials"}