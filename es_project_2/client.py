import boto3

import tkinter as tk
from tkinter import filedialog

authentication_queue = "https://sqs.eu-west-1.amazonaws.com/628510486601/authentication_queue"
sqs = boto3.client('sqs')


def upload_photo(image_data) -> str:
    s3 = boto3.resource('s3')
    bucket_name = 'es-photos-auth'
    folder = 'requests'
    
    s3.Bucket(bucket_name).put_object(Key = folder + "/" + response['MessageId'], Body = image_data)
    
    return "https://" + bucket_name + ".s3.amazonaws.com/" + folder + "/" + response['MessageId']


option = input("1 - Manual\n2 - Automatic\n3 - Anonymous\nOption: ")

if option == str(1):
    username = input("Username: ")
    credit = input("Value to credit: ")
    response = sqs.send_message(QueueUrl = authentication_queue,
                                MessageBody = str(credit),
                                MessageAttributes = {
                                    'Mode': {
                                        'StringValue': 'manual',
                                        'DataType': 'String'
                                    },
                                    'Username': {
                                        'StringValue': str(username),
                                        'DataType': 'String'
                                    }
                                })

elif option == str(2):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    
    image = open(file_path, 'rb')
    image_content = image.read()

    credit = input("Value to credit: ")

    response = sqs.send_message(QueueUrl = authentication_queue,
                                       MessageBody = str(credit),
                                       MessageAttributes = {
                                           'Mode': {
                                               'StringValue': 'automatic',
                                               'DataType': 'String'
                                           }
                                       })

    upload_photo(image_content)
    
else:
    credit = input("Value to credit: ")
    response = sqs.send_message(QueueUrl = authentication_queue,
                                MessageBody = str(credit),
                                MessageAttributes = {
                                    'Mode': {
                                        'StringValue': 'anonymous',
                                        'DataType': 'String'
                                    }
                                })





