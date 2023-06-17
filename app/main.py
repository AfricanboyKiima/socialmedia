from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel#we then defined a schema to be able to define what we would want our data to look like
from typing import Optional#make a field to be nullable
import psycopg2
from psycopg2.extras import RealDictCursor
import time


#This post class allows us to post stuff from the frontend based on a well defined schema or data model
#In such a way a user will only send us the data we defined in the model and nothing else.
#In addition, we are able to define what datatype of the data we want for each of our properties
#We achieve such behaviour by inheriting from the BaseModel class imported from the pydantic library

app = FastAPI() #Instantiate object from the FASTAPI class(model) to access its attributes and methods


#API schema
class Post(BaseModel):
    title:str
    content:str
    published : bool = True
    rating: Optional[int] = None#a completely optional field that means it's nullable


#database connection
while True:#infinite loop 
    try: #this is mostly likey going to cause an error so we place code that we suspect could cause an error in the try clause
        conn = psycopg2.connect(host="localhost",database="fastapi",user="postgres",password="12345678", 
        cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Hoorray!!!!! Connection to database established")
        break
    except Exception as error:#Here we place code on what is to happen in case a error occurs
        print("Connection to database failed")
        print("Error", error)
        time.sleep(2)



#This takes us to the root page of our api http://127.0.0.1:8000
@app.get("/")
def root():
    return {"message":  "People are not leveraging the power of asking, WELCOME, let me teach you how to ask"}
#...All this is referred to as a path operation


#Get all posts endpoint
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data":posts}

@app.get("/posts/{id}")
def get_post(id:int):
    post = find_posts(id)
    if not post:#if you do not find the post with that specific id then raise an HTTPException
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return {"post_detail":post}

#Create posts endpoint
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
   cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s, %s, %s) RETURNING * """,
                  (post.title,post.content,post.published))
   #post saved in variable
   new_post = cursor.fetchone()
   #To save the data, we reference the connection by issuing a commit method    
   conn.commit()
   return {"data":new_post}

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

