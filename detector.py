import cv2
import numpy as np
from datetime import datetime

cap = cv2.VideoCapture(0) #set the input here
whT = 320
confThreshold =0.5
nmsThreshold= 0.2


classes = ["person"]
modelConfiguration = 'yolov3.cfg'
modelWeights = 'yolov3.weights'


net = cv2.dnn.readNetFromDarknet(modelConfiguration,modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


def findObjects(outputs,img):
    hT, wT, cT = img.shape
    bbox = []
    classIds = []
    confs = []
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                w,h = int(det[2]*wT) , int(det[3]*hT)
                x,y = int((det[0]*wT)-w/2) , int((det[1]*hT)-h/2)
                bbox.append([x,y,w,h])
                classIds.append(classId)
                confs.append(float(confidence))
 
    indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)
    
    
    humanDetected = False
    for i in indices:
        
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        # print(x,y,w,h)
        cv2.rectangle(img, (x, y), (x+w,y+h), (255, 0 , 255), 2)
        try:
            cv2.putText(img,f'{classes[classIds[i]].upper()} {int(confs[i]*100)}%',
                    (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
            print("humans detected!")
            humanDetected = True
        except:
            print("nothing detected!")
    return humanDetected

def notify(frames):
    print("generating a video from the frames")
  
    out = cv2.VideoWriter('suspect.avi',cv2.VideoWriter_fourcc(*'XVID'),20,(640,480))
    for frame in frames:
        out.write(frame)

        
    out.release()
    print("video saved!")    


while True:
    success, img = cap.read()
    
    blob = cv2.dnn.blobFromImage(img,1/255,(whT,whT),[0,0,0],1,crop=False)
    net.setInput(blob)
    
    layerNames = net.getLayerNames()
    outputNames = [(layerNames[i - 1]) for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(outputNames)
    humanDetected = findObjects(outputs,img)
    
    if humanDetected:
        print("human detected. starting saving a clip...")
        startTime = datetime.now()
        timeDifference = 0
        frameCollection = []
        while timeDifference < 10:
            presentTime = datetime.now()
            timeDifference = (presentTime - startTime).total_seconds()
            print("frame saving : time difference",timeDifference)
            
            success, img = cap.read()
    
            frameCollection.append(img)
            cv2.imshow('Image', img)
            key = cv2.waitKey(1)
            
        notify(frameCollection)
        break
            
            
 
    cv2.imshow('Image', img)
    key = cv2.waitKey(1)
    
    # this is for terminating the program
    if key == ord("q"):
        break

