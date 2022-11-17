from flask import Flask,Response,send_file,request,jsonify,send_from_directory
import cv2
from flask_cors import cross_origin
import threading
from camera import Camera
from pathlib import Path
import subprocess


class flask_api(threading.Thread):
    
    
    def __init__(self,frame_buffer,cam_buffer,db_helper):
        threading.Thread.__init__(self)
        self.frame_buffer = frame_buffer
        self.cam_buffer = cam_buffer
        self.db_helper = db_helper
        
        
    def run(self):
        app = Flask(__name__)
        
        def gen(camera_id):
            while True:
                #get camera frame
                ret, image = cv2.imencode('.jpg', self.frame_buffer[camera_id])
                image = image.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n\r\n')
        
        @app.route('/video_feed/<camera_id>')
        def video_feed(camera_id):
            print("Camera is: ",camera_id)
            return Response(gen(camera_id), mimetype='multipart/x-mixed-replace; boundary=frame')
        
        
        
        @app.route('/add/camera',methods = ['POST'])
        @cross_origin()
        def add_camera():
            try:
                data = request.get_json()
                name = data["name"]
                cam_id = data["id"]
                type =data['type']
                link = data["source"]
                
                if type == "IP_CAMERA":
                    is_ip = '1'
                    new_camera = Camera(name,cam_id,self.frame_buffer,link,self.db_helper)
                else:
                    is_ip = '0'
                    new_camera = Camera(name,cam_id,self.frame_buffer,int(link),self.db_helper)
                
                self.cam_buffer.append(new_camera)
                new_camera.start()
                
                self.db_helper.add_camera(cam_id,name,is_ip,link)
                return Response(status=200)
            except Exception as e:
                print(e)
                return Response(status=500)
            
        @app.route('/get/image/<intrusion_id>/<image_number>',methods=["GET"])
        @cross_origin()
        def get_intrusion_image(intrusion_id,image_number):
            try:
                file_path  = self.db_helper.get_intrusion_image(intrusion_id,image_number)
                return send_file(file_path,mimetype='image/gif')
            except Exception as e:
                print(e)
                return Response(status=500)
            
        # function to return the all the frames of the video.
        def gen_local_video(video_path):
            cap = cv2.VideoCapture(video_path)
            
            while cap.isOpened():
                #get camera frame
                ret,frame = cap.read()
                if not ret:
                    continue
                ret, image = cv2.imencode('.jpg', frame)
                image = image.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n\r\n')
        
        # function to stream the intrution video.
        
        @app.route("/get/intrusion_video/<intrusion_id>")
        @cross_origin()
        def get_intrusion_video(intrusion_id):
            try:
                file_path = self.db_helper.get_intrusion_video(intrusion_id)
                file_path.replace('intrusion_videos/','')
                real_path = str(Path(__file__).parent.absolute())
                command = 'explorer '+real_path+'\\'+file_path
                
                subprocess.Popen(command)
                return Response(status=200)
            except Exception as e:
                print("error",e)
                return Response(status=500)
        
        
        
        @app.route('/get_record')
        def get_record():
            return send_file('records/Recordcam111_11_2022_15_02_10.avi')
            
        
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
            
        @app.route("/delete/camera/<camera_id>",methods=["DELETE"])
        @cross_origin()
        def delete_camera(camera_id):
            try:
                self.db_helper.delete_camera(camera_id)
                for camera in self.cam_buffer:
                    if camera.id == camera_id:
                        camera.stop_camera()
                        self.cam_buffer.remove(camera)
                        break
                return Response(status=200)
            except Exception as e:
                print(e)
                return Response(status=500)

        @app.route("/get/intrusions",methods = ["GET"])
        @cross_origin()
        def get_all_intrusions():
            try:
                data =  self.db_helper.get_all_intrusion_data()
                return jsonify(data=data)
            except Exception as e:
                print(e)
                return Response(500)
            
            

        
        app.run(port='5000',host='0.0.0.0')
    
    
    