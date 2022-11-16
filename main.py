from flask_api import flask_api
from camera import Camera
from web_connector_api import web_connector
from db_helper import DbHelper


if __name__ == '__main__':
    # creating the db helper object to get the functions of the database.
    db_helper = DbHelper()
    
    
    # starting the cameras.
    frame_buffer = {}
    camera1 = Camera("cam1",frame_buffer,0,db_helper)
    camera1.start()
    camera1.set_detectBool(True)


    # camera2 = Camera("cam2",frame_buffer,'http://10.10.30.209:4747/video',db_cursor,db_connection)
    # camera2.start()
    # camera2.set_detectBool(True)

    # camera_buffer = [camera1,camera2]
    camera_buffer = [camera1]

    # starting the web connector with azure.
    web_connector_thread = web_connector(camera_buffer)
    web_connector_thread.start()

    # starting the flask api which is used to pass the data to front end.
    flask_thread = flask_api(frame_buffer,camera_buffer)
    flask_thread.start()
    
    




