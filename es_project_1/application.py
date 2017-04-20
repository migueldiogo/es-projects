from functools import wraps

from flask import Flask, jsonify
from flask import Response
from flask import abort
from flask import render_template
from flask import request
from crud import Session
from crud import user as crud_user
from crud import song as crud_song
from crud import playlist as crud_playlist
from models import Song, User, Playlist
from serializers import UserSerializer, SongSerializer, PlaylistSerializer
import utils
import aws

application = Flask(__name__)

REST_PREFIX = '/api/v1'


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers['Authorization']
        if not token:
            abort(401)
        session = Session()
        user = crud_user.get_user_by_token(session, token)
        
        if not user:
            session.close()
            abort(401)
            
        session.close()
        return f(user, *args, **kwargs)
    
    return decorated


@application.route('/')
def hello_world():
    return render_template("login.html")


@application.route(REST_PREFIX + '/users/', methods = ['POST'])
def create_user():
    data = request.get_json()

    session = Session()
    result = create_secure_user(
            session,
            data['firstName'],
            data['lastName'],
            data['email'],
            data['password'])
    session.close()
    
    if not result:
        return Response(status = 409,
                        response = {'code': 409, 'message': "There is already an user with this email",
                                    'fields': "email"})
    else:
        return Response(status = 200)


@application.route(REST_PREFIX + '/users/self/<int:user_id>/', methods = ['PUT'])
@requires_auth
def update_user(user, user_id):
    data = request.get_json()
    session = Session()
    user.first_name = data['firstName'] if data['firstName'] != "" else user.first_name
    user.last_name = data['lastName'] if data['lastName'] != "" else user.last_name
    user.password_hashed = data['password'] if data['password'] != "" else user.password_hashed
    password_salt = utils.generate_uuid() if data['password'] != "" else user.password_salt
    user.password_hashed = utils.hash_password(password_raw = user.password_hashed, salt = password_salt) if data[
                                                                                                                 'password'] != "" else user.password_hashed
    crud_user.update_user(session, user.id, user.first_name, user.last_name, None, user.password_hashed, password_salt)
    session.close()
    return Response(status = 200)


@application.route(REST_PREFIX + '/users/self/', methods = ['GET'])
@requires_auth
def get_user(user):
    return jsonify(UserSerializer.serialize(user))


@application.route(REST_PREFIX + '/users/self/', methods = ['DELETE'])
@requires_auth
def delete_user(user):
    session = Session()

    data = crud_song.get_all_songs_from_user(session,
                                             offset=0,
                                             limit=10,
                                             user_id=user.id)

    super_user = crud_user.get_user_by_email(session, "admin@admin.com")

    if not super_user:
        create_secure_user(session, first_name="admin", last_name="", email="admin@admin.com", password="admin")

    super_user = crud_user.get_user_by_email(session, "admin@admin.com")

    for item in data:
        crud_song.update_song_ownership(session, item.id, super_user.id)

    crud_user.delete_user(session, user.id)
    session.close()
    return Response(status = 200)


@application.route(REST_PREFIX + '/users/self/tokens/', methods = ['POST'])
def get_token():
    data = request.get_json()

    session = Session()
    user = crud_user.get_user_by_email(session, data['email'])
    
    if not user:
        session.close()
        abort(401)
    
    input_hash = utils.hash_password(data['password'], user.password_salt)
    right_hash = user.password_hashed
    
    if input_hash != right_hash:
        session.close()
        abort(401)
    
    result = {'token': user.auth_token}
    session.close()
    
    return jsonify(result)


@application.route(REST_PREFIX + '/users/self/songs/', methods = ['GET'])
@requires_auth
def get_user_songs(user):
    args = request.args
    
    offset = args.get('offset') if 'offset' in args else 0
    limit = args.get('limit') if 'limit' in args else None

    session = Session()
    data = crud_song.get_all_songs_from_user(session,
                                             offset = offset,
                                             limit = limit,
                                             user_id = user.id)
    session.close()
    return jsonify(SongSerializer.serialize(data, many = True))


@application.route(REST_PREFIX + '/users/self/playlists/', methods = ['GET'])
@requires_auth
def get_user_playlists(user):
    args = request.args
    
    offset = args.get('offset') if 'offset' in args else 0
    limit = args.get('limit') if 'limit' in args else None

    session = Session()
    data = crud_playlist.get_all_playlists(session,
                                           offset = offset,
                                           limit = limit,
                                           user_id = user.id)
    session.close()
    return jsonify(PlaylistSerializer.serialize(data, many = True))


@application.route(REST_PREFIX + '/songs', methods = ['GET'])
@requires_auth
def get_songs(user):
    args = request.args
    
    offset = args.get('offset') if 'offset' in args else 0
    limit = args.get('limit') if 'limit' in args else None
    title = args.get('title')
    artist = args.get('artist')

    session = Session()
    data = crud_song.get_all_songs(session,
                                   offset = offset,
                                   limit = limit,
                                   song_title = title,
                                   song_artist = artist)
    session.close()
    return jsonify(SongSerializer.serialize(data, many = True))


@application.route(REST_PREFIX + '/songs/', methods = ['POST'])
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

    session = Session()
    crud_song.create_song(session,
                          user_id = user.id,
                          song_title = form['title'],
                          song_artist = form['artist'],
                          song_album = form['album'],
                          song_release_year = int(form['releaseYear']),
                          song_url = song_url)
    session.close()
    
    return Response(status = 200)


@application.route(REST_PREFIX + '/songs/<int:song_id>/', methods = ['GET'])
@requires_auth
def get_song(user, song_id):
    session = Session()
    song = crud_song.get_song(session, song_id = song_id)
    if not song:
        session.close()
        abort(404)
    session.close()
    return jsonify(SongSerializer.serialize(song))


@application.route(REST_PREFIX + '/songs/<int:song_id>/', methods = ['DELETE'])
@requires_auth
def delete_song(user, song_id):
    # if there isn't any super user, create one
    session = Session()
    super_user = crud_user.get_user_by_email(session, "admin@admin.com")
    
    if not super_user:
        create_secure_user(session, first_name = "admin", last_name = "", email = "admin@admin.com", password = "admin")
    
    super_user = crud_user.get_user_by_email(session, "admin@admin.com")

    song = crud_song.get_song(session, song_id = song_id)
    if not song:
        session.close()
        abort(404)
    if song.user_id != user.id:
        session.close()
        abort(403)
    
    crud_song.update_song_ownership(session, song_id, super_user.id)
    session.close()

    return Response(status = 200)


@application.route(REST_PREFIX + '/songs/<int:song_id>/', methods = ['PUT'])
@requires_auth
def update_song(user, song_id):
    form = request.form

    session = Session()
    song = crud_song.get_song(session, song_id = song_id)
    
    if not song:
        session.close()
        abort(404)
    if song.user_id != user.id:
        session.close()
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
            session.close()
            abort(400)
        
        song_new_filename = utils.generate_uuid()
        
        song.url = aws.upload_song(song_new_filename, file_extension, song_file)

    crud_song.update_song(session, song)
    session.close()
    
    return Response(status = 200)


@application.route(REST_PREFIX + '/playlists/', methods = ['POST'])
@requires_auth
def create_playlist(user):
    data = request.get_json()

    session = Session()
    crud_playlist.create_playlist(session,
                                  user_id = user.id,
                                  playlist_name = data['name'])
    session.close()
    return Response(status = 200)


@application.route(REST_PREFIX + '/playlists/<int:playlist_id>/', methods = ['DELETE'])
@requires_auth
def delete_playlist(user, playlist_id):
    session = Session()
    playlist = crud_playlist.get_playlist(session, playlist_id = playlist_id)
    if not playlist:
        session.close()
        abort(404)
    if playlist.user_id != user.id:
        session.close()
        abort(403)
    
    crud_playlist.delete_playlist(session, playlist_id)
    session.close()
    
    return Response(status = 200)


@application.route(REST_PREFIX + '/playlists/<int:playlist_id>/', methods = ['PUT'])
@requires_auth
def update_playlist(user, playlist_id):
    data = request.get_json()
    playlist_name = data['name']

    session = Session()
    playlist = crud_playlist.get_playlist(session, playlist_id = playlist_id)
    if not playlist:
        session.close()
        abort(404)
    if playlist.user_id != user.id:
        session.close()
        abort(403)
    
    if playlist_name:
        playlist.name = playlist_name
        crud_playlist.update_playlist(session, playlist)

    session.close()
    return Response(status = 200)


@application.route(REST_PREFIX + '/playlists/<int:playlist_id>/songs/', methods = ['GET'])
@requires_auth
def get_songs_from_playlist(user, playlist_id):
    args = request.args
    session = Session()
    playlist = crud_playlist.get_playlist(session, playlist_id = playlist_id)
    
    if not playlist:
        session.close()
        abort(404)
    
    if playlist.user_id != user.id:
        session.close()
        abort(403)
    
    offset = args.get('offset') if 'offset' in args else 0
    limit = args.get('limit') if 'limit' in args else None
    title = args.get('title')
    artist = args.get('artist')
    
    data = crud_song.get_all_songs_from_playlist(session,
                                                 playlist_id = playlist_id,
                                                 offset = offset,
                                                 limit = limit,
                                                 song_title = title,
                                                 song_artist = artist)
    session.close()
    return jsonify(SongSerializer.serialize(data, many = True))


@application.route(REST_PREFIX + '/playlists/<int:playlist_id>/songs/<int:song_id>/', methods = ['POST'])
@requires_auth
def add_song_to_playlist(user, playlist_id, song_id):
    session = Session()
    playlist = crud_playlist.get_playlist(session, playlist_id = playlist_id)
    if not playlist:
        session.close()
        abort(404)
    if playlist.user_id != user.id:
        session.close()
        abort(403)
    
    song = crud_song.get_song(session, song_id = song_id)
    if not song:
        session.close()
        abort(404)
    
    playlist.songs.append(song)
    playlist.size += 1
    crud_playlist.update_playlist(session, playlist)
    session.close()
    
    return Response(status = 200)


@application.route(REST_PREFIX + '/playlists/<int:playlist_id>/songs/<int:song_id>/', methods = ['DELETE'])
@requires_auth
def remove_song_from_playlist(user, playlist_id, song_id):
    session = Session()
    playlist = crud_playlist.get_playlist(session, playlist_id = playlist_id)
    if not playlist:
        session.close()
        abort(404)
    if playlist.user_id != user.id:
        session.close()
        abort(403)
    
    song = crud_song.get_song(session, song_id = song_id)
    if not song:
        session.close()
        abort(404)
    
    playlist.songs.remove(song)
    playlist.size -= 1
    
    crud_playlist.update_playlist(session, playlist)
    session.close()
    
    return Response(status = 200)


def fibonacci(n):
    if n <= 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


@application.route(REST_PREFIX + '/computefibonacci/', methods = ['GET'])
def compute_fibonacci():
    try:
        n = int(request.args['n'])
    except ValueError:
        abort(400)
    return 'Fibonacci(' + str(n) + ') = ' + str(fibonacci(n))


def create_secure_user(session: Session, first_name: str, last_name: str, email: str, password: str) -> User:
    password_salt = utils.generate_uuid()
    
    password_hashed = utils.hash_password(password_raw = password, salt = password_salt)
    
    auth_token = utils.generate_uuid()
    
    result = crud_user.create_user(
            session,
            first_name,
            last_name,
            email,
            password_hashed,
            password_salt,
            auth_token)
    
    return result


@application.errorhandler(400)
def bad_request(error = None):
    message = {
        'code': 400,
        'message': 'Bad request',
    }
    resp = jsonify(message)
    resp.status_code = 400
    
    return resp


@application.errorhandler(401)
def unauthorized(error = None):
    message = {
        'code': 401,
        'message': 'Not authorized',
    }
    resp = jsonify(message)
    resp.status_code = 401
    
    return resp


@application.errorhandler(403)
def unauthorized(error = None):
    message = {
        'code': 403,
        'message': 'Forbidden',
    }
    resp = jsonify(message)
    resp.status_code = 403
    
    return resp


@application.errorhandler(404)
def not_found(error = None):
    message = {
        'code': 404,
        'message': 'Not Found',
    }
    resp = jsonify(message)
    resp.status_code = 404
    
    return resp


if __name__ == '__main__':
    application.run()
