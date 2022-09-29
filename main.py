from detector import detect
from webConnect import *

createConnection()
while True:
    if detectBool:
        print("detection started in main..calling detection method!")
        detect()
    


