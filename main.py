from fastapi import FastAPI, Response, status #access the fastapi class to instantiate objects from it
from fastapi.params import Body#we used this to send receive posts but a user could send anything which isn't what we want 
from pydantic import BaseModel#we then defined a schema to be able to define what we would want our data to look like
from typing import Optional#make a field to be nullable
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
    rating: Optional[int] = None#a completely optional field that means it's nullable

app = FastAPI() #Instantiate object from the FASTAPI class(model) to access its attributes and methods


my_posts = [{"title":"title of post 1","content":"Content of post1","id":1},
            
            {"title":"title of post 2","content":"Content of post 2","id":2}]

#this returns a post based on a given id since each post has a unique value(id)
def find_posts(id):
    for p in my_posts:
        if p['id'] == id:
            return p


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


#this takes us to post url http://127.0.0.1:8000/posts it accesses all the posts
@app.get("/posts")
def get_posts():
    return {"data":my_posts}


@app.get("/posts/{id}")
def get_post(id:int, response: Response):
    post = find_posts(id)
    if not post:#if the post trying to be accessed isn't found, throw a status error
        response.status_code = status.HTTP_404_NOT_FOUND#response accesses the status_code property since
        return {"message":f"post with id :{id} was not found"}
        #it's an instance of the Response class, we then equate the status to the status HTTP_404.....
    return {"post_detail":post}


#http://127.0.0.1:8000/posts 
@app.post("/posts")
def create_post(post: Post):
   post_dict = post.dict()#convert sent post to dictionnary first before any further processing
   post_dict["id"] = randrange(0, 100000000)#when post is sent assign an id to dictionnary post automatically
   #this simply means that every post will have a unique id
   my_posts.append(post_dict)#after assigning id to specific post, go include it in the my_posts list
   return {"data":post_dict}


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