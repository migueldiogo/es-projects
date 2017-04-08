from crud import song as crud_song
from crud import user as crud_user
from crud import playlist as crud_playlist
from .custom_exceptions import *
from models import Song

# CRUD WRAPPER


def create_song(user_auth_token:str, song_title: str, song_album : str, song_release_year: int, song_url: str) -> bool:
    user = crud_user.get_user(user_auth_token)
    return crud_song.create_song(user.id, song_title, song_album, song_release_year, song_url)


def update_song(user_auth_token:int, song_id: int, song_title: str, song_album : str, song_release_year: int, song_url: str) -> bool:
    user_id = crud_user.get_user(user_auth_token)
    song = crud_song.get_song(song_id)
    
    if not song:
        raise NotFound
    
    if song.user_id != user_id:
        raise Forbidden
    
    return crud_song.update_song(song_id, song_title, song_album, song_release_year, song_url)


def get_song(song_id: int) -> Song:
    return crud_song.get_song(song_id)


def delete_song(user_auth_token: str, song_id: str) -> bool:
    user_id = crud_user.get_user(user_auth_token)
    song = crud_song.get_song(song_id)
    
    if not song:
        raise NotFound
    
    if song.user_id != user_id:
        raise Forbidden
        
    return crud_song.delete_song(song_id)

# ##

