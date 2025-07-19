from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.database import database

from app import models
from app import utils, oauth2
from sqlalchemy.orm import Session


router = APIRouter(
   tags=['Authentication']
)


@router.post("/login")
def login(user_credential:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):

    user = db.query(models.users.User).filter(models.users.User.email == user_credential.username).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid credentials")
    
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id":user.user_id})
    
    return {"access_token":access_token, "token_type":"bearer"}