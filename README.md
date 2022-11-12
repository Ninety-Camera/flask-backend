# flask-backend

## Before run
Please download yolo3.weights file using this link. 
https://pjreddie.com/media/files/yolov3.weights
This file uses for the detection part.

since we are using azure data connections please install below module using following command.
pip install azure-storage-blob azure-identity

To get the dotenv module for the python run the below command.
pip install python-dotenv
## Purpose
This repo contains human detection part using python. 


## Functions 
Algorithm will recieve footages from a camera input and it will analyze it frame by frame, then it will detect the humans. 
After detecting save a small clip to send the users of the system and there will be some screenshots too.
