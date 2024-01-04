from flask import Flask, Response, render_template, jsonify
import cv2
import yaml
import os
from threading import Thread, Lock
import time
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG to get detailed logs
logger = logging.getLogger(__name__)  # Create a logger for your application

app = Flask(__name__)

# Load camera configurations from YAML file
def load_camera_configs(filename):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

# Adjust the path for config.yaml
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')
config = load_camera_configs(config_path)

# Initialize camera streams
camera_streams = {}
lock = Lock()

def init_camera_stream(url):
    logger.debug(f"Initializing camera stream: {url}")
    cap = cv2.VideoCapture(url)
    while not cap.isOpened():
        logger.info(f"Waiting for camera stream at {url}...")
        time.sleep(5)
        cap = cv2.VideoCapture(url)
    return cap

def maintain_camera_stream(camera_id, url):
    global camera_streams
    try:
        while True:
            with lock:
                if not camera_streams[camera_id].isOpened():
                    camera_streams[camera_id] = init_camera_stream(url)
            time.sleep(10)
    except Exception as e:
        logger.exception(f"Exception in maintain_camera_stream for camera {camera_id}: {e}")


for cam in config['cameras']:
    logger.info(f"Starting stream for camera: {cam['id']}")
    stream = init_camera_stream(cam['url'])
    camera_streams[cam['id']] = stream
    t = Thread(target=maintain_camera_stream, args=(cam['id'], cam['url']))
    t.daemon = True
    t.start()

def generate_frame(camera_id):
    frame_interval = 1 / 10  # Limit to 10 frames per second
    last_time = time.time()

    while True:
        try:
            current_time = time.time()
            if current_time - last_time < frame_interval:
                continue

            with lock:
                success, frame = camera_streams[camera_id].read()
                if not success:
                    logger.debug(f"No frame read from camera {camera_id}")
                    time.sleep(0.1)
                    continue
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            last_time = time.time()
        except Exception as e:
            logger.exception(f"Error generating frame for camera {camera_id}")

@app.route('/stream/<int:camera_id>')
def video_feed(camera_id):
    logger.info(f"Video feed requested for camera: {camera_id}")
    return Response(generate_frame(camera_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cameras')
def camera_list():
    logger.info("Camera list requested")
    camera_info = [{"id": cam["id"], "name": cam["name"]} for cam in config['cameras']]
    return jsonify(camera_info)

@app.route('/')
def index():
    logger.info("Index page requested")
    return render_template('index.html', cameras=config['cameras'])

def run():
    logger.info("Starting Flask app on host 0.0.0.0 at port 5000")
    app.run(host='0.0.0.0', port=5000, threaded=True)

# if __name__ == '__main__':
#     server_thread = Thread(target=run)
#     server_thread.daemon = True
#     server_thread.start()

if __name__ == '__main__':
    logger.info("Starting Flask app...")
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
