from fastapi import FastAPI 
from fastapi.params import Body
from pydantic import BaseModel


"""
Implement schema through which we can define 
what we want our data to look like
"""
#This post class allows us to post stuff from the frontend based on a well defined schema or database model
#In such a way a user will only send us the data we defined in the model and nothing else.
#In addition, we are able to define what datatype of the data we want for each of our properties
#We achieve such behaviour by inheriting from the BaseModel class imported from the pydantic library
class Post(BaseModel):
    title:str
    content:str


app = FastAPI() #Instantiate object from the FASTAPI class(model) to access its attributes and methods

"""
fastapi is an asynchronous capable python programming language framework 
This simply means that a webserver forwards requests to it using the ASGI convention
Asynchronous Server Gateway interface
"""
#...path operation OR route(synonym) in other frameworks
"""Async here means something that's going to take some amount of time such as making an api call"""
"""The decorator changes the behaviour of our function so that is acts as an api end point"""

#This takes us to the root page of our api http://127.0.0.1:8000
@app.get("/")
def root():
    return {"message":"Welcome to my start up"}
#...All this is referred to as a path operation

#this takes us to post url http://127.0.0.1:8000/posts
@app.get("/posts")
def get_posts():
    return {"data":"This is your first retrieved post"}

@app.post("/createpost")
def create_post(cont: Post):
    print(cont)
    return {"results":cont}