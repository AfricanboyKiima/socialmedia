from fastapi import FastAPI
from . import database
from . import models
from .routers import post,user

models.Base.metadata.create_all(bind = database.engine)#allows us to implement the database tables

app = FastAPI() 

app.include_router(post.router)
app.include_router(user.router)







