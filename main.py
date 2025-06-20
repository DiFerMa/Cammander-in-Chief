#!/usr/bin/env python3
import time
import subprocess
from gpiozero import LED, Button
from signal import pause

# GPIO setup
led1 = LED(17)  # Camera running
led2 = LED(27)  # Sleep
button = Button(23, pull_up=False, bounce_time=0.1)  # Corrected for pull-down

# Track the subprocess running Flask app
app_process = None

def start_cameras():
    global app_process
    if app_process is None:
        print("[INFO] Starting camera app...")
        app_process = subprocess.Popen(["python3", "backend/app.py"])
        led1.on()
        led2.off()

def stop_cameras():
    global app_process
    if app_process:
        print("[INFO] Stopping camera app...")
        app_process.terminate()
        app_process.wait()
        app_process = None
    led1.off()
    led2.on()

def restart_after_delay(delay_sec):
    stop_cameras()
    print(f"[INFO] Waiting {delay_sec} seconds before restart...")
    time.sleep(delay_sec)
    start_cameras()

def monitor_button():
    while True:
        button.wait_for_press()
        print("[INFO] Button pressed! Entering sleep mode for 1 hour.")
        restart_after_delay(3)  # 1 hour = 3600 sec

# Run startup
start_cameras()
monitor_button()  # Loop forever
