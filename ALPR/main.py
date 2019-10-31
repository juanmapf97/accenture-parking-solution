import sys
import cv2
import json
import boto3
import os
from botocore.exceptions import NoCredentialsError
from alvr import detectPlate
from datetime import datetime, timezone
from card1 import id_detection

ACCESS_KEY = 'X'
SECRET_KEY = 'X'

path = '../DB/'
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


def action(image_path):
    global pk
    
    # Detecting and processing image
    text, cropped, img = detectPlate(image_path)

    license_name, license_crop = id_detection()

    # Save files locally
    nameFull = str(pk) + '-full.png'
    if not cv2.imwrite(os.path.join(path, nameFull), img):
        raise Exception("Could not write image")


    nameCropped = str(pk) + '-cropped.png'
    if not cv2.imwrite(os.path.join(path, nameCropped), cropped):
        raise Exception("Could not write image")

    licenceCropped = str(pk) + '-id.png'
    if not cv2.imwrite(os.path.join(path, licenceCropped), license_crop):
        raise Exception("Could not write image")

    nameText = str(pk) + '-text.json'
    data = {
        'plate' : text,
        'created_on': datetime.now().strftime('%d %b %Y'),
        'name': license_name
    }
    with open(os.path.join(path, nameText), 'w') as fp:
        json.dump(data, fp)
    
    print(data)
    cv2.imshow('image',img)
    cv2.imshow('cropped',cropped)
    cv2.imshow('license',license_crop)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Upload things to bucket and delete local files
    # uploadToAws(path + nameFull, 'accenture-parking-solution', nameFull)
    # uploadToAws(path + nameCropped, 'accenture-parking-solution', nameCropped)
    # uploadToAws(path + nameText, 'accenture-parking-solution', nameText)
    # uploadToAws(path + licenceCropped, 'accenture-parking-solution', licenceCropped)

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