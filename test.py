from operator import truediv
import threading
from detector import detect, record
from webConnect import *

recordingThread = threading.Thread(target=record,name="recorder")
recordingThread.start()

detectionListeningThread = threading.Thread(target=createConnection,name="instrution-listener")
detectionListeningThread.start()

# detectBool = True

while True:
    if detectBool:
        detect(detectBool)
        print("detection started!")
        
        