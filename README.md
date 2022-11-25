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

pip install flask-cors

### 3. Create following files.
* create a .env file and insert, AZURE_STORAGE_CONNECTION_STRING = 'connection string'

* create a folder intrusion_images

* create a folder intrusion_videos

* create a folder records

## Purpose
Connecting to front end of the desktop application and recieve and data with server and front end.


## Functions 
### 1. camera
* detecting humans.
* recording the footages.
* saving the intrusion video with three screenshots.
* sending the intrusion videos and the ss to server.

### 2. flask api
* Connecting the backend to the front end.
* sending the readed frames from the camera to front end.
* adding the cameras to the system when requets comes from the front end.
* sending the intrusion images.
* sending all intrusion id s.
* opening and playing the intrusion videos.
* sending the record id s.
* opening the records and playing them using the requested id.
* adding the user to database. (in our system we are only having one user for the desktop application.)
* sending the user details.
* delete the user details.


### 3. uploader
* uploading the given files to azure server. 
* In this we are sending intrusion videos and the screenshots to the server when detected.

### 4. web connector api
* connected to web server which will help to communicate with the mobile app users.
* when intrusion detected notification will be send and the web connector will change the intrusion mode when mobile users changed it.

### 5. db helper
* connecting the mysql lite 3 database with the application and performing value create, insert, select, upadate, delete functions to the database.
* Mainly db having 4 tables. They are,
    * Camera - camera_id, camera_name, is_ip_camera, camera_link
    * Intrusion - intrusion_id, video_path, image1_path, image2_path, image3_path, date_time
    * Record - record_id, video_path, date_time
    * User_data - email, user_id, role, token, first_name, last_name
* Adding functions.
    * add intrusion.
    * add record video
    * add user data.
    * add camera.
* Getting functions.
    * get token.
    * get one intrusion data.
    * get all intrusion data.
    * get all intrusion id s.
    * get intrusion image.
    * get intrusion video.
    * get record id s.
    * get record video.
    * get user details.
    * get camera details.
* Update functions.
    * update user token.
* Delete functions.
    * delete user data.
    * delete camera.
