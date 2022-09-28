import numpy as np
from datetime import datetime
import socketio


# standard Python
sio = socketio.Client()


@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

authDict = {"systemId":"00c2aa5b-9ed7-4cb9-9fd7-235f180caded"}
sio.connect('https://ninetycamera.azurewebsites.net',auth = authDict,wait_timeout=10)

