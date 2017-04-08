from .custom_exceptions import *
from crud import playlist as crud_playlist
from crud import user as crud_user
from crud import song as crud_song
from models import Playlist


def create_playlist(user_auth_token:str, playlist_name: str) -> bool:
    user_id = crud_user.get_user(user_auth_token)
    return crud_playlist.create_playlist(user_id, playlist_name)


def update_playlist(user_auth_token: str, playlist_id: int, playlist_name: str) -> bool:
    user_id = crud_user.get_user(user_auth_token)
    playlist = crud_playlist.get_playlist(playlist_id)
    
    if not playlist:
        raise NotFound
    
    if playlist.user_id != user_id:
        raise Forbidden
    
    return crud_playlist.update_playlist(playlist_id, playlist_name)


def get_playlist(user_auth_token: str, playlist_id: int) -> Playlist:
    user_id = crud_user.get_user(user_auth_token)
    playlist = crud_playlist.get_playlist(playlist_id)

    if not playlist:
        raise NotFound

    if playlist.user_id != user_id:
        raise Forbidden

    return crud_playlist.get_playlist(playlist_id)


def delete_playlist(user_auth_token: str, playlist_id: int) -> bool:
    user_id = crud_user.get_user(user_auth_token)
    playlist = crud_playlist.get_playlist(playlist_id)
    
    if not playlist:
        raise NotFound
    
    if playlist.user_id != user_id:
        raise Forbidden
    
    return crud_playlist.delete_playlist(playlist_id)


def get_all_playlists(user_auth_token: str) -> list:
    user_id = crud_user.get_user(user_auth_token)
    return crud_playlist.get_all_playlists(user_id)


def get_all_songs_from_playlist(user_auth_token: str, playlist_id: int) -> list:
    user_id = crud_user.get_user(user_auth_token)
    playlist = crud_playlist.get_playlist(playlist_id)
    
    if not playlist:
        raise NotFound
    
    if playlist.user_id != user_id:
        raise Forbidden
    
    return playlist.songs


def add_song_to_playlist(user_auth_token:str, song_id: int, playlist_id: int) -> bool:
    user_id = crud_user.get_user(user_auth_token)
    playlist = crud_playlist.get_playlist(playlist_id)

    if not playlist:
        raise NotFound

    if playlist.user_id != user_id:
        raise Forbidden
    
    song = crud_song.get_song(song_id)
    
    if not song:
        raise NotFound

    playlist.songs.append(song)
    playlist.size += 1

    return crud_playlist.update_playlist(playlist)


def remove_song_from_playlist(user_auth_token:str, song_id: int, playlist_id: int) -> bool:
    user_id = crud_user.get_user(user_auth_token)
    playlist = crud_playlist.get_playlist(playlist_id)
    
    if not playlist:
        raise NotFound
    
    if playlist.user_id != user_id:
        raise Forbidden
    
    song = crud_song.get_song(song_id)
    
    if not song:
        raise NotFound
    
    playlist.songs.remove(song)
    playlist.size -= 1
    
    return crud_playlist.update_playlist(playlist)

