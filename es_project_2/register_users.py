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
    user_id = str(uuid.uuid4())
    table.put_item(
            Item = {
                'id': user_id,
                'username': filename.split(".", 1)[0],
                'balance': 100
            }
    )
    
    image = open("photos_database/" + filename, 'rb')
    image_content = image.read()
    
    upload_photo(image_content, user_id)


