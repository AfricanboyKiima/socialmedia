from .database import Base
from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.sql.expression import Null



class Post(Base):#post model extends base
    __tablename__ = "posts"
    id = Column(Integer, primary_key = True,nullable = False)
    title = Column(String, nullable= False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default="TRUE",nullable=False)