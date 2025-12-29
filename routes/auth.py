from fastapi import APIRouter, Depends, Header
import uuid
import bcrypt
from fastapi import HTTPException
import jwt
from database import get_db
from models.user import User
from pydantic_schemas.user_create import UserCreate
from sqlalchemy.orm import Session
from pydantic_schemas.user_login import UserLogin




router=APIRouter()

@router.post('/signup',status_code=201)
def signup_user(user:UserCreate,db:Session=Depends(get_db)):
    
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

@router.post('/login')
def login_user(user:UserLogin,db:Session=Depends(get_db)):
    #check is user with same email exist or not
    user_db=db.query(User).filter(User.email == user.email).first()

    if not user_db:
        raise HTTPException(400,'User with this email does not exist!')

    is_match=bcrypt.checkpw(user.password.encode(),user_db.password)

    if not is_match:
        raise HTTPException(400,'Incorrect password')
    
    token=jwt.encode({'id':user_db.id},'password_key')

    return {'token':token,'user':user_db}
    #if doesnot exist signup
    #password matching or not
    #if doesnot match return error
@router.get('/')
def current_user_data(db: Session = Depends(get_db), x_auth_token = Header()):
    # 1. Check for token
    if not x_auth_token:
        raise HTTPException(401, 'No auth token, access denied!')

    try:
        # 2. Decode the token (Logic must be inside 'try')
        verified_token = jwt.decode(x_auth_token, 'password_key', algorithms=['HS256'])

        if not verified_token:
            raise HTTPException(401, 'Token verification failed, authorization')

        # 3. Get the id from the token
        uid = verified_token.get('id')
        return uid
    
    #postgress database get the user info 
    except jwt.PyJWTError:
        # This catches errors like expired or fake tokens
        raise HTTPException(401, 'Token is not valid, authorization failed')

