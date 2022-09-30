import threading
from trace import Trace
import socketio
from detector import detectThread
from recorder import record


# standard Python
sio = socketio.Client(reconnection_delay=10)
state = False
detectionThread = detectThread("detector")



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
        detectThread.raise_exception()
        detectionThread.join()
        
    elif message == "RUNNING":
        print("Human detection activated!")
        detectionThread.start()
        
    
    else:
        print("Incorrect message!")
        
def createConnection():
    try:
        authDict = {"systemId":"00c2aa5b-9ed7-4cb9-9fd7-235f180caded"}
        sio.connect('https://ninetycamera.azurewebsites.net',auth = authDict)
    except:
        print("establishing the connection failed!")
        
def main():
    # recording starts in another thread.
    # recordingThread = threading.Thread(target=record,name="recorder")
    # recordingThread.start()
    
    #creating the connection with the server.
    createConnection()
    
    print("afterwards")
    # creating the detection thread.
  

main()