from fastapi import APIRouter, Depends, Header
import uuid
import bcrypt
from fastapi import HTTPException
import jwt
from database import get_db
from middleware.auth_middleware import auth_middleware
from models import user
from models.user import User
from pydantic_schemas.user_create import UserCreate
from sqlalchemy.orm import Session
from pydantic_schemas.user_login import UserLogin
from sqlalchemy.orm import joinedload




router=APIRouter()

@router.post('/signup',status_code=201)
def signup_user(user:UserCreate,db:Session=Depends(get_db)):
    
    #extracts the data thats coming from req
    
    
    #check if the user already exists or not in db
    user_db = db.query(User).filter(User.email == user.email).first()

    if user_db:
        raise HTTPException(400,'user with same email already exists!')
    hashed_pw=bcrypt.hashpw(user.password.encode(),bcrypt.gensalt())
    user_db = User(id=str(uuid.uuid4()), email=user.email, password=hashed_pw, name=user.name)

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
def current_user_data(db: Session = Depends(get_db), user_dict=Depends(auth_middleware)):
    user=db.query(User).filter(User.id == user_dict['uid']).options(joinedload(User.favotites)).first()

    if not user:
        raise HTTPException(404,'User not found!')
    return user

