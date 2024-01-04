from flask import Flask, Response, render_template, jsonify
import cv2
import yaml
import os
from threading import Thread, Lock
import time

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
    cap = cv2.VideoCapture(url)
    while not cap.isOpened():
        print(f"Waiting for camera stream at {url}...")
        time.sleep(5)
        cap = cv2.VideoCapture(url)
    return cap

def maintain_camera_stream(camera_id, url):
    global camera_streams
    while True:
        with lock:
            if not camera_streams[camera_id].isOpened():
                camera_streams[camera_id] = init_camera_stream(url)
        time.sleep(10)

for cam in config['cameras']:
    stream = init_camera_stream(cam['url'])
    camera_streams[cam['id']] = stream
    t = Thread(target=maintain_camera_stream, args=(cam['id'], cam['url']))
    t.daemon = True
    t.start()

def generate_frame(camera_id):
    while True:
        with lock:
            success, frame = camera_streams[camera_id].read()
            if not success:
                time.sleep(0.1)
                continue
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/stream/<int:camera_id>')
def video_feed(camera_id):
    return Response(generate_frame(camera_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cameras')
def camera_list():
    # Extracting just the id and name from each camera in the configuration
    camera_info = [{"id": cam["id"], "name": cam["name"]} for cam in config['cameras']]
    return jsonify(camera_info)

@app.route('/')
def index():
    return render_template('index.html', cameras=config['cameras'])

def run():
    app.run(host='0.0.0.0', port=5000, threaded=True)

if __name__ == '__main__':
    server_thread = Thread(target=run)
    server_thread.daemon = True
    server_thread.start()
