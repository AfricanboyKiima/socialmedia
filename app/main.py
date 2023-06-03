from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel#we then defined a schema to be able to define what we would want our data to look like
from typing import Optional#make a field to be nullable
import psycopg2
from psycopg2.extras import RealDictCursor
import time

"""
Implement schema through which we can define 
what we want our data to look likels

"""
#This post class allows us to post stuff from the frontend based on a well defined schema or data model
#In such a way a user will only send us the data we defined in the model and nothing else.
#In addition, we are able to define what datatype of the data we want for each of our properties
#We achieve such behaviour by inheriting from the BaseModel class imported from the pydantic library

app = FastAPI() #Instantiate object from the FASTAPI class(model) to access its attributes and methods


class Post(BaseModel):
    title:str
    content:str
    published : bool = True
    rating: Optional[int] = None#a completely optional field that means it's nullable

while True:#infinite loop 
    #database connection
    try: #this is mostly likey going to cause an error so we place code that we suspect could cause an error in the try clause
        conn = psycopg2.connect(host="localhost",database="fastapi",user="postgres",password="12345678", 
        cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print("Hoorray!!!!! Connection to database established")
        break
    except Exception as error:#Here we place code on what is to happen in case a error occurs
        print("Connection to database failed")
        print("Error", error)
        time.sleep(2)



my_posts = [{"title":"title of post 1","content":"Content of post1","id":1},
            
            {"title":"title of post 2","content":"Content of post 2","id":2}]

#this returns a post based on a given id since each post has a unique value(id)
def find_posts(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

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
    return {"message":  "People are not leveraging the power of asking, WELCOME, let me teach you how to ask"}
#...All this is referred to as a path operation


#this takes us to post url http://127.0.0.1:8000/posts it accesses all the posts
@app.get("/posts")
def get_posts():
    cur.execute("""SELECT * FROM posts""")
    posts = cur.fetchall()
    return {"data":posts}

@app.get("/posts/{id}")
def get_post(id:int):
    post = find_posts(id)
    if not post:#if you do not find the post with that specific id then raise an HTTPException
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return {"post_detail":post}

#if the post trying to be accessed isn't found, throw a status error
        #response.status_code = status.HTTP_404_NOT_FOUND#response accesses the status_code property since
        #return {"message":f"post with id :{id} was not found"}
        #it's an instance of the Response class, we then equate the status to the status HTTP_404.....
#http://127.0.0.1:8000/posts 
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
   post_dict = post.dict()#convert sent post to dictionnary first before any further processing
   post_dict["id"] = randrange(0, 100000000)#when post is sent assign an id to dictionnary post automatically
   my_posts.append(post_dict)#after assigning id to specific post, go include it in the my_posts list
   return {"data":post_dict}

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_index_post(id)
    if index == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id ; {id} doesn't exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    index = find_index_post(id)
    if index == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id ; {id} doesn't exist")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return{"data":post_dict}

    


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
