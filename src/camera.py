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
PICTURE_WIDTH = int(os.getenv('PICTURE_WIDTH', 1920))
PICTURE_HEIGHT = int(os.getenv('PICTURE_HEIGHT', 1080))
PICTURE_SAVE_PATH = str(os.getenv('PICTURE_SAVE_PATH', ''))


# Preview can only be used in development mode,
# when SHOW_PREVIEW = True.
def showPreview():
    if (ENV == 'development' and SHOW_PREVIEW == 'True'):
        return True
    return False


class Camera:
    def __init__(self):
        self.picam = Picamera2()

        # Configuration for picture
        stillConfig = self.picam.create_still_configuration(
            main={"size": (PICTURE_WIDTH, PICTURE_HEIGHT)})
        self.picam.configure(stillConfig)

        # Configuration for preview
        if (showPreview()):
            previewConfig = self.picam.create_preview_configuration(
                main={"size": (PICTURE_WIDTH, PICTURE_HEIGHT)})
            self.picam.configure(previewConfig)

    # uuid is used for naming the picture
    def capture(self, uuid=str(uuid.uuid4())):
        if (showPreview()):
            self.picam.start_preview(Preview.QTGL)

        self.picam.start()

        if (showPreview()):
            time.sleep(2)

        self.picam.capture_file(PICTURE_SAVE_PATH + '/' + uuid + '.jpg')
        self.picam.close()


##
test = Camera()
test.capture()
