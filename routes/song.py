from fastapi import APIRouter, Depends,UploadFile,File,Form
from sqlalchemy.orm import Session
from database import get_db
from middleware import auth_middleware
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os

router=APIRouter()

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

@router.post('/upload')
def upload_song(song:UploadFile=File(...),
                thumbnail:UploadFile=File(...),
                artist:str=Form(...),
                song_name:str=Form(...),
                hex_code:str=Form(...),
                db:Session=Depends(get_db),
                auth_dict=Depends(auth_middleware)):
    pass




