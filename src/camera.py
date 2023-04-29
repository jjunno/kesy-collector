import os
import time
import uuid

import libcamera
from picamera2 import Picamera2, Preview
from dotenv import load_dotenv

load_dotenv()

# Env variables
ENV = str(os.getenv('ENV', 'development'))
SHOW_PREVIEW = str(os.getenv('SHOW_PREVIEW', False))
IMAGE_WIDTH = int(os.getenv('IMAGE_WIDTH', 1920))
IMAGE_HEIGHT = int(os.getenv('IMAGE_HEIGHT', 1080))
IMAGE_SAVE_PATH = str(os.getenv('IMAGE_SAVE_PATH', ''))


# Preview can only be used in development mode,
# when SHOW_PREVIEW = True.
def showPreview():
    if (ENV == 'development' and SHOW_PREVIEW == 'True'):
        return True
    return False


class Camera:
    def __init__(self):
        self.picam = Picamera2()

        # Configuration for image
        stillConfig = self.picam.create_still_configuration(
            main={"size": (IMAGE_WIDTH, IMAGE_HEIGHT)})
        self.picam.configure(stillConfig)

        # Configuration for preview
        if (showPreview()):
            previewConfig = self.picam.create_preview_configuration(
                main={"size": (IMAGE_WIDTH, IMAGE_HEIGHT)})
            self.picam.configure(previewConfig)

    # uuid is used for naming the image
    def capture(self, uuid=str(uuid.uuid4())):
        if (showPreview()):
            self.picam.start_preview(Preview.QTGL)

        self.picam.start()

        if (showPreview()):
            time.sleep(2)

        self.picam.capture_file(IMAGE_SAVE_PATH + '/' + uuid + '.jpg')
        self.picam.close()


##
test = Camera()
test.capture()
