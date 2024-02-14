#Schemas define the structure of requests and responses
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content:str
    published: bool = True

class PostCreate(PostBase):
    pass #helps avoid errors in our class 
