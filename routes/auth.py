from fastapi import APIRouter
import uuid
import bcrypt
from fastapi import HTTPException
from models.user import User
from pydantic_schemas.user_create import UserCreate
from database import db

router=APIRouter()

@router.post('/signup')
def signup_user(user:UserCreate):
    
    #extracts the data thats coming from req
    
    
    #check if the user already exists or not in db
    user_db = db.query(User).filter(User.email == user.email).first()

    if user_db:
        raise HTTPException(400,'user with same email already exists!')
    hashed_pw=bcrypt.hashpw(user.password.encode(),bcrypt.gensalt())
    user_db = User(id=str(uuid.uuid4()), email=user.email, password=hashed_pw, Name=user.name)

    #add the user to the db if do not exists
    
    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return user_db


