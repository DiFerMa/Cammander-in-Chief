from flask import Flask, Response, render_template_string, redirect, url_for
import cv2
import threading
import time
import requests

app = Flask(__name__)

# Working camera device paths
camera_paths = {
    "cam1": "/dev/video0",
    "cam2": "/dev/video2",
    "cam3": "/dev/video4",
}

# Shelly light bulb IP
SHELLY_IP = "http://192.168.178.45"
light_timer_thread = None
light_lock = threading.Lock()

def generate_frames(camera_path):
    cap = cv2.VideoCapture(camera_path)
    if not cap.isOpened():
        return
    # Set to best resolution and format
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    while True:
        success, frame = cap.read()
        if not success:
            break
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()

@app.route('/')
def home():
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cammander-in-Chief</title>
        <style>
            body {
                font-family: sans-serif;
                padding: 1em;
                max-width: 600px;
                margin: auto;
                line-height: 1.6;
            }
            h1 {
                font-size: 1.5em;
                text-align: center;
            }
            ul {
                padding-left: 0;
                list-style: none;
            }
            li {
                margin: 1em 0;
            }
            a.button {
                display: block;
                padding: 0.75em;
                background-color: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                text-align: center;
                font-size: 1.2em;
                margin-bottom: 10px;
            }
            a.button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <h1>📷 Cammander-in-Chief: Camera Dashboard</h1>
        <ul>
            <li><a class="button" href="/cam/cam1">View Flur</a></li>
            <li><a class="button" href="/cam/cam2">View Dinning room</a></li>
            <li><a class="button" href="/cam/cam3">View Balcon</a></li>
        </ul>
        <h2>💡 Light Control</h2>
        <a class="button" href="/light/on">Turn ON Light (Auto-off in 20 min)</a>
        <a class="button" href="/light/off">Turn OFF Light</a>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/cam/<cam_id>')
def camera_page(cam_id):
    if cam_id not in camera_paths:
        return f"Camera '{cam_id}' not found", 404
    return Response(generate_frames(camera_paths[cam_id]),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/light/on')
def light_on():
    try:
        requests.get(f"{SHELLY_IP}/light/0?turn=on", timeout=3)
        start_light_timer()
    except Exception as e:
        print(f"[ERROR] Failed to toggle light: {e}")

    return redirect(url_for('home'))

@app.route('/light/off')
def light_off():
    try:
        requests.get(f"{SHELLY_IP}/light/0?turn=off", timeout=3)
    except Exception as e:
        print(f"[ERROR] Failed to toggle light: {e}")

    return redirect(url_for('home'))

def start_light_timer():
    global light_timer_thread
    with light_lock:
        if light_timer_thread is not None and light_timer_thread.is_alive():
            return  # already counting down
        def timer():
            time.sleep(20 * 60)
            try:
                requests.get(f"{SHELLY_IP}/light/0?turn=off", timeout=3)
            except Exception as e:
                print(f"[ERROR] Failed to toggle light: {e}")

        light_timer_thread = threading.Thread(target=timer, daemon=True)
        light_timer_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
