from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import List#make a field to be nullable
from sqlalchemy.orm import Session
from .database import engine,get_db
from . import models, schemas
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")#We are defining the default hashing algorithm
models.Base.metadata.create_all(bind=engine)#allows us to implement the database tables

app = FastAPI() #Instantiate object from the FASTAPI class(model) to access its attributes and methods


 
#The root end point
@app.get("/")
def root():
    return {"message":  "Welcome to our first lesson on api creation, we are going to learn lots of stuff!!! So grab a cup of coffee and get rolling"}



#Get posts
@app.get("/posts",response_model = List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts



#Get individual post
@app.get("/posts/{id}",response_model=schemas.PostResponse)
def get_post(id: int, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} doesn't exist")
    return post


#Create posts
@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_post(post:schemas.PostCreate, db:Session= Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)#add post to database table
    db.commit()
    db.refresh(new_post)
    return new_post         


#Delete individual post
@app.delete("/posts/{id}",status_code = status.HTTP_204_NO_CONTENT) 
def delete_post(id:int, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id ==id)
    if post.first() is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"posts with id {id} doesn't exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id:int, updated_post:schemas.PostCreate, db:Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id{id} doesn't exist")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()


@app.get("/users",response_model=List[schemas.UserResponse])
def get_users(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.get("/users/{id}",response_model= schemas.UserResponse)
def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"user with id {id} doesn't exist ")
    return user


@app.post("/users",status_code = status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.delete("/users/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if user.first() is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"user with id {id} doesn't exist")
    user.delete(synchronize_session =False)
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)


@app.put("/users/{id}", response_model=schemas.UserResponse)
def update_user(id:int, updated_user:schemas.UserUpdate, db:Session=Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id {id} doesn't exist")
    user_query.update(updated_user.dict(),synchronize_session=False)
    db.commit()
    return user_query.first() 


