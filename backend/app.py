from flask import Flask, Response, render_template_string
import cv2

app = Flask(__name__)

# Only working camera device paths
camera_paths = {
    "cam1": "/dev/video0",
    "cam2": "/dev/video2",
    "cam3": "/dev/video4",
}

def generate_frames(camera_path):
    cap = cv2.VideoCapture(camera_path)
    if not cap.isOpened():
        return  # Don't attempt to stream if camera fails to open

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Rotate 180° (cameras installed upside down)
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def home():
    return render_template_string('''
        <h1>📷 Cammander-in-Chief: Camera Dashboard</h1>
        <ul>
          <li><a href="/cam/cam1">View Flur</a></li>
          <li><a href="/cam/cam2">View Dinning room</a></li>
          <li><a href="/cam/cam3">View Balcon</a></li>
        </ul>
    ''')

@app.route('/cam/<cam_id>')
def camera_page(cam_id):
    if cam_id not in camera_paths:
        return f"Camera '{cam_id}' not found", 404
    return Response(generate_frames(camera_paths[cam_id]),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
