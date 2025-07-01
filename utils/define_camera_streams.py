import cv2

print("Testing available /dev/video* devices...\n")

"""
INFO:
Each USB camera may expose multiple device nodes under /dev/video*.

Examples:
- /dev/video0: actual video stream
- /dev/video1: metadata stream or alternate format (e.g. MJPEG/YUYV)
- /dev/video2: still image or unused function

This script identifies working video streams among all listed video devices.

Use the outputs to define the correct camera paths in app.py.

"""

for i in range(0, 18):  # check /dev/video0 to /dev/video9
    cap = cv2.VideoCapture(i)
    if cap is None or not cap.isOpened():
        print(f"/dev/video{i} Not useful")
    else:
        ret, frame = cap.read()
        if ret:
            print(f"/dev/video{i} Working fine")
        else:
            print(f"/dev/video{i} Opened but no frame captured")
        cap.release()