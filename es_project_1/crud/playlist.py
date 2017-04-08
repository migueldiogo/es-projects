from business import session
from models import Playlist


def create_playlist(user_id:int, playlist_name: str) -> bool:
    playlist = Playlist(user_id = user_id, name = playlist_name)
    session.add(playlist)
    session.commit()
    return True


def update_playlist(playlist_id: int, playlist_name: str) -> bool:
    playlist = session.query(Playlist).filter(Playlist.id == playlist_id)
    if playlist:
        playlist.name = playlist_name
        session.commit()
        return True
    else:
        return False


def get_playlist(playlist_id: int) -> Playlist:
    return session.query(Playlist).filter(Playlist.id == playlist_id)


def delete_playlist(playlist_id: str) -> bool:
    rows_affected = session.query(Playlist).filter(Playlist.id == playlist_id).delete()
    return rows_affected > 0
    


