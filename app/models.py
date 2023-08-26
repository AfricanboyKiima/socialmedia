from .database import Base
from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):#post model extends base
    __tablename__ = "posts"
    id = Column(Integer, primary_key = True,nullable = False)
    title = Column(String, nullable= False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default="TRUE",nullable=False)
    created_at = Column()