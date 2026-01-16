import uuid
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import auth_middleware
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os

from models.song import Song

router = APIRouter()

load_dotenv()

# Cloudinary configuration
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True  
)

@router.post('/upload', status_code=201)
def upload_song(
    song: UploadFile = File(...),
    thumbnail: UploadFile = File(...),
    artist: str = Form(...),
    song_name: str = Form(...),
    hex_code: str = Form(...),
    db: Session = Depends(get_db),
    auth_dict = Depends(auth_middleware)
):
    song_id = str(uuid.uuid4())

    # Upload song
    song_res = cloudinary.uploader.upload(
        song.file,
        resource_type='auto',
        folder=f'songs/{song_id}'
    )

    # Upload thumbnail
    thumbnail_res = cloudinary.uploader.upload(
        thumbnail.file,
        resource_type='image',
        folder=f'songs/{song_id}'
    )
    new_song = Song(
        id=song_id,
        song_name=song_name,
        artist=artist,
        hex_code=hex_code,
        song_url=song_res['secure_url'],          
        thumbnail_url=thumbnail_res['secure_url'] 
    )
    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song

@router.get('/list')
def list_songs(
    db: Session = Depends(get_db),
    auth_details = Depends(auth_middleware)
):
    songs = db.query(Song).all()
    return songs
