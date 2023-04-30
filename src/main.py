import cameraModule
import apiModule
import uuid as UUID
import time

uuid = str(UUID.uuid4())

camera = cameraModule.Camera()
camera.capture(uuid)

trash = apiModule.Trash(uuid)
trash.send()
time.sleep(1)

clientLocation = apiModule.ClientLocation(uuid)
clientLocation.send()
