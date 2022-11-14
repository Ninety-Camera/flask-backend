from flask import Flask,Response,render_template
import cv2
from flask_cors import CORS, cross_origin
import threading
from camera import detectThread

class flask_api(threading.Thread):
    
    
    def __init__(self,frame_buffer,cam_buffer):
        threading.Thread.__init__(self)
        self.frame_buffer = frame_buffer
        self.cam_buffer = cam_buffer
        
        
    def run(self):
        app = Flask(__name__)
        
        @app.route('/')
        def index():
            # rendering webpage
            return render_template('index.html')
        
        def gen(camera):
            while True:
                #get camera frame
                ret, image = cv2.imencode('.jpg', self.frame_buffer[camera])
                image = image.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n\r\n')
        
        @app.route('/video_feed/<camera>')
        def video_feed(camera):
            print("Camera is: ",camera)
            return Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')
        
        
        
        @app.route('/add/camera',methods = ['POST'])
        def add_camera():
            name = 'cam1'
            new_camera = detectThread(name,self.frame_buffer)
            self.cam_buffer.append(new_camera)
            new_camera.start()
        
        app.run(port='5000',host='0.0.0.0')
    
    
    