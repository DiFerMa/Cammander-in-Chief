#!/usr/bin/env python3
import time
import subprocess
from gpiozero import LED, Button
import sys
from pathlib import Path

# GPIO setup
led1 = LED(17)  # Indicates cameras are running
led2 = LED(27)  # Indicates cameras are in sleep mode
button = Button(23, pull_up=False, bounce_time=0.1)  # Using pull-down resistor

# Track the subprocess running Flask app
app_process = None
APP_PATH = (Path(__file__).resolve().parent / "backend" / "app.py").as_posix()

def start_cameras():
    global app_process
    if app_process is None:
        print("[INFO] Starting camera app...")
        app_process = subprocess.Popen([sys.executable, APP_PATH])
        led1.on()
        led2.off()

def stop_cameras():
    global app_process
    if app_process:
        print("[INFO] Stopping camera app...")
        app_process.terminate()
        try:
            app_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            app_process.kill()
        app_process = None
    led1.off()
    led2.on()

def restart_after_delay(delay_sec):
    stop_cameras()
    print(f"[INFO] Waiting {delay_sec} seconds before restarting cameras...")
    time.sleep(delay_sec)
    start_cameras()

def monitor_button():
    while True:
        button.wait_for_press()
        print("[INFO] Button pressed! Cameras going to sleep for 1 hour.")
        restart_after_delay(3600)  # 1 hour sleep

# --- Start ---
if __name__ == "__main__":
    start_cameras()
    monitor_button()
