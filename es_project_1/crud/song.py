from business import session
from models import Song


def create_song(user_id: int, song_title: str, song_album: str, song_release_year: int, song_url: str) -> bool:
    song = Song(user_id = user_id,
                title = song_title,
                album = song_album,
                release_year = song_release_year,
                url = song_url)
    session.add(song)
    session.commit()
    return True


def update_song(song_id: int, song_title: str, song_album : str, song_release_year: int, song_url: str) -> bool:
    song = session.query(Song).filter(Song.id == song_id)
    if song:
        song.title = song_title if song_title else song.title
        song.album = song_album if song_album else song_album
        song.release_year = song_release_year if song_release_year else song_release_year
        song.url = song_url if song_url else song.url
        session.commit()
        return True
    else:
        return False


def get_song(song_id: int) -> Song:
    return session.query(Song).filter(Song.id == song_id)


def get_all_songs(song_title: str = None, song_artist: str = None) -> list:
    if song_title and song_artist:
        songs_result = session.query(Song).filter(Song.title == song_title, Song.artist == song_artist)
    elif song_title:
        songs_result = session.query(Song).filter(Song.title == song_title)
    elif song_artist:
        songs_result = session.query(Song).filter(Song.artist == song_artist)
    else:
        songs_result = session.query(Song).all()
    return songs_result


def delete_song(song_id: int) -> bool:
    rows_affected = session.query(Song).filter(Song.id == song_id).delete()
    return rows_affected > 0