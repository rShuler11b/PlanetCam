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

# Initialize the Arducam Pivariety Camera
camera_manager = CameraManager()
cameras = camera_manager.cameras

if not cameras:
    print("No cameras found!")
    exit()

camera = cameras[0]
camera.acquire()

# Configure the camera for still capture
config = camera.generate_configuration([libcamera.StreamRole.StillCapture])
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

def capture_image(exposure_time_ns=None):
    """
    Capture and save an image from the Arducam camera.
    
    If exposure_time_ns is provided, the function sets the camera controls to
    use a manual 5-second (or other) exposure. Note that exposure time for libcamera
    is typically specified in nanoseconds (5 sec = 5e9 ns).
    
    Without an exposure_time_ns parameter, a standard (auto-exposure) image is captured.
    """
    filename = f'image_{int(time.time())}.jpg'
    request = camera.create_request()
    
    if request:
        if exposure_time_ns is not None:
            # Disable auto-exposure and set a manual 5-second exposure
            request.controls = {
                libcamera.controls.AE_LOCK: 1,  # Lock auto-exposure
                libcamera.controls.EXPOSURE_TIME: exposure_time_ns
            }
            # Queue the request and then wait for the full exposure duration
            camera.queue_request(request)
            # Wait for the exposure to integrate (convert ns to seconds)
            time.sleep(exposure_time_ns / 1e9)
        else:
            camera.queue_request(request)
        
        # In a real-world application you would use callbacks or check for request completion.
        # For this example, we assume that after the wait the buffer is ready.
        buffer = request.buffers[0]
        with open(filename, "wb") as f:
            f.write(buffer.data)
        print(f"Image captured: {filename}")
    
    return filename

# Example usage:
# Toggle live feed on (or off)
toggle_feed()

# Capture a standard image:
capture_image()

# Capture a long exposure image (5 seconds = 5e9 ns)
capture_image(exposure_time_ns=5000000000)
