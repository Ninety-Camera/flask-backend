from flask import Flask,Response,render_template
import cv2
from flask_cors import CORS, cross_origin


app = Flask(__name__)
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def index():
    # rendering webpage
    return render_template('index.html')

cap = cv2.VideoCapture('http://10.10.30.209:4747/video')

def gen():
    while True:
        #get camera frame
        sucess,frame = cap.read()
        # ret, jpeg = cv2.imencode('.jpg', frame)
        # image = jpeg.tobytes()
        # yield (b'--frame\r\n'
        #        b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n\r\n')
        cv2.imshow("Video",frame)
        cv2.waitKey(1)



if __name__ == '__main__':
    gen()