from crud import session
from models import Song


def create_song(user_id: int, song_title: str, song_artist: str, song_album: str, song_release_year: int, song_url: str) -> bool:
    song = Song(user_id = user_id,
                title = song_title,
                artist = song_artist,
                album = song_album,
                release_year = song_release_year,
                url = song_url)
    session.add(song)
    session.commit()
    return True


def update_song(song_id: int, song_title: str, song_album : str, song_release_year: int, song_url: str) -> bool:
    song = session.query(Song).filter_by(id = song_id).first()
    if song:
        song.title = song_title if song_title else song.title
        song.album = song_album if song_album else song_album
        song.release_year = song_release_year if song_release_year else song_release_year
        song.url = song_url if song_url else song.url
        session.commit()
        return True
    else:
        return False
    
    
def update_song(song_id: int, song_title: str, song_album : str, song_release_year: int, song_url: str) -> bool:
    song = session.query(Song).filter_by(id = song_id).first()
    if song:
        song.title = song_title if song_title else song.title
        song.album = song_album if song_album else song_album
        song.release_year = song_release_year if song_release_year else song_release_year
        song.url = song_url if song_url else song.url

        session.commit()
        return True
    else:
        return False
    
    
def update_song_ownership(song_id: int, new_owner_user_id: int) -> bool:
    song = session.query(Song).filter_by(id = song_id).first()
    if song:
        song.user_id = new_owner_user_id
        session.commit()
        return True
    else:
        return False
    
    
def update_song(song: Song) -> bool:
    session.add(song)
    session.commit()
    return True


def get_song(song_id: int) -> Song:
    return session.query(Song).filter_by(id = song_id).first()


def get_all_songs_from_user(offset: int = 0, limit: int = 10, song_title: str = None, song_artist: str = None, user_id: int = None) -> list:
    if song_title and song_artist:
        songs_result = session.query(Song).filter_by(title = song_title, artist = song_artist, user_id = user_id)\
            .offset(offset)\
            .limit(limit)
    elif song_title:
        songs_result = session.query(Song).filter_by(title = song_title, user_id = user_id)\
            .offset(offset)\
            .limit(limit)
    elif song_artist:
        songs_result = session.query(Song).filter_by(artist = song_artist, user_id = user_id)\
            .offset(offset)\
            .limit(limit)
    else:
        songs_result = session.query(Song).filter_by(user_id = user_id)\
            .offset(offset)\
            .limit(limit)\
            .all()
    return songs_result


def get_all_songs(offset: int = 0, limit: int = 10, song_title: str = None, song_artist: str = None) -> list:
    if song_title and song_artist:
        songs_result = session.query(Song).filter_by(title = song_title, artist = song_artist)\
            .offset(offset)\
            .limit(limit)
    elif song_title:
        songs_result = session.query(Song).filter_by(title = song_title)\
            .offset(offset)\
            .limit(limit)
    elif song_artist:
        songs_result = session.query(Song).filter_by(artist = song_artist)\
            .offset(offset)\
            .limit(limit)
    else:
        songs_result = session.query(Song)\
            .offset(offset)\
            .limit(limit)\
            .all()
    return songs_result


def get_all_songs_from_playlist(playlist_id: int, offset: int = 0, limit: int = 10, song_title: str = None, song_artist: str = None) -> list:
    if song_title and song_artist:
        songs_result = session.query(Song).filter(Song.title == song_title,
                                                 Song.artist == song_artist,
                                                 Song.playlists.any(id = playlist_id))\
            .offset(offset)\
            .limit(limit)\
            .all()
    elif song_title:
        songs_result = session.query(Song).filter(Song.title == song_title,
                                                  Song.playlists.any(id = playlist_id)) \
            .offset(offset) \
            .limit(limit) \
            .all()
    elif song_artist:
        songs_result = session.query(Song).filter(Song.artist == song_artist,
                                                  Song.playlists.any(id = playlist_id)) \
            .offset(offset) \
            .limit(limit) \
            .all()
    else:
        songs_result = session.query(Song).filter(Song.playlists.any(id = playlist_id)) \
            .offset(offset) \
            .limit(limit) \
            .all()
    return songs_result


def delete_song(song_id: int) -> bool:
    rows_affected = session.query(Song).filter(Song.id == song_id).delete()
    return rows_affected > 0