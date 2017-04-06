from models import Base
from sqlalchemy.orm import sessionmaker

from models.Song import Song
from models.User import User
from models.Playlist import Playlist

if __name__ == '__main__':
    from sqlalchemy import create_engine
    engine = create_engine("mysql+pymysql://es:es@localhost:3306/soundshare",echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    p1 = User(first_name="Abel")
    s1 = Song(title="Andre")
    session.add(p1)
    session.add(s1)
    session.commit()





