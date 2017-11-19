import cv2
import base64
import faceplusplus_analysis.config as config
import requests
from faceplusplus_analysis.models import Face

url = "https://api-us.faceplusplus.com/facepp/v3/search"
default_payload = {'api_key': config.API_KEY, 'api_secret': config.API_SECRET}

def compareFace(cv2face):
    cnt = cv2.imencode('.png',cv2face)[1]
    b64 = base64.b64encode(cnt)
    payload = {"image_base64": b64,
                "outer_id":config.FACE_SET_NAME}
    payload = {**default_payload, **payload}
    response = requests.post(url, data=payload)
    if response.status_code == requests.codes.ok:
        responsedict = response.json()
        if not 'results' in responsedict:
            print("Request did not contain results")
            return False
        print(responsedict['results'])
        match = responsedict['results'][0]['face_token']
        matching = Face.get(fpp_id=match)
        return matching.filename[:20] + "." + matching.filename[20:] +".jpg"
    else:
        print("Request failed: {}".format(response.text()))
        return False



# image = cv2.imread('clipped/20170916152036247540t5vesGu_clipped_1.jpg')
# print(compareFace(image))
