from fastapi import status, HTTPException,Depends, APIRouter, Response
from sqlalchemy.orm import Session
from .. import schemas, models
from typing import List
from app.database import get_db


router = APIRouter(
    prefix="/posts",
    tags=['Posts'] #used to group posts endpoints routes in one place 
)

#Get posts

@router.get("/",response_model = List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts



#Get individual post
@router.get("/{id}",response_model=schemas.PostResponse)
def get_post(id: int, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} doesn't exist")
    return post


#Create posts
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_post(post:schemas.PostCreate, db:Session= Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)#add post to database table
    db.commit()
    db.refresh(new_post)
    return new_post         


#Delete individual post
@router.delete("/{id}",status_code = status.HTTP_204_NO_CONTENT) 
def delete_post(id:int, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id ==id)
    if post.first() is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"posts with id {id} doesn't exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

#update individual post
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id:int, updated_post:schemas.PostCreate, db:Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} doesn't exist")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()