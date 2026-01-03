import uuid
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import auth_middleware
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os

router = APIRouter()

load_dotenv()


cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

@router.post('/upload')
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

    print(song_res)
    print(thumbnail_res)

    # Example: access user id from token
    user_id = auth_dict["uid"]

    # TODO: store data in DB

    return {
        "message": "Song uploaded successfully",
        "song_url": song_res["secure_url"],
        "thumbnail_url": thumbnail_res["secure_url"],
        "user_id": user_id
    }
