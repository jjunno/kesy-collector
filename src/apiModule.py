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
IMAGE_SAVE_PATH = str(os.getenv('IMAGE_SAVE_PATH', ''))


class ClientLocation:
    def __init__(self, uuid):
        self.uuid = uuid
        self.url = RPI1CLIENTACCESS_API_URL + '?uuid=' + uuid
        self.headers = {'Content-Type': 'application/json'}

    def send(self):
        print('Requesting client to send location to master server, UUID', self.uuid)
        try:
            response = requests.get(self.url, headers=self.headers, timeout=5)
            print(response)
        except requests.exceptions.ConnectTimeout:
            print('ConnectTimeout: the client HTTP server is unreachable')
        except requests.exceptions.ConnectionError:
            print('ConnectionError: the client HTTP server refused connection')


class Trash:
    def __init__(self, uuid):
        self.uuid = uuid
        self.headers = {'Content-Type': 'application/json'}
        self.imagePath = IMAGE_SAVE_PATH + '/' + self.uuid + '.jpg'
        self.encodedImage = None

        self.imageToBase64()

    def send(self):
        print('Sending trash to master server UUID', self.uuid)
        payload = {"uuid": self.uuid,
                   "encodedImage": self.encodedImage}

        try:
            response = requests.post(RECEIVER_API_URL, json=payload, headers=self.headers, auth=(
                RECEIVER_API_USERNAME, RECEIVER_API_PASSWORD), timeout=30)
            print(response)
        except requests.exceptions.ConnectTimeout:
            print('ConnectTimeout: the master server is unreachable')
        except requests.exceptions.ConnectionError:
            print('ConnectionError: the master server refused connection')

    def imageToBase64(self):
        with open(self.imagePath, "rb") as f:
            base64Bytes = base64.b64encode(f.read())
            base64String = base64Bytes.decode('utf-8')
            self.encodedImage = base64String
            return base64String
