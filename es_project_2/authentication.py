import boto3
from botocore.exceptions import ClientError
import sys

s3 = boto3.client('s3')
sqs = boto3.client('sqs')
rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')

bucket_name = 'es-photos-auth'
s3_folder_requests = 'requests/'
s3_folder_database = 'database/'


def get_photo(request_id) -> str:
    return s3.get_object(Bucket = bucket_name, Key = s3_folder_requests + "/" + request_id)


while True:
    authentication_queue = "https://sqs.eu-west-1.amazonaws.com/628510486601/authentication_queue"
    
    response = sqs.receive_message(QueueUrl = authentication_queue)
    
    try:
        messages = response['Messages']
    except KeyError:
        continue
    
    message_id = response['Messages'][0]['MessageId']
    amount = int(response['Messages'][0]['Body'])
    receipt_handle = response['Messages'][0]['ReceiptHandle']
    
    print("New request [id = " + message_id + "]")
    
    s3_result = s3.list_objects(
            Bucket = bucket_name,
            Prefix = s3_folder_database
    )
    
    photos_database = s3_result['Contents']
    
    user_recognized = None
    print("Recognizing user...", end = '')

    if len(photos_database) > 0:
        for photo in photos_database:
            photo_key = photo['Key']
            
            if photo_key == s3_folder_database:
                continue
            
            response = rekognition.compare_faces(
                    SourceImage = {
                        'S3Object': {
                            'Bucket': bucket_name,
                            'Name': s3_folder_requests + message_id
                        }
                    },
                    TargetImage = {
                        'S3Object': {
                            'Bucket': bucket_name,
                            'Name': photo_key,
                        }
                    }
            )
            
            if len(response['FaceMatches']) == 1:
                user_recognized = photo_key.split("/", 1)[1]
                break
            
            print(".", end = '')
            sys.stdout.flush()

    print()

    if user_recognized is not None:
        table = dynamodb.Table('users')
        try:
            user = table.get_item(Key = {'id': user_recognized})
            print("User " + user['Item']['username'] + " has been recognized! Balance: $"
                  + str(user['Item']['balance']) + " | Debit: $"
                  + str(amount))
            
            user_updated = table.update_item(Key = {'id': user_recognized},
                              ReturnValues = 'UPDATED_NEW',
                              UpdateExpression = "SET balance = balance - :val",
                              ConditionExpression = "balance >= :val",
                              ExpressionAttributeValues = {':val': amount}
                              )
            print("User " + user['Item']['username'] + " | New balance: $" + str(user_updated['Attributes']['balance']))

        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print("User " + user['Item']['username'] + " has not enough balance.")
            else:
                raise
    
    else:
        print("No user recnognized")
        
        
    sqs.delete_message(
            QueueUrl = authentication_queue,
            ReceiptHandle = receipt_handle)
    
    print("=======")
