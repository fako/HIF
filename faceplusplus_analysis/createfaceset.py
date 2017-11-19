import requests
import config
# import cv2
from models import Face
# import sys, os
from tqdm import tqdm

url = "https://api-us.faceplusplus.com/facepp/v3/faceset/addface"
default_payload = {'api_key': config.API_KEY, 'api_secret': config.API_SECRET}
failed = []
noffaces = 0 

if config.FACE_SET_TRY_CREATE:
    print("creating faceset: '{}'...".format(config.FACE_SET_NAME))
    createurl = "https://api-us.faceplusplus.com/facepp/v3/faceset/create"
    payload = {"display_name": config.FACE_SET_NAME,
               "outer_id": config.FACE_SET_NAME}
    payload = {**default_payload, **payload}
    create_response = requests.post(createurl, data=payload)
    if "error_message" in create_response.json():
        if create_response.json()["error_message"] == "FACESET_EXIST":
            print("Faceset {} already exists, carrying on...".format(config.FACE_SET_NAME))
        else:
            print("Faceset {} creation failed with error message: '{}'".format(config.FACE_SET_NAME, create_response.json()['error_message']))
else:
    print("Faceset creation skipped due to config...")

face_token_list = list(map(lambda f: f.fpp_id, Face.select()))
for face in tqdm(face_token_list):
    payload = {"outer_id":config.FACE_SET_NAME,
               "face_tokens": face}
    payload = {**default_payload, **payload}
    response = requests.post(url, data=payload)
    if response.status_code != requests.codes.ok:
        failed.append((facelist, response.json()['error_message']))
    else:
        tqdm.write(str(response.json()['face_added']))
        noffaces = response.json()['face_count']

print("faces in set:", noffaces)
print("failed:", failed)
# for fivefaces in list(Face.select())[::5]:
    # print(fivefaces)

# # detectFace(imagefile)
# print('Failed:', failed)
# print('Multiple:', multiple)
# print('Skipped:', skipped)
