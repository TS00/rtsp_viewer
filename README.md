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
Install python3 and pip3 if not already installed.
pip3 install -r requirements.txt
flask run

### Prerequisites
- Python 3.x
- Flask
- OpenCV-Python
- PyYAML

### Setup Instructions
1. Clone the repository to your local machine.
2. Install the required Python packages: `Flask`, `opencv-python`, and `pyyaml`.
3. Update the `config.yaml` file in the root directory of the project with your camera URLs and identifiers.

## Running
Run app.py to start the Flask server.

## Usage
Navigate to http://localhost:5000 in your web browser to view the camera streams. Each camera's stream can be accessed via the route /video_feed/<camera_id>, where camera_id is the identifier of a specific camera as configured in cameras.yaml.

## Frontend
Super-simple html, css, js frontend. No frameworks, no build tools, no nothing. Index.html, script.js, style.css. That's it. They are served up by the flask server.

## Deployment with Gunicorn
Gunicorn is a Python WSGI HTTP Server that is a robust and efficient way to deploy your Flask application. Follow these steps to deploy your application using Gunicorn.

### Prerequisites
Make sure you have Gunicorn installed in your virtual environment. If you haven't installed it yet, you can install it using pip:

pip install gunicorn

Your application should be tested and working correctly using Flask's development server before proceeding with deployment using Gunicorn.

### Deploying the Application
Start the Application with Gunicorn:

Navigate to the root directory of your application and run the following command:

gunicorn --workers 3 --bind 0.0.0.0:5000 app:app

Replace app:app with <module>:<application>, where <module> is the Python file that contains your Flask application instance and <application> is the Flask app variable.

The --workers option allows you to specify the number of worker processes. Adjust this number based on your workload and server capabilities.

### Accessing the Application
Once Gunicorn is running, your Flask application should be accessible at http://<server-ip>:5000, where <server-ip> is the IP address of the server running Gunicorn.

### Running Gunicorn as a System Service
For a more robust deployment, you can run Gunicorn as a system service, which allows the application to start automatically on boot and restart if it crashes.

Create a Systemd Service File:
Create a new systemd service file for your application:

sudo nano /etc/systemd/system/myapp.service

Replace myapp with a name of your choice for the service. Inside the file, add the following content:


[Unit]
Description=Gunicorn instance to serve myapp
After=network.target

[Service]
User=<your-user>
Group=www-data
WorkingDirectory=/path/to/your/app
Environment="PATH=/path/to/your/venv/bin"
ExecStart=/path/to/your/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 module:app

[Install]
WantedBy=multi-user.target
Replace <your-user>, /path/to/your/app, and module:app with your username, application directory, and module name, respectively.

Start and Enable the Service:

Start the service and enable it to launch on boot:

sudo systemctl start myapp.service
sudo systemctl enable myapp.service
Replace myapp.service with the name of your service file.

Checking the Service Status:

To check the status of your service:

sudo systemctl status myapp.service
Replace myapp.service with the name of your service file.

