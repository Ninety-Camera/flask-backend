import threading
from detector import detect, record
from webConnect import *

recordingThread = threading.Thread(target=record,name="recorder")
recordingThread.start()

detectionListeningThread = threading.Thread(target=createConnection,name="instrution-listener")
detectionListeningThread.start()

while True:
    if detectBool:
        detect()
        print("detection started!")


