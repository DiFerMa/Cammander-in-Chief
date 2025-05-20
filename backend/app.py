from flask import Flask, Response, render_template_string
import cv2

app = Flask(__name__)

camera_paths = [
    '/dev/video2',  # external cam
    '/dev/video0',  # integrated cam
]

# Open each camera
cameras = [cv2.VideoCapture(path) for path in camera_paths]

# Route: Homepage - lists camera links
@app.route('/')
def index():
    links_html = ''.join(
        f'<li><a href="/camera/{i}">Camera {i}</a></li>'
        for i in range(len(cameras))
    )
    return render_template_string(f'''
        <html>
            <head><title>Cammander-in-Chief</title></head>
            <body>
                <h1>Camera Dashboard</h1>
                <ul>{links_html}</ul>
            </body>
        </html>
    ''')

# Route: Live camera feed for browser <img src="">
@app.route('/video_feed/<int:camera_index>')
def video_feed(camera_index):
    def generate_frames():
        cap = cameras[camera_index]
        while True:
            success, frame = cap.read()
            if not success:
                break
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Route: Camera viewing page (shows stream)
@app.route('/camera/<int:camera_index>')
def camera_page(camera_index):
    if 0 <= camera_index < len(cameras):
        return render_template_string(f'''
            <html>
                <head><title>Camera {camera_index}</title></head>
                <body>
                    <h1>Camera {camera_index}</h1>
                    <img src="/video_feed/{camera_index}" width="640" />
                    <br><br><a href="/">← Back to index</a>
                </body>
            </html>
        ''')
    return 'Camera not found', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
