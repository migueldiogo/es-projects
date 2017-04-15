import base64
import tempfile
from functools import wraps

from flask import Flask, jsonify
from flask import Response
from flask import abort
from flask import render_template
from flask import request
from crud import user as crud_user
from crud import song as crud_song
from crud import playlist as crud_playlist
from models import Song, User, Playlist
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
    return render_template("login.html")


@app.route(REST_PREFIX + '/users/', methods = ['POST'])
def create_user():
    data = request.get_json()
    
    result = create_secure_user(
            data['firstName'],
            data['lastName'],
            data['email'],
            data['password'])
    
    if not result:
        return Response(status = 409,
                        response = {'code':409, 'message':"There is already an user with this email", 'fields':"email"})
    else:
        return Response(status = 200)
    

@app.route(REST_PREFIX + '/users/self/<int:user_id>/', methods = ['PUT'])
@requires_auth
def update_user(user, user_id):
    data = request.get_json()
    user.first_name = data['firstName'] if data['firstName'] != "" else user.first_name
    user.last_name = data['lastName'] if data['lastName'] != "" else user.last_name
    user.password_hashed = data['password'] if data['password'] != "" else user.password_hashed
    password_salt = utils.generate_uuid() if data['password'] != "" else user.password_salt
    user.password_hashed = utils.hash_password(password_raw=user.password_hashed, salt=password_salt) if data['password'] != "" else user.password_hashed
    crud_user.update_user(user.id, user.first_name, user.last_name, None, user.password_hashed, password_salt)
    return Response(status=200)


@app.route(REST_PREFIX + '/users/self/', methods = ['GET'])
@requires_auth
def get_user(user):
    return jsonify(UserSerializer.serialize(user))


@app.route(REST_PREFIX + '/users/self/', methods = ['DELETE'])
@requires_auth
def delete_user(user):
    # if there isn't any super user, create one
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
    args = request.args

    offset = args.get('offset') if 'offset' in args else 0
    limit = args.get('limit') if 'limit' in args else None

    data = crud_playlist.get_all_playlists(offset = offset,
                                           limit = limit,
                                           user_id = user.id)
    return jsonify(PlaylistSerializer.serialize(data, many = True))


@app.route(REST_PREFIX + '/songs/', methods = ['GET'])
@requires_auth
def get_songs(user):
    args = request.args
        
    offset = args.get('offset') if 'offset' in args else 0
    limit = args.get('limit') if 'limit' in args else None
    title = args.get('title')
    artist = args.get('artist')
    
    data = crud_song.get_all_songs(offset = offset,
                                   limit = limit,
                                   song_title = title,
                                   song_artist = artist)
    return jsonify(SongSerializer.serialize(data, many = True))


@app.route(REST_PREFIX + '/songs/', methods = ['POST'])
@requires_auth
def create_song(user):
    form = request.form

    song_file = request.files['file']

    import os
    filename, file_extension = os.path.splitext(song_file.filename)
    
    if file_extension != ".wav" and file_extension != ".mp3":
        abort(400)

    song_new_filename = utils.generate_uuid()
    
    song_url = aws.upload_song(song_new_filename, file_extension, song_file)

    crud_song.create_song(user_id = user.id,
                          song_title = form['title'],
                          song_artist = form['artist'],
                          song_album = form['album'],
                          song_release_year = int(form['releaseYear']),
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
    # if there isn't any super user, create one
    super_user = crud_user.get_user_by_email("admin")

    if not super_user:
        create_secure_user(first_name = "admin", last_name = "", email = "admin", password = "admin")
    else:
        super_user = crud_user.get_user_by_email("admin")

    song = crud_song.get_song(song_id = song_id)
    if not song:
        abort(404)
    if song.user_id != user.id:
        abort(403)
        
    crud_song.update_song_ownership(song_id, super_user.id)
    
    return Response(status = 200)


@app.route(REST_PREFIX + '/songs/<int:song_id>/', methods = ['PUT'])
@requires_auth
def update_song(user, song_id):
    form = request.form
        
    song = crud_song.get_song(song_id = song_id)

    if not song:
        abort(404)
    if song.user_id != user.id:
        abort(403)

    song.title = form['title'] if 'title' in form else song.title
    song.artist = form['artist'] if 'artist' in form else song.artist
    song.album = form['album'] if 'album' in form else song.album
    song.release_year = form['releaseYear'] if 'releaseYear' in form else song.release_year
    if 'file' in request.files:
        song_file = request.files['file']

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
    args = request.args
    playlist = crud_playlist.get_playlist(playlist_id = playlist_id)
    
    if not playlist:
        abort(404)
    
    if playlist.user_id != user.id:
        abort(403)
    
    offset = args.get('offset') if 'offset' in args else 0
    limit = args.get('limit') if 'limit' in args else None
    title = args.get('title')
    artist = args.get('artist')
    
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


def fibonacci(n):
    if n <= 2:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)


@app.route(REST_PREFIX + '/computefibonacci/', methods = ['GET'])
def compute_fibonacci():
    try:
        n = int(request.args['n'])
    except ValueError:
        abort(400)
    return 'Fibonacci(' + str(n) + ') = ' + str(fibonacci(n))
        

def create_secure_user(first_name: str, last_name: str, email: str, password: str) -> User:
    password_salt = utils.generate_uuid()
    
    password_hashed = utils.hash_password(password_raw = password, salt = password_salt)
    
    auth_token = utils.generate_uuid()
    
    result = crud_user.create_user(
            first_name,
            last_name,
            email,
            password_hashed,
            password_salt,
            auth_token)
    
    return result


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
