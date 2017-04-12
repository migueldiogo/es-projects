class UserSerializer:
    @classmethod
    def serialize(cls, data, many: bool = False):
        if many:
            serializer = []
            for user in data:
                serializer.append({'firstName':user.first_name,
                                   'lastName':user.last_name,
                                   'email':user.email,
                                   'id':user.id})
        else:
            serializer = {'firstName':data.first_name,
                          'lastName':data.last_name,
                          'email':data.email,
                          'id': data.id}
        return serializer


class PlaylistSerializer:
    @classmethod
    def serialize(cls, data, many: bool = False):
        if many:
            serializer = []
            for playlist in data:
                serializer.append({'id':playlist.id,
                                   'name':playlist.name,
                                   'createdAt':playlist.created_at,
                                   'size':playlist.size})
        else:
            serializer = {'id':data.id,
                          'name':data.name,
                          'createdAt':data.created_at,
                          'size':data.size}
        return serializer


class SongSerializer:
    @classmethod
    def serialize(cls, data, many: bool = False):
        if many:
            serializer = []
            for song in data:
                serializer.append({'id':song.id,
                                   'title':song.title,
                                   'artist':song.artist,
                                   'album':song.album,
                                   'releaseYear':song.release_year,
                                   'url':song.url})
        else:
            serializer = {'id':data.id,
                          'title':data.title,
                          'artist':data.artist,
                          'album':data.album,
                          'releaseYear':data.release_year,
                          'url':data.url}
        return serializer
