from fastapi import APIRouter, Depends,UploadFile,File,Form
from sqlalchemy.orm import Session
from database import get_db
from middleware import auth_middleware

router=APIRouter()

@router.post('/upload')
def upload_song(song:UploadFile=File(...),
                thumbnail:UploadFile=File(...),
                artist:str=Form(...),
                song_name:str=Form(...),
                hex_code:str=Form(...),
                db:Session=Depends(get_db),
                auth_dict=Depends(auth_middleware)):
    pass




