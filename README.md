# RTSP Viewer

RTSP Viewer is a web application designed for aggregating and displaying video feeds from multiple RTSP cameras. Built using Flask, this app offers a simple, effective solution for real-time monitoring through a web interface.

## Features

- **Multi-Camera Support**: Configure and view multiple RTSP streams.
- **Real-Time Streaming**: Watch live video feeds from each camera.
- **Graceful Stream Handling**: Automatically reconnects to streams.
- **Easy Configuration**: Easy setup through a YAML file.
- **Thread-Safe Stream Processing**: Safe and consistent stream access.
- **Web-Based Interface**: View streams in any standard web browser.

## Installation

### Prerequisites

Ensure you have the following prerequisites installed:
- Python 3.x
- Flask
- OpenCV-Python
- PyYAML

### Setup Instructions

- Clone the repository: `git clone https://github.com/TS00/rtsp_viewer.git`
- Navigate to the project directory: `cd rtsp-viewer`
- Install dependencies: `pip3 install -r requirements.txt`
- Update `config.yaml` with your camera URLs and identifiers.

## Running the Application

To start the Flask server, run: `python app.py`
Then, open a web browser and navigate to `http://localhost:5000` to view the streams.

## Frontend

The frontend consists of simple HTML, CSS, and JavaScript files, served by the Flask server.

## Deployment with Gunicorn

### Prerequisites

Before deploying with Gunicorn, make sure it is installed in your virtual environment: `pip install gunicorn`

### Deploying with Gunicorn

To start Gunicorn in the project directory, use: `gunicorn --workers 3 --bind 0.0.0.0:5000 app:app`
Replace `app:app` with your module and application name. The application will be accessible at `http://<server-ip>:5000`.

### Running Gunicorn as a System Service

#### Creating a Systemd Service

- Create a systemd service file: `sudo nano /etc/systemd/system/myapp.service`
- Populate the file with the following:
  ```
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
  ```
  Update the placeholders to match your configuration.

#### Managing the Service

- To start the service: `sudo systemctl start myapp.service`
- To enable auto-start on boot: `sudo systemctl enable myapp.service`
- To check the service status: `sudo systemctl status myapp.service`

Replace `myapp.service` with the name of your service file.
