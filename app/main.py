from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel#we then defined a schema to be able to define what we would want our data to look like
from typing import Optional#make a field to be nullable
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI() #Instantiate object from the FASTAPI class(model) to access its attributes and methods


#This post class allows us to post stuff from the frontend based on a well defined schema or data model
class Post(BaseModel):
    title:str
    content:str
    published : bool = True
    rating: Optional[int] = None#a completely optional field that means it's nullable


#database connection
while True:#infinite loop 
    try: 
        conn = psycopg2.connect(host="localhost",database="fastapi",user="postgres",password="12345678", 
        cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Hoorray!!!!! Connection to database established")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error", error)
        time.sleep(2)



#This is the root end point
@app.get("/")
def root():
    return {"message":  "Welcome to our first lesson on api creation, we are going to learn lots of stuff!!! So grab a cup of coffee and get rolling"}
#...All this is referred to as a path operation


#Get all posts endpoint
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data":posts}




#Retrieve individual post
@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(str(id)))#we convert the id to a string
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
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
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
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

