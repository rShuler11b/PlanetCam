"""
Handles camera initialization, live feed toggle, and image capture for the Arducam Pivariety camera.
Uses picamera2 for capturing images and saving them to the Raspberry Pi storage.
"""

import time
import cv2
from picamera2 import Picamera2
from config import IMAGE_WIDTH, IMAGE_HEIGHT

# Initialize the Arducam Pivariety Camera
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"size": (IMAGE_WIDTH, IMAGE_HEIGHT)}))
camera.start()

feed_running = False

def toggle_feed():
    """Start or stop live feed."""
    global feed_running
    feed_running = not feed_running
    if feed_running:
        print("Feed started")
    else:
        print("Feed stopped")

def capture_image():
    """Capture and save an image from the Arducam camera."""
    filename = f'image_{int(time.time())}.jpg'
    camera.capture_file(filename)
    print(f"Image captured: {filename}")
    return filename
