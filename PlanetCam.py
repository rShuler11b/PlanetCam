"""
Main program loop for the Raspberry Pi planetary camera project.
Listens for button inputs to start/stop the feed and capture images, displaying them on the TFT screen.
"""

import time
import button_control
import camera_control
import display_control
from config import BUTTON_FEED, BUTTON_CAPTURE

try:
    while True:
        if button_control.is_button_pressed(BUTTON_FEED):
            camera_control.toggle_feed()
            button_control.wait_for_button_release(BUTTON_FEED)

        if button_control.is_button_pressed(BUTTON_CAPTURE):
            image_path = camera_control.capture_image()
            display_control.display_image(image_path)
            button_control.wait_for_button_release(BUTTON_CAPTURE)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Shutting down...")
    GPIO.cleanup()

