import boto3
import time
from botocore.exceptions import ClientError
import sys

s3 = boto3.client('s3')
sqs = boto3.client('sqs')
rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

bucket_name = 'es-photos-auth'
s3_folder_requests = 'requests/'
s3_folder_database = 'database/'

auth_mode = "automatic"

authentication_queue = "https://sqs.eu-west-1.amazonaws.com/628510486601/authentication_queue"
client_queue = "https://sqs.eu-west-1.amazonaws.com/628510486601/response_queue"


def get_photo(request_id) -> str:
    return s3.get_object(Bucket = bucket_name, Key = s3_folder_requests + "/" + request_id)


while True:
    user_recognized = None
    
    response_to_client = "Autch... some error occurred backstage..."
    
    response = sqs.receive_message(QueueUrl = authentication_queue,
                                   MessageAttributeNames = ['All'])
    
    try:
        messages = response['Messages']
    except KeyError:
        continue
    
    message = response['Messages'][0]
    
    message_id = message['MessageId']
    amount = int(message['Body'])
    receipt_handle = message['ReceiptHandle']
    
    print("New request [id = " + message_id + "]")
    
    auth_mode = message['MessageAttributes']['Mode']['StringValue']
    
    if auth_mode == "manual":
        user_recognized = message['MessageAttributes']['Username']['StringValue']
    elif auth_mode == "automatic":
        s3_result = s3.list_objects(
                Bucket = bucket_name,
                Prefix = s3_folder_database
        )
        
        photos_database = s3_result['Contents']
        
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
    
    else:
        response_to_client = "Anonymous user has payed in cash: $" + str(amount)
        print(response_to_client)
    
    if user_recognized is not None or auth_mode == "anonymous":
        if auth_mode == "manual" or auth_mode == "automatic":
            try:
                user = table.get_item(Key = {'username': user_recognized})
                
                response_to_client = "Hi, " + user['Item']['username'] \
                                     + "! Previous balance: $" \
                                     + str(user['Item']['balance']) + " | Debit: $" + str(amount)
                print("User " + user['Item']['username']
                      + " has been recognized! Previous balance: $"
                      + str(user['Item']['balance']) + " | Debit: $" + str(amount))
                
                user_updated = table.update_item(Key = {'username': user_recognized},
                                                 ReturnValues = 'UPDATED_NEW',
                                                 UpdateExpression = "SET balance = balance - :val",
                                                 ConditionExpression = "balance >= :val",
                                                 ExpressionAttributeValues = {':val': amount}
                                                 )
                response_to_client += "\nCurrent balance: $" \
                                      + str(user_updated['Attributes']['balance'])
                print("User " + user['Item']['username'] \
                      + " | Current balance: $" \
                      + str(user_updated['Attributes']['balance']))
            
            except ClientError as e:
                if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                    response_to_client += "\nYou don't have enough credits."
                    print("User " + user['Item']['username'] + " doesn't have enough credits")
                else:
                    raise
        else:
            pass
    
    else:
        response_to_client = "User not recognized."
        print(response_to_client)
    
    sqs.delete_message(
            QueueUrl = authentication_queue,
            ReceiptHandle = receipt_handle)
    
    print("=======================================")
    
    sqs.send_message(QueueUrl = client_queue,
                     MessageBody = response_to_client)
    
    time.sleep(1) # sleep for 1 seconds
