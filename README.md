# flask-backend

## Before run

### 1. Please download yolo3.weights file using this link. 
https://pjreddie.com/media/files/yolov3.weights
This file uses for the detection part.

### 2. Install following python packages.

pip install azure-storage-blob azure-identity

pip install python-dotenv

### 3. Create following files.
create a .env file and insert, AZURE_STORAGE_CONNECTION_STRING = 'connection string'

## Purpose
This repo contains human detection part using python. 


## Functions 
Algorithm will recieve footages from a camera input and it will analyze it frame by frame, then it will detect the humans. 
After detecting save a small clip to send the users of the system and there will be some screenshots too.
