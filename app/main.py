from fastapi import FastAPI
from . import database,models
from app.routers import post,user
models.Base.metadata.create_all(bind = database.engine)


app = FastAPI() 

app.include_router(post.router)
app.include_router(user.router)







