from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional
import time

try:
    conn = psycopg2.connect(host="localhost",database="project1",user="postgres",password="12345678",cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Connection has been established")
except Exception as error:
    print("Connection has failed")
    print("Error",error)


app = FastAPI()

class Person(BaseModel):
    name:str
    surname:str
    email:Optional[str] = None
    phone:int

@app.get("/")
def root():
    return {"message":"This is an api about people information, plus, I am practicing api creation using row SQL"}

@app.get("/person")
def get_person():
    cursor.execute("""SELECT * FROM person""")
    persons = cursor.fetchall()
    return {"data": persons}


@app.get("/person/{id}")
def get_person(id:int):
    cursor.execute("""SELECT * FROM person WHERE id = %s """,(str(id),))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"person with id {id} doesn't exist")
    return {"data":post}


@app.post("/person",status_code = status.HTTP_201_CREATED)
def create_person(person:Person):
    cursor.execute("""INSERT INTO person(name,surname,email,phone) VALUES(%s,%s,%s,%s) RETURNING *""",(person.name,person.surname,person.email,person.phone))
    created_person = cursor.fetchone()
    conn.commit()
    return {"data":created_person}





