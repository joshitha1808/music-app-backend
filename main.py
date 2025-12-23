from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import TEXT, VARCHAR, Column, LargeBinary, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app=FastAPI()

DATABASE_URL='postgresql://postgres:g4st=sTevi@localhhost:5432/musicapp'

engine=create_engine(DATABASE_URL)
sessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

db=sessionlocal()

class UserCreate(BaseModel):
    name:str
    email:str
    password:str
Base=declarative_base()

class User(Base):
    __tablename__='users'

    id=Column(TEXT,primary_key=True)
    Name=Column(VARCHAR(100))
    email=Column(VARCHAR(100))
    password=Column(LargeBinary)



@app.post('/signup')
def signup_user(user:UserCreate):
    
    #extracts the data thats coming from req
    print(user.name)
    print(user.email)
    print(user.password)
    #check if the user already exists or not in db

    #add the user to the db if do not exists
    pass 

