from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Sequence
from sqlalchemy import String
from sqlalchemy.orm import relationship

from models import Base


class Playlist(Base):
    __tablename__ = "playlists"
    
    id = Column(Integer, Sequence("playlist_id_seq"), primary_key=True)
    name = Column(String(100))
    created_at = Column(Date)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="playlists")
    songs = relationship("Song", secondary = "playlist_song")

    def __repr__(self):
        return "<Playlist(id = '%i', name = '%s', date = '%s', user_id = '%i', user_name = '%s')>"  \
               % (self.id, self.name, self.created_at, self.user_id, self.user.name)
