from flask import Flask, render_template, Response, request, redirect, url_for
from pytapo import Tapo
import cv2
import time

# --------------------
# CONFIGURATION
# --------------------

TAPO_IP = "192.168.178.51"         # Replace with your camera IP
CAMERA_USER = "c51a_camera"             # Camera Account username (from RTSP setup)
CAMERA_PASSWORD = "123456"  # Camera Account password

RTSP_URL = f"rtsp://{CAMERA_USER}:{CAMERA_PASSWORD}@{TAPO_IP}:554/stream1"

# --------------------
# INIT
# --------------------

app = Flask(__name__)
camera = Tapo(TAPO_IP, CAMERA_USER, CAMERA_PASSWORD)

# --------------------
# STREAM
# --------------------

def generate_frames():
    cap = cv2.VideoCapture(RTSP_URL)
    while True:
        success, frame = cap.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

# --------------------
# CONTROL
# --------------------

@app.route("/move/<direction>")
def move(direction):
    if direction == "left":
        camera.move_motor(horizontal=-0.5, vertical=0)
    elif direction == "right":
        camera.move_motor(horizontal=0.5, vertical=0)
    elif direction == "up":
        camera.move_motor(horizontal=0, vertical=-0.5)
    elif direction == "down":
        camera.move_motor(horizontal=0, vertical=0.5)
    return redirect(url_for("index"))

@app.route("/night/<mode>")
def night(mode):
    if mode in ["on", "off", "auto"]:
        camera.set_night_vision(mode)
    return redirect(url_for("index"))

# --------------------
# UI
# --------------------

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
