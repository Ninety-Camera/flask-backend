import threading
from detector import detect, record
from webConnect import *


# starting the recording. 
recordingThread = threading.Thread(target=record,name="recorder")
recordingThread.start()

# starting create connection and listening to connection.
detectionListeningThread = threading.Thread(target=createConnection,name="instrution-listener")
detectionListeningThread.start()

#checking for detectBool and starting human detection if it's True.
while True:
    if detectBool:
        detect(detectBool)
        print("detection started!")

