#Schemas define the structure of requests and responses
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content:str
    published: bool = True

#Defines structure of how data should be sent from the frontend
class PostCreate(PostBase):
    pass #helps avoid errors in our class 


#Defines structure of how data should be sent to the user or how a response should be structured
class PostResponse(BaseModel):
    title:str
    content:str
    published:bool

    class Config:
        orm_mode = True