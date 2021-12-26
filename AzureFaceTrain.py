import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person
KEY = "3ec64d13489b49b9a4cf8ac796471f6b"
ENDPOINT = "https://face-recognition-azure.cognitiveservices.azure.com/"
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
PERSON_GROUP_ID = 'friends'
face_client.person_group.delete(person_group_id=PERSON_GROUP_ID)
print('Person group: ', PERSON_GROUP_ID)
face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)
karthik = face_client.person_group_person.create(PERSON_GROUP_ID, "Karthik")
deepak = face_client.person_group_person.create(PERSON_GROUP_ID, "Deepak")
krishna = face_client.person_group_person.create(PERSON_GROUP_ID, "Krishna")
karthik_images = [file for file in glob.glob('*.jpg') if file.startswith("S02")]
deepak_images = [file for file in glob.glob('*.jpg') if file.startswith("S03")]
krishna_images = [file for file in glob.glob('*.jpg') if file.startswith("S01")]
for image in karthik_images:
    w = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, karthik.person_id, w)
    time.sleep(3)
for image in deepak_images:
    m = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, deepak.person_id, m)
    time.sleep(3)
for image in krishna_images:
    ch = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, krishna.person_id, ch)
    time.sleep(3)
print()
print('Training the person group...')
face_client.person_group.train(PERSON_GROUP_ID)
while (True):
    training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
    print("Training status: {}.".format(training_status.status))
    print()
    if (training_status.status is TrainingStatusType.succeeded):
        break
    elif (training_status.status is TrainingStatusType.failed):
        face_client.person_group.delete(person_group_id=PERSON_GROUP_ID)
        sys.exit('Training the person group has failed.')
    time.sleep(5)
print(karthik.person_id)
print()
print(deepak.person_id)
print()
print(krishna.person_id)
print()
