from time import sleep
from detector import detectThread

detection_thread = detectThread("Detection thread")
detection_thread.start()

detection_thread.set_detectBool(True)
sleep(10)
detection_thread.set_detectBool(False)

