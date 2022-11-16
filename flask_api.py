from flask import Flask,Response,send_file,request,jsonify
import cv2
from flask_cors import cross_origin
import threading
from camera import Camera


class flask_api(threading.Thread):
    
    
    def __init__(self,frame_buffer,cam_buffer,db_helper):
        threading.Thread.__init__(self)
        self.frame_buffer = frame_buffer
        self.cam_buffer = cam_buffer
        self.db_helper = db_helper
        
        
    def run(self):
        app = Flask(__name__)
        
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
        @cross_origin()
        def add_camera():
            data = request.data()
            name = data["name"]
            cam_id = data["cam_id"]
            is_ip = data["is_ip_camera"]
            link = data["source"]
            
            new_camera = Camera(name,self.frame_buffer,link)
            self.cam_buffer.append(new_camera)
            new_camera.start()
            
        @app.route('/get_image/<intrusion_id>')
        def get_intrusion_image(intrusion_id):
            return send_file('intrusion_images/1.png',mimetype='image/gif')
        
        @app.route('/get_record')
        def get_record():
            return send_file('records/Recordcam111_11_2022_15_02_10.avi')
            
        @app.route('/trial/<id>')
        def home(id):
            return "home"+id
        
        @app.route("/add/user",methods=['POST'])
        @cross_origin()
        def add_user():
            try:
                data = request.get_json()
                print(data)
                email = data['email']
                user_id = data['id']
                token = data['token']
                first_name = data["firstName"]
                last_name = data['lastName']
                role = data['role']
                
                self.db_helper.add_user_data(email,user_id,role,token,first_name,last_name)
                return Response(status=201)
            except Exception as e:
                print(e)
                return Response(status=500)
                
            
        @app.route("/")
        @cross_origin()
        def homepage():
            return "done"
        
        @app.route("/get/user",methods= ["GET"])
        @cross_origin()
        def get_user():
            try:
                data = self.db_helper.get_user_details()
                return jsonify(email=data[0],userId = data[1],role=data[2],token=data[3],firstName=data[4],lastName=data[5])
            except Exception as e:
                print(e)
                return Response(status=500)
        
        @app.route("/delete/user",methods=["DELETE"])
        @cross_origin()
        def delete_user():
            try:
                self.db_helper.delete_userdata()
                return Response(status=201)
            except Exception as e:
                print(e)
                return Response(status=500)

        
        
        
        app.run(port='5000',host='0.0.0.0')
    
    
    