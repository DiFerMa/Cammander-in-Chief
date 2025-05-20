# 📹 Cammander-in-Chief – Flask Camera Streamer

This module serves a lightweight Flask web app that streams live video from multiple connected webcams (e.g., `/dev/video0`, `/dev/video1`, etc.). Each camera gets its own page, and the root (`/`) provides a simple index with links.

---

## 🔧 Requirements

Install the required Python packages:

```bash
pip install opencv-python flask
```

To check which cameras are available and working:

```bash
sudo apt install v4l-utils
v4l2-ctl --list-devices
```

---

## 🎥 How It Works

- Edit the `camera_paths` list in `backend/app.py` to include the paths to your webcams.
- Each camera gets its own page at `/camera/<index>` (e.g. `/camera/0`, `/camera/1`)
- The root path `/` shows a simple index with links to the individual feeds.

---

## 📄 Example Output

```bash
$ ls /dev/video*
/dev/video0  /dev/video1  /dev/video2  /dev/video3

$ v4l2-ctl --list-devices
BN100-WC: BN100-WC (usb-0000:00:14.0-3):
	/dev/video2
	/dev/video3
	/dev/media1

Integrated_Webcam_HD: Integrate (usb-0000:00:14.0-6):
	/dev/video0
	/dev/video1
	/dev/media0
```

In this case:

- `/dev/video2` and `/dev/video3` are from an **external USB webcam**
- `/dev/video0` and `/dev/video1` are from the **integrated laptop webcam**

---

## 🧪 Run the App

If using a virtual environment and `make`, you can use:

```bash
make flask-start
```

Or run it manually:

```bash
python backend/app.py
```

Then visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🔍 Notes

- Some cameras may have multiple video interfaces (e.g., `/dev/video2`, `/dev/video3`) — test each.
- If a camera feed is slow or delayed, try running fewer streams at once.
- This app uses `multipart/x-mixed-replace` for streaming — compatible with most modern browsers.

---

Feel free to modify the HTML template or integrate a nicer frontend later.
