from fastapi import FastAPI

from app.database import database
from app.routers import post,user, auth

from app.models import posts as post_model
from app.models import users as user_model



database.Base.metadata.create_all(bind = database.engine)




app = FastAPI() 

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)







