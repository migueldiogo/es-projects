import boto3

import base64

import tkinter as tk
from tkinter import filedialog


def upload_photo(image_data) -> str:
    s3 = boto3.resource('s3')
    bucket_name = 'es-photos-auth'
    folder = 'requests'
    
    s3.Bucket(bucket_name).put_object(Key = folder + "/" + response['MessageId'], Body = image_data)
    
    return "https://" + bucket_name + ".s3.amazonaws.com/" + folder + "/" + response['MessageId']


credit = input("Value to credit: ")

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

image = open(file_path, 'rb')
image_content = image.read()

#image_encoded = base64.b64encode(image_content).decode('ascii')

authentication_queue = "https://sqs.eu-west-1.amazonaws.com/628510486601/authentication_queue"

client = boto3.client('sqs')

response = client.send_message(QueueUrl = authentication_queue,
                               MessageBody = str(credit))

upload_photo(image_content)


