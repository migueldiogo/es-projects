import boto3

s3 = boto3.resource('s3')
songs_bucket_name = bucket_name = 'es-soundshare'


def upload_song(song_filename: str, song_format_ext: str, song_data) -> str:
    
    filename = song_filename + song_format_ext
    
    s3.Bucket(bucket_name).put_object(Key = filename, Body = song_data)
    
    return "https://" + bucket_name + ".s3.amazonaws.com/" + filename
