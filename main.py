from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app=FastAPI()

DATABASE_URL='postgresql://postgres:g4st=sTevi@localhhost:5432/musicapp'

engine=create_engine(DATABASE_URL)
sessionlocal=sessionmaker()

class UserCreate(BaseModel):
    name:str
    email:str
    password:str


@app.post('/signup')
def signup_user(user:UserCreate):
    
    #extracts the data thats coming from req
    print(user.name)
    print(user.email)
    print(user.password)
    #check if the user already exists or not in db

    #add the user to the db if do not exists
    pass 

