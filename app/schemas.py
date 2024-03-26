#Schemas define the structure of requests and responses
from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content:str
    published: bool = True

#Defines structure of how data should be sent from the frontend
class PostCreate(PostBase):
    pass #helps avoid errors in our class 


#Defines structure of how data should be sent to the user or how a response should be structured
class PostResponse(PostBase):
    id:int
    created_at:datetime

    class Config:
        orm_mode = True# pydantic's orm_mode tells the pydantinc model to read the data even if it's not a dict



#My user schema
class UserBase(BaseModel):
    email:str
    password:str



class UserCreate(UserBase):
    pass


class UserResponse(BaseModel):
    created_at:datetime
    email:str
    class Config:
        orm_mode = True
