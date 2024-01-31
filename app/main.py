from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel#we then defined a schema to be able to define what we would want our data to look like
from typing import Optional#make a field to be nullable
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from .database import engine,get_db
from . import models

models.Base.metadata.create_all(bind=engine)#allows us to implement the database tables

app = FastAPI() #Instantiate object from the FASTAPI class(model) to access its attributes and methods




#This post class allows us to post stuff from the frontend based on a well defined schema or data model
class Post(BaseModel):
    title:str
    content:str
    published : bool = True


 
#The root end point
@app.get("/")
def root():
    return {"message":  "Welcome to our first lesson on api creation, we are going to learn lots of stuff!!! So grab a cup of coffee and get rolling"}



#Get posts
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data":posts}



#Get individual post
@app.get("/posts/{id}")
def get_post(id: int, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} doesn't exist")
    return {"data": post}


#Create posts
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:Post, db:Session= Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)#add post to database table
    db.commit()
    db.refresh(new_post)
    return {"data":new_post}         


#Delete individual post
@app.delete("/posts/{id}",status_code = status.HTTP_204_NO_CONTENT) 
def delete_post(id:int, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id ==id)
    if post.first() is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"posts with id {id} doesn't exist")
    db.delete(post)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)
