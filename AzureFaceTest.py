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
KEY = "<FACE_API_KEY>"
ENDPOINT = "FACE_API_ENDPOINT>"
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
PERSON_GROUP_ID = 'friends'
print('Person group:', PERSON_GROUP_ID)
test_image_array = glob.glob('S01_(5).jpg')
image = open(test_image_array[0], 'r+b')
face_ids = []
faces = face_client.face.detect_with_stream(image, detection_model='detection_03')
for face in faces:
    face_ids.append(face.face_id)
results = face_client.face.identify(face_ids, PERSON_GROUP_ID)
if not results:
    print('No person identified in the person group for faces.')
for person in results:
    if len(person.candidates) > 0:
        print(person.candidates[0].person_id)
        if(person.candidates[0].person_id=='98e96b2a-217c-4d68-b45b-ec3baf7f2219'):
            recognisedname = 'Karthik Sajjan'
        elif(person.candidates[0].person_id=='e7c9a74a-1152-438f-9575-e2cb84aa6f23'):
            recognisedname = 'Deepak Chowdary'
        else:
            recognisedname = 'Krishna Paanchajanya'
        print('{} is identified with a confidence of {}.'.format(recognisedname, person.candidates[0].confidence))
    else:
        print('No person is identified for face ID {}.'.format(person.face_id))
