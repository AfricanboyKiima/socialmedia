from fastapi import FastAPI 
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


"""
Implement schema through which we can define 
what we want our data to look like
"""
#This post class allows us to post stuff from the frontend based on a well defined schema or data model
#In such a way a user will only send us the data we defined in the model and nothing else.
#In addition, we are able to define what datatype of the data we want for each of our properties
#We achieve such behaviour by inheriting from the BaseModel class imported from the pydantic library
class Post(BaseModel):
    title:str
    content:str
    published : bool = True
    rating: Optional[int] = None#a completely optional field 

app = FastAPI() #Instantiate object from the FASTAPI class(model) to access its attributes and methods


my_posts = [{"title":"title of post 1","content":"Content of post1","id":1},
            
            {"title":"title of post 2","content":"Content of post 2","id":2}]

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
    return {"message":"Welcome to my start up. My name is Kiima Samuel"}
#...All this is referred to as a path operation

#this takes us to post url http://127.0.0.1:8000/posts
@app.get("/posts")
def get_posts():
    return {"data":my_posts}

#http://127.0.0.1:8000/createposts 
@app.post("/posts")
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0,  100000000000)#randrange imported from random module
    my_posts.append(post_dict)
    return {"data":post_dict}



@app.get('/')
def welcome():
    return {"message":"Welcome to my person api testing end point"}



"""

#Created person schema 
class Person(BaseModel):
    first_name:str
    last_name:str
    email:Optional[str] = None#this is nullable
    about:str

@app.get("/person")
def get_person():
    return {"data":"You've accessd a person"}

@app.post("/person")
def person(var:Person):
    my_posts.append(var)
    print(my_posts)
    return {"data":var}
"""