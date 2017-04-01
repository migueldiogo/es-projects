from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Sequence
from sqlalchemy import String
from sqlalchemy.orm import relationship

from models import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    access_token = Column(String(40))
    first_name = Column(String(30))
    last_name = Column(String(30))
    email = Column(String(100))
    password_hashed = Column(String(200))
    playlists = relationship("Playlist", back_populates = "user")

    def __repr__(self):
        return "<User(id = '%i', first_name = '%s', last_name = '%s', email = '%s')>" \
               % (self.id, self.first_name, self.last_name, self.email)
