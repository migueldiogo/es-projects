import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Sequence
from sqlalchemy import SmallInteger
from sqlalchemy import String
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, Sequence("user_id_seq"), primary_key = True)
    session_token = Column(String(200))
    first_name = Column(String(30))
    last_name = Column(String(30))
    email = Column(String(100))
    password_hashed = Column(String(200))
    password_salt = Column(String(200))
    auth_token = Column(String(200))
    playlists = relationship("Playlist", back_populates = "user", cascade = "delete")
    songs = relationship("Song", back_populates = "user")

    def __init__(self, first_name, last_name, email, password_hashed):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hashed = password_hashed
    
    def __repr__(self):
        return "<User(id = '%i', first_name = '%s', last_name = '%s', email = '%s')>" \
               % (self.id, self.first_name, self.last_name, self.email)


class Playlist(Base):
    __tablename__ = "playlists"
    
    id = Column(Integer, Sequence("playlist_id_seq"), primary_key = True)
    name = Column(String(100))
    created_at = Column(Date, default = datetime.datetime.now())
    size = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates = "playlists")
    songs = relationship("Song", secondary = "playlist_song")
    
    def __init__(self, name, created_at, user_id):
        self.name = name
        self.created_at = created_at
        self.user_id = user_id
    
    def __repr__(self):
        return "<Playlist(id = '%i', name = '%s', date = '%s', user_id = '%i', user_name = '%s')>" \
               % (self.id, self.name, self.created_at, self.user_id, self.user.name)


class Song(Base):
    __tablename__ = "songs"
    
    id = Column(Integer, Sequence("song_id_seq"), primary_key = True)
    title = Column(String(100))
    artist = Column(String(80))
    album = Column(String(80))
    release_year = Column(SmallInteger)
    url = Column(String(300))
    playlists = relationship("Playlist", secondary = "playlist_song")
    
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates = "songs")
    
    def __init__(self, title, artist, album, release_year, url, user_id):
        self.title = title
        self.artist = artist
        self.album = album
        self.release_year = release_year
        self.url = url
        self.user_id = user_id
    
    def __repr__(self):
        return "<Song(id = '%i', title = '%s', album = '%s', artist = '%s', release_year = '%d', url = '%s')>" \
               % (self.id, self.title, self.artist, self.artist, self.release_year, self.url)
