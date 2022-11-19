import threading
import socketio

class web_connector(threading.Thread):
    def __init__(self,camera_buffer,system_id):
        threading.Thread.__init__(self)
        self.camera_buffer = camera_buffer
        self.system_id = system_id
        
    # method to set the intrution mode in all cameras once
    def set_intrusion_all(self,state):
            for camera in self.camera_buffer:
                camera.set_detectBool(state)
                
    # method to set the intrusion mode in a specific camera
    def set_intrusion(self,state,camId):
        for camera in self.camera_buffer:
            if camera.id == camId:
                camera.set_detectBool(state)
                return
        
                
        
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
            createConnection()


        @sio.on("intrusion-message")
        def instrutionMessage(message):
            print("message recieved",message)
            if message == "STOP":
                print("Human detection deactivated!")
                self.set_intrusion_all(False)
                
                
            elif message == "RUNNING":
                print("Human detection activated!")
                self.set_intrusion_all(True)
            else:
                print("Incorrect message!")
                
        @sio.on("intrusion-message-camera")
        def instrutionMessageCamera(message):
            print("single camera off message recieved.",message)
            target_camera_id = message['id']
            state = True if message['status'] == 'RUNNING' else False
            
            self.set_intrusion(state,target_camera_id)
            
                
        def createConnection():
            try:
                authDict = {"systemId":self.system_id}
                sio.connect('https://ninetycamera.azurewebsites.net',auth = authDict)
                # sio.connect("10:10:10:249:4000",auth=authDict)

            except Exception as e:
                print("trying again to connect...",e)
                if str(e) != "Already connected":
                    createConnection()
                
        
                

        # creating the connection with server.
        createConnection()