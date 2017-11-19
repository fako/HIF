# from facepp import API
import requests
import config
import cv2
from models import Face
import sys, os
from tqdm import tqdm

url = "https://api-us.faceplusplus.com/facepp/v3/detect"
# api = API(config.API_KEY, config.API_SECRET)

default_payload = {'api_key': config.API_KEY, 'api_secret': config.API_SECRET}
failed = []
multiple = []
skipped = []

def sourceImagePaths(directory):
    result = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            result.append(os.path.join(directory, filename))
    return result


def detectFace(imagefile):
    payload = default_payload
    imagename = "_".join(os.path.split(imagefile)[1].split("_")[:-2])
    query = Face.select().where(Face.filename == imagename)
    if query.exists():
        skipped.append(imagename)
        return
    else:
        files = {"image_file": open(imagefile, 'rb')}
        response = requests.post(url, data=payload, files=files)
        if response.status_code == requests.codes.ok:
            if len(response.json()['faces']) > 1:
                multiple.append(imagename)
                return
            for face in response.json()['faces']:
                rect = face['face_rectangle']
                x = rect['left']
                y = rect['top']
                w = rect['width']
                h = rect['height']
                new_face = Face(filename = imagename, fpp_id = face['face_token'], fpp_x = x, fpp_y = y, fpp_w = w, fpp_h = h)
                new_face.save()
        else:
            failed.append(imagename)


for file in tqdm(sourceImagePaths("clipped/")):
    detectFace(file)

# detectFace(imagefile)
print('Failed:', failed)
print('Multiple:', multiple)
print('Skipped:', skipped)
