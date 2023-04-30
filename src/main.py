import cameraModule
import apiModule
import RPi.GPIO as GPIO
import uuid as UUID

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering https://pinout.xyz

# Setup GPIO for to button
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def onButton(channel):
    print('Button was pushed')
    uuid = str(UUID.uuid4())
    camera = cameraModule.Camera()
    camera.capture(uuid)

    trash = apiModule.Trash(uuid)
    trash.send()

    clientLocation = apiModule.ClientLocation(uuid)
    clientLocation.send()


# Listen to events on GPIO 3
GPIO.add_event_detect(3, GPIO.RISING, callback=onButton)

# The button listener is on, so until the user hits enter on types anyting, the program (thus the listener) is on
input("Hit ENTER to exit program.\n")
