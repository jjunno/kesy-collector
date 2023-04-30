import cameraModule
import apiModule
import uuid as UUID

uuid = str(UUID.uuid4())

camera = cameraModule.Camera()
camera.capture(uuid)

trash = apiModule.Trash(uuid)
trash.send()
