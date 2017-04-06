from models import Base
from sqlalchemy.orm import sessionmaker
from models.Song import Song
from models.User import User
from models.Playlist import Playlist
from sqlalchemy import create_engine


engine = create_engine("mysql+pymysql://es:es@localhost:3306/soundshare",echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()