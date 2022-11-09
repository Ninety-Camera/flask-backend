import threading
import socketio

class web_connector(threading.Thread):
    def __init__(self,camera_buffer):
        threading.Thread.__init__(self)
        self.camera_buffer = camera_buffer
        
    def set_intrusion(self,state):
            for camera in self.camera_buffer:
                camera.set_detectBool(state)
        
    def run(self):
        # standard Python
        sio = socketio.Client(reconnection_delay=10)
        state = False
        
        @sio.event
        def connect():
            print("I'm connected!")

        @sio.event
        def connect_error(data):
            print("The connection failed!",data["message"])

        @sio.event
        def disconnect():
            print("I'm disconnected!")


        @sio.on("intrusion-message")
        def instrutionMessage(message):
            global detectionThread
            print("message recieved",message)
            if message == "STOP":
                print("Human detection deactivated!")
                self.set_intrusion(False)
                
                
            elif message == "RUNNING":
                print("Human detection activated!")
                self.set_intrusion(True)
            else:
                print("Incorrect message!")
                
        def createConnection():
            try:
                authDict = {"systemId":"55d60bd7-4a39-4bfc-ac08-40e290444c2e"}
                sio.connect('https://ninetycamera.azurewebsites.net',auth = authDict)

            except:
                print("trying again to connect...")
                createConnection()
                
        
                

        # creating the connection with server.
        createConnection()