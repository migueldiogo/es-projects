import base64
from functools import wraps

from flask import Flask, jsonify
from flask import Response
from flask import abort
from flask import render_template
from flask import request
from crud import user as crud_user
from crud import song as crud_song
from crud import playlist as crud_playlist
from serializers import UserSerializer, SongSerializer, PlaylistSerializer
import utils
import aws


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
    #return 'Hello World!'
    return render_template("login.html")


@app.route(REST_PREFIX + '/users/', methods = ['POST'])
def create_user():
    data = request.get_json()
    password_salt = utils.generate_uuid()
    
    password_hashed = utils.hash_password(password_raw = data['password'], salt = password_salt)
    
    auth_token = utils.generate_uuid()
    
    result = crud_user.create_user(
            data['firstName'],
            data['lastName'],
            data['email'],
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
    data = request.get_json()
    
    user = crud_user.get_user_by_email(data['email'])
    
    if not user:
        abort(401)
    
    input_hash = utils.hash_password(data['password'], user.password_salt)
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
    data = request.get_json()
        
    song_file = base64.b64decode(data['file'])

    import os
    filename, file_extension = os.path.splitext(song_file.filename)
    
    if file_extension != ".wav" and file_extension != ".mp3":
        abort(400)

    song_new_filename = utils.generate_uuid()
    
    song_url = aws.upload_song(song_new_filename, file_extension, song_file)

    crud_song.create_song(user_id = user.id,
                          song_title = data['title'],
                          song_artist = data['artist'],
                          song_album = data['album'],
                          song_release_year = int(data['releaseYear']),
                          song_url = song_url)
    
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
    data = request.get_json()
        
    song = crud_song.get_song(song_id = song_id)

    if not song:
        abort(404)
    if song.user_id != user.id:
        abort(403)

    song.title = data['title'] if 'title' in data else song.title
    song.artist = data['artist'] if 'artist' in data else song.artist
    song.album = data['album'] if 'album' in data else song.album
    song.release_year = data['releaseYear'] if 'releaseYear' in data else song.release_year
    if 'file' in data:
        song_file = base64.b64decode(data['file'])

        import os
        filename, file_extension = os.path.splitext(song_file.filename)
    
        if file_extension != ".wav" and file_extension != ".mp3":
            abort(400)
    
        song_new_filename = utils.generate_uuid()
    
        song.url = aws.upload_song(song_new_filename, file_extension, song_file)
        
    crud_song.update_song(song)
    
    return Response(status = 200)


@app.route(REST_PREFIX + '/playlists/', methods = ['POST'])
@requires_auth
def create_playlist(user):
    data = request.get_json()
    
    crud_playlist.create_playlist(user_id = user.id,
                                  playlist_name = data['name'])
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
    data = request.get_json()
    playlist_name = data['name']

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
