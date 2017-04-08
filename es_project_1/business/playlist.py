from .custom_exceptions import *
from crud import playlist as crud_playlist
from crud import user as crud_user
from crud import song as crud_song

from models import Playlist


# CRUD WRAPPER

def create_playlist(user_auth_token:str, playlist_name: str) -> bool:
    user_id = crud_user.get_user(user_auth_token)
    return crud_playlist.create_playlist(user_id, playlist_name)


def update_playlist(user_auth_token: str, playlist_id: int, playlist_name: str) -> bool:
    user_id = crud_user.get_user(user_auth_token)
    playlist = crud_song.get_song(playlist_id)
    
    if not playlist:
        raise NotFound
    
    if playlist.user_id != user_id:
        raise Forbidden
    
    return crud_playlist.update_playlist(playlist_id, playlist_name)


def get_playlist(user_auth_token: str, playlist_id: int) -> Playlist:
    user_id = crud_user.get_user(user_auth_token)
    playlist = crud_song.get_song(playlist_id)

    if not playlist:
        raise NotFound

    if playlist.user_id != user_id:
        raise Forbidden

    return crud_playlist.get_playlist(playlist_id)


def delete_playlist(user_auth_token: str, playlist_id: str) -> bool:
    user_id = crud_user.get_user(user_auth_token)
    playlist = crud_song.get_song(playlist_id)
    
    if not playlist:
        raise NotFound
    
    if playlist.user_id != user_id:
        raise Forbidden
    
    return crud_playlist.delete_playlist(playlist_id)

# ####



