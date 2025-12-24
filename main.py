from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import TEXT, VARCHAR, Column, LargeBinary, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uuid

app=FastAPI()

DATABASE_URL='postgresql://postgres:g4st=sTevi@localhost:5432/musicapp'

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

#create all the tables in the database




@app.post('/signup')
def signup_user(user:UserCreate):
    
    #extracts the data thats coming from req
    
    
    #check if the user already exists or not in db
    user_db = db.query(User).filter(User.email == user.email).first()

    if user_db:
        return 'user with same email already exists!'
    
    

    #add the user to the db if do not exists
    new_user = User(id=str(uuid.uuid4()), email=user.email, password=user.password.encode(), Name=user.name)
    db.add(new_user)
    db.commit()

    return {"message": "User created successfully", "user_id": new_user.id}

Base.metadata.create_all(engine) 

