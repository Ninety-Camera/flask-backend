# flask-backend

## Before run

### 1. Please download yolo3.weights file using this link. 
https://pjreddie.com/media/files/yolov3-tiny.weights
This file uses for the detection part.

### 2. Install following python packages.

pip install azure-storage-blob azure-identity

pip install python-dotenv

pip install Flask

pip install python-socketio

pip install opencv-python

### 3. Create following files.
* create a .env file and insert, AZURE_STORAGE_CONNECTION_STRING = 'connection string'

* create a folder intrusion_images

* create a folder intrusion_videos

## Purpose
This repo contains human detection part using python. 


## Functions 
### 1. camera
* detecting humans
* recording the footages
* saving the intrusion video with three screenshots.
* sending the intrusion videoa and the ss to server.

### 2. flask api
* Connecting the backend to the front end.
* sending the readed frames from the camera to front end.

### 3. uploader
* uploading the given files to azure server. 
* In this we are sending intrusion videos and the screenshots to the server when detected.

### 4. web connector api
* connected to web server which will help to communicate with the mobile app users.
* when intrusion detected notification will be send and the web connector will change the intrusion mode when mobile users changed it.

### 5. db helper
* connecting the mysql lite 3 database with the application and performing value insertion functions to the database.
* when we need save the videos and images in the database we are saving the path for the object.
