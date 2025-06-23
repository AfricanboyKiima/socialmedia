#IMPORTING SQLALCHEMY PARTS
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:12345678@localhost/socialmedia_app'


#The engine allows us to connect sqlalchemy as an orm to our database in postgresql
engine = create_engine(SQLALCHEMY_DATABASE_URL)#Here sqlalchemy is now connected to our database

#Sessions allow our sqlalchemy to communicate with our database hence its now able to communicate with the database that will ofcoure contain our tables
SessionFactory = sessionmaker(autocommit = False, autoflush=False, bind= engine)#Session factory is used to create a session factory that's responsible for creating a function to create new sessions
#A database session is used to interact with the database and perform operations in it

#Parent class from which all models will inherit
Base = declarative_base()


#creates a database seesion and returns it
def get_db():
    db = SessionFactory()#instantiate session objects for each user
    try:
        yield db
    finally:
        db.close()#close session/communication when request is done


