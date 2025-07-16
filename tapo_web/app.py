from flask import Flask, render_template, Response, redirect, url_for
import cv2
from pytapo import Tapo
import time

# --------------------
# CONFIGURATION
# --------------------

# nodam55911@coderdir.com
# =Gabyhalo45

TAPO_IP = "192.168.178.51"         # Replace with your camera IP
CAMERA_USER = "tapoc51a"             # Camera Account username (from RTSP setup)
#CAMERA_USER = "tapoc500"             # Camera Account username (from RTSP setup)

CAMERA_PASSWORD = "=Gabyhalo45"  # Camera Account password 123456

RTSP_URL = f"rtsp://{CAMERA_USER}:{CAMERA_PASSWORD}@{TAPO_IP}:554/stream1"
print ("RTSP_URL: "+RTSP_URL)
# --------------------
# INIT
# --------------------

app = Flask(__name__)
tapo = Tapo(TAPO_IP, CAMERA_USER, CAMERA_PASSWORD)

# --------------------
# VIDEO STREAM
# --------------------

def generate_frames():
    cap = cv2.VideoCapture(RTSP_URL)
    while True:
        success, frame = cap.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# --------------------
# PAN / TILT
# --------------------

@app.route("/move/<direction>")
def move(direction):
    if direction == "up":
        tapo.moveMotor(0, 50)
    elif direction == "down":
        tapo.moveMotor(0, -50)
    elif direction == "left":
        tapo.moveMotor(-50, 0)
    elif direction == "right":
        tapo.moveMotor(50, 0)
    return redirect(url_for("index"))

# --------------------
# NIGHT VISION
# --------------------

@app.route("/night/<mode>")
def night(mode):
    if mode in ["on", "off", "auto"]:
        try:
            tapo.setDayNightMode(mode)
            print(f"✅ Night vision set to {mode}")
        except Exception as e:
            print(f"❌ Failed to set night vision: {e}")
    else:
        print("❌ Invalid mode requested")
    return redirect(url_for("index"))

# --------------------
# UI
# --------------------

@app.route("/")
def index():
    try:
        night_mode = tapo.getDayNightMode()
    except Exception:
        night_mode = "unknown"
    return render_template("index.html", night_mode=night_mode)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
