from doctest import FAIL_FAST
import numpy as np
from datetime import datetime
import socketio


# standard Python
sio = socketio.Client(reconnection_delay=10)

detectBool = False

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")






@sio.on("intrusion-message")
def instrutionMessage(message):
    print("message recieved",message)
    if message == "Stop Proccessing":
        print("Human detection deactivated!")
        detectBool = False
        
    elif message == "RUNNING":
        print("Human detection activated!")
        detectBool = True
    
    else:
        print("Incorrect message!")
        
def createConnection():
    try:
        authDict = {"systemId":"00c2aa5b-9ed7-4cb9-9fd7-235f180caded"}
        sio.connect('https://ninetycamera.azurewebsites.net',auth = authDict)
    except:
        print("establishing the connection failed!")