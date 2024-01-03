# RTSP Viewer
Multiple RTSP stream viewer

# Backend
## Overview
RTSP Stream Viewer is a web application designed to aggregate and display video feeds from multiple RTSP cameras. Built using Flask, the app provides a simple yet effective way to monitor multiple video streams in real-time through a web interface. The application is configured to handle RTSP streams gracefully, ensuring stability and continuous access to the video feeds.

## Features
- **Multi-Camera Support**: Configure multiple RTSP streams through a YAML file.
- **Real-Time Streaming**: View real-time video feeds from each configured camera.
- **Graceful Stream Handling**: Automatically reconnects to streams if they become unavailable.
- **Easy Configuration**: Set up camera URLs and identifiers through a simple YAML configuration.
- **Thread-Safe Stream Processing**: Ensures safe and consistent access to camera streams.
- **Web-Based Interface**: Access your camera streams through any standard web browser.

## Installation

### Prerequisites
- Python 3.x
- Flask
- OpenCV-Python
- PyYAML

### Setup Instructions
1. Clone the repository to your local machine.
2. Install the required Python packages: `Flask`, `opencv-python`, and `pyyaml`.
3. Create a `cameras.yaml` file in the root directory of the project with the structure:

   ```yaml
   cameras:
     - id: "camera1"
       url: "rtsp://your_camera_stream_url"
     - id: "camera2"
       url: "rtsp://your_second_camera_stream_url"

## Running
Run app.py to start the Flask server.

## Usage
Navigate to http://localhost:5000 in your web browser to view the camera streams. Each camera's stream can be accessed via the route /video_feed/<camera_id>, where camera_id is the identifier of a specific camera as configured in cameras.yaml.

## Deployment
For production deployment, consider using a production-grade WSGI server like Gunicorn and a reverse proxy like Nginx.

# Frontend