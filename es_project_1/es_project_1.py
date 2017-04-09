from functools import wraps

from flask import Flask, jsonify
from flask import Response
from flask import abort
from flask import request
from crud import user as crud_user
from crud import song as crud_song
from crud import playlist as crud_playlist

import utils
from serializers import UserSerializer, SongSerializer, PlaylistSerializer

app = Flask(__name__)

REST_PREFIX = '/api/v1'


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers['Authorization']
        if not token:
            abort(401)
        
        user = crud_user.get_user_by_token(token)
        
        if not user:
            abort(401)
        return f(user, *args, **kwargs)
    
    return decorated


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route(REST_PREFIX + '/users/', methods = ['POST'])
def create_user():
    form = request.form
    password_salt = utils.generate_uuid()
    
    password_hashed = utils.hash_password(password_raw = form['password'], salt = password_salt)
    
    auth_token = utils.generate_uuid()
    
    result = crud_user.create_user(
            form['firstName'],
            form['lastName'],
            form['email'],
            password_hashed,
            password_salt,
            auth_token)
    
    if not result:
        return Response(status = 409,
                        response = {'code':409, 'message':"There is already an user with this email", 'fields':"email"})
    else:
        return Response(status = 200)


@app.route(REST_PREFIX + '/users/self/', methods = ['GET'])
@requires_auth
def get_user(user):
    return jsonify(UserSerializer.serialize(user))


@app.route(REST_PREFIX + '/users/self/', methods = ['DELETE'])
@requires_auth
def delete_user(user):
    crud_user.delete_user(user.id)
    return Response(status = 200)


@app.route(REST_PREFIX + '/users/self/tokens/', methods = ['POST'])
def get_token():
    form = request.form
    
    user = crud_user.get_user_by_email(form['email'])
    
    if not user:
        abort(401)
    
    input_hash = utils.hash_password(form['password'], user.password_salt)
    right_hash = user.password_hashed
    
    if input_hash != right_hash:
        abort(401)
    
    result = {'token':user.auth_token}
    
    return jsonify(result)


@app.route(REST_PREFIX + '/users/self/songs/', methods = ['GET'])
@requires_auth
def get_user_songs(user):
    # TODO EXTRA
    return 'Hello World!'


@app.route(REST_PREFIX + '/users/self/playlists/', methods = ['GET'])
@requires_auth
def get_user_playlists(user):
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    
    data = crud_playlist.get_all_playlists(offset = offset,
                                           limit = limit,
                                           user_id = user.id)
    return jsonify(PlaylistSerializer.serialize(data, many = True))


@app.route(REST_PREFIX + '/songs/', methods = ['GET'])
@requires_auth
def get_songs(user):
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    title = request.args.get('title')
    artist = request.args.get('artist')
    
    data = crud_song.get_all_songs(offset = offset,
                                   limit = limit,
                                   song_title = title,
                                   song_artist = artist)
    return jsonify(SongSerializer.serialize(data, many = True))


@app.route(REST_PREFIX + '/songs/', methods = ['POST'])
@requires_auth
def create_song(user):
    # TODO substitute song url for the file per se
    form = request.form
    
    crud_song.create_song(user_id = user.id,
                          song_title = form['title'],
                          song_artist = form['artist'],
                          song_album = form['album'],
                          song_release_year = int(form['releaseYear']),
                          song_url = form['url'])
    return Response(status = 200)


@app.route(REST_PREFIX + '/songs/<int:song_id>/', methods = ['GET'])
@requires_auth
def get_song(user, song_id):
    song = crud_song.get_song(song_id = song_id)
    if not song:
        abort(404)
    
    return jsonify(SongSerializer.serialize(song))


@app.route(REST_PREFIX + '/songs/<int:song_id>/', methods = ['DELETE'])
@requires_auth
def delete_song(user, song_id):
    song = crud_song.delete_song(song_id = song_id)
    if not song:
        abort(404)
    
    return Response(status = 200)


@app.route(REST_PREFIX + '/songs/<int:song_id>/', methods = ['PUT'])
@requires_auth
def update_song(user, song_id):
    form = request.form
    song_title = form['title'],
    song_artist = form['artist'],
    song_album = form['album'],
    song_release_year = int(form['releaseYear']),
    song_url = form['url']
    
    song = crud_song.get_song(song_id = song_id)
    if not song:
        abort(404)
    if song.user_id != user.id:
        abort(403)

    song.title = song_title if song_title else song.title
    song.artist = song_artist if song_artist else song.artist
    song.album = song_album if song_album else song.album
    song.release_year = song_release_year if song_release_year else song.release_year
    song.url = song_url if song_url else song.url
    
    crud_song.update_song(song)
    
    return Response(status = 200)


@app.route(REST_PREFIX + '/playlists/', methods = ['POST'])
@requires_auth
def create_playlist(user):
    form = request.form
    
    crud_playlist.create_playlist(user_id = user.id,
                                  playlist_name = form['name'])
    return Response(status = 200)


@app.route(REST_PREFIX + '/playlists/<int:playlist_id>/', methods = ['DELETE'])
@requires_auth
def delete_playlist(user, playlist_id):
    playlist = crud_playlist.get_playlist(playlist_id = playlist_id)
    if not playlist:
        abort(404)
    if playlist.user_id != user.id:
        abort(403)
    
    crud_playlist.delete_playlist(playlist_id)
    
    return Response(status = 200)


@app.route(REST_PREFIX + '/playlists/<int:playlist_id>/', methods = ['PUT'])
@requires_auth
def update_playlist(user, playlist_id):
    form = request.form
    playlist_name = form['name']

    playlist = crud_playlist.get_playlist(playlist_id = playlist_id)
    if not playlist:
        abort(404)
    if playlist.user_id != user.id:
        abort(403)
    
    if playlist_name:
        playlist.name = playlist_name
        crud_playlist.update_playlist(playlist)
    
    return Response(status = 200)


@app.route(REST_PREFIX + '/playlists/<int:playlist_id>/songs/', methods = ['GET'])
@requires_auth
def get_songs_from_playlist(user, playlist_id):
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    title = request.args.get('title')
    artist = request.args.get('artist')
    
    data = crud_song.get_all_songs_from_playlist(playlist_id = playlist_id,
                                                 offset = offset,
                                                 limit = limit,
                                                 song_title = title,
                                                 song_artist = artist)
    return jsonify(SongSerializer.serialize(data, many = True))


@app.route(REST_PREFIX + '/playlists/<int:playlist_id>/songs/<int:song_id>/', methods = ['POST'])
@requires_auth
def add_song_to_playlist(user, playlist_id, song_id):
    playlist = crud_playlist.get_playlist(playlist_id = playlist_id)
    if not playlist:
        abort(404)
    if playlist.user_id != user.id:
        abort(403)
    
    song = crud_song.get_song(song_id = song_id)
    if not song:
        abort(404)
    
    playlist.songs.append(song)
    playlist.size += 1
    crud_playlist.update_playlist(playlist)
    
    return Response(status = 200)


@app.route(REST_PREFIX + '/playlists/<int:playlist_id>/songs/<int:song_id>/', methods = ['DELETE'])
@requires_auth
def remove_song_from_playlist(user, playlist_id, song_id):
    playlist = crud_playlist.get_playlist(playlist_id = playlist_id)
    if not playlist:
        abort(404)
    if playlist.user_id != user.id:
        abort(403)
    
    song = crud_song.get_song(song_id = song_id)
    if not song:
        abort(404)
    
    playlist.songs.remove(song)
    playlist.size -= 1

    crud_playlist.update_playlist(playlist)
    
    return Response(status = 200)


@app.errorhandler(400)
def bad_request(error = None):
    message = {
        'code':400,
        'message':'Bad request',
    }
    resp = jsonify(message)
    resp.status_code = 400
    
    return resp


@app.errorhandler(401)
def unauthorized(error = None):
    message = {
        'code':401,
        'message':'Not authorized',
    }
    resp = jsonify(message)
    resp.status_code = 401
    
    return resp


@app.errorhandler(403)
def unauthorized(error = None):
    message = {
        'code':403,
        'message':'Forbidden',
    }
    resp = jsonify(message)
    resp.status_code = 403
    
    return resp


@app.errorhandler(404)
def not_found(error = None):
    message = {
        'code':404,
        'message':'Not Found',
    }
    resp = jsonify(message)
    resp.status_code = 404
    
    return resp


if __name__ == '__main__':
    app.run()

if __name__ == '__main__':
    app.run()
