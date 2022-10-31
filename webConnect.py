import threading
from trace import Trace
import socketio
from detector import detectThread
from recorder import record


# standard Python
sio = socketio.Client(reconnection_delay=10)
state = False
detectionThread = detectThread("detector")
detectionThread.start()



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
    global detectionThread
    print("message recieved",message)
    if message == "STOP":
        print("Human detection deactivated!")
        detectionThread.set_detectBool(False)
        
        
    elif message == "RUNNING":
        print("Human detection activated!")
        detectionThread.set_detectBool(True)
        
    
    else:
        print("Incorrect message!")
        
def createConnection():
    try:
        authDict = {"systemId":"00c2aa5b-9ed7-4cb9-9fd7-235f180caded"}
        sio.connect('https://ninetycamera.azurewebsites.net',auth = authDict)
    except:
        print("establishing the connection failed!\nTrying again to connect...")
        createConnection()
        

# creating the connection with server.
createConnection()
