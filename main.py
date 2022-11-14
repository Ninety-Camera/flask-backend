from flask_api import flask_api
from camera import Camera
from web_connector_api import web_connector


if __name__ == '__main__':
    
    
    frame_buffer = {}
    camera1 = Camera("cam1",frame_buffer,0)
    camera1.start()
    camera1.set_detectBool(True)


    # camera2 = Camera("cam2",frame_buffer,'http://10.10.30.209:4747/video')
    # camera2.start()
    # camera2.set_detectBool(True)

    # camera_buffer = [camera1,camera2]
    camera_buffer = [camera1]

    web_connector_thread = web_connector(camera_buffer)
    web_connector_thread.start()

    flask_thread = flask_api(frame_buffer,camera_buffer)
    flask_thread.start()
    
    




