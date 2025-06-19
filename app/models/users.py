
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from . import post_like_association
from app.database import database



class User(database.Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    email = Column(String,nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default= text('now()'))
    liked_posts = relationship("Post", secondary = post_like_association.post_liker, back_populates ="liked_by")#represents M:M relationship
    posts = relationship("Post", back_populates="owner")#represents 1:M relationship


