import cv2
import numpy as np
from datetime import datetime, timedelta
import threading




class detectThread(threading.Thread):
    
    def __init__(self, name,buffer,link):
        threading.Thread.__init__(self)
        self.name = name
        self.buffer = buffer
        self.link = link
        self.recorder_frames = []
        
        recording_thred = threading.Thread(target=self.record,name="recorder")
        recording_thred.start()
        
        self.cap = cv2.VideoCapture(self.link) #set the input here

        self.whT = 320 # width and height of the video
        self.confThreshold =0.5
        self.nmsThreshold= 0.2

        self.classes = ["person"] # since we are only detecting humans classes contains only person.
        self.modelConfiguration = 'yolov3.cfg' # directory of the yolo config file.
        self.modelWeights = 'yolov3.weights' # directory of the yolo weight file.


        self.net = cv2.dnn.readNetFromDarknet(self.modelConfiguration,self.modelWeights)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        
        self.detectBool = False # intrution detection boolean
        print("Detecting thread initiated")
        
    def run(self):
        self.detect()
    
    def get_id(self):
 
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
            
    def raise_exception(self):
        # thread_id = self.get_id()
        # res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
        #       ctypes.py_object(SystemExit))
        # if res > 1:
        #     ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
        #     print('Exception raise failure')
        
        raise ValueError
    
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
        
        while True:
            success, img = self.cap.read()
            
            if not success:
                continue
            self.buffer[self.name] = img
            self.recorder_frames.append(img)
        
            if self.detectBool or instrution_clip_collecting:
            
                blob = cv2.dnn.blobFromImage(img,1/255,(self.whT,self.whT),[0,0,0],1,crop=False)
                self.net.setInput(blob)
                
                layerNames = self.net.getLayerNames()
                outputNames = [(layerNames[i - 1]) for i in self.net.getUnconnectedOutLayers()]
                outputs = self.net.forward(outputNames)
                humanDetected = self.findHumans(outputs,img)
                
                if instrution_clip_collecting:
                    present_instrution_clip_time = datetime.now() - last_detection_time
                    if present_instrution_clip_time.total_seconds() >instrution_clip_time:
                        filename = "instrution videos\suspect "+last_detection_time.strftime("%m_%d_%Y_%H_%M_%S")+".avi" 
    
                        #initializing a thread for saving suspect frames into video.    
                        videoGeneratingThread = threading.Thread(target=self.generateVideo,name="suspect-videoGenerator",args=(instrution_frame_collection,filename))
                        videoGeneratingThread.start()
                        
                        instrution_clip_collecting = False
                    else:
                        instrution_frame_collection.append(img)
                        
                elif humanDetected and (datetime.now()-last_detection_time).total_seconds()>instrusion_clip_gap:
                    print("Instrution detected. Saving a clip from now.")
                    instrution_frame_collection = [img]
                    instrution_clip_collecting = True
                    last_detection_time = datetime.now()
            
                

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
    
    def record(self):
        print("recorder started")
        recording_gap = 60 # recording clip set to 30 minutes.
        time_started = datetime.now()
        while True:
            present_time = datetime.now()
            time_delta = (present_time - time_started).total_seconds()
            if time_delta >= recording_gap:
                print("saving the recorded clip.")
                filename = "records\Record"+self.name+time_started.strftime("%m_%d_%Y_%H_%M_%S")+".avi" 
                videoGeneratingThread = threading.Thread(target=self.generateVideo,name="record-videoGenerator",args=(self.recorder_frames,filename ))
                videoGeneratingThread.start()
                time_started = present_time
                self.recorder_frames = []
        
        

    # This function will generate a video using input frame list.
    def generateVideo(self,frames,filename):
        print("generating a video from the frames")
    
        out = cv2.VideoWriter(filename,cv2.VideoWriter_fourcc(*'XVID'),5,(640,480))
        for frame in frames:
            out.write(frame)

            
        out.release()
        print("video saved!",filename)    


        
    