from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Sequence
from sqlalchemy import String
from sqlalchemy import SmallInteger
from sqlalchemy import Table
from sqlalchemy.orm import relationship

from models import Base

playlist_song = Table("playlist_song", Base.metadata,
                    Column('playlist_id', ForeignKey("playlists.id"), primary_key=True),
                    Column('song_id', ForeignKey("songs.id"), primary_key = True))

class Song(Base):
    __tablename__ = "songs"
    
    id = Column(Integer, Sequence("song_id_seq"), primary_key=True)
    title = Column(String(100))
    artist = Column(String(80))
    release_year = Column(SmallInteger)
    url = Column(String(300))
    playlists = relationship("Playlist", secondary = "playlist_song")
    
    def __init__(self, title, artist, release_year, url):
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.url = url
    
    def __repr__(self):
        return "<Song(id = '%i', title = '%s', artist = '%s', release_year = '%d', url = '%s')>"  \
               % (self.id, self.title, self.artist, self.release_year, self.url)
