import cv2
from datetime import datetime
import threading

# This will record all the footages from the cameras.
def record():
    cap = cv2.VideoCapture(0)
    frameCollection = []
    timeDelta = 0
    startingTime = datetime.now()
    recordingTime = 5*60
    while True:
        timeDelta = (datetime.now() - startingTime).total_seconds()
        if timeDelta > recordingTime: # set to save five minutes clips
            filename = "records/clip "+startingTime.strftime("%m_%d_%Y_%H_%M_%S")+".avi"
            
            videoGeneratingThread = threading.Thread(target=generateVideo,name="videoGenerator",args=(frameCollection,filename))
            videoGeneratingThread.start()
            # generateVideo(frameCollection,filename)
            
            startingTime = datetime.now()
            frameCollection = []
            
        success,img = cap.read()
        if success:
            frameCollection.append(img)
            
            cv2.imshow('Image', img)
            key = cv2.waitKey(1)
        
        # this is for terminating the program
        if key == ord("q"):
            break
    
# This function will generate a video using input frame list.
def generateVideo(self,frames,filename):
    print("generating a video from the frames")

    out = cv2.VideoWriter(filename,cv2.VideoWriter_fourcc(*'XVID'),20,(640,480))
    for frame in frames:
        out.write(frame)

        
    out.release()
    print("video saved!")  