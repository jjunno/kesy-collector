import os
import requests
import base64
from dotenv import load_dotenv
load_dotenv()

# Env variables
ENV = str(os.getenv('ENV', 'development'))
RPI1CLIENTACCESS_API_URL = str(os.getenv('RPI1CLIENTACCESS_API_URL', ''))
RECEIVER_API_URL = str(os.getenv('RECEIVER_API_URL', ''))
RECEIVER_API_USERNAME = str(os.getenv('RECEIVER_API_USERNAME', ''))
RECEIVER_API_PASSWORD = str(os.getenv('RECEIVER_API_PASSWORD', ''))
PICTURE_SAVE_PATH = str(os.getenv('PICTURE_SAVE_PATH', ''))


class ClientLocation:
    def __init__(self, uuid):
        self.uuid = uuid
        self.url = RPI1CLIENTACCESS_API_URL + '?uuid=' + uuid
        self.headers = {'Content-Type': 'application/json'}

    def send(self):
        print('Requesting client to send location to master server, UUID', self.uuid)
        response = requests.get(self.url, headers=self.headers)
        print(response)


# clientLocation = ClientLocation('123-1123-1233')
# clientLocation.request()

class Trash:
    def __init__(self, uuid):
        self.uuid = uuid
        self.headers = {'Content-Type': 'application/json'}
        self.picturePath = PICTURE_SAVE_PATH + '/' + self.uuid + '.jpg'
        self.encodedPicture = None

        self.pictureToBase64()

    def send(self):
        print('Sending trash to master server UUID', self.uuid)
        payload = {"uuid": self.uuid,
                   "encodedPicture": str(self.encodedPicture)}

        response = requests.post(RECEIVER_API_URL, json=payload, headers=self.headers, auth=(
            RECEIVER_API_USERNAME, RECEIVER_API_PASSWORD))
        print(response)

    def pictureToBase64(self):
        with open(self.picturePath, "rb") as f:
            encodedString = base64.b64encode(f.read())
            self.encodedPicture = encodedString
            return encodedString


# trash = Trash('123-1123-1233')
# trash.send()
