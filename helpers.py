print('working')

import sys, os
sys.path.append("/home/fako/Datascope/datascope")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "datascope.settings")

import socket
import json
from random import randint, shuffle
from faceplusplus_analysis import compareface
from PIL import Image
from time import time

import django
from django.core.files.storage import default_storage


SOCKET_SERVER_ADDRESS = ('192.168.43.133', 8001)
SOCKET_LOCAL_ADDRESS = ('0.0.0.0', 8002)


class Roaster(object):

    _roasts = {}
    _comments = None

    def load_roasts(self, post_id):

        if not self._comments:
            from trolls.models.community import RedditScrapeCommunity
            community = RedditScrapeCommunity.objects.get_latest_by_signature("RoastMe")
            data = community.get_growth("comments")
            self._comments = data.output.individual_set

        self._roasts[post_id] = list(self._comments.filter(identity=post_id).order_by('created_at')[:10])
        shuffle(self._roasts[post_id])
        #self._roasts[post_id] = sorted(self._comments.filter(identity=post_id).all(), key=lambda comment: int(comment["author_score"]))[:3]

    def get_roast(self, post_id):
        if post_id not in self._roasts:
            self.load_roasts(post_id)
            return self.get_roast(post_id)

        roast = self._roasts[post_id].pop()
        if not len(self._roasts[post_id]):
            del self._roasts[post_id]
        return roast


roaster = Roaster()


def send_action(action, payload):
    sock = socket.create_connection(SOCKET_SERVER_ADDRESS)
    message_data = {
        "command": action,
        "payload": payload
    }
    message = json.dumps(message_data).encode('utf-8')  # TODO: correct encoding for all types?
    sock.sendall(message)
    sock.close()


def get_random_comment():
    from trolls.models.community import RedditScrapeCommunity
    community = RedditScrapeCommunity.objects.get_latest_by_signature("RoastMe")
    data = community.get_growth("comments")
    posts = data.input.individual_set
    comments = data.output.individual_set

    posts_count = posts.all().count()
    random_index = randint(0, posts_count - 1)
    random_post = posts.all()[random_index]
    random_comment = comments.filter(identity=random_post["id"]).first()

    print('Random post id={} comments={} '.format(random_post["id"], random_post["details_link"]))
    print('Random comment id={}'.format(random_comment["id"]))
    print('-' * 80)
    print(random_comment["comment"])
    return random_comment["comment"]


def get_matching_comment(opencv_face):
    closest_face = compareface.compareFace(opencv_face)
    if not closest_face:
        print("No closes face")
        return get_random_comment()
    from trolls.models.community import RedditScrapeCommunity
    community = RedditScrapeCommunity.objects.get_latest_by_signature("RoastMe")
    data = community.get_growth("comments")
    posts = data.input.individual_set
    comments = data.output.individual_set

    file_name = closest_face.split('.')[-2]
    closest_post = posts.filter(properties__regex=file_name).first()
    if not closest_post:
        print("File name not found in posts: " + file_name)
        return get_random_comment()

    #closest_comment = comments.filter(identity=closest_post["id"]).order_by('?').first()
    closest_comment = roaster.get_roast(closest_post["id"])

    print('Closest post id={} comments={} '.format(closest_post["id"], closest_post["details_link"]))
    print('Closest comment id={}'.format(closest_comment["id"]))
    print('-' * 80)
    print(closest_comment["comment"])
    print('-' * 80)
    pil_image = Image.fromarray(opencv_face)
    pil_image.save("/home/fako/Datascope/datascope/system/files/media/mugs/{}.{}.jpg".format(closest_post["details_link"].replace('/','+'),time()))
    return closest_comment["comment"]


def send_face_detected(opencv_face):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(SOCKET_LOCAL_ADDRESS)
    sock.listen(1)

    send_action(
        "Face.Detected",
        get_matching_comment(opencv_face)
    )

    # Wait for a connection
    connection, client_address = sock.accept()
    try:
        # Receive the data in small chunks and retransmit it
        response = b""
        while True:
            data = connection.recv(16)
            if data:
                response += data
            if data.endswith(b"\n"):
                connection.sendall(b'ACK\n')
                break
    finally:
        # Clean up the connection
        connection.close()
        sock.close()
    print('-' * 80)
    print(json.loads(response.decode('utf-8')))

