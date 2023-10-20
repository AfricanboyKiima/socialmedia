from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel#we then defined a schema to be able to define what we would want our data to look like
from typing import Optional#make a field to be nullable
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from .database import engine,get_db
from . import models

models.Base.metadata.create_all(bind=engine)#allows us to create database tables

app = FastAPI() #Instantiate object from the FASTAPI class(model) to access its attributes and methods




#This post class allows us to post stuff from the frontend based on a well defined schema or data model
class Post(BaseModel):
    title:str
    content:str
    published : bool = True
    rating: Optional[int] = None#a completely optional field that means it's nullable


 
#This is the root end point
@app.get("/")
def root():
    return {"message":  "Welcome to our first lesson on api creation, we are going to learn lots of stuff!!! So grab a cup of coffee and get rolling"}
#...All this is referred to as a path operation


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data":posts}






#Retrieve individual post
@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(str(id),))#we convert the id to a string
    post = cursor.fetchone()
    if  post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return {"post_detail":post}



#Create posts endpoint
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: models.Post , db: Session = Depends(get_db)):
   new_post = db.add(post)
   db.commit()
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
def update_post(id:int,post:Post):
    cursor.execute("""UPDATE posts SET title = %s,content = %s, published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published, str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} doesn't exist")
    return {"updated":updated_post}