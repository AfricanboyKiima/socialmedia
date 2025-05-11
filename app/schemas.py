#Schemas define the structure of requests and responses
from pydantic import BaseModel,EmailStr
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
    email:EmailStr
    password:str



class UserCreate(UserBase):#used to create users
    pass


class UserUpdate(UserBase):#used to update user data
    pass


class UserResponse(BaseModel):#defines structure of data to the frontend
    id:int
    email:EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
