"""
Handles camera initialization, live feed toggle, and image capture for the Arducam Pivariety camera.
Uses libcamera for capturing images and saving them to the Raspberry Pi storage.
"""

import time
import libcamera
import libcamera.controls
from libcamera import CameraManager
import subprocess
from config import IMAGE_WIDTH, IMAGE_HEIGHT

# External SSD
SAVE_PATH = "/mnt/ssd"  # SSD mount path


# Initialize the Arducam Pivariety Camera
camera_manager = CameraManager()
cameras = camera_manager.cameras

if not cameras:
    print("No cameras found!")
    exit()

camera = cameras[0]
camera.acquire()

# Configure the camera for still capture
config = camera.generate_configuration([libcamera.StreamRole.Raw])
config[0].size = (IMAGE_WIDTH, IMAGE_HEIGHT)
camera.configure(config)

camera.start()

feed_running = False

def toggle_feed():
    """Start or stop live feed using libcamera-vid."""
    global feed_running
    if feed_running:
        subprocess.run(["pkill", "libcamera-vid"])  # Stop live feed
        print("Feed stopped")
    else:
        subprocess.Popen([
            "libcamera-vid",
            "-t", "0",          # Run indefinitely
            "--inline",
            "--width", str(IMAGE_WIDTH),
            "--height", str(IMAGE_HEIGHT),
            "--autofocus"
        ])
        print("Feed started")
    feed_running = not feed_running

def capture_raw(exposure_time_ns):
    """
    Captures a RAW image from the camera with the specified exposure time
    and saves it to the specified path.

    Parameters:
    - exposure_time_ns (int): The exposure time in nanoseconds. This is used 
      to manually set the exposure time for the image capture process. 
      (e.g., 5 seconds would be 5e9 nanoseconds).

    The function locks the auto-exposure (AE_LOCK), sets the manual exposure 
    time, captures the image, and saves it as a RAW file to the specified 
    directory (`SAVE_PATH`). The filename is timestamped based on the current 
    time to avoid overwriting previous images.

    Returns:
    - None: The function does not return any value; it directly saves the image 
      to disk and prints the file path.
    """
    filename = f"{SAVE_PATH}/image_{int(time.time())}.raw"
    request = camera.create_request()
    
    if request:
        request.controls = {
            libcamera.controls.AE_LOCK: 1,  # Lock auto-exposure
            libcamera.controls.EXPOSURE_TIME: exposure_time_ns  # Set manual exposure time
        }
        camera.queue_request(request)
        time.sleep(exposure_time_ns / 1e9)  # Wait for exposure duration
        
        buffer = request.buffers[0]
        with open(filename, "wb") as f:
            f.write(buffer.data)
        print(f"RAW Image saved to: {filename}")
