from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL='postgresql://postgres:g4st=sTevi@localhost:5432/musicapp'

engine=create_engine(DATABASE_URL)
sessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

db=sessionlocal()