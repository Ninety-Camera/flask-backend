from flask_api import flask_api
from camera import Camera
from web_connector_api import web_connector
from db_helper import DbHelper


if __name__ == '__main__':
    # creating the db helper object to get the functions of the database.
    db_helper = DbHelper()
   
    
    # starting the cameras.
    frame_buffer = {}
    camera_buffer = []
    
    # starting the cameras.
    camera_details  = db_helper.get_camera_details()
    for one_camera_details in camera_details:
        id,name,is_ip,link = one_camera_details

        if is_ip == 1:
            camera = Camera(name,id,frame_buffer,link,db_helper)
        else:
            camera = Camera(name,id,frame_buffer,int(link),db_helper)
        camera.start()
        camera_buffer.append(camera)

    # starting the flask api which is used to pass the data to front end.
    flask_thread = flask_api(frame_buffer,camera_buffer,db_helper)
    flask_thread.start()
    
    
    
    




