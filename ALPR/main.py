import sys
import cv2
import json
import boto3
from botocore.exceptions import NoCredentialsError
from alvr import detectPlate
from datetime import datetime, timezone

ACCESS_KEY = 'AKIA2NEDLSIHWVJLPJVW'
SECRET_KEY = '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'

path = 'C:/Users/oscar/Desktop/accenture-parking-solution/DB/'
pk = 0

def uploadToAws(local_file, bucket, s3_file = None):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    
    content_type = 'image/png' if local_file.split('.')[1] == 'png' else 'text/plain'
    try:
        s3.upload_file(local_file, bucket, s3_file, ExtraArgs={'ACL': 'public-read', 'Metadata': {'Content-Type': content_type}})
        # print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def action(path):
    global pk
    
    # Detecting and processing image
    text, cropped, img = detectPlate(path)

    # Save files locally
    nameFull = str(pk) + '-full.png'
    cv2.imwrite(path + nameFull, img)

    nameCropped = str(pk) + '-cropped.png'
    cv2.imwrite(path + nameCropped, cropped)

    nameText = str(pk) + '-text.json')
    data = {
        'plate' : text,
        'created_on': datetime.now()
    }
    with open(path + nameText, 'w') as fp:
        json.dump(data, fp)
    
    # Upload things to bucket and delete local files
    uploadToAws(path + nameFull, 'accenture-parking-solution', nameFull)
    uploadToAws(path + nameCropped, 'accenture-parking-solution', nameCropped)
    uploadToAws(path + nameText, 'accenture-parking-solution', nameText)

    pk += 1

def main():
    path = str(sys.argv[1])
    action(path)

main()

# python main.py "C:\Users\oscar\Desktop\semanaI\plates\plate27.png"
# cv2.imshow('image',img)
# cv2.imshow('Cropped',cropped)

# cv2.waitKey(0)
# cv2.destroyAllWindows()