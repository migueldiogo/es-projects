import os

import boto3
import uuid


def upload_photo(image_data, key) -> str:
    s3 = boto3.resource('s3')
    bucket_name = 'es-photos-auth'
    folder = 'database'
    
    s3.Bucket(bucket_name).put_object(Key = folder + "/" + key, Body = image_data)
    
    return "https://" + bucket_name + ".s3.amazonaws.com/" + folder + "/" + key


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

for filename in os.listdir("photos_database/"):
    username = filename.split(".", 1)[0]
    table.put_item(
            Item = {
                'username': username,
                'balance': 100
            }
    )
    
    image = open("photos_database/" + filename, 'rb')
    image_content = image.read()
    
    upload_photo(image_content, username)


