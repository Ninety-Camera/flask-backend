import cv2
import numpy as np
from datetime import datetime, timedelta
import threading
from uploder import upload_to_blob_storage,upload_video
import requests




class Camera(threading.Thread):
    
    def __init__(self, name,id,buffer,link,db_helper):
        threading.Thread.__init__(self)
        self.name = name
        self.id = id
        self.buffer = buffer
        self.link = link
        self.db_helper = db_helper
        self.recorder_frames = []
        
        # starting the recording in the camera.
        recording_thred = threading.Thread(target=self.record,name="recorder")
        recording_thred.start()
        
        self.cap = cv2.VideoCapture(self.link) #set the input here

        self.whT = 320 # width and height of the video
        self.confThreshold =0.5
        self.nmsThreshold= 0.2

        self.classes = ["person"] # since we are only detecting humans classes contains only person.
        self.modelConfiguration = 'yolov3.cfg' # directory of the yolo config file.
        self.modelWeights = 'yolov3-tiny.weights' # directory of the yolo weight file.


        self.net = cv2.dnn.readNetFromDarknet(self.modelConfiguration,self.modelWeights)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        
        self.detectBool = False # intrution detection boolean
        self.buffer[self.id] = cv2.imread('public/loading.png') # setting the first frame as loading.
        self.running = True
        print(self.name,"camera initiated.")
        
    def run(self):
        self.detect()
    
    # function to stop the camera.
    def stop_camera(self):
        self.running =  False
    
    # function to change the value of the detect_bool
    def set_detectBool(self,bool):
        self.detectBool = bool
        print("Detection mode changed....")
            
    # This is the function which capture the frames from the input and output the moderated frame.
    def detect(self):
        last_detection_time = datetime.now() - timedelta(minutes=16) # pre last detection time. This will take care of sending instrution alearts nearly.
        instrution_clip_time = 15 # seconds
        instrution_frame_collection = [] # instrution frame collection when human detected.
        instrution_clip_collecting = False # boolean value to check, generating the instrution clip.
        instrusion_clip_gap = 60*15 # Gap between instrution alerts.(seconds)
        
        last_frame_checked = datetime.now() - timedelta(seconds=5)
        while self.running:
            success, img = self.cap.read()
            
            if not success:
                continue
            self.buffer[self.id] = img
            self.recorder_frames.append(img)
            frame_check_time_difference = (datetime.now()-last_frame_checked).total_seconds()
            
            
        
            if (self.detectBool or instrution_clip_collecting) and frame_check_time_difference>5:
            
                blob = cv2.dnn.blobFromImage(img,1/255,(self.whT,self.whT),[0,0,0],1,crop=False)
                self.net.setInput(blob)
                
                layerNames = self.net.getLayerNames()
                outputNames = [(layerNames[i - 1]) for i in self.net.getUnconnectedOutLayers()]
                outputs = self.net.forward(outputNames)
                humanDetected = self.findHumans(outputs,img)
                
                if instrution_clip_collecting:
                    present_instrution_clip_time = datetime.now() - last_detection_time
                    if present_instrution_clip_time.total_seconds() >instrution_clip_time:
                        filename = "intrusion_videos\suspect "+last_detection_time.strftime("%m_%d_%Y_%H_%M_%S")+".mp4" 
    
                        #initializing a thread for saving suspect frames into video.    
                        videoGeneratingThread = threading.Thread(target=self.generateVideo,name="suspect-videoGenerator",args=(instrution_frame_collection,filename,True))
                        videoGeneratingThread.start()
                        
                        instrution_clip_collecting = False
                    else:
                        instrution_frame_collection.append(img)
                        
                elif humanDetected and (datetime.now()-last_detection_time).total_seconds()>instrusion_clip_gap:
                    print("Intrution detected. Saving a clip from now.")
                    instrution_frame_collection = [img]
                    instrution_clip_collecting = True
                    last_detection_time = datetime.now()
            
            elif instrution_clip_collecting:
                instrution_frame_collection.append(img)
            
            if frame_check_time_difference>5:
                last_frame_checked = datetime.now()

            cv2.imshow('Image', img)
            key = cv2.waitKey(1)
            
            # this is for terminating the program
            if key == ord("q"):
                break



                



    # This function will identify humans and draw a rectangle around the object.
    # returning boolean input frame contains a human or not. True for a human.
    def findHumans(self,outputs,img):
        hT, wT, cT = img.shape
        bbox = []
        classIds = []
        confs = []
        for output in outputs:
            for det in output:
                scores = det[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.confThreshold:
                    w,h = int(det[2]*wT) , int(det[3]*hT)
                    x,y = int((det[0]*wT)-w/2) , int((det[1]*hT)-h/2)
                    bbox.append([x,y,w,h])
                    classIds.append(classId)
                    confs.append(float(confidence))
    
        indices = cv2.dnn.NMSBoxes(bbox, confs, self.confThreshold, self.nmsThreshold)
        
        
        humanDetected = False
        for i in indices:
            
            box = bbox[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            cv2.rectangle(img, (x, y), (x+w,y+h), (255, 0 , 255), 2)
            
            try:
                cv2.putText(img,f'{self.classes[classIds[i]].upper()} {int(confs[i]*100)}%',
                        (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
                # print("humans detected!")
                humanDetected = True
            except:
                # print("nothing detected!")
                pass
                
        return humanDetected
    
    # function to do the recording part. We can change the recording gap parameter and set recording clip duration.
    def record(self):
        print("recorder started")
        recording_gap = 60*30 # recording clip set to 30 minutes.
        time_started = datetime.now()
        while True:
            present_time = datetime.now()
            time_delta = (present_time - time_started).total_seconds()
            if time_delta >= recording_gap:
                print("saving the recorded clip.")
                filename = "records\Record"+self.name+time_started.strftime("%m_%d_%Y_%H_%M_%S")+".mp4" 
                videoGeneratingThread = threading.Thread(target=self.generateVideo,name="record-videoGenerator",args=(self.recorder_frames,filename ))
                videoGeneratingThread.start()
                time_started = present_time
                self.recorder_frames = []
        
        

    # This function will generate a video using input frame list.
    def generateVideo(self,frames,filename,intrusion=False):
        datetime_now = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        if intrusion:
            print("saving intrusion screen shots.")
            # sending the request
            token = self.db_helper.get_token()
            header = {"Content-Type": "application/json; charset=utf-8",'Authorization':token}

            req = requests.post('https://ninetycamera.azurewebsites.net/api/intrusion/add',json={"systemId":"55d60bd7-4a39-4bfc-ac08-40e290444c2e"},headers=header)
            # response = req.json()['data']['intrusion']
            response = req.json()
            print(response)
            intrusion_id = response['data']['intrusion']['id']
            # print(response)
            
            # saving suspect images.
            suspect_photo_paths = []
            display_photo_paths = []
            
            for i in range(3):
                image_name = intrusion_id+datetime_now+str(i)+'.png'
                supecpect_photo = cv2.imwrite('intrusion_images/'+image_name,frames[i])
                suspect_photo_paths.append('intrusion_images/'+image_name)
                display_photo_paths.append(intrusion_id+'/'+image_name)
            
            image_link_list = upload_to_blob_storage(suspect_photo_paths,display_photo_paths)
            req = requests.post('https://ninetycamera.azurewebsites.net/api/intrusion/image',json={"intrusionId":intrusion_id,'images':image_link_list},headers=header)
            print(image_link_list)
        
        print("generating a video from the frames")
        out = cv2.VideoWriter(filename,cv2.VideoWriter_fourcc(*'mp4v'),10,(640,480))
        for frame in frames:
            out.write(frame)

            
        out.release()
        
        if intrusion:
            #sending the video to database
            video_link = upload_video(filename,intrusion_id+"/"+datetime_now+".mp4")
            req = requests.post('https://ninetycamera.azurewebsites.net/api/intrusion/video',json={"intrusionId":intrusion_id,'video':video_link},headers=header)
            # adding the intrusion to db.
            self.db_helper.add_intrusion(intrusion_id,filename,suspect_photo_paths[0],suspect_photo_paths[1],suspect_photo_paths[2],datetime.now().isoformat())
            
        else:
            self.db_helper.add_record_video(filename,datetime.now().isoformat()) # adding the record to db.
        
        
        

                
        
            


        
    