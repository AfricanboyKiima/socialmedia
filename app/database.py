#IMPORTING SQLALCHEMY PARTS
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:12345678@localhost/fastapi'


#The engine allows us to connect sqlalchemy as an orm to our database in postgresql
engine = create_engine(SQLALCHEMY_DATABASE_URL)#Here sqlalchemy is now connected to our database

#Sessions allow our sqlalchemy to communicate with our database hence its now able to communicate with the database that will ofcoure contain our tables
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind= engine)

#Parent class from which all models will inherit
Base = declarative_base()
