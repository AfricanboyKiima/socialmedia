from app.database import database
from . import post_like_association
from sqlalchemy.orm import relationship
from sqlalchemy import Column,Integer,String,Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text



class Post(database.Base):#post model extends base
    __tablename__ = "posts"
    post_id = Column(Integer, primary_key = True)
    title = Column(String, nullable= False)
    content = Column(String, nullable = False)                                                                                                                                 
    published = Column(Boolean, server_default="TRUE",nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False,server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"),nullable = False)
    owner = relationship("User", back_populates = "posts")#represents 1:M relationship
    liked_by = relationship("User",secondary= post_like_association.post_liker, back_populates= "liked_posts" )#M:M relationship



