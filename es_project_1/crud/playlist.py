from crud import Session
from models import Playlist


def create_playlist(session: Session, user_id: int, playlist_name: str) -> bool:
    playlist = Playlist(user_id = user_id, name = playlist_name)
    session.add(playlist)
    session.commit()
    return True


def update_playlist(session: Session, playlist_id: int, playlist_name: str) -> bool:
    playlist = session.query(Playlist).filter(Playlist.id == playlist_id)
    if playlist:
        playlist.name = playlist_name
        session.commit()
        return True
    else:
        return False
    
    
def update_playlist(session: Session, playlist: Playlist) -> bool:
    session.add(playlist)
    session.commit()
    return True


def get_playlist(session: Session, playlist_id: int) -> Playlist:
    return session.query(Playlist).filter_by(id = playlist_id).first()


def get_all_playlists(session: Session, user_id: int, offset: int = 0, limit: int = 10) -> list:
    return session.query(Playlist).filter_by(user_id = user_id)\
            .offset(offset)\
            .limit(limit)


def delete_playlist(session: Session, playlist_id: int) -> bool:
    rows_affected = session.query(Playlist).filter_by(id = playlist_id).delete()
    return rows_affected > 0
    


